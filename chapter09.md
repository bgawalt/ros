# Chapter 9: Prediction and Bayesian inference

[(Return to README)](./README.md)


## Subsection rundown

### 9.1, Propagating uncertainty in inference using posterior simulations

TK

### 9.2, Prediction and uncertainty: `predict`, `posterior_linpred`, and `posterior_predict`

TK

### 9.3, Prior information and Bayesian synthesis

TK

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