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

They provide some off-the-shelf formulas for predictive uncertainty
($\hat{\sigma}_\text{linpred}$ and $\hat{sigma}_\text{prediction}$), the
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

The standard error of the Bayes estimate goes to zero:

$$\begin{align}
\text{se}_\text{Bayes} &= \left.1\middle/\sqrt{\frac{1}{\text{se}^2_\text{prior}} + \frac{1}{\text{se}^2_\text{data}}}\right.
  &= \frac{\text{se}_\text{data}\text{se}_\text{prior}}{\sqrt{\text{se}^2_\text{data} + \text{se}^2_\text{prior}}}
\end{align}$$

Typically, $\text{se}^2_\text{data}$ drops to zero with enough data, so even
though the prior's standard error is fixed, the overall posterior standard error
also drops to zero.  The prior barely makes a dent in the overall parameter
estimate, when you have enough data.

It's important to highlight what they say about the standard error of the Bayes
estimate: it *must* be less than the standard error you'd get for the data-only
estimate.  If the prior is proper, you are reducing uncertainty in your reported
estimates.  Maybe that's bad, if you pick a bad prior!

They note a key assumption about Bayesian information aggregation: the prior
and the data are independent of each other.  That's kind of implied by the name
"prior," if you fix it prior to seeing the data, it's an independent source of
data.  Or it isn't definitely dependent.  It may still be accidentally
independent if whoever is providing the data is aware of, and responding to, the
same prior info you're incorporating.

I take the closing subsection to mean there's no standard way of picking a
prior distribution.  Sometimes, like in the election and births examples, you
use subject matter expertise.  Sometimes, they allow that you just won't know
enough about what you're estimating ("\[multivariate regression\] coefficients 
for which we have little knowledge or about which we do not want to make any
strong assumptions").

### 9.4, Example of Bayesian inference: beauty and sex ratio

They talk about a study where 3,000 parent-pairs were surveyed for their
attractiveness and how many of their kids were girls.

This is obviously a sociological/bureaucratic process by which we declare
something is "well known," the way that "\[i\]t is well known that variation in
the human sex ratio occurs in a very narrow range."  They have a set of
expectations for what a truly large change in girl-boy birth share would be, and
encode it as $\mathcal{N}(0\%, 0.25\%)$, so basically no chance of sex ratios
outside the range $[49.3\%, 50.7\%]$.

They run a bunch of numbers on standard errors of proportions from Chapter 4,
on the whole 3,000.  The data on "very attractive" parents
($n_\text{hot} = 300$) had a estimate-and-standard-error of $58\% \pm 3\%$.
That's very different than the usual 50-50 for sure. But.

> Estimating a comparison to an accuracy of 2 or 3 percentage points is pretty
> good -- for many purposes. But for studying differences in the sex ratio, we
> need much higher precision, more on the scale of 0.1 percentage point.

I don't think this quite sells their actual beef with the study.  Yes, the Bayes
estimate fails to reject the 50-50 null.  That's cuz you set a prior to things
"well known" to you!  I guess the actual issues -- like, who set the rules for
what counts as "very attractive" and did they set them so that they could reject
the null -- are outside this particular book's remit.  But as is, the section
is light on arguments for why no, really, you need sub-0.1% precision for
studying sex ratios.

They want you to know this could be a Type M error, but they can only compare
the standard error to the prior that they insist upon: "the data standard error
is more than 10 times the prior uncertainty."  I think one more paragraph where
they adjust the prior to once again admit a null-rejecting Bayes estimate would
be interesting.  They could point to how wide it is, and say, if sex ratios
really can vary this much, how come we've never seen a (say) 66-33 split ever,
anywhere, for any reason.

### 9.5, Uniform, weakly informative, and informative priors in regression

This section is about using `stan_glm` to set priors on regression coefficients.

By opening with the "uniform distribution" (actually an improper prior): it's
wild to me they don't even get into the API docs of `stan_glm` here.  This
is the first time we see `prior_intercept`, `prior`, and `prior_aux`, and
there's not yet been a description of what those arguments expect.  Integers?
Callbacks?

The default prior is norms for all coefficients.  They word it weirdly -- they
make it sound like you need to know the $b$ coefficents times the predictor
meansbefore you can set the prior on the intercept -- but the later codeblock
makes clear you just need to know the empirical mean and standard deviation of
the labels to set the prior on the intercept.  (Due to a faith that the
regression is supposed to pass through $(\bar{x}, \bar{y})$.)

This part is worth going into:

> If $x$ and $y$ have both been standardized, then the coefficient is the
> expected difference in standard deviations in $y$ corresponding to a change of
> 1 standard deviation in $x$. We typically expect such a difference to be less
> than 1 in absolute value, hence a normal prior with mean 0 and scale 2.5 will
> partially pool noisy coefficient estimates toward that range.

Why do we expect such a difference to be less than 1?  Because we're doing
statistics, and no one needs to do statistics to learn obvious effects.  This
loops back around to the sociology of where priors come from, where this is the
biggest fact of all: all of this stuff is only useful for the narrow range of
study between hopelessly noisy and blindingly obvious effects.

I'm still not loving their case against the beauty-sex-ratio study.  "There's
no steady, linear increase in girl-share as a function of attractiveness bucket"
is different than "something's going on, there's lots of girls in the most
attractive bucket."  It's interesting that if you *did* think about the
dataset in the first version ("girl-share is a linear function of parental
hotness"), that the data rule that out.  But that's a different thing!  And the
averages in each bucket are insufficient to check the second thing right now
(but are sufficient to fit the regression, especially if you weight each
bucket by corresponding number of parents).


## Exercises

Plots and computation powered by [Chapter09.ipynb](./notebooks/Chapter09.ipynb)

### 9.1, Prediction for a comparison

> A linear regression is fit on high school students modeling grade point
> average given household income. Write R code to compute the 90% predictive
> interval for the difference in grade point average comparing two students,
> one with household incomes of $40,000 and one with household income of
> $80,000.

Using Bambi as best I can right now:

```python
rng = numpy.random.default_rng("Exercise 9.1")

data = pandas.DataFrame({"income": income, "gpa": gpa})
model = bambi.Model("gpa ~ income", data)
fitted = model.fit()

diffs = []
sigmas = []
for chain in range(4):
    chain_df = (
        fitted.posterior.sel(chain=chain).to_dataframe().groupby("draw").mean())
    diffs.extend(inc * 40_000 for inc in chain_df["income"])
    sigmas.extend(chain_df["sigma"].to_list())
noisy_diffs = [d + rng.normal(0, 2 * s) for d, s in zip(diffs, sigmas)]
print(numpy.percentiles(noisy_diffs, [5, 90]))
```

### 9.2, Predictive simulation for linear regression

> Using data of interest to you, fit a linear regression.  Use the output from
> this model to simulate a predictive distribution for observations with a
> particular combination of levels of all the predictors in the regression.

Bringing back my fantasy football dataset from [Chapter 6](./chapter06.md), 
Exercise 6.7:

![Scatter plot with log-log axes labeled "Total IDP Score for 2023" (x axis)
and "... for 2024" (y axis), both running from 2^4 to 2^9.  The 739 blue dots
representing each player-performance are uniformly spread, though they make
a kind of acute isoceles triangle shape, point northeast -- narrowing by a
factor of three (again, log scale) between low-score and high-score regions.
A red line is overlain labeled "log(y) ~ 1.8 + 0.59 log(x)](./fig/ex06_07_nfl_idp.png)

I fit a regression in Bambi to this, and evaluated the predictive posterior
distribution for players at the 25th, 50th, and 75th percentile IDP level
in 2023:

![Three subplots stacked on top of each other, each with a histogram.  The
shared x axis is labeled "Predicted IDP Score, 2024 (log scale)" and runs
from 2 to 7.  All three histograms are nice bell curves, with what appears to be
the same standard deviation; all mass is within 1.2 x-axis units of the mean.
The top one, in blue, for a 25%-ile 2023 player, has a mean of 4.1.  The middle,
in green, for the median '23 player, has a mean of 4.45. The bottom, in red,
for a 75%-ile player, has mean 4.7.](./fig/ex09_02_idp_log.png)

If I redo the histogram after transforming the sampled predictions to the linear
scale, you can see that the upside of drafting a 75%-ile player is in that
greater chance of a truly outstanding season:

![Three subplots stacked on top of each other, each with a histogram.  The
histograms are the above three, exponentiated back to a linear scale.  The
shared x-axis is labeled "Predicted IDP Score, 2024" and runs from 0 to 400.
The histograms no longer resemble each other.  They're all heavy tailed, but
the tail gets much heavier as you go from 25% to 50% to 75%ile player.
](./fig/ex09_02_idp_linear.png)

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