# Chapter 4: Statistical inference

[(Return to README)](./README.md)

Spiciest part of the intro paragraph is that the book will be introducing "the
theme of uncertainty in statistical inference and discuss how it is a mistake to
use hypothesis tests or statistical significance to attribute certainty from
noisy data."


## Subsection rundown

### 4.1, Sampling distributions and generative models

#### Sampling, measurement error, and model error

That's the three ways to think about what inference is about:

*  **Sampling:** estimating some characteristics of a population (mean, std. dev
    of height of US women) from a subset of that population
*  **Measurement error:** estimating an underlying pattern, like linear
    regression coefficients, from noisy data.  Note: could be non-additive
    noise (e.g., multiplicative noise); could be discrete data.
*  **Model error:** "All models are wrong, some are useful," so we need
    techniques to characterize the wrongness of your models.  I anticipate: by
    using it to draw some inferences and then see if they make sense.

> \[T\]he sampling model makes no reference to measurements, the measurement
> model can apply even when complete data are observed, and model error can
> arise even with perfectly precise observations. In practice, we often consider
> all three issues when constructing and working with a statistical model.

In $y_i = a + bx_i + \epsilon_i$, you can make arguments each way that the
$\epsilon$ terms are measurement or model error.

#### The sampling distribution

It's whatever generated your data, or whatever you can say about what generated
your data:

> The term “sampling distribution” is somewhat misleading, as this variation
> need not come from or be modeled by any sampling process—a more accurate term
> might be “probabilistic data model”—but for consistency with traditional
> terminology in statistics, we call it the sampling distribution even when no
> sampling is involved.

I think this is trying to cover the case -- which I've seen in my own work on
occasion -- where the dataset is a complete census, and "sampling" isn't part
of the generative process.  You still have to pay attention to this generative
distribution even in the census case, they're saying, and how it is unknowable
but estimatable.

I actually do like the measurement error example, where the scenario is that
there exists a definite slope and intercept driving
$y_i = a + bx_i + \epsilon_i$, but we don't get to know what they are exactly,
and to connect that back to the "randomly sample $n$ from a population of $N$."

### 4.2 Estimates, standard errors, and confidence intervals

#### Parameters, estimands, and estimates

"\[P\]arameters are the unknown numbers that determine a statistical model",
estimands are some function of the parameters, and estimates are what we call
our guesses about estimand values. "The sampling distribution of an estimate is
a byproduct of the sampling distribution of the data used to construct it."

#### Standard errors, inferential uncertainty, and confidence intervals

Standard error: "the estimated standard deviation of an estimate," though they
nowadays also use "looser meaning to cover any measure of uncertainty that is
comparable to the posterior standard deviation."  (Hey, neat, sneaking a Bayes
concept in here.)

They're declining to hammer the tricky definition of confidence interval.  They
say, rightly, "in repeated applications the 50% and 95% confidence intervals
will include the true value 50% and 95% of the time." But don't point out that
in those unlucky 50% or 5% of the time, you don't know what the range should
have been, and you don't know whether you're looking at a lucky or unlucky range
when you've calculated one.

#### Standard errors and confidence intervals for averages and proportions

Formulae to keep handy:

*  For $n$ datapoints whose standard deviation is $\sigma$ the standard error
    for the estimate of the population mean is $\sigma/\sqrt{n}$.  "This
    property holds regardless of any assumption about the shape of the sampling
    distribution, but the standard error might be less informative for sampling
    distributions that are far from normal."
*  For $n$ datapoints that are all either 0 or 1, that mean is a proportion.
    Plugging in mean and std. deviation formula for Bernoullis gives (for
    $y$ being the number of 1's):
    *  Mean: $\hat{p} \leftarrow y / n$
    *  Std. Deviation:  $\sigma \leftarrow \sqrt{\hat{p}(1 - \hat{p})}$
    *  Std. Error: $\sigma/\sqrt{n} = \sqrt{\hat{p}(1 - \hat{p})/n}$
    *  "If $p$ \[note: no hat! -brian\] is near 0.5, we can approximate this by
        $0.5/\sqrt{n}$.  They give convincing evidence that this works all the
        way out to $p$ being 30% (or equivalently, 70%).

It's kind of fun to look at Figure 4.2 and spot the times the horizontal line is
outside the 95% confidence intervals:


![Figure 4.2, with x-axis "Simulation" running from 0 to 100, y-axis "Estimate,
50%, and 95% confidence interval" running from -10 to 20, and one hundred thin
vertical lines where the middle part is thicker (the 50% uncertainty interval)
and there's a circle marker in the middle (the estimate).  Caption: "Simulation
of coverage of confidence intervals: the horizontal line shows the true
parameter value, and dots and vertical lines show estimates and confidence
intervals obtained from 100 random simulations from the sampling distribution.
If the model is correct, 50% of the 50% intervals and 95% of the 95% intervals
should contain the true parameter value, in the long run.](./fig/fig04_2_confidence_intervals.png)

#### Standard error and confidence interval for a proportion when $y = 0$ or $y = n$

When $p$ is close to 0 or 1 -- they give a convention of either $y$ or $(n - y)$
is under 5 -- they say, rerun the same procedure, but put in four fake
datapoints, two 0's and two 1's.  If your uncertainty intervals are below 0 or
above 1, just truncate and move on.

#### Standard error for a comparison

For two independent quantities, the standard error ($\textrm{se}$) of their
difference is:

$$\textrm{se}_\textrm{diff} = \sqrt{\textrm{se}_1 + \textrm{se}_2}$$

#### Sampling distribution of the sample mean and standard deviation; normal and $\chi^2$ distributions

If you have $n$ samples from a distribution $y_i \sim \mathcal{N}(\mu, \sigma)$,
and calculate sample mean and sample standard deviation (using $\frac{1}{n-1} for the
variance estimate!), then:

*  The sample mean is distributed as $\mathcal{N}(\mu, sigma/\sqrt{n})$
*  The sample standard deviation, called $s_y$, is distribued such that its
    transformation $s_y^2(n-1)/\sigma^2$ is distributed as a $\chi^2$ RV with
    $n-1$ degrees of freedom.

Too complicated for this book to go into details on, though!

#### Degrees of freedom

> Roughly speaking, we can think of observed data as supplying $n$ “degrees of
> freedom” that can be used for parameter estimation, and a regression with $k$
> coefficients is said to use up $k$ of these degrees of freedom. The fewer
> degrees of freedom that remain at the end, the larger the required adjustment
> for overfitting, as we discuss more carefully in Section 11.8.

They don't describe what a $\chi^2$ distribution looks like as a function of its
degrees of freedom, so I can only assume that as its degree count shrinks, its
tail grows longer.

Implicit: the above sample standard deviation calculation is doing what a
regression with one coefficient would do to the degrees of freedom.  That one
coefficient is just an intercept term, whose estimate is the sample mean.

#### Confidence intervals from the $t$ distribution

> When a standard error is estimated from $n$ data points, we can account for
> uncertainty using the $t$ distribution with $n + 1$ degrees of freedom,
> calculated as $n$ data points minus 1 because the mean is being estimated from
> the data.
> 
> \[...\]
> 
> The difference between the normal and t intervals will only be apparent with
> low degrees of freedom.

They provide a recipe for uncertainty around an estimate of a mean:

1.  Start by taking the sample mean as the center of the estimate distribution
2.  Calculate the standard error as sample standard deviation over the square
    root of $n$
3.  Look up how far from 0 the 97.5-th percentile of a $n-1$-degree $t$
    distribution is.  Multiply that by the standard error.  That's how far above
    the sample mean the uncertainty range should go (for 95% coverage).
    Similarly for the lower end, using the 2.5-th percentile.

#### Inference for discrete data

Your data are integers?  Count data?  Fine, whatever, use the same formulae and
procedures, it's fine.

#### Linear transformations

Any linear transformation applied to a parameter, can map straight onto its
confidence interval bounds.

#### Weighted averages

Assume a setup where for each of $k$ estimates, you have triplets of
{mean $\mu_i$, standard error $\textrm{se}_i$, weight $N_i$ (non-negative)},
with $N_\textrm{tot}$ as the sum total of all weights.  The weighted average of
these $k$ individual estimates looks like:

*  Mean: $\frac{1}{N_\textrm{tot}}\sum_i N_i\mu_i$
*  Standard error: $\frac{1}{N_\textrm{tot}} \sqrt{\sum_i \left(N_i\textrm{se}_i\right)^2}$

Then you just multiply the s.e. by $\pm2$, add those to the mean, and you have
a 95% confidence interval.

### 4.3, Bias and unmodeled uncertainty

Time to take a look at model error.

#### Bias in estimation

If you want an estimate of an attribute in the overall US population, but women
are more likely to answer your survey than men, then your sample statistics
will be biased estimates of the population statistics.  (This kind of bias, you
can fix with reweighting.)

It's impossible to cover every base, but you have to start somewhere.

#### Adjusting inferences to account for bias and unmodeled uncertainty

Large sample sizes help correct sample error, and correction of sample error
past a certain point is not a huge help since you've already entered the noise
floor of nonsampling error. If you do have a budget, rather than running the
same study/survey but 10x bigger, they say instead,

*  Invest in better data collection, like spreading out the survey requests
    across time and space
*  Improve the model: don't just do flat proprotion estimates any more, build
    a logistic regression model of the response variable over survey respondent
    predictors, and perhaps also poststratify that model.
*  "\[W\]hen all else fails," just increase the reported uncertainty width.
    Unclear where an estimate of nonsampling error, but if you have one (like
    they do for US election polling), you can do the Pythagorean sum of the
    nonsampling standard error and the sampling standard error to get a wider
    total.

> \[W\]e should be aware of sources of errors that are not in our models, we
> should design our data collection to minimize such errors, and we should set
> up suitably complex models to capture as much uncertainty and variation as we
> can. Indeed, this is a key role of regression: adding information to a model
> to improve prediction should also allow us to better capture uncertainty in
> generalization to new data.

### 4.4, Statistical significance, hypothesis testing, and statistical errors

Can you know in advance if you're about to mistakenly arrive at a strong
conclusion?

#### Statistical significance

They don't like/recommend using significance tests, but they do define them for
the sake of completeness: define a null hypothesis value for the estimand, then
see if your estimate's mean is more than two standard errors away from that
null value.  When it is, declare significance.

#### Hypothesis testing for simple comparisons

A simple comparison between treatment and control group, where you have
sample {mean $\bar{y}_X$, standard deviation $s_X$, size $n_X$},
$X \in \{T, C\}$.  Is there a difference in the means of the two groups? 
The latent mean parameters are $\theta_T$ and $\theta_C$, and the estimand of
interest is $\theta = \theta_T - \theta_C$.

*  **Estimate, standard error, and degrees of freedom.**
    *  Mean of our $\theta$ estimate: $\hat{\theta} = \bar{y}_T - \bar{y}_C$
    *  Standard error:
        $\textrm{se}\left(\hat{\theta}\right) = \sqrt{s_C^2/n_C + s_T^2/n_T}$
    *  Confidence interval:  Find the bounding quantiles of a $t$ distribution
        with $(n_C + n_T - 2)$ degrees of freedom.  (I guess we get that $-2$
        from "using up" two degrees on the two sample means?)
*  **Null and alternative hypotheses.**  The null hypothesis is
    $\theta_T = \theta_C$, or equivalently $\theta = 0$.  Test the hypothesis
    with the convential statistic: take the absolute value of the $t$-score,
    $t = \left|\hat{\theta}\right|/\textrm{se}\left(\hat{\theta}\right)$.
    The absolute value is what makes this a two-sided test; you're checking for
    swings in either the positive or negative direction.
*  **$p$-value.**  A summary statistic that aims to describe "the probability of
    observing something at least as extreme as the observed test statistic."
    *  Look up the CDF of a $t$ distribution with $(n_C + n_T - 2)$ degrees of
        freedom,
    *  evaluate it at the $t$-score value from above, 
        $\left|\hat{\theta}\right|/\textrm{se}\left(\hat{\theta}\right)$
    *  subtract that value from 1 to get the PDF's remaining tail area above the
        $t$-score, then double it for two-sided testing.  This is now the
        $p$-value.
    *  Traditionally, check that against 5%.  Lower is better.

#### Hypothesis testing: general formulation

The more complicated form of hypothesis testing, the null is composite.  They
give the regression case where the model is defined by
(slope, intercept, Gaussian noise's variance).  The null hypothesis only fixes
a value for the slope (at zero).  So you fit (overfit?!) the intercept and
noise level to the data assuming zero-slope, then compare the test statistic
(recipe for which is unspecified) of the varying-slope alternative hypothesis
case vs. that overfit null hypothesis.

This is all mentioned in the book briefly, to say that it only needs
understanding in some detail for simple comparisons, and only abstractly in
general formulations.

#### Comparisons of parameters to fixed values and each other: interpreting confidence intervals as hypothesis tests

Does a parameter's confidence interval include zero?  That yes/no question is a
hypothesis test of "does the parameter *equal* zero."

*  Is a parameter zero?  Check if zero is in its confidence interval.
*  Are two parameters equal?  Check if zero is in the confidence interval of
    the estimate of their difference.
*  Is a parameter positive?  Check if the confidence interval is strictly above
    zero.
*  Is parameter A greater than parameter B?  Check if the confidence interval of
    their difference is strictly above zero.

> The possible outcomes of a hypothesis test are “reject” or “not reject.” It is
> never possible to “accept” a statistical hypothesis, only to find that the
> data are not sufficient to reject it. This wording may feel cumbersome but we
> need to be careful, as it is a common mistake for researchers to act as if an
> effect is negligible or zero, just because this hypothesis cannot be rejected
> from data at hand.

#### Type 1 and type 2 errors and why we don’t like talking about them

*  Type 1 error: You rejected the null hypothesis and shouldn't have (false
    positive; your radar said an enemy plane was there and it wasn't)
*  Type 2 error: You didn't reject the null hypothesis and should have (false
    negative, you didn't think there was enough evidence from the radar to say
    an enemy plane was there, and there was)

They don't like it because it's a bad fit for social science, and perhaps
science generally.  One problem is that a lot of the time, it's stupid to think
an effect is literally zero.  The effect is going to vary across time and space
and subject.

The other is if you declare significance, the next step is almost always to use
the point estimate mean of the effect as your assumed baseline for the effect
strength you'll see in the future.

#### Type M (magnitude) and type S (sign) errors

Does your estimate of the effect have the wrong sign compared to the true value?
Is it the same size, but an order of magnitude larger than the true value?

The statistical significance filter (only $p < 0.05$ gets published) lends
itself to making type M errors.

Note that this doesn't talk at all about effect varying across space and time
and subject.

#### Hypothesis testing and statistical practice

> We do not find it particularly helpful to formulate and test null hypotheses
> that we know ahead of time cannot be true. Testing null hypotheses is just a
> matter of data collection: with sufficient sample size, any hypothesis can be
> rejected, and there is no real point to gathering a mountain of data just to
> reject a hypothesis that we did not believe in the first place.

Though they do appreciate running the above checks and learning from
non-rejection of the null that the particular dataset is undersized to learn
about whatever effect/parameter is being estimated.

> The problem here is that a *statistical* hypothesis (for example, $\beta = 0$ 
> or $\beta_1 = \beta_2$) is much more specific than a *scientific* hypothesis 
> (for example, that a certaincomparison averages to zero in the population, or
> that any net effects are too small to be detected). A rejection of the former
> does not necessarily tell you anything useful about the latter, because
> violations of technical assumptions of the statistical model can lead to high
> probability of rejection of the null hypothesis even in the absence of any
> real effect. What the rejection can do is motivate the next step of modeling
> the comparisons of interest.

### 4.5, Problems with the concept of statistical significance

TK

### 4.6, Example of hypothesis testing: 55,000 residents need your help!

TK

### 4.7, Moving beyond hypothesis testing

TK

## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer