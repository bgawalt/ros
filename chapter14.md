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

TK


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer