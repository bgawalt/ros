# Chapter 9: Prediction and Bayesian inference

[(Return to README)](./README.md)

Three steps that "go beyond classical estimation:"

1.  Form a posterior distribution, represented by a set of simulated parameter
    values.
2.  Propogate uncertainty in this distribution/these parameters when making
    "simulation-based predictions for unobserved or future outcomes."
3.  Feed additional information into the mode using a prior distribution.

## Subsection rundown

### 9.1, Propagating uncertainty in inference using posterior simulations

*  "\[S\]tart by considering Bayesian simulation simply as a way of expressing
    uncertainty in inferences and predictions\[...\]."
*  "The real advantage of summarizing inference by simulations is that we can
    directly use these to propagate uncertainty."  Especially for derived
    quantities, they use $a/b$, intercept over slope, as an example.  You just
    calculate that for all 1000 simulated $(a,b)$ pairs and report quantiles.

### 9.2, Prediction and uncertainty: `predict`, `posterior_linpred`, and `posterior_predict`

If you have the Bayesian regression fit (i.e., the simulation matrix of $(a, b)$
pairs), there's three kinds of prediction you can make on a new input $x$:

1.  Collapse the simulations into a point estimate set of parameters, then use
    that point estimate to generate a prediction from $x$ ("point prediction").
    "The point prediction ignores uncertainty."
2.  Calculate predictions based on $x$ for each of the simulated parameter sets,
    then report on the empirical distribution of those predictions ("linear 
    predictor with uncertainty").  The specific uncertainty you're reporting is
    the "uncertainty about the **expected or average** value of $y$," emphasis
    mine.
3.  Do what you did in (2), but now also rope in estimates of the error term(s).
    They call this "the predictive distribution for a new observation."  In our
    case, this would be augmenting the uncertainty in the mean value of $y$ with
    estimates of what we think $\sigma$ is.

These are actually very useful terms of art for me to keep in mind.  I think the
one to lead with every time is "predictive distribution" though.

The "by hand" implementation of the predictive distribution is cruder than I'd
thought it'd be: it looks like they're just turning each simulated $\sigma_j$
into a single draw from $\mathcal{N}(0, \sigma_j)$ and then adding that scalar
draw to the point prediction $a_j + b_jx^\text{new}$ for each simulation.

The "Propagating uncertainty" section is interesting.  They feed a distinct
$x$ (drawn from a distribution of interest) to each simulated parameter set,
rather than a constant $x^\text{new}$.  They show how this increases the
uncertainty interval around the same point estimate for $y$.

They provide some off-the-shelf formulas for predictive uncertainty, the
standard deviation of the point estimate for $y$ and for the width of the noise
interval around it.  But they don't like those formulae, "which do not even work
once we move to more complicated models and nonlinear predictions."  The
simulations, though: those always work.

Finally, when I look at their R code snippets: I have no idea where these
functions are defined.  You should care about stuff like that!  Your code style
should insist on making this easy to determine at the point of use!

### 9.3, Prior information and Bayesian synthesis

They won't talk about Bayesian inference in general, but they do say we're
going to have a compromise between the prior and the data we provide, when
making our estimations.

Their formula for the parameter estimate, $\hat{\theta}_\text{Bayes}$, might
look nicer with a rewrite (multiply top and bottom by
$\text{se}^2_\text{prior}\text{se}^2_\text{data}$):

$$\begin{align}
  \hat{\theta}_\text{Bayes} &= \left.
       \left(\frac{1}{\text{se}^2_\text{prior}}\hat{\theta}_\text{prior} +
             \frac{1}{\text{se}^2_\text{data}}\hat{\theta}_\text{data}\right)
       \middle/
       \left(\frac{1}{\text{se}^2_\text{prior}} + \frac{1}{\text{se}^2_\text{data}}\right)
       \right.\\
   &= \frac{\text{se}^2_\text{data}\hat{\theta}_\text{prior} + \text{se}^2_\text{prior}\hat{\theta}_\text{data}}{\text{se}^2_\text{prior} + \text{se}^2_\text{data}}
\end{align}$$

Typically, $\text{se}^2_\text{data}$ drops to zero with enough data, and the
prior barely makes a dent in the overall parameter estimate.

It's important to highlight what they say about the standard error of the Bayes
estimate: it *must* be less than the standard error you'd get for the data-only
estimate.  If the prior is proper, you are reducing uncertainty in your reported
estimates.  Maybe that's bad, if you pick a bad prior!

### 9.4, Example of Bayesian inference: beauty and sex ratio

TK

### 9.5, Uniform, weakly informative, and informative priors in regression

TK


## Exercises

Plots and computation powered by [Chapter09.ipynb](./notebooks/Chapter09.ipynb)

### 9.1, Prediction for a comparison

> A linear regression is fit on high school students modeling grade point
> average given household income. Write R code to compute the 90% predictive
> interval for the difference in grade point average comparing two students,
> one with household incomes of $40,000 and one with household income of
> $80,000.

TK

### 9.2, Predictive simulation for linear regression

> Using data of interest to you, fit a linear regression.  Use the output from
> this model to simulate a predictive distribution for observations with a
> particular combination of levels of all the predictors in the regression.

TK

### 9.3, Uncertainty in the predicted expectation and the forecast

> Consider the economy and voting example from Section 7.1. Fit the linear
> regression model to the data through 2012; these are available in the folder
> `ElectionsEconomy`. Make a forecast for the incumbent party’s share of the
> two-party vote in a future election where economic growth is 2%.
>
> (a) Compute the point forecast, the standard deviation of the predicted
>     expectation from (9.1), and the standard deviation of the predicted value
>     from (9.2).
>
> (b) Now compute these using the relevant prediction functions discussed in
>     Section 9.2. Check that you get the same values as in part (a) of this
>     problem.

TK

### 9.4, Partial pooling

> Consider the example in Section 9.3 of combining prior information and survey
> data to forecast an election. Suppose your prior forecast for a given
> candidate’s share of the two-party vote is 42% with a forecast standard
> deviation of 5 percentage points, and you have survey data in which this
> candidate has 54% support. Assume that the survey is a simple random sample of
> voters with no nonresponse, and that voters will not change their mind between
> the time of the survey and the election.
> 
> (a) When you do the calculation, it turns out that your posterior mean
>     estimate of the candidate’s vote share is 49%. What must the sample size
>     of the survey be?
> 
> (b) Given this information, what is the posterior probability that the
>     candidate wins the election?

TK

### 9.5, Combining prior information and data

> A new job training program is being tested. Based on the successes and
> failures of previously proposed innovations, your prior distribution on the
> effect size on log(income) is normal with a mean of 􀀀0:02 and a standard
> deviation of 0.05. You then conduct an experiment which gives an unbiased
> estimate of the treatment effect of 0.16 with a standard deviation of 0.08.
> What is the posterior mean and standard deviation of the treatment effect?

TK

### 9.6, Bayesian inference with a zero-centered informative prior on the log scale

> Perform the Bayesian analysis for the Jamaica experiment described on page 15.
> We shall work on the logarithmic scale:
> 
> (a) Do Exercise 4.8 to get the estimate and standard error of the log of the
>     multiplicative treatment effect.
>
> (b) Combine these with a normal prior distribution with mean 0 and standard
>     deviation 0.10 to get the posterior distribution of the log of the
>     multiplicative treatment effect.
>
> (c) Exponentiate the mean of this distribution and check that it comes to 1.1,
>     that is, an estimated treatment effect of +10%.
>
> (d) Compute the 95% interval on the log scale and exponentiate it; check that
>     this comes to [0:9; 1:3], that is, a range from 􀀀10% to +30% on the
>     original scale.

TK

### 9.7, Uniform, weakly informative, and informative priors

> Follow the steps of Section 9.5 for a different example, a regression of
> earnings on height using the data from the folder `Earnings`. You will need to
> think what could be an informative prior distribution in this setting.

TK

### 9.8, Simulation for decision analysis

> An experiment is performed to measure the efficacy of a television advertising
> program. The result is an estimate that each minute spent on a national
> advertising program will increase sales by $500 000, and this estimate has a
> standard error of $200,000. Assume the uncertainty in the treatment effect can
> be approximated by a normal distribution. Suppose ads cost $300,000 per
> minute. What is the expected net gain for purchasing 20 minutes of ads? What
> is the probability that the net gain is negative?

TK

### 9.9, Prior distributions

> Consider a regression predicting final exam score $y$ from midterm exam score
> $x$. Suppose that both exams are on the scale of 0–100, that typical scores
> range from 50–100, that the correlation of midterm and final is somewhere in
> the range 0.5–0.8, and that the average score on the final exam might be up to
> 20 points higher or lower than the average score on the midterm.  Given the
> above information, set up reasonable priors for the slope and the intercept
> after centering.

TK

### 9.10, Prior distribution and likelihood

> Consider the model, $y = a + bx + \text{error}$, with predictors $x$ uniformly
> sampled from the range (-1, 1), independent prior distributions for the
> coefficients $a$ and $b$, and the default prior distribution for the residual
> standard deviation $\sigma$. For $a$, assume a normal prior distribution with
> mean 0 and standard deviation 1; for $b$, assume a normal prior distribution
> with mean 0 and standard deviation 0.2.
>
> (a) Simulate $n = 100$ data points from this model, assuming the true
>     parameter values are $a = 1, b = 0.1, \sigma = 0.5$.  Compute the least
>     squares estimate of $a, b$ and compare to the Bayesian estimate obtained
>     from `stan_glm` using the above priors.
>
> (b) Repeat the simulations with different values of $n$. Graph the Bayes
>     estimates for $a$ and $b$ as a function of $n$. What will these values
>     be in the limit of $n = 0$? $n = \infty$?
>
> (c) For what value of $n$ is the Bayes estimate for $a$ halfway between the
>     prior mean and the least squares estimate? For what value of $n$ is the
>     Bayes estimate for $b$ halfway between the prior mean and the least
>     squares estimate?

TK