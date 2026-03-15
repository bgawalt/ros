# Chapter 11: Assumptions, diagnostics, and model evaluation

[(Return to README)](./README.md)

Here come a bunch of different plots you can make to see what the data is doing
to your model coefficients.  They go out of their way in the intro here to say
this is a subset of checks you need to do, and not even the most important
subset. "Some of the most important assumptions rely on the researcher's
knowledge of the subject area and may not be testable from the data alone."

## Subsection rundown

### 11.1, Assumptions of regression analysis

In decreasing order of importance:

#### Validity

Does the data you have, align with the question you want to answer?

*  the outcome measure should accurately reflect the phenomenon of interest,
*  the model should include all relevant predictors,
*  and the model should generalize to the cases to which it will be applied.

#### Representativeness

The sample should be representative of the population of interest, and it's
particularly crucial that the sampled outcomes look the the general distribution
of those outcome values in the overall population.

"Selection on $x$ does not interfere with inferences from the regression model,
but selection on $y$ does."  This is not exactly true.  If the relationship
is nonlinear, like $y \propto \sqrt{x}$, then a linear fit will depend heavily
on what slice of $x$ values wind up in your sample.

#### Additivity and linearity

They mention that you can try some simple transformations of the predictors
or output, but that really you just need more data to add nonlinear dynamics
to the model.

#### Independence of errors

"The simple regression model assumes that the errors from the prediction line
are independent, an assumption that is violated in time series, spatial, and
multilevel settings."

#### Equal variance of errors

If you know this is a problem, and how it affects different observations, you
can use the weighted least squares approach described last chapter.  It
definitely makes probabilistic prediction harder.

#### Normality of errors

They claim "the assumption of normality is typically barely important at all."
I think asymmetric noise would definitely yield incorrect coefficient estimates,
and we've done some synthetic data generation (like in Exercise 8.4) where the
noise distribution yields different max-likelihood estimates.

#### Failures of the assumptions

*  Validity problems? Try a measurement error model
*  Unrepresentative data? Try a selection model
*  Non-additivity or non-linearity? Try those data transforms as mentioned
*  Dependence between observed values? Try correlated errors or latent variable
    models
*  And there are modeling options for heteroscedasticity and non-normal error
    distribution, too.

You can also just go back and get better/richer data.  Or just trim your
research question down to whatever makes this data aligned.

#### Causal inference

To turn a regression coefficient into a causal prediction of "what happens to
the outcome if I adjust this input", you need to take on even further
assumptions.

### 11.2, Plotting the data and fitted model

This seems pretty redundant!  We have done this a lot already in this book!
Novel points made:

*  If you have a two-predictor model, where one is more obviously interesting
    w.r.t. the outcome, consider plotting a few lines of the outcome vs. the
    interesting predictor, for a few in-range values of the less-interesting
    predictor.
*  You can combine the previous advice with the advice of "make one plot for
    each of the (two, implicitly, in this case) predictors."
*  And you can reduce a $k$-predictor problem into a two-predictor problem by
    just treating "b_0 + $\sum b_i x_i$ for the $k-1$ uninteresting $i$s" as a
    synthesized single predictor.  A key case of this is when one of the
    predictors is your "treatment or control" indicator predictor.

### 11.3, Residual plots

Important: plot residuals vs. predicted values, *not* vs. actual values.
"\[F\]rom the regression model, the errors $\epsilon_i$ should be independent of
the predictors $x_i$, but not the data $y_i$."  They use a fake data simulation
where we're in total control and know we got the answer right, and show that
residual-vs-output is still painting an alarming picture.

### 11.4, Comparing data to replications from a fitted model

They demonstrate a case where the observed data has *something* going on other
than sampling from a normal distribution.  It's obvious from just the histogram
of the data that the minimum value is much, much lower than a normal
distribution is likely to ever generate.  Figure 11.11 does actually do a good
job of highlighting how this wrecks the model fit, even in the non-pathological
range of the data:

![Figure 11.11 Density estimates of the speed-of-light data y and 100
replications, y^rep, from the predictive distribution under the normal model.
Each density estimate displays the result of original data or drawing 66
independent values y_i^rep i from a common normal distribution with mean and
standard deviation (mu, sigma) simulated from the fitted
model.](./fig/part2/fig11_11_bad_fit.png)

I don't get much out of the rest, the test statistic of taking the minimum value
of each simulated re-draw from the fit model.

"In more complicated problems, more effort may be needed to effectively display
the data and replications for useful comparisons, but the same general idea
holds."  I guess?

### 11.5, Example: predictive simulation to check the fit of a time-series model

The simulation routine is more involved here than in the 11.4 Newcomb case.
They have to write out the iterative, autoregressive process that comes from
predicting $y_{t+1}$ from $y_t$.  "We could not simply create these simulations
using `posterior_predict` because with this time-series model we need to
simulate each year conditional on the last."

They come up with a test statistic -- number of times where the discrete-time
first order derivative changes signs -- and show it's conspicuously higher in
the simulated time series.  "In this case, 99% of the `n_sims = 4000`
replications had more than 26 switches, with 80% in the range [31, 41], implying
that this aspect of the data was not captured well by the model."

I don't know how to trade that off against other test statistics you could
gussy up.  Like do the simulated trajectories have comparable max and min
values.  But I take their larger advice: find a bug, fix a bug.  In this case,
their model has too many switches, so fix it.  If the fix introduces too much
deviation in the max-min limits: fix it again.
 
### 11.6, Residual standard deviation $\sigma$ and explained variance $R^2$

A definition I understood in prose, but which is nice to see mathematicized:

$$R^2 = 1 - \left(\hat{\sigma} / s^2_y\right)^2$$

where $s_y^2$ is the sample standard deviation of the output variable.

They also introduce a $V_{i=1}^n$ notation which is alien and useless to me.

This metric, $R^2$, the share of output variance the model explains, is
the same under scalings of $x$ or $y$.

It's interesting to see their example where $\sigma$ can stay the same between
two model evalaution runs, while $R^2$ differs a lot.  They do it with a subset
operation that reduces $s_y^2$.

In the Bayes case, where there are 1,000 linear rules fit by the MCMC sampler,
you can work with an empirical distribution of $R^2$ values for each of those
1,000 fits.  What does it mean that we don't just go with the single MCMC
sampled line that has the best $R^2$?  Why isn't that $R^2$-maximizer not the
mode of the sampled-line distribution?

### 11.7, External validation: checking fitted model on new data

"The most fundamental way to test a model" is to just bring new, unseen data to
it, and see if the model does a good job predicting the labels from the
predictors.  Though if you get a bad eval from this, it's not necessarily that
you did a bad job fitting the model over the original dataset: maybe the new
data is just not compatible with models fit to the old data.

### 11.8, Cross validation

Where can you find some new data to use for external validation?  Why not just
carve out a subset of your original data?  Call that carve-out the hold-out set.
"Cross validation removes the overfitting problem arising from using the same
data for estimation and evaluation, but at the cost of requiring the model to be
fit as many times as the number of partitions."

It's neat to hear the strategy they took for fast leave-one-out crossvalidation.
I want to hear more about that smoothing, though.  (I can't use their package
in Python, or at least, I don't know how and won't look it up.)

They introduce the log score as an alternative to $R^2$, which "measures only
the prediction error relative to the mean of the predictive distribution,
ignoring the uncertainty represented by the predictive distribution."  It's
clear how to calculate this with a point estimate of the model coefficients, but
not yet a talk about the Bayes case of 1,000 simulated coefficient sets.

They also give a paragraph to Akaike information criterion, which is very
similar to the log score, but with an adjustment for the number of predictors.
"AIC is an estimate of the deviance that would be expected if the fitted
model is used to predict new data.\[...\] We prefer to use cross validation as
it is more general and directly interpretable as an estimate of prediction
error, but for simple models the two methods should give similar answers."

The talk about adding predictors that are pure random noise as a baseline to
talk about differences in log score.  "\[A\]dding a linear predictor that is
pure noise and with a weak prior on the coefficient should increase the log
score of the fitted model by 0.5, in expectation, but should result in an
expected *decrease* of 0.5 in the LOO log score."

Their example, where they literally add noise predictors to a dataset, shows
a mild boost in raw $R^2$, though the `sigma` auxiliary parameter hasn't
changed.

## Exercises

Plots and computation powered by [Chapter11.ipynb](./notebooks/Chapter11.ipynb)

### 11.1, Assumptions of the regression model

> For the model in Section 7.1 predicting presidential vote share from the
> economy, discuss each of the assumptions in the numbered list in Section 11.1.
> For each assumption, state where it is made (implicitly or explicitly) in the
> model, whether it seems reasonable, and how you might address violations of
> the assumptions.

TK

### 11.2, Descriptive and causal inference

> (a) For the model in Section 7.1 predicting presidential vote share from the
>     economy, describe the coefficient for economic growth in purely
>     descriptive, non-causal terms.
>
> (b) Explain the difficulties of interpreting that coefficient as the effect of
>     economic growth on the incumbent party’s vote share.

TK

### 11.3, Coverage of confidence intervals: Consider the following procedure:

> *  Set $n = 100$ and draw n continuous values $x_i$ uniformly distributed
>    between 0 and 10. Then simulate data from the model
>    $y_i = a + bx_i + \text{error}_i$, for $i = 1, \ldots, n$, with $a = 2$,
>    $b = 3$, and independent errors from a normal distribution.
>
> *  Regress $y$ on $x$. Look at the median and mad sd of $b$. Check to see if
>    the interval formed by the median $\pm 2$ mad sd includes the true value,
>    $b = 3$.
> *  Repeat the above two steps 1000 times.
>
> (a) True or false: the interval should contain the true value approximately
>     950 times. Explain your answer.
>
> (b) Same as above, except the error distribution is bimodal, not normal. True
>     or false: the interval should contain the true value approximately 950
>     times. Explain your answer.

TK

### 11.4, Interpreting residual plots

> Anna takes continuous data $x_1$ and binary data $x_2$, creates fake data
> $y$ from the model, $y = a + b_1x_1 + b_2x_2 + b_3x_1x_2 + \text{error}$, and
> gives these data to Barb, who, not knowing how the data were constructed, fits
> a linear regression predicting $y$ from $x_1$ and $x_2$ but without the
> interaction. In these data, Barb makes a residual plot of $y$ vs. $x_1$, using
> dots and circles to display points with $x_2 = 0$ and $x_2 = 1$, respectively.
> The residual plot indicates to Barb that she should fit the interaction model.
> Sketch with pen on paper a residual plot that Barb could have seen after
> fitting the regression without interaction.

TK

### 11.5, Residuals and predictions

> The folder `Pyth` contains outcome $y$ and predictors $x_1, x_2$ for 40 data
> points, with a further 20 points with the predictors but no observed outcome.
> Save the file to your working directory, then read it into R using
> `read.table()`.
>
> (a) Use R to fit a linear regression model predicting $y$ from $x_1, x_2$,
>     using the first 40 data points in the file. Summarize the inferences and
>     check the fit of your model.
>
> (b) Display the estimated model graphically as in Figure 11.2.
>
> (c) Make a residual plot for this model. Do the assumptions appear to be met?
>
> (d) Make predictions for the remaining 20 data points in the file. How
>     confident do you feel about these predictions?
>
> After doing this exercise, take a look at Gelman and Nolan (2017, section
> 10.4) to see where these data came from.

TK

### 11.6, Fitting a wrong model

> Suppose you have 100 data points that arose from the following model:
> $y = 3 + 0.1 x_1 + 0.5 x_2 + \text{error}$, with independent errors drawn from
> a $t$ distribution with mean 0, scale 5, and 4 degrees of freedom. We shall
> explore the implications of fitting a standard linear regression to these
> data.
>
> (a) Simulate data from this model. For simplicity, suppose the values of $x_1$
>     are simply the integers from 1 to 100, and that the values of $x_2$ are
>     random and equally likely to be 0 or 1. In R, you can define
>     `x_1 <- 1:100`, simulate `x_2` using `rbinom`, then create the linear
>     predictor, and finally simulate the random errors in `y` using the `rt`
>     function. Fit a linear regression (with normal errors) to these data and
>     see if the 68% confidence intervals for the regression coefficients (for
>     each, the estimates $\pm 1$ standard error) cover the true values.
>
> (b) Put the above step in a loop and repeat 1000 times. Calculate the
>     confidence coverage for the 68% intervals for each of the three
>     coefficients in the model.

TK

### 11.7, Correlation and explained variance

> In a least squares regression with one predictor, show that $R^2$ equals the
> square of the correlation between $x$ and $y$.

TK

### 11.8, Using simulation to check the fit of a time-series model

> Find time-series data and fit a first-order autoregression model to it. Then
> use predictive simulation to check the fit of this model as in Section 11.5.

TK

### 11.9, Leave-one-out cross validation

> Use LOO to compare different models fit to the beauty and teaching evaluations 
> example from Exercise 10.6:
>
> (a) Discuss the LOO results for the different models and what this implies, or
>     should imply, for model choice in this example.
>
> (b) Compare predictive errors pointwise. Are there some data points that have
>     high predictive errors for all the fitted models?

TK

### 11.10, K-fold cross validation

> Repeat part (a) of the previous example, but using 5-fold cross validation:
>
> (a) Randomly partition the data into five parts using the `sample` function in
>     R.
>
> (b) For each part, re-fitting the model excluding that part, then use each
>     fitted model to predict the outcomes for the left-out part, and compute
>     the sum of squared errors for the prediction.
>
> (c) For each model, add up the sum of squared errors for the five steps in
>     (b). Compare the different models based on this fit.

TK