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

$$\textrm{se}_\textrm{diff} = \sqrt{\textrm{se}_1^2 + \textrm{se}_2^2}$$

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

"The difference between significant and nonsignificant is not itself
significant" is not a direct quote from the opener, but Gelmnans used this
aphorism in his blog and it's the same idea.

#### Statistical significance is not the same as practical importance

Just from the title: this is one of those things that people just know to
knee-jerk say whenever a statistical analysis comes up.  Its popularity is 
second only to "correlation is not causation" in the world of lazy C+ replies.
It's worth noting in the book for completeness, but I'm allowed to think it's
overrated.

#### Non-significance is not the same as zero

They don't draw it out explicitly, but earlier they talk about how the two
options are "reject" or "don't reject" a hypothesis, and this is the same as
that.  "We don't reject the null" is not "we accept the null (the effect is
zero)."

#### The difference between “significant” and “not significant” is not itself statistically significant

Hey, called shot!  Didn't know this was coming when I typed up my initial entry
at the start of this section.

I think this might be one of a few times so far where we start to peek at the
use of inference (and regression) in practice.  It's not one clean study,
analysis of the study's data, and then conclusions.  It's *lots* of analyses of
different parts of the data from one study.  This is telling you not to use
statsig as a feather of Anubis to separate the virtuous effects from the
vicious. 

The example they use is comparing two different studies of the same phenomenon,
but the next section is...

#### Researcher degrees of freedom, p-hacking, and forking paths

... about multiple comparisons!  I.e., doing lots of analyses within the same
dataset, studying the same effect.

Just to get it out of the way, one of the bigger XKCD's is about this.
["Significant," #882](https://xkcd.com/882/):

![Scientists are asked to study effects of jelly beans on acne; they find no
effect; they're told to look for effects among particular colors of jelly bean;
they find nothing 19 times and do find one for green jelly beans; the newspaper
headlines freakout](./fig/ch04_a_xkcd_jellybeans.png)

The authors want to talk about the subtler variant of this.  Not just crude
data dredging, not just malice-aforethought $p$-hacking.  Instead, it's that
doing the good things the book has encouraged so far -- plot your data, get to
know it -- suggests what test/predictors/outlier-santization/etc. would be
appropriate.  Except if those are *post hoc* decisions, your inferences are
overfit; "a different test would have been performed given different data."

The proposed remedial approach is vague: "directly model the variation that is
otherwise hidden in all these possible data coding and analysis choices, and
to accept uncertainty and not demand statistical significance in our results."

We, as readers, don't know how to do that variation-modeling (yet?).  And I
think "not demand statistical significance in our results" is going to have
some socio-organizational problems.  Even if you don't summarize it a $p$-value,
results with strong signal are going to get more attention than those that
don't.

*  It's easy to get weak signal just by goofing something up; maybe your weak
    signal study is a false positive.  The academic community receiving the work
    is going to price that risk in.
*  Most comparisons are weak signal (including mostly zeros).  Washington, DC,
    rainfall timeseries from 1900-1950 does not predict coral bleaching in 2025
    as a function of latitude.  They're unrelated, it will present as a lot of
    uncertainty/variance for you to accept.  But no one is going to praise you
    for talking about how high-variance it is.

Meanwhile, strong signal studies are going to be high value, received by
the community with interest and praise.  And that will funnel down to authors
who will transmute the community's demand into demands on the data.

#### The statistical significance filter

From Nov 2014, Gelman's blog,
["This is what “power = .06” looks like. Get used to it."](https://statmodeling.stat.columbia.edu/2014/11/17/power-06-looks-like-get-used/):

![A bell curve representing an estimated effect size's PDF.  The tails beyond
which the estimated effect would pass a $p$ < 0.05 test are in red.  The
negative effect tail is a Type S error, which has a 24% chance of arising under
low power like this.  The positive effect tail is a Type M error: in order to
have the proper sign and meet statsig, the estimate must be over 9 times larger
than the true effect.](./fig/ch04_b_power_006.png)

The book states this as:

> Any estimate with $p$ < 0.05 is by necessity at least two standard errors from
> zero. If a study has a high noise level, standard errors will be high, and
> so statistically significant estimates will automatically be large, no matter
> how small the underlying effect.

#### Example: A flawed study of ovulation and political attitudes

I hope we get to see an example of what "all the comparisons" would look like
for a study like this.  Maybe there's a graph worth 1,000 words that quickly
conveys many comparisons all at once?

I think the key thing here is, the authors already know "that opinion polls find
very few people switching their vote preferences during the campaign for any
reason."  I imagine that *this* is what drew attention to the study and its
problems in the first place.  Knowing that the result was likely a Type M error,
they can assume low power to the study, and can also look into the details of
how contrived and multplie-comparisony the analysis appears.  (Put another way,
I think but for the Type M error, this study would not appear in this book.)

### 4.6, Example of hypothesis testing: 55,000 residents need your help!

The test statistic, and the $\chi^2$ tests, require a lot of focus to make sense
of.  But the actual reply is much more intuitive and convincing, it's pretty
effective to save it till the end:

> As we explained to the writer of the fax, opinion polls of 1000 people are
> typically accurate to within 2%, and so, if voters really are arriving at
> random, it makes sense that batches of 1000 votes are highly stable.

The original letter thinks that 4% variance is suspiciously stable, but the
"margin of error" for 1000-subject surveys is the same order of magnitude, and
it's easy to point to that in the reply.

### 4.7, Moving beyond hypothesis testing

The advice:

*  Analyze all your data.  Upgrade your statistical method to one with the
    "ability to incorporate more information into the analysis."
*  Present all your comparisons.  "We recognize that, compared to the usual
    deterministically framed summary, this might represent a larger burden of
    effort for the consumer of the research as well as the author of the 
    paper."

## Exercises

Plots and computation powered by [Chapter04.ipynb](./notebooks/Chapter04.ipynb)

### 4.1, Comparison of proportions

> A randomized experiment is performed within a survey. 1000 people are
> contacted. Half the people contacted are promised a $5 incentive to
> participate, and half are not promised an incentive. The result is a 50%
> response rate among the treated group and 40% response rate among the control
> group. Give an estimate and standard error of the average treatment effect.

The estimated treatment effect is 10%:

$$\hat{p_1} - \hat{p_2} = 0.5 - 0.4 = 0.1$$

The standard error is:

$$\begin{align} \textrm{se}_{\textrm{diff}} &= \sqrt{\textrm{se}_1^2 + \textrm{se}_2^2} \\
\textrm{se}_1 &= \sqrt{\hat{p_1}\left(1 - \hat{p_1}\right) / 500} \\
  &= \sqrt{0.5 \times 0.5 / 500} \\
  &= 0.0224 \\
\textrm{se}_2 &= \sqrt{\hat{p_2}\left(1 - \hat{p_2}\right) / 500} \\
  &= \sqrt{0.4 \times 0.6 / 500} \\
  &= 0.0219 \\
\textrm{se}_{\textrm{diff}} &= \sqrt{0.0224^2 + 0.0219^2} \\
  &= 0.313 \\
\end{align}$$

So a reasonable uncertainty interval in the effect size is $[3.7\%, 16.3\%]$.

### 4.2, Choosing sample size

> You are designing a survey to estimate the gender gap: the difference in
> support for a candidate among men and women. Assuming the respondents are a
> simple random sample of the voting population, how many people do you need to
> poll so that the standard error is less than 5 percentage points?

If we assume that both gender populations support the candidate within the
30%-to-70% range (Harris-Trump was 43%-55% for men and 53%-46% for women),
then the $0.5/\sqrt{n}$ approximation for standard error holds.

$$\begin{align} \textrm{se}_{\textrm{diff}} &= \sqrt{\textrm{se}_M^2 + \textrm{se}_W^2} \\
  &= \sqrt{\left(0.5/\sqrt{n/2}\right)^2 + \left(0.5/\sqrt{n/2}\right)^2} \\
  &= \sqrt{2 \times \frac{0.25}{n/2}} \\
  &= \sqrt{1 / n}
\sqrt{1 / n} < 0.05 &\Rightarrow 1/n < 0.0025 \\
    &\Rightarrow n > (1 /0.0025) \\
    &\Rightarrow n > 400 \\
\end{align}$$

So 400 people, assuming a 50-50 split in respondents by gender, and also that
the within 30-to-70 assumption also holds.

### 4.3, Comparison of proportions

> You want to gather data to determine which of two students is a better
> basketball shooter. One of them shoots with 30% accuracy and the other is a
> 40% shooter. Each student takes 20 shots and you then compare their shooting
> percentages. What is the probability that the better shooter makes more shots
> in this small experiment?

Using a brute-force loop over the scenarios where the good shooter hits
\{0, 1, ... 20\} shots, I can
[use `scipy.stats.binom.logsf`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html#scipy.stats.binom)
to calculate the (log-)probability that the bad shooter hits more than that.

I get a final result of a 12% chance, but I don't entirely trust that I avoided
off-by-one errors on this.  Probably fine.

### 4.4, Designing an experiment

> You want to gather data to determine which of two students is a better
> basketball shooter. You plan to have each student take $N$ shots and then
> compare their shooting percentages. Roughly how large does $N$ have to be for
> you to have a good chance of distinguishing a 30% shooter from a 40% shooter?

Here we can use the formula from "Hypothesis testing for simple comparisons"
above:

$$\textrm{se}\left(\hat{\theta}\right) = \sqrt{s_C^2/n_C + s_T^2/n_T}$$

Where $n_C = n_T = N$:

$$\begin{align}
    s_C^2 &= \hat{p_C}\left(1 - \hat{p_C}\right) \\
      &= 0.3 \times (1 - 0.3) \\
    s_T^2 &= \hat{p_T}\left(1 - \hat{p_T}\right) \\
      &= 0.4 \times (1 - 0.4) \\
\textrm{se}\left(\hat{\theta}\right) &= \sqrt{\frac{0.3(1 - 0.3) + 0.4(1 - 0.4)}{N}} \\
    &= \sqrt{\frac{0.45}{N}} \\
\end{align}$$

We combine this with the approximate 95% interval formula:

$$[\hat{\theta} \pm t_{2N - 2}^{0.975} \times \textrm{se}\left(\hat{\theta}\right)]$$

We want that interval to always be above 0, and $\hat{\theta}$ is 0.1.  So let's
brute-force linear scan (too lazy to code up the corner cases for binary search)
for the first $N$ that satisfies:

$$t_{2N - 2}^{0.975} \times \textrm{se}\left(\hat{\theta}\right) < 0.1$$

My Python script says: we need 175 shots from each shooter to reliably tell the
good one from the bad one.

### 4.6, Hypothesis testing

> The following are the proportions of girl births in Vienna for each month in 
> 1908 and 1909 (out of an average of 3900 births per month):
> 
>  `.4777 .4875 .4859 .4754 .4874 .4864 .4813 .4787 .4895 .4797 .4876 .4859`
>  `.4857 .4907 .5010 .4903 .4860 .4911 .4871 .4725 .4822 .4870 .4823 .4973`
> 
> The data are in the folder `Girls`. These proportions were used by
> von Mises (1957) to support a claim that that the sex ratios were less
> variable than would be expected under the binomial distribution. We think
> von Mises was mistaken in that he did not account for the possibility that
> this discrepancy could arise just by chance.
> 
> (a) Compute the standard deviation of these proportions and compare to the
>   standard deviation that would be expected if the sexes of babies were
>   independently decided with a constant probability over the 24-month period.
> 
> (b) The observed standard deviation of the 24 proportions will not be
>   identical to its theoretical expectation. In this case, is this difference
>   small enough to be explained by random variation?  Under the randomness
>   model, the actual variance should have a distribution with expected value
>   equal to the theoretical variance, and proportional to a $\chi^2$ random
>   variable with 23 degrees of freedom; see page 53.

The standard deviation of that list of numbers is 6.275e-3.

The mean is 48.57%, and that's out of 3,900 births per month.  A binomial random
variable $\textrm{Bin}(0.4857, 3900)$  would have a standard deviation of 31.2,
or 8e-3.

Evaluating the CDF of a $\chi^2(23)$ RV with mean 8e-3 at the observed 6.3e-3
gives a value of 25%, so this is not so far from a typical value for that
distribution.  It's not way down in the left tail, for sure.


### 4.7, Inference from a proportion with $y = 0$

> Out of a random sample of 50 Americans, zero report having ever held political
> office. From this information, give a 95% confidence interval for the
> proportion of Americans who have ever held political office.

If we use the trick of "pretend to have observed 2 heads and 2 tails prior to
seeing the actual coin toss data," we have:

$$\hat{p} = \frac{2}{54} = 3.7%$$

$$\textrm{se} = \sqrt{\hat{p}(1-\hat{p})/54} = 2.6%$$

So using the (truncated) range $\hat{p} \pm 2\textrm{se}$, we get [0%, 8.8%].

Note that the
[Rule of 3](https://en.wikipedia.org/wiki/Rule_of_three_(statistics)) suggests
an upper bound of 3/50 = 6%.

### 4.8, Transformation of confidence or uncertainty intervals

> On page 15 there is a discussion of an experimental study of an
> education-related intervention in Jamaica. The point estimate of the
> multiplicative effect is 1.42 with a 95% confidence interval of
> \[1.02, 1.98\], on a scale for which 1.0 corresponds to a multiplying by 1,
> or no effect. Reconstruct the reasoning by which this is a symmetric interval
> on the log scale:
> 
> (a) What is the point estimate on the logarithmic scale? That is, what is the
>   point estimate of the treatment effect on log earnings?
> 
> (b) What is the standard error on the logarithmic scale?

Log scale treatment effect: 0.351

Log scale standard error: 0.166

### 4.9, Inference for a probability

> A multiple-choice test item has four options. Assume that a student taking
> this question either knows the answer or does a pure guess. A random sample of
> 100 students take the item, and 60% get it correct. Give an estimate and 95%
> confidence interval for the percentage in the population who know the answer.

Let's define two rates:

1.  $p$, the rate at which we see a correct answer
2.  $q$, the rate at which students know the answer

We observe $\hat{p}$ of 60%, with standard error:

$$\textrm{se}(p) = \sqrt{0.6 \times 0.4 / 100} = 0.049$$

so that gives an interval on $\hat{p}$ of \[50.2%, 69.8%\].

The relationship between $p$ and $q$ is given that everyone who knows the answer
increments $p$, and so do a quarter of students who don't know the answer:

$$p = q + 0.25(1 - q) = 0.25 + 0.75q$$

Reversing this linear relationship gives:

$$0.75q = (p - 0.25) \Rightarrow q = (4p - 1)/3$$

If we apply that transformation to the bounds on $\hat{p}$, we get a range for
$\hat{q}$ of \[33.6%, 59.7%\].

### 4.10, Survey weighting

> Compare two options for a national opinion survey: (a) a simple random sample
> of 1000 Americans, or (b) a survey that oversamples Latinos, with 300 randomly
> sampled Latinos and 700 others randomly sampled from the non-Latino
> population. One of these options will give more accurate comparisons between
> Latinos and others; the other will give more accurate estimates for the total
> population average.
> 
> (a) Which option gives more accurate comparisons and which option gives more
>   accurate population estimates?
> 
> (b) Explain your answer above by computing standard errors for the
>   Latino/other comparison and the national average under each design. Assume
>   that the national population is 15% Latino, that the items of interest are
>   yes/no questions with approximately equal proportions of each response, and
>   (unrealistically) that the surveys have no problems with nonresponse.

TK