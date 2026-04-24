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

You need to set $n$ such that the hypothesized effect size is greater than
$2.8\text{se}$.


### 16.3, Sample size and design calculations for continuous outcomes

TK

### 16.4, Interactions are harder to estimate than main effects

TK

### 16.5, Design calculations after the data have been collected

TK

### 16.6, Design analysis using fake-data simulation

TK


## Exercises

Plots and computation powered by [Chapter16.ipynb](./notebooks/Chapter16.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer