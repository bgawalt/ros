# Chapter 16: Design and sample size decisions

[(Return to README)](./README.md)

The book has focused on what to do with the data once you have it, but this
chapter will take a quick detour through how to get that data in the first
place.  Chiefly, how much data do you need?

## Subsection rundown

### 16.1, The problem with statistical power

"Power" means the probability that you will detect an effect of such-and-such
size, at such-and-such level of certainty, given the size of your sample.
The way this is usually approached, that "level of certainty" means a $p$-value
below 0.05 from a null hypothesis statistical test.

They are worried that making statsig the goal encourages risk taking: there's
always a chance that you find $p$ < 0 with a low-data study, just by luck.
So if the study is cheap, go for it.  Except we already know that comes with
large chances of sign and magnitude errors for the mean coefficent estimates.


They officially introduce the graphic I snipped in for Chapter 4, as Figure
16.1.  The version I found looked:

![A bell curve representing an estimated effect size's PDF.  The tails beyond
which the estimated effect would pass a $p$ < 0.05 test are in red.  The
negative effect tail is a Type S error, which has a 24% chance of arising under
low power like this.  The positive effect tail is a Type M error: in order to
have the proper sign and meet statsig, the estimate must be over 9 times larger
than the true effect.](./fig/part1/ch04_b_power_006.png)

and Figure 16.1 is the same, with slightly different annotation.

> Put simply, when signal is low and noise is high, statistically significant
> patterns in data are likely to be wrong, in the sense that the results are
> unlikely to replicate....  From the perspective of scientific learning, the
> real failures are the 6% of the time that the study appears to succeed, in
> that these correspond to ridiculous overestimates of treatment effects that
> are likely to be in the wrong direction as well.  In such an experiment, to
> win is to lose.  Thus, a key risk for a low-power study is not so much that it
> has a small chance of succeeding, but rather that an apparent success merely
> masks a larger failure.

And of course, we don't know the effect size in advance, so we have to guess at
one.  You can pick one based on prior expectations from what previous studies
have found, or else working backwards from the minimally interesting effect
size.

### 16.2, General principles of design, as illustrated by estimates of proportions

They point out that a doubling of the effect size reduces uncertainty as much as
quadrupling the sample size.  So if you can design your study so that the effect
is nudged upwards -- select participants who are likely to respond in non-boring
ways to the survey or treatment -- that will quadratically pay off in terms of
reducing uncertainty intervals later. "\[C\]onclusive effects on a subgroup are
generally preferred to inconclusive but more generalizable results, and so
conditions are usually set up to make effects as large as possible."  (So long
as everyone can remember that the effect size juicing was done at the design
phase.)

When picking a sample size, sometimes people work from "how narrow do I want my
standard error to be," or "how likely do I want my uncertainty interval to
exclude zero."  Answering either requires picking a hypothetical effect size
first, though, so the calculation "cannot really be tested until the data have
been collected."

The cap-on-standard-error approach is straightforward, working from
$\sigma/\sqrt{n} < \text{cap}$.

The try-for-statsig approach is more complicated:

1.  The mean estimate must be 1.96 standard errors above zero to have a
    95% confidence interval that excludes zero (i.e., statsig)
2.  The actual mean effect must be *even higher* than that 1.96 to have an 80%   
    chance of drawing a *sample* mean that exceeds 1.96 s.e.'s.

Figure 16.3 sketeches out this Texas two-step:

![Figure 16.3: "Sketch illustrating that, to obtain 80% power for a 95%
confidence interval, the true effect size must be at least 2.8 standard errors
from zero (assuming a normal distribution for estimation error).  The top curve
shows that the estimate must be at least 1.96 standard errors from zero for the
95% interval to be entirely positive.  The bottom curve shows the distribution
of the parameter estimates that might occur, if the true effect size is 2.8.
Under this assumption, there is an 80% probability that the estimate will exceed
1.96. The two curves together show that the lower curve must be centered all the
way at 2.8 to get an 80% probability that the 95% interval will be entirely
positive."](./fig/part4/fig16_3_power_calc.png)

For estimating differences in proportions between two equally-sized subsamples
whose total count sums to $n$:

$$n \gt 2 \times \left[p_1(1 - p_1) + p_2(1 - p_2)\right] \times
    \left[2.8 / (p_1 - p_2)\right]^2$$

where 2.8 is the magic number that drops out of a 95% confidence interval (1.96
standard errors) on the null hypothesis side, and how far the actual mean
estimate must be above that 1.96 to have an 80% chance of the sample mean
beating the statsig threshold.

For *unequally* sized subsample group comparisons, the standard error of the
difference in proportions is:

$$\text{se}[\hat{p}_1 - \hat{p}_2] = \sqrt{p_1(1-p_1)/n_1 + p_2(1-p_2)/n_2}$$

If you pose $n_i$ as fractions $f_i$ of the overall $n$, you can use the fact
that that square root is upper bounded by the case where both $p_i(1-p_i)$ are
0.5, and get:

$$\begin{align}
    \text{se}[\hat{p}_1 - \hat{p}_2] &\lt 0.5\sqrt{\frac{1}{f_1n} + \frac{1}{f_2n}} \\
        &\lt \frac{0.5}{\sqrt{n}}\sqrt{\frac{f_1 + f_2}{f_1f_2}} \\
        &\lt \frac{0.5}{\sqrt{nf_1(1 - f_1)}}
\end{align}$$

You need to set $n$ such that the hypothesized effect size (i.e., hypothetical
difference in proportions) is greater than $2.8\text{se}$.

### 16.3, Sample size and design calculations for continuous outcomes

Extending the previous section, designs for non-binary outcomes work the same
way, except the mean and variance of the outcome at the population level are
now decoupled.

(It's fun for the book to elide that we just learned in Chapter 15 that we can
decouple mean and variance in binary outcomes with the beta-binomial
distribution.  I guess this rarely pays off, vs. handling overdispersion in
count outcomes.)

For a population standard deviation $\sigma$, estimating the population mean
$\theta$:

*  Achieve a particular standard error level by setting
    $n > (\sigma/\text{se})^2$
*  Achieve 80% power of detecting a difference between $\theta$ and $\theta_0$
    by setting $n > \left(\frac{2.8\sigma}{\theta - \theta_0}\right)^2$

Except you probably don't *know* $\sigma$, and need to estimate it from the
same set of observed outcomes.  If you back off from "my sample mean is
distributed normally with variance $\sigma$" to "my sample mean is distributed
as a $t$ with $n - 2$ degrees of freedom," you have to pick different
multipliers than the 1.96 and 0.84 used in Fig 16.3.

They demonstrate this as:

*  `qnorm(0.8) + qnorm(0.975)` was our normal-distribution s.e. count needed to
    escape zero 80% of the time
*  But `qt(0.8, n - 2) + qt(0.975, n - 2)` being what's needed for the new
    $t$-dist case of 80% power

For $n = 12$, this means an increase from 2.8 to 3.1.  So like, ten percent
more data?  Pretty close, and as $n$ grows the difference will only shrink.
"We usually don’t worry about the $t$ correction because it is minor except when
sample sizes are very small."

For comparing two means,

$$\text{se}[\bar{y}_1 - \bar{y}_2] = \sqrt{\sigma_1^2/n_1 + \sigma_2^2/n_2}$$

They don't break down the general case in deriving this, but for 80% power when
detecting a difference of $\Delta$:

$$n > 2(\sigma_1^2 + \sigma_2^2)(2.8 / \Delta)^2$$

When upgrading from "no predictors" when estimating means as above, to "some
predictors", the noise pattern is reduced.  You swap the population $\sigma$ for
the residual standard deviation.  "Adding relevant predictors should decrease
the residual standard deviation and thus reduce the required sample size for any
specified level of precision or power."

If you have a wide uncertainty interval for a regression coefficient, they
advise you use the "standard errors fall as $1/\sqrt{n}$" proportionality to
intuit how much larger the sample size would need to be for a range still
centered on the mean estimate to exclude zero.

They noodle through some design calculations, then say:

> This design calculation is close to meaningless, however, because it makes the
> very strong assumption that the true value of $\beta$ is 0.018%, the estimate
> that we happened to obtain from our survey. But the estimate from the
> regression is $0.018\% \pm 0.015\%$, which implies that these data are
> consistent with a low, zero, or even negative value of the true $\beta$....
> If the true $\beta$ is actually less than 0.018, then even a sample size of
> 9000 would be insufficient for 80% power.  This is not to say the design
> analysis is useless but just to point out that, even when done correctly, it
> is based on an assumption that is inherently untestable from the available
> data (hence the need for a larger study).

They conclude saying, look, even if you did have a larger sample size, you'd
just immediately spring for a bigger model with more interactions.  And then
you'd have wide uncertainties again, among some of the coefficients.  So just
work with what you have and cop to the limited certainty any sample can provide,
including yours.

### 16.4, Interactions are harder to estimate than main effects

Interactions: important to cover!  Frequently requested!

Loosely, interactions cut a sample into half, as a best case scenario.  So the
estimation within those half-size subsamples will have standard errors (which
go as $1/sqrt{n}$) that are $2^2 = 4$ times as large.

The only way you come out ahead is if the interaction term meaningfully
reduces the residual standard deviation -- the interaction-free model measures
the main effect with s.e. $2\sigma^{(main)}/\sqrt{n}$, and the interaction of
the main effect with a 50-50 split binary variable of
$4\sigma^{(inter)}/\sqrt{n}$.  So you gotta hope you cut the residual standard
error in *half* by including the interaction, which is a high bar to clear.

> This \[the fact that interactions take 4x as much data to match a main
> effect's uncertainty width\] implies a big problem with the common plan of
> designing a study with a focus on the main effect and then looking to see what
> shows up in the interactions.  Or, even worse, designing a study, not finding
> the anticipated main effect, and then using the interactions to bail you out.
> The problem is not just that this sort of analysis is "exploratory"; it’s that
> these data are a lot noisier than you realize, so what you think of as
> interesting exploratory findings could be just a bunch of noise.

I did not especially follow the case made with the pure-noise example, where
shifting from (-0.5, 0.5) to (0, 1) caused a 40% increase in standard error.

### 16.5, Design calculations after the data have been collected

They revisit the implausible sex-ratios-and-beauty study from earlier, which
found a mean effect of 8% more girls among beautiful parents than uggos, when
most sex ratio studies never find a sex ratio shift greater than 0.5%.

They trace three possible scenarios for hypothetical effect sizes that are
consistent with prior work, while maintaining *this* study's 3 pct-pt standard
error:

1.  True difference of zero: just wildly good luck mixed perhaps with some
    wiggling around of researcher degrees of freedom (what's the dividing line
    between beauty and uggo?) to produce a normal Type I error.
2.  True difference of 0.2%: `1 - pnorm(6, 0.2, 3)` gives a 2.7% chance of
    finding a positive-and-significant estimate, and `pnorm(-6, 0.2, 3)` adds
    another 1.9% chance of negative-and-significant.  So conditional on landing
    in the "found statsig" bucket, that's a 42% chance of Type S error.  And
    any statsig estimate will be 30x higher than the true difference.
3.  True difference of 0.5%: Same calculations mean 4.8% chance of statsig,
    at least 12x too large an estimate and 31% chance of a Type S error.

> A sample of this size is just not useful for estimating variation on the order
> of half a percentage points or less, which is why most studies of the human
> sex ratio use much larger samples, typically from demographic databases. The
> example shows that if the sample is too small relative to the expected size of
> any differences, it is not possible to draw strong conclusions even when
> estimates appear strong in the sense of being more than two standard errors
> from zero.

They emphasize that even Case (3) there is still way bigger than any other
published effect/coefficient for sex ration shifts.

### 16.6, Design analysis using fake-data simulation

This is fun.  The important advice is, keep an eye on the standard error of
the coefficient of interest.  Is it too wide to be of practical interest, given
the effect size you'd expect from prior experience?

They also introduce a neat trick to simulate selection bias, where the
control-or-treatment coin toss is governed by a logistic sigmoid that uses the 
same underlying latent parameter that governs the outcome values.  It's pretty
neat that simply adjusting for this latent parameter corrects the selection bias
and I'm sure we'll hear more about this in the section on causal inference.


## Exercises

Plots and computation powered by [Chapter16.ipynb](./notebooks/Chapter16.ipynb)

### 16.1, Sample size calculations for estimating a proportion

> (a) How large a sample survey would be required to estimate, to within a
>     standard error of $\pm$3%, the proportion of the U.S. population who
>     support the death penalty?
>
> (b) About 14% of the U.S. population is Latino. How large would a national
>     sample of Americans have to be in order to estimate, to within a standard
>     error of $\pm$3%, the proportion of Latinos in the United States who
>     support the death penalty?
>
> (c) How large would a national sample of Americans have to be in order to
>     estimate, to within a standard error of $\pm$1%, the proportion who are
>     Latino?

If I go with the convenient approximation $0.5/\sqrt{n}$ for standard error of
a proportion between 30 and 70, and I want 0.03 to be the upper bound on that
standard error, then:

$$0.03 \gt 0.5/\sqrt{n}$$
$$\sqrt{n} \gt 0.5 / 0.03$$
$$n \gt 277.7$$

So 278 or more people sampled to get an estimate of the national proportion.

To get the same precision when estimating the level of support among Latinos, we
need 278 Latinos in our sample.  A national sample will have a "standard
error" of $\sqrt{0.14(1 - 0.14)/n} = 0.35/\sqrt{n}$ of its Latino respondent
proportion.  So we want 14%, minus two of those standard errors, times the 
sample size, to be at least 278 respondents:

$$\left(0.14 - 2\frac{0.35}{\sqrt{n}}\right)n = 278$$
$$0.14n - 0.69\sqrt{n} = 278$$

If I let $z = \sqrt{n}$ I can use the quadratic equation:

$$0.14z^2 - 0.69z - 278 = 0$$
$$\begin{align}
    z &= -\frac{(-0.69)}{2 \cdot 0.14} \pm \frac{1}{2 \cdot 0.14}\sqrt{0.69^2 - 4(0.14)(-278)}$$
        &= 2.48 \pm 3.57\sqrt{156.16}
        &= 47.11
\end{align}$$
$$n = z^2 = 2219.2$$

So 2,220 people to be sure we get a standard error of 3% for our estimate of the
proportion among Latinos.  This lines up pretty good with the heuristic of,
"Latinos are one seventh of the US population, so to sample 278 Latinos, we need
278-times-7-equals-1,946 respondents.  We're just buying some insurance against
unluckily low Latino response rate due to sampling error with the extra 300
respondents I've added.

To estimate the proportion of Latinos to a standard error of 1%, that's easy
again, going off the ballpark estimate of 14%,

$$0.35 / \sqrt{n} \lt 0.01$$
$$\sqrt{n} \gt 0.35 / 0.01$$
$$n > 1204$$

So, 1,204 respondents to get an estimate of the Latino share of the population
to within a 1% standard error.

### 16.2, Sample size calculation for estimating a difference

> Consider an election with two major candidates, A and B, and a minor
> candidate, C, who are believed to have support of approximately 45%, 35%, and
> 20% in the population. A poll is to be conducted with the goal of estimating
> the difference in support between candidates A and B. How large a sample would
> you estimate is needed to estimate this difference to within a standard error
> of 5 percentage points? (Hint: consider an outcome variable that is coded as
> +1, -1, and 0 for supporters of A, B, and C, respectively.)

The hint suggests a "continuous" outcome $y$ that has a standard deviation
$\sigma$ of:

$$\mathbb{E}[y] = 0.45(1) + 0.35(-1) + 0.2(0) = 0.1$$
$$\mathbb{E}[y^2] = 0.45(1^2) + 0.35\left((-1)^2\right) + 0.2(0^2) = 0.7$$
$$\text{Var}[y] = \mathbb{E}[y^2] - \mathbb{E}[y] = 0.6$$
$$\sigma = \sqrt{\text{Var}[y]} = 0.77$$

That mean of that outcome, $y$, is the difference in proportions between A's
support and B's support, and its standard error is $0.77/\sqrt{n}$.  So,

$$0.77/\sqrt{n} \lt 0.05$$
$$\sqrt{n} \gt 0.77 / 0.05$$
$$n \gt 240$$

If you sample 240 or more people, you should get the precision you want.

Note that you'd expect around 180 to 205 of those 240 respondents to be A-or-B
supporters, using two standard errors around C's support.  With 180 respondents,
you would have a standard error of 3.5 pct-pts in estimating A's share of the
two-person vote.  I dunno, seems close?

### 16.3, Power

> Following Figure 16.3, determine the power (the probability of getting an
> estimate that is "statistically significantly" different from zero at the 5%
> level) of a study where the true effect size is X standard errors from zero.
> Answer for the following values of X: 0, 1, 2, and 3.

Figure 16.3 makes it clear what we want is, for a zero-mean, unit-variance
normal curve centered at X, what is the area under the curve from 1.96 to
infinity.  This is the same as one minus the CDF of a N(0, 1) evaluated at 1.96.

X  | Power
-- | ------
 0 |  2%
 1 | 17%
 2 | 52%
 3 | 85%

### 16.4, Power, type M error, and type S error

> Consider the experiment shown in Figure 16.1 where the true effect could not
> realistically be more than 2 percentage points and it is estimated with a
> standard error of 8.1 percentage points.
>
> (a) Assuming the estimate is unbiased and normally distributed and the true
>     effect size is 2 percentage points, use simulation to answer the following
>     questions: What is the power of this study? If only "statistically
>     significant" results are reported, what is the average type M error and
>     what is the type S error rate?
>
> (b) Assuming the estimate is unbiased and normally distributed and the true
>     effect size is no more than 2 percentage points in absolute value, what
>     can you say about the power, average type M error, and type S error rate?

TK

### 16.5, Design analysis for an experiment

> You conduct an experiment in which half the people get a special
> get-out-the-vote message and others do not. Then you follow up after the
> election with a random sample of 500 people to see if they voted.
>
> (a) What will be the standard error of your estimate of effect size? Figure
>     this out making reasonable assumptions about voter turnout and the true
>     effect size.
>
> (b) Check how sensitive your standard error calculation is to your
>     assumptions.
>
> (c) For a range of plausible effect sizes, consider conclusions from this
>     study, in light of the statistical significance filter. As a researcher,
>     how can you avoid this problem?

TK

### 16.6, Design analysis with pre-treatment information

> A new teaching method is hoped to increase scores by 5 points on a certain
> standardized test. An experiment is performed on $n$ students, where half get
> this intervention and half get the control. Suppose that the standard
> deviation of test scores in the population is 20 points. Further suppose that
> a pre-test is available which has a correlation of 0.8 with the post-test
> under the control condition. What will be the standard error of the estimated
> treatment effect based on a fitted regression, assuming that the treatment
> effect is constant and independent of the value of the pre-test?

TK

### 16.7, Decline effect

> After a study is published on the effect of some treatment or intervention, it
> is common for the estimated effect in future studies to be lower. Give five
> reasons why you might expect this to happen.

TK

### 16.8, Effect size and sample size

> Consider a toxin that can be tested on animals at different doses. Suppose a
> typical exposure level for humans is 1 (in some units), and at this level the
> toxin is hypothesized to introduce a risk of 0.01% of death per person.
>
> (a) Consider different animal studies, each time assuming a linear
>     dose-response relation (that is, 0.01% risk of death per animal per unit
>     of the toxin), with doses of 1, 100, and 10,000. At each of these exposure
>     levels, what sample size is needed to have 80% power of detecting the
>     effect?
>
> (b) This time assume that response is a logged function of dose and redo the
>     calculations in (a).

TK

### 16.9, Cluster sampling with equal-sized clusters

> A survey is being planned with the goal of interviewing n people in some
> number $J$ of clusters. For simplicity, assume simple random sampling of
> clusters and a simple random sample of size $n/J$ (appropriately rounded)
> within each sampled cluster.
>
> Consider inferences for the proportion of Yes responses in the population for
> some question of interest. The estimate will be simply the average response
> for the $n$ people in the sample.
>
> Suppose that the true proportion of Yes responses is not too far from 0.5 and
> that the standard deviation among the mean responses of clusters is 0.1.
>
> (a) Suppose the total sample size is $n = 1000$. What is the standard error
>     for the sample average if $J = 1000$? What if $J = 100, 10, 1$?
>
> (b) Suppose the cost of the survey is $50 per interview, plus $500 per
>     cluster. Further suppose that the goal is to estimate the proportion of
>     Yes responses in the population with a standard error of no more than 2%.
>     What values of $n$ and $J$ will achieve this at the lowest cost?

TK

### 16.10, Simulation for design analysis

> The folder `ElectricCompany` contains data from the Electric Company
> experiment analyzed in Chapter 19. Suppose you wanted to perform a new
> experiment under similar conditions, but for simplicity just for second
> graders, with the goal of having 80% power to find a statistically significant
> result (at the 5% level) in grade 2.
>
> (a) State clearly the assumptions you are making for your design calculations.
>     (Hint: you can set the numerical values for these assumptions based on the
>     analysis of the existing Electric Company data.)
>
> (b) Suppose that the new data will be analyzed by simply comparing the average
>     scores for the treated classrooms to the average scores for the controls.
>     How many classrooms would be needed for 80% power?
>
> (c) Repeat (b), but supposing that the new data will be analyzed by comparing
>     the average gain scores for the treated classrooms to the average gain
>     scores of the controls.
>
> (d) Repeat, but supposing that the new data will be analyzed by regression,
>     adjusting for pre-test scores as well as the treatment indicator.

TK

### 16.11, Optimal design

> (a) Suppose that the zinc study described in Section 16.3 would cost $150 for
>     each treated child and $100 for each control. Under the assumptions given
>     in that section, determine the number of control and treated children
>     needed to attain 80% power at minimal total cost. You will need to set up
>     a loop of simulations as illustrated for the example in the text.  Assume
>     that the number of measurements per child is fixed at $K = 7$ (that is,
>     measuring every two months for a year).
>
> (b) Make a generalization of Figure 16.1 with several lines corresponding to
>     different values of the design parameter $K$, the number of measurements
>     for each child.

TK

### 16.12, Experiment with pre-treatment information

> An intervention is hoped to increase voter turnout in a local election from
> 20% to 25%.
>
> (a) In a simple randomized experiment, how large a sample size would be needed
>     so that the standard error of the estimated treatment effect is less than
>     2 percentage points?
>
> (b) Now suppose that previous voter turnout was known for all participants in
>     the experiment. Make a reasonable assumption about the correlation between
>     turnout in two successive elections. Under this assumption, how much would
>     the standard error decrease if previous voter turnout was included as a
>     pre-treatment predictor in a regression to estimate the treatment effect?

TK

### 16.13, Sample size calculations for main effects and interactions

> In causal inference, it is often important to study varying treatment effects:
> for example, a treatment could be more effective for men than for women, or
> for healthy than for unhealthy patients. Suppose a study is designed to have
> 80% power to detect a main effect at a 95% confidence level. Further suppose
> that interactions of interest are half the size of main effects.
>
> (a) What is its power for detecting an interaction, comparing men to women
>     (say) in a study that is half men and half women?
>
> (b) Suppose 1000 studies of this size are performed. How many of the studies
>     would you expect to report a "statistically significant" interaction? Of
>     these, what is the expectation of the ratio of estimated effect size to
>     actual effect size?

TK