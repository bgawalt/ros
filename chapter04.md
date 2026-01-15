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

## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer