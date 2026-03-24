# Chapter 12: Transformations and regression

[(Return to README)](./README.md)

The intro talks about *standardization*, which "connects to 'regression to the
mean'" by putting predictors and outcomes on a shared zero-mean, unit-variance
scale.  And it also talks about "logarithmic and other transformations... in
order to get more understandable models and better predictions."

## Subsection rundown

### 12.1, Linear transformations

#### Scaling of predictors and regression coefficients

Units matter!  A regression coefficient describes the expected change in the
output given an increase in its predictor by "one unit".  But the same attribute
can be expressed in small units (inches of distance) or large ones (miles) and
that is going to dictate the scale of coefficient you get.

Linear transformations of predictors or outcome don't affect the model fit or
predicted values.  But they "can improve interpretability of coefficients and
make a fitted model easier to understand."  (Unsaid: they can also make the
numerical operations run during the model fit procedure go smoother.)

#### Standardization using z-scores

Linearly transform your predictors into versions with zero mean and unit
variance.  That makes unit changes in the predictor correspond to moving up or
down by one standard deviation:

> This is helpful because standard deviations can be seen as a measure of
> practical significance; in this case, a difference in one standard deviation
> on the input scale is a meaningful difference in that it roughly reflects a
> typical difference between the mean and a randomly drawn observation.

Standardization like this requires you have reliable values of the mean and
standard deviation for each predictor.  Maybe you estimate that from your data;
we call using the sample means and standard deviations "$z$-scoring".
Or maybe your data are too thin for that....

#### Standardization using an externally specified population distribution

If your data is too thin for that, look up good values of mean and standard
deviation to use from some other authority.  One benefit of *not* using
sample statistics is that it makes it easier to compare estimates of, e.g.,
coefficients.  (You just directly compare them.)

#### Standardization using reasonable scales

You can also just be a normal human being and use the same units everyone does:
inches, dollars, years, etc.  Maybe you adjust them a bit, to keep coefficients
on a "human" scale, like picking "thousands of dollars" to express a personal
income predictor.  Work backwards from what you want "one unit" to mean when
your coefficients express "change in expected outcome per change by one unit."

### 12.2, Centering and standardizing for models with interactions

We've seen lots of hard-to-reckon-with cases of intercepts that have to take on
weird values because "all predictors have value zero" is so far outside the
ranges observed in the dataset.

Same thing happens in models with interaction predictors.  A binary feature that
is included in the model, but the model also has an interaction with a
continuous predictor, is serving as an alternative intercept for the data when
the binary feature is 1.  And so, if the continuous predictor is never actually
zero, the binary feature gets the same weird-intercept valuation as before.

#### Centering by subtracting the mean of the data

If you replace the raw predictors with zero-mean equivalents, "\[e\]ach main
effect now corresponds to a predictive difference with the other input at its
average value."

In their example, with two main predictor and their interaction, the main
effect coefficients change a lot.  But the interaction coefficient estimate
doesn't change at all, not its median nor its mad sd.

#### Using a conventional centering point

You don't have to move to zero-mean predictors.  You could pick conventional
options like "what a human would presume to be the central predictor value."
Their example doesn't show a big change from the zero-mean transforms, because
it just so happens that the conventional value and the dataset-mean values are
close to each other.

#### Standardizing by subtracting the mean and dividing by 2 standard deviations

Zero-mean and dividing by 2x the standard deviation of a predictor gives a
coefficient "corresponds to a change from 1 standard deviation below the mean,
to 1 standard deviation above."

#### Why scale by 2 standard deviations?

So that a 50-50 binary variable winds up taking on the values $\pm 0.5$, and
we've seen that this is still basically true even for 70-30 binaries.  That
means the coefficient is on the scale that it was pre-transformation, where the
the jump from "false" to "true" was 1 unit, just as it is in the 2-s.d.
rescaling here (from -0.5 to +0.5).

If you have a lot of predictors, you can leave the binaries alone as 0 or 1,
and rescale the continuous predictors by 2 s.d., and they'll all be on
comparable scales.

I think this kind of gets hung up on "what does it mean for a binary predictor
to change by one standard deviation."  They can't actually do that, they only
have (at most) two possible numerical values under any continuous
transformation.

#### Multiplying each regression coefficient by 2 standard deviations of its predictor

If you have a no-interactions model already fit, you can rescale *the
coefficients** by multiplying them by 2-s.d. of their corresponding predictor:

> This gives a sense of the importance of each variable, adjusting for all the
> others in the linear model. As noted, scaling by 2 (rather than 1) standard
> deviations allows these scaled coefficients to be comparable to unscaled
> coefficients for binary predictors.

### 12.3, Correlation and “regression to the mean”

In the univariate regression case, where $x$ and $y$ are both zero-mean, unit
variance, the slope term will just be the correlation between the two.
Fun fact included here: "if a regression slope is more than 1 in absolute
value, then the variance of $y$ must exceed that of $x$."  (Only for univariate
regressions, I suppose.)

#### The principal component line and the regression line

Now this is what I'm talking about:

![Figure 12.2 from the book: "Data simulated from a bivariate normal
distribution with correlation 0.5. (a) The principal component line goes closest
through the cloud of points. (b) The regression line, which represents the best
prediction of y given x, has half the slope of the principal component line."
](./fig/part2/fig12_2_pca_v_linreg.png)

The PCA "miniz\[es\] the sum of squared distances between the points and the
line."  But the regression line only cares about verticsl distance to the line.
They note that, just like I would, asking people to draw a line-of-best-fit, 
they'll draw the PCA line.

This is worse for predictive purposes, they say, because look at the points
at the extremes.  They all lie entirely above or below the PCA line.  Not so
for the regression line, which goes through the vertical-middle of the far
right and far left points.

This is actually pretty clarifying, sitting back and thinking about it.  For one
thing, if I only *have* access to an $x$ value sitting around: I know how to
project that out to a $y$ value.  But projecting onto the PCA line, I need both
$x$ and $y$.  I don't really know how to make predictions with just an $x$ and
the PCA line, in that lots of points all share an $x$ while having noticeably
different projection-points in the latent PCA value.

#### Regression to the mean

Repeating from earlier: if $x$ and $y$ are standardized (share a common
standard deviation), the (univariate) regression coefficient must have magnitude
less than 1.  So units with larger $x$ than average, will have usually have a
$y$ that is larger than average, but not *as much* of a deviation as the $x$
had.  They emphasize that the "regression to the mean" only applies as a tug on
the output's conditional expected value, and when you get the error term added
in, you can wind up with outputs that have greater deviations than their
predictors had.

### 12.4, Logarithmic transformations

For all-positive outcomes, the additivity-and-linearity structure of typical
linear regression can't actually guarantee that predictions are also
all-positive.  A log-transform of the outcome variable restores this (while also
changing *how* changes in predictors influence outcome expectations).

They implicitly advise transforming the predictors so that coefficients for
predicting log-outcome typically fall between -1 and 1.  If you do that, and
use the natural log (base $e$) for transforming the outcome, you get a handy
approximate equivalence of where a coefficient of 0.05 corresponds to a 5%
increase in the expected outcome for each unit increase of the predictor.
Compared to using base 10, this makes it harder to interpret the predicted
values by mentally exponentiating -- that's the trade off, easy interpretation
of coefficients vs. predictions.

They couch log-log model coefficients "as the expected proportional difference
in $y$ per proportional difference in $x$."  A slope $b = 1.66$ means a 1%
increase in the predictor makes for a 1.6% increase in the expected outcome.

I don't quite follow their overall advice on when to take a log transformation.
They note in closing that it only makes a difference when the dynamic range of
a predictor is high (when the ratio of its max value to its min value is at
least 2).

### 12.5, Other transformations

*  **Square root:** Compresses the dynamic range of the predictor more mildly
    than the log transform.  But doesn't leave you with an easily interpreted
    coefficient.  And the predictions themselves windup both nonmonotonic and
    very weird, since predictions on the transformed $\sqrt{y} ~ x$ scale can be
    negative (what??) and when converted via squaring back to the original scale
    means large negative and large positive predictions both map to large
    positive orig-scale predictions.

*  **Idiosyncratic/ad hoc:** Sometimes your data is calling out for a bespoke
    transformation.  In their earnings prediction, so many of the outcomes are
    $0 (for the 40% of Americans who don't work) that they float the idea of
    splitting it into a prediction of zero-or-nonzero binary classification,
    maybe followed by a if-nonzero,-how-much regression.  They also say, if
    you know your data bucketizes in a nice, explainable way, make up your own
    bucket scheme for it (and turn one continuous variable into a categorical
    one).

*  **Swap discrete for continuous:** Sometimes you'll have a pair of discrete
    predictors -- "is Democrat", "is Republican" -- that naturally slot into a
    continuous, ordinal predictor.

*  **Swap continuous for discrete:** They don't recommend you do this with any
    regularity.  It throws away information, relative to continuous
    transformations.  But it is super convenient!  They *don't* talk about the
    stability of bucketized coefficient estimates, vs. their
    transform-coefficient counterparts: when using a continuous transform, you
    pool info from the whole range of predictors into the coefficient(s). But
    bucket coefficient estimates are all unable to leverage any trends from
    "neighboring" buckets; the model has no idea they're structurally related.

*  **Indices and indicators:** Some predictors are just plainly categorical in
    and of themselves, like indicators for which of the 50 states the
    observation comes from.  They represent a heightened risk for introducing
    linear dependence among predictors, which makes models nonidentifiable and
    their coefficient estimates unstable.

### 12.6, Building and comparing regression models for prediction

They explain that the reason it's taken so long for the chapter to get around to
actually building models using the above transformations, is because "it is
usually easiest to start with a simple model and then build in additional
complexity, taking care to check for problems along the way."

Their list of general principles on how to (iteratively) build a model:

1.  Include any predictor available that plausibly connects to the outcome.

2.  However, it still counts as "including" a predictor if you preemptively
    combine it with some other set of predictors.  "\[S\]ometimes several inputs
    can be averaged or summed to create a 'total score' \[predictor\]."

3.  If a predictor has a large effect, go back and try adding plausible
    interactions.

4.  Always keep an eye on standard errors (mad sd) when looking at coefficient
    estimates.  (No word on how to use them to, like, disregard a "large effect"
    finding in Step 3, not here anyway.)

5.  Changing the predictor set:
    *  Low s.e. coefficient estimates should definitely survive to the next
        round of modeling
    *  Large s.e. coefficients that don't have a strong prior reason to include,
        should probably drop out in the next round.  Dropping it will tighten up
        other coefficient estimates.
    *  "Strong prior reason to include" means things like "this categorical
        variable is the actual subject of our research question."  You then need
        to handle their large uncertainty with a prior (in the Bayes sense) or
        going out for more data.
    *  If a coefficient set doesn't make sense, like its sign or magnitude seem
        counterintuitive, look into it.  Is it explained by a large s.e.?
        If the s.e. is small, is it because there's some subpopulation structure
        going on w.r.t. the predictor taking on its particular values?

They emphasize thinking all this through, gaming out things like "what if this
coefficient's mean and s.e. are both large", *before* starting the model fit
iterations.  "It’s always easier to justify a coefficient’s sign once we have
seen it than to think hard ahead of time about what we expect."

Finally, write down the decisions you make in model iterations, and their
rationale, in real time.  If you can back up each step with a crossvalidation
check, even better.  If you don't do these checks, and just go for as many
iterations as possible, you'll wind up chasing noise artifacts in the data
(since these modeling decisions are basically infinite degrees of freedom to
fit the elephant and wiggle its trunk).

#### Lessons from their example

*  Their initial, simple model -- dump all the raw predictors value into a
    straight linear model -- winds up looking pretty bad under their LOO
    microscope.  One thing that happens is `p_loo` wound up noticeably higher
    than the actual number of predictors.  Though I don't know what they mean
    by "\[d\]iagnostics indicate that the approximate LOO computation is
    unstable."  I don't know what they're reading out to reach that conclusion.

*  The next model, log-transforming the outcome and all predictors (except for
    the one binary predictor), does well under LOO analysis, at least in terms
    of its stability.  (I now infer that stability comes from having
    small/negative Pareto $k$ values from the PSIS stage of PSIS-LOO, and
    having none above 0.7.)  The ELPD estimate is now much closer to zero, by
    like a factor of 15.

*  However, the ELPD values from the two model checks "are not directly
    comparable.  When we compare models with transformed continuous outcomes, we
    must take into account how the nonlinear transformation warps the continuous
    variable."  Doing the appropriate correction still makes the log-transform
    model look better than the linear, but not by 15x.

*  They look back and say, ah, the better predictions must come from the
    fact that now $\hat{y}$ can't be negative.

*  They look at two predictors whose coefficients have high uncertainty, and
    plot their simulated coefficient draws to show that (like you'd expect)
    the coefficients are negatively correlated (because the predictors
    themselves are noticeably positively correlated).

*  When they go simpler, they get a nice stable univariate coefficient estimate,
    but it winds up being worse under LOO than the richer model.  So they add
    a bit more back in and achieve slightly-better-than-parity results.

And a big block quote of what to make of "we went simpler and preffered it":

> One reason we get as good or better performance and understanding from a
> simpler model is that we are fitting all these regressions with weak prior
> distributions. With weak priors, the data drive the inferences, and when
> sample sizes are small or predictors are highly correlated, the coefficients
> are poorly identified, and so their estimates are noisy. Excluding or
> combining predictors is a way to get more stable estimates, which can be
> easier to interpret without losing much in predictive power. An alternative
> approach is to keep all the predictors in the model but with strong priors on
> their coefficients to stabilize the estimates. Such a prior can be constructed
> based on previous analyses or using a multilevel model.

### 12.7, Models for regression coefficients

They work another example, with many more predictors this time.  They
$z$-standardize the predictors to get coefficient standard errors that are all
roughly the same.  They look at the within-sample $R^2$ and compare it to the
LOO $R^2$ to diagnose overfitting.  And the `p_loo` exactly matches the actual
number of predictors, "which indicates the model is fitting to all predictors."

They do a rundown of what the default priors are saying about the coefficients:
twenty-six coefficients with zero mean and s.d. 2.5 comes to a "prior standard
deviation of the modeled predictive means" of $2.5\sqrt{26} = 12.7$.  That's
way bigger than the prior on the error term $\sigma$ allows for, so the $R^2$
you expect from the prior is very close to 1.  "The priors often considered as
weakly informative for regression coefficients turn out to be, in the multiple
predictor case, highly informative for the explained variance."

If you instead work backwards from "the prior on explained variance should peak
at 0.3," you get a sense of how to rescale the individual coefficient priors:
$\mathcal{N}(0, \sqrt{0.3/26}\text{sd}(y))$, with the prior on $\sigma$ getting
an exponential prior $\text{Exp}(\sqrt{0.7}\text{sd}(y))$.  In this example,
this reduces the difference between in-sample and LOO $R^2$.

You can also work it from the direction of "I think there's about $p_0$
coefficents that matter to this prediction."  They go through a complicated
setup of a horseshoe prior, which they conflate with a spike-and-slab prior.
In their example, this has a nice attribute of dropping a bunch of coefficients
to near-zero (including a counterintuitive finding that increased study time
means worse test-time performance).  They use this as a feature selection
routine and fit a final model with just four predictors that survived the
spike-and-slab (and show that the Bayesian v. LOO $R^2$ is a similar gap).

Closing line: "ideally the selection and averaging of models should be made
using formal decision-theoretic cost-benefit analysis, which is beyond the scope
of this book."


## Exercises

Plots and computation powered by [Chapter12.ipynb](./notebooks/Chapter12.ipynb)

### 12.1 Plotting linear and quadratic regressions

> The folder `Earnings` has data on weight (in pounds), age (in years), and
> other information from a sample of American adults. We create a new variable,
> `age10 = age/10`, and fit the following regression predicting weight:

```
            Median MAD_SD
(Intercept) 148.7   2.2
age10         1.8   0.5

Auxiliary parameter(s):
      Median MAD_SD
sigma 34.5    0.6
```

> (a) With pen on paper, sketch a scatterplot of weights versus age (that is,
>     weight on y-axis, age on x-axis) that is consistent with the above
>     information, also drawing the fitted regression line. Do this just given
>     the information here and your general knowledge about adult heights and
>     weights; do not download the data.
>
> (b) Next, we define `age10_sq = (age/10)^2` and predict weight as a quadratic
> function of age:

```
            Median MAD_SD
(Intercept) 108.0    5.7
age10        21.3    2.6
age10sq      -2.0    0.3

Auxiliary parameter(s):
      Median MAD_SD
sigma 33.9    0.6
```

> Draw this fitted curve on the graph you already sketched above.

TK

### 12.2, Plotting regression with a continuous variable broken into categories

> Continuing Exercise 12.1, we divide age into 4 categories and create
> corresponding indicator variables, `age18_29`, `age30_44`, `age45_64`, and
> `age65_up`. We then fit the following regression:

```
   stan_glm(weight ~ age30_44 + age45_64 + age65_up, data=earnings)

            Median MAD_SD
(Intercept) 147.8    1.6
age30_44TRUE  9.6    2.1
age45_64TRUE 16.6    2.3
age65_upTRUE  7.5    2.7

Auxiliary parameter(s):
      Median MAD_SD
sigma 34.1    0.6
```

> (a) Why did we not include an indicator for the youngest group, `age18_29`?
>
> (b) Using the same axes and scale as in your graph for Exercise 12.1, sketch
>     with pen on paper the scatterplot, along with the above regression
>     function, which will be discontinuous.

TK

### 12.3, Scale of regression coefficients

> A regression was fit to data from different countries, predicting the rate of
> civil conflicts given a set of geographic and political predictors. Here are
> the estimated coefficients and their $z$-scores (coefficient divided by
> standard error), given to three decimal places:
> 
> 
> |                      | Estimate | $z$-score |
> | -------------------- | -------- | --------- |
> | Intercept            |   -3.814 |   -20.178 |
> | Conflict before 2000 |    0.020 |     1.861 |
> | Distance to border   |    0.000 |     0.450 |
> | Distance to capital  |    0.000 |     1.629 |
> | Population           |    0.000 |     2.482 |
> | % mountainous        |    1.641 |     8.518 |
> | % irrigated          |   -0.027 |    -1.663 |
> | GDP per capita       |   -0.000 |    -3.589 |
> 
> Why are the coefficients for distance to border, distance to capital,
> population, and GDP per capita so small?

TK

### 12.4, Coding a predictor as both categorical and continuous

> A linear regression is fit on a group of employed adults, predicting their
> physical flexibility given age. Flexibility is defined on a 0–30 scale based
> on measurements from a series of stretching tasks. Your model includes age in
> categories (under 30, 30–44, 45–59, 60+) and also age as a linear predictor.
> Sketch a graph of flexibility vs. age, showing what the fitted regression
> might look like.

TK

### 12.5, Logarithmic transformation and regression

> Consider the following regression:
>
> $$\log(weight) = -3.8 + 2.1 \log(height) + \text{error}$$
> 
> with errors that have standard deviation 0.25. Weights are in pounds and
> heights are in inches.
> 
> (a) Fill in the blanks: Approximately 68% of the people will have weights
>     within a factor of and of their predicted values from the regression.
>
> (b) Using pen and paper, sketch the regression line and scatterplot of
>     log(weight) versus log(height) that make sense and are consistent with the
>     fitted model. Be sure to label the axes of your graph.

TK

### 12.6, Logarithmic transformations

> The folder `Pollution` contains mortality rates and various environmental
> factors from 60 U.S. metropolitan areas (see McDonald and Schwing, 1973). For
> this exercise we shall model mortality rate given nitric oxides, sulfur
> dioxide, and hydrocarbons as inputs. This model is an extreme
> oversimplification, as it combines all sources of mortality and does not
> adjust for crucial factors such as age and smoking. We use it to illustrate
> log transformations in regression.
>
> (a) Create a scatterplot of mortality rate versus level of nitric oxides. Do
>     you think linear regression will fit these data well? Fit the regression
>     and evaluate a residual plot from the regression.
>
> (b) Find an appropriate transformation that will result in data more
>     appropriate for linear regression. Fit a regression to the transformed
>     data and evaluate the new residual plot.
>
> (c) Interpret the slope coefficient from the model you chose in (b).
>
> (d) Now fit a model predicting mortality rate using levels of nitric oxides,
>     sulfur dioxide, and hydrocarbons as inputs. Use appropriate
>     transformations when helpful. Plot the fitted regression model and
>     interpret the coefficients.
> 
> (e) Cross validate: fit the model you chose above to the first half of the
>     data and then predict for the second half. You used all the data to
>     construct the model in (d), so this is not really cross validation, but it
>     gives a sense of how the steps of cross validation can be implemented.

TK

### 12.7, Cross validation comparison of models with different transformations of outcomes

> When we compare models with transformed continuous outcomes, we must take into
> account how the nonlinear transformation warps the continuous variable. Follow
> the procedure used to compare models for the mesquite bushes example on page
> 202.
>
> (a) Compare models for earnings and for log(earnings) given height and sex as
>     shown on pages 84 and 192. Use earnk and log(earnk) as outcomes.
>
> (b) Compare models from other exercises in this chapter.

TK

### 12.8, Log-log transformations

> Suppose that, for a certain population of animals, we can predict log weight
> from log height as follows:
> 
> *  An animal that is 50 centimeters tall is predicted to weigh 10 kg.
> *  Every increase of 1% in height corresponds to a predicted increase of 2% in
>     weight.
> * The weights of approximately 95% of the animals fall within a factor of 1.1
>     of predicted values.
>
> (a) Give the equation of the regression line and the residual standard
>     deviation of the regression.
>
> (b) Suppose the standard deviation of log weights is 20% in this population.
>     What, then, is the R2 of the regression model described here?

TK

### 12.9, Linear and logarithmic transformations

> For a study of congressional elections, you would like a measure of the
> relative amount of money raised by each of the two major-party candidates in
> each district. Suppose that you know the amount of money raised by each
> candidate; label these dollar values $D_i$ and $R_i$. You would like to
> combine these into a single variable that can be included as an input variable
> into a model predicting vote share for the Democrats. Discuss the advantages
> and disadvantages of the following measures:
>
> (a) The simple difference, $D_i - R_i$
>
> (b) The ratio, $D_i/R_i$
> 
> (c) The difference on the logarithmic scale, $\log D_i - \log R_i$
> 
> (d) The relative proportion, $D_i/(D_i + R_i)$

TK

### 12.10, Special-purpose transformations

> For the congressional elections example in the previous exercise, propose an
> idiosyncratic transformation as in the example on page 196 and discuss the
> advantages and disadvantages of using it as a regression input.

TK

## 12.11, Elasticity

> An economist runs a regression examining the relations between the average
> price of cigarettes, $P$, and the quantity purchased, $Q$, across a large
> sample of counties in the United States, assuming the functional form,
> $logQ = \alpha + \beta \log P$. Suppose the estimate for $\beta$ is -0.3.
> Interpret this coefficient.

TK

### 12.12, Sequence of regressions

> Find a regression problem that is of interest to you and can be performed
> repeatedly (for example, data from several years, or for several countries).
> Perform a separate analysis for each year, or country, and display the
> estimates in a plot as in Figure 10.9.

TK

### 12.13,  Building regression models

> Return to the teaching evaluations data from Exercise 10.6. Fit regression
> models predicting evaluations given many of the inputs in the dataset.
> Consider interactions, combinations of predictors, and transformations, as
> appropriate. Consider several models, discuss in detail the final model that
> you choose, and also explain why you chose it rather than the others you had
> considered.

TK

### 12.15, Models for regression coefficients

> Using the Portuguese student data from the `Student` folder, repeat the
> analyses in Section 12.7 with the same predictors, but using as outcome the
> Portuguese language grade rather than the mathematics grade.

TK