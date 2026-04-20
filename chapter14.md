# Chapter 14: Working with logistic regression

[(Return to README)](./README.md)

Now that we can fit logistic regressions, we can build on them with:

*  better ways to visualize the models,
*  better interpretation of coefficients, including under linear transformation
    and interactions of features,
*  making probabilistic predictions with the models, and aggregating those
    predictions into average predictive comparisons that work as model
    summaries,
*  better evaluation methods, using binned residual plots and predictive errors,
*  better handling of sparse, discrete data.


## Subsection rundown

### 14.1, Graphing logistic regression and binary data

When $y$ is binary, scatter plotting $y$ vs. $x$ doesn't really work any more.
The dots wind up too piled on top of each other.  For univariate data, consider
binning by $x$ and plotting the proportion of $y = 1$ (i.e., mean of $y$) in
each bin.  For 2-D data, consider scatter plotting $x_2$ vs. $x_1$, with
different color dots for depending on $y$'s value.

### 14.2, Logistic regression with interactions

The arsenic-wells example from Chapter 13 is revisited, this time adding an
interaction term between distance to nearest clean well and local well's
arsenic level.  The coefficients for non-interaction/pure-linear terms are
interpreted by plugging in the mean values of one-or-both predictors and using
the divide-by-four rule to describe what a unit change in a particular predictor
(or the intercept) does to predicted probability of switching, in terms of
percentage point shift.

The interaction term interpretation is interesting.  For each predictor, they
describe how a unit increase in *that* predictor changes the *other* predictor's
coefficient:

> Looking from one direction, for each additional unit of arsenic, the value
> −0.18 is added to the coefficient for distance.... Looking at it the other
> way, for each additional 100 meters of distance to the nearest well, the value
> −0.18 is added to the coefficient for arsenic.

When the predictor inputs are centered to be zero-mean, this makes no difference
to the predictor coefficients (though does change the intercept).  It makes it
a bit easier to do the coefficients, now that mean values don't need plugging in
to interpret the coefficients' impact on predicted probability of switching.

They look at LOO log score differences when the interaction term is, vs. isn't,
included in the model, and find that the two models are fairly equivalently
accurate on the held-out samples.

When they add a predictor for education level (on an ordinal scale of grades
completed, divided by four to bring into a more typical order of magnitude) and
a binary predictor for "are you in any community associations", they find a
low-s.e. coefficient around education and a medium-high-s.e. for association,
and so just keep the education predictor "for clarity and stability." (The
association estimate was also of a counterintuitive sign, which I think really
sunk it, in combo with the s.e. width.) The LOO comparison *probably* favors
inclusion of the new predictors, but with wide uncertainty.

Because the education coefficient's s.e. was so narrow, they try out 
interactions between education and local arsenic level, and find pretty
decent coefficient estimates for them.  They then repeat the interpretation
routine for these two interaction coefficients.  (The inputs have all been
centered.)  When they compare this model, with education plus two education
interactions, to one that omits education level, they definitely find
improvement in LOO scores.

### 14.3, Predictive simulation

They fit a simpler arsenic well switch model, just based on distance to the
nearest clean well, and reach into the individual coefficient samples to
produce (a) a graph of a few random curves implied by some of the coefficient
pairs, (b) predictions on ten new subjects, which can be aggregated across the
4,000 simulations into single probability-of-switching estimates.

### 14.4, Average predictive comparisons on the probability scale

When you compare the difference in expected outcomes between subjects where
predictor $i$ varies over some range, the individual expectations are sensitive
to all predictor (and coefficient) values.  They do not recommend you just pick
some frozen set of values for the other predictors and all coefficients and then
calculate the expectations: whatever "central value" you pick for those
arguments can be arbitrarily unrealistic, if, e.g., the predictors are all
binary or strongly bimodal or something.

Instead, they say, just take the mean coefficient estimates, and apply them to
the $n$ datapoints to get predictions where your particular predictor is either
at the top or bottom of the range of interest.  Make a synthetic dataset of size
$2n$ from your $n$ actual observations, where in the first $n$ you clobber the
predictor of interest with the high value, in the second $n$ you use the low
value, and then apply the mean-coefficient model to all $2n$ to come up with
an estimate of the effect of going from high to low on that particular
predictor.

### 14.5, Residuals for discrete-data regression

If you repeat "residual vs. predicted value" for logistic regression, you just
get two pretty similar downward sloping lines, separated by the intercept
offset of $y = 0$ vs. $y = 1$.  They recommend instead binning by predicted
value, then plotting the average (actual) $y$ value within each bin. Their 
example uses variable width bins, such that a constant number of
observations falls in each bin.  This is a good way to spot problems where your
model is failing in one region or another.

You can also do this with a particular predictor on the x-axis; as in, the
predictor value for an observation on the x-axis, and that observation's
residual on the y-axis.  That makes a good diagnosis, too, on a per-feature
basis.  Their example shows a residual that's way outside the expected
uncertainty interval for a low-end value of a particular predictor.  They use
their domain expertise to know that a non-linear transformation (quadratic or
logarithmic) would help, so they go with logarithmic and reap a big LOO score 
win.

In discussing error rates vs. the null-model error rate, (a) the delta in error
rate depends on whether most of the data is near the central values (where
"just guess the mean label" is most effective), and (b) can be *very* misleading
when the average label is quite close to 0 (or to 1).  They call error rate "an
incomplete summary" for their hypothetical example of (b).

### 14.6, Identification and separation

The same issue of collinearity from linear regression arises in logistic
regression: if the two predictors are basically perfect proxies for each other,
you get wide uncertainty around whether the predictive lift is all due to one, 
the other, or some halfway mix of the two.

There's another identifiability failure mode, new to logistic regression, where
if a particular predictor has a perfect threshold that separates the $y = 1$
from $y = 0$ cases, the associated coefficient goes infinite.  (The same thing
happens if any linear combo of predictors perfectly separates the observations
by label: at least one of the coefficients for a predictor in the combo will be
infinite.)

They recommend the Bayesian resolution of just applying a prior to shrink the
estimates away from non-finiteness.  They conclude the chapter saying a prior
doesn't necessarily have to encode all you know about a data dynamic, and you'll
always have to stop adding complexity to the model before you've actually
encoded everything you know or believe in advance.

## Exercises

Plots and computation powered by [Chapter14.ipynb](./notebooks/Chapter14.ipynb)

### 14.1, Graphing binary data and logistic regression

> Reproduce Figure 14.1 with the model,
> $\text{Pr}(y =1) = \text{logit}^{-1}(0.4 - 0.3x)$, with 50 data points $x$
> sampled uniformly in the range $[A, B]$. (In Figure 14.1 the $x$’s were drawn
> from a normal distribution.) Choose the values $A$ and $B$ so that the plot
> includes a zone where values of $y$ are all 1, a zone where they are all 0,
> and a band of overlap in the middle.

We want the $x$ values to reach into the "saturated" region of the logit
sigmoid, which means the $z$ values of the linear predictor applied to $x$ has
to hit -6 and +6.  Working backwards from that, we get the $[A, B]$ range of:

$$[A, B] = [-18.7,  21.3]$$

Here's some simulated data from that range, plus the prescribed curve:

![Recreation of Figure 14.1, fifty simulated datapoints in blue, x axis ranging
from -18.7 to 23, with the left half of the blue dots mostly at y = 1 and the
right half mostly at y = 0, with mixing happening between -5 and 5 (and also two
fluke y = 1s around x = 9 and x = 10)](./fig/part3/ex14_01_sim.png)

### 14.2, Logistic regression and discrimination lines

> Reproduce Figure 14.2 with the model,
> $\text{Pr}(y = 1) = \text{logit}^{-1}(0.4 - 0.3x_1 + 0.2x_2)$, with $(x1, x2)$
> sampled uniformly from the rectangle $[A_1, B_1] \times [A_2, B_2]$. Choose
> the values $A_1, B_1, A_2, B_2$ so that the plot includes a zone where values
> of $y$ are all 1, a zone where they are all 0, and a band of overlap in the
> middle, and with the three lines corresponding to
> $\text{Pr}(y = 1) = 0.1, 0.5,$ and 0.9 are all visible.

If I gamble on (0, 0) being fairly central to the rectangle of interest -- not
a bad bet, since logit(0.4) is not *too* far from 50% -- I can repeat the same
procedure I used in x. 14.1 to calculate upper and lower bounds on $x_1$ and
$x_2$ to get good coverage of $y = 1$, $y = 0$, and their mixture:

$$[A_1, B_1] = [-18.7, 21.3]$$
$$[A_2, B_2] = [-32.0, 28.0]$$

![Recreation of Figure 14.2 under the new generating model, where the lines of
equal probability now slope upward.  Empty red circles are in the northwest half
of the graph, and filled-in blue circles are in the southeast, with some mixing
in the middle.](./fig/part3/ex14_02_sim2d.png)

### 14.3, Graphing logistic regressions

> The well-switching data described in Section 13.7 are in the folder `Arsenic`.
>
> (a) Fit a logistic regression for the probability of switching using
>     log(distance to nearest safe well) as a predictor.
>
> (b) Make a graph similar to Figure 13.8b displaying $\text{Pr(switch)}$ as a
>     function of distance to nearest safe well, along with the data.
>
> (c) Make a residual plot and binned residual plot as in Figure 14.8.
>
> (d) Compute the error rate of the fitted model and compare to the error rate
>     of the null model.
>
> (e) Create indicator variables corresponding to dist < 100; dist between 100
>     and 200; and dist > 200. Fit a logistic regression for $\text{Pr(switch)}$
>     using these indicators. With this new model, repeat the computations and
>     graphs for part (a) of this exercise.

TK

### 14.5, Working with logistic regression

> In a class of 50 students, a logistic regression is performed of course grade
> (pass or fail) on midterm exam score (continuous values with mean 60 and
> standard deviation 15). The fitted model is
> $\text{Pr(pass)} = \text{logit}^{-1}(-24 + 0.4x)$.
> 
> (a) Graph the fitted model. Also on this graph put a scatterplot of
>     hypothetical data consistent with the information given.
> 
> (b) Suppose the midterm scores were transformed to have a mean of 0 and
>     standard deviation of 1. What would be the equation of the logistic
>     regression using these transformed scores as a predictor?
> 
> (c) Create a new predictor that is pure noise; for example, in R you can
>     create `newpred <- rnorm(n,0,1)`. Add it to your model. How much does the
>     leave-one-out cross validation score decrease?

TK

### 14.6, Limitations of logistic regression

> Consider a dataset with $n = 20$ points, a single predictor $x$ that takes on
> the values $1, \ldots, 20$, and binary data $y$. Construct data values
> $y_1, \ldots, y_{20}$ that are inconsistent with any logistic regression on
> $x$. Fit a logistic regression to these data, plot the data and fitted curve,
> and explain why you can say that the model does not fit the data.

TK

### 14.7, Model building and comparison

> Continuing with the well-switching example:
>
> (a) Fit a logistic regression for the probability of switching using, as
>     predictors, distance, log(arsenic), and their interaction. Interpret the
>     estimated coefficients and their standard errors.
> 
> (b) Make graphs as in Figure 14.3 to show the relation between probability of
>     switching, distance, and arsenic level.
> 
> (c) Following the procedure described in Section 14.4, compute the average
>     predictive differences corresponding to:
> 
>     i. A comparison of `dist` = 0 to `dist` = 100, with `arsenic` held
>         constant.
> 
>     ii. A comparison of `dist` = 100 to `dist` = 200, with `arsenic` held
>         constant.
> 
>     iii. A comparison of `arsenic` = 0.5 to `arsenic` = 1.0, with `dist` held
>         constant.
> 
>     iv. A comparison of `arsenic` = 1.0 to `arsenic` = 2.0, with `dist` held
>         constant.
> 
> Discuss these results.

TK

### 14.8, Learning from social science data

> The General Social Survey (GSS) has been conducted in the United States every
> two years since 1972.
>
> (a) Go to the GSS website and download the data. Consider a question of
>     interest that was asked in many rounds of the survey and convert it to a
>     binary outcome, if it is not binary already. Decide how you will handle
>     nonresponse in your analysis.
> 
> (b) Make a graph of the average response of this binary variable over time,
>     each year giving $\pm1$ standard error bounds as in Figure 4.3.
> 
> (c) Set up a logistic regression of this outcome variable given predictors for
>     age, sex, education, and ethnicity. Fit the model separately for each year
>     that the question was asked, and make a grid of plots with the time series
>     of coefficient estimates $\pm$ standard errors over time.
> 
> (d) Discuss the results and how you might want to expand your model to answer
>     some social science question of interest.

TK

### 14.9, Linear or logistic regression for discrete data

> Simulate continuous data from the regression model,
> $z = a + bx + \text{error}$. Set the parameters so that the outcomes $z$ are
> positive about half the time and negative about half the time.
> 
> (a) Create a binary variable $y$ that equals 1 if $z$ is positive or 0 if $z$
>     is negative. Fit a logistic regression predicting $y$ from $x$.
> 
> (b) Fit a linear regression predicting $y$ from $x$: you can do this, even
>     though the data $y$ are discrete.
> 
> (c) Estimate the average predictive comparison -- the expected difference in
>     $y$, corresponding to a unit difference in $x$ -- based on the fitted
>     logistic regression in (a). Compare this average predictive comparison to
>     the linear regression coefficient in (b).

TK

### 14.10,  Linear or logistic regression for discrete data

> In the setup of the previous exercise:
> 
> (a) Set the parameters of your simulation so that the coefficient estimate in
>     (b) and the average predictive comparison in (c) are close.
> 
> (b) Set the parameters of your simulation so that the coefficient estimate in
>     (b) and the average predictive comparison in (c) are much different.
> 
> (c) In general, when will it work reasonably well to fit a linear model to
>     predict a binary outcome?
> 
> See also Exercise 13.12.

TK