# Chapter 5: Simulation

[(Return to README)](./README.md)


## Subsection rundown

Three reasons simulation is important:

1.  Better understand and intuit the variation that we're modeling; "our brains
    don’t seem to be able to do a good job understanding that random swings
    will be present in the short term but average out in the long run"
2.  Approximate sampling distributions for data and propogate this to the
    sampling distributions of estimates and procedures
3.  "\[R\]egression models are not deterministic; they produce probabilistic
    predictions. Simulation is the most convenient and general way to represent
    uncertainties in forecasts."

### 5.1, Simulation of discrete probability models

#### How many girls in 400 births?

The base rate probability of a girl birth is "approximately 48.8%\[...\] and
th\[is\] do\[es\] not vary much across the world."  Weirdly low, wonder what
that's about.

*  Starts by simulating the girl-count among 400 births, once
*  Then does 1,000 simulations of same

All very straightforward.  Just calls into the binomial random variable function
in R.

#### Accounting for twins

Given rates of identical (1/300) and fraternal (1/125) twins, constructs the
more sophisticated sampling scheme of "for 400 births, first flip the coin for
birth type, then flip the coin for number of girls born."

![Figure 5.1, "Histogram of 1000 simulated values for the number of girls born
in a hospital from 400 births, as simulated from the model that includes the
possibility of twins."](./fig/fig05_01_girls_w_twins.png)

Kind of a missed opportunity to overlay the with/without twin adjustment
simulations....

In any event, this is mostly exposing readers to how to do somewhat-complicated
simulation in R.

### 5.2, Simulation of continuous and mixed discrete/continuous models

Some examples of tracking nontrivial derived quantities from the simulation; in
this case, the mean and max of the heights across groups of 10 US adults
(where you flip a coin for "man/woman" and then draw from the corresponding
normal distribution).

#### Simulation in R using custom-made functions

Demonstrates defining functions in R (in this case, to sample $N$ US adult
heights), then passing the function invocation to `replicate`.

### 5.3., Summarizing a set of simulations using median and median absolute deviation

They introduce not just median absolute deviation, but this tradition they have
to scale it up to what a standard deviation *would* be in a normal curve of
same M.A.D. value (calling the scaled up quantity "mad sd").  I have no reason
to do this; I can't picture an audience for my work that would care about this.

They say it's used a lot in their reporting of regression coefficients when
using Stan to fit generalized linear models, since they're more numerically
stable than mean and actual-sd.  Stan and other MCMC Bayes samplers need their
results summarized *some* how, and this is how they communicate point estimate
and uncertainty (rather than just thinking of them as "more reliable
summaries").

Includes some pointers to R's `quantile` function for getting more quantile
ranges out of an array of samples.

### 5.4, Bootstrapping to simulate a sampling distribution

Distribution-free and generative-model-free way to estimate a sampling
distribution: just resample, with replacement, from the data you have. Like the
other methods, "giv\[es\] some sense of the variation that could be expected
if the data collection process had been re-done."

They give an example of generating a standard error around a ratio of medians,
by running 10,000 bootstrap resamples.

#### Choices in defining the bootstrap distribution

Two alternatives for bootstrapping uncertainty into regression model estimates:
(1) just resample from the $(x, y)_i$ directly, or (2) resample the *residuals*
that you find from the original model estimate, to get a new set of
$y_i^{\text{boot}}$ labels for each $x_i$ and fit a new model to that single
resampling.  No word on why you'd choose one or the other, though I suppose
it's not hard to try both.

They list some structured models that are examples of needing extra attention
and thought in their resampling:

*  **Time series.**  Given $(t, y)_i$ timestamped data, simple resample gives
    multiple observations at some time instants, and drops others entirely.
    Bootstrapping residuals "has issues too."  Their whole point is that there's
    no easy answer here.
*  **Multilevel structure.**  If you have groupable observations -- multiple
    students tested per school, or multiple tests done per student -- how do you
    resample?  Resample each group, or resample each observation?  First the
    group, then an observation?  "These three choices correspond to different
    sampling models and yield different bootstrap standard errors for estimates
    of interest."
*  **Discrete data.**  Binomial logistic regression (where you see $n_i$ copies
    of $(x, y)_i$ pairs) can be resampled just like the multilevel structure
    above -- you can either resample the $(x, n, y)$ triples themselves, or
    break them up into $\sum_i n_i$ observations of binary logistic outcome
    pairs. "\[N\]either of these two bootstrapping options is wrong here; they
    just correspond to two different sampling models."

#### Limitations of bootstrapping

You can't resample what you never observed in the first place, so
rare-but-presumably-extant phenomenon.  "Black Barry Goldwater voter" may
not appear in your 1,000 voter sample, and so won't in any of the bootstrap
resamples, either; you can't put error bars capping the odds of "Black voter
picks Goldwater" just with the bootstrap.

Note: we handled this in Ch. 4 by just assuming, for any category, a foursome
of fake observations, two yes and two no.  Used like a Bayesian prior.  They
allude to that fact when they say, "the problem arose with a simple
unregularized logistic regression."  Regularization is another way of saying
"put a prior on it."


## Exercises

Plots and computation powered by [Chapter05.ipynb](./notebooks/Chapter05.ipynb)

### 5.1, Discrete probability simulation

> Suppose that a basketball player has a 60% chance of making a shot, and he
> keeps taking shots until he misses two in a row. Also assume his shots are
> independent (so that each shot has 60% probability of success, no matter what
> happened before).
>
> (a) Write an R function to simulate this process.
>
> (b) Put the R function in a loop to simulate the process 1000 times. Use the
> simulation to estimate the mean and standard deviation of the total number of
> shots that the player will take, and plot a histogram representing the
> distribution of this random variable.
>
> (c) Using your simulations, make a scatterplot of the number of shots the
> player will take and the proportion of shots that are successes.

![Histogram for part (b), most of the mass is at 4 or below, but it decays
steadily until around 12 shots, and doesn't still entirely until 16](./fig/ex05_01_basket_hist.png)

![Scatterplot for part (c), I added jitter noise, but the success rate just
rises mechanically like a hyperbola headed for an asymptote of 1, though it
doesn't get that close, since the scatter plot points peter out after around 12](./fig/ex05_01_basket_scatter.png)

### 5.2, Continuous probability simulation

> The logarithms of weights (in pounds) of men in the United States are
> approximately normally distributed with mean 5.13 and standard deviation 0.17;
> women’s log weights are approximately normally distributed with mean 4.96 and
> standard deviation 0.20. Suppose 10 adults selected at random step on an
> elevator with a capacity of 1750 pounds. What is the probability that their
> total weight exceeds this limit?

[5.46%, 5.76%], using a standard error calculation for the uncertainty range
(rather than re-simulating a bunch of times).

### 5.3, Binomial distribution

> A player takes 10 basketball shots, with a 40% probability of making each
> shot. Assume the outcomes of the shots are independent. 
>
> (a) Write a line of R code to compute the probability that the player makes
> exactly 3 of the 10 shots.
>
> (b) Write an R function to simulate the 10 shots. Loop this function 10,000
> times and check that your simulated probability of making exactly 3 shots is
> close to the exact probability computed in (a).

The official chance is 21.5%.

My simulation came up with the range [21.1%, 22.8%], using two standard errors
as the uncertainty.

### 5.4, Demonstration of the Central Limit Theorem

> Let $x = x_1 + \ldots + x_{20}$, the sum of 20 independent uniform(0; 1)
> random variables. In R, create 1000 simulations of $x$ and plot their
> histogram.  What is the normal approximation to this distribution provided by
> the Central Limit Theorem? Overlay a graph of the normal density on top of the
> histogram. Comment on any differences between the histogram and the curve.

The Central Limit Theorem says that, with $\mu = 0.5$, $\sigma^2 = 1/12$ for our
$U[0, 1]$ case with $n = 20$:

$$(\bar{x}_n - \mu)\sqrt{n} \sim N(0, \sigma^2)$$
$$\Rightarrow \left(\frac{1}{n}\sum_i x_i - \mu\right)\sqrt{n} \sim N(0, \sigma^2)$$
$$\Rightarrow \left(\sum_i x_i - n\mu\right)\frac{1}{\sqrt{n}} \sim N(0, \sigma^2)$$
$$\Rightarrow \left(\sum_i x_i - n\mu\right) \sim N(0, n\sigma^2)$$
$$\Rightarrow \sum_i x_i \sim N(n\mu, n\sigma^2)$$
$$\Rightarrow \sum_i x_i \sim N(10, 5)$$

Here's that overlaying the histogram of sums:

![A light blue histogram, x axis running from 0 to 20, where all the mass
is between 5 and 15, and most of the mass is between 7.5 and 12.5, like a bell
curve.  An actual normal distribution, mean 10, variance 5/3, is overlain in
a red dotted line.](./fig/ex05_04_central_limit_thm.png)


### 5.5, Distribution of averages and differences

> The heights of men in theUnited States are approximately normally distributed
> with mean 69.1 inches and standard deviation 2.9 inches. The heights of women
> are approximately normally distributed with mean 63.7 inches and standard
> deviation 2.7 inches. Let $x$ be the average height of 100 randomly sampled
> men, and $y$ be the average height of 100 randomly sampled women. In R, create
> 1000 simulations of $x - y$ and plot their histogram. Using the simulations,
> compute the mean and standard deviation of the distribution of $x - y$ and
> compare to their exact values.

TK

### 5.6, Propagation of uncertainty

> We use a highly idealized setting to illustrate the use of simulations in
> combining uncertainties. Suppose a company changes its technology for widget
> production, and a study estimates the cost savings at $5 per unit, but with a
> standard error of $4. Furthermore, a forecast estimates the size of the market
> (that is, the number of widgets that will be sold) at 40 000, with a standard
> error of 10 000. Assuming these two sources of uncertainty are independent,
> use simulation to estimate the total amount of money saved by the new product
> (that is, savings per unit, multiplied by size of the market).

TK

### 5.7, Coverage of confidence intervals

> Reconstruct the graph in Figure 4.2. The simulations are for an estimate whose
> sampling distribution has mean 6 and standard deviation 4.

TK

### 5.8, Coverage of confidence intervals

> On page 15 there is a discussion of an experimental study of an
> education-related intervention in Jamaica, in which the point estimate of the
> treatment effect, on the log scale, was 0.35 with a standard error of 0.17.
> Suppose the true effect is 0.10 — this seems more realistic than the point
> estimate of 0.35 — so that the treatment on average would increase earnings by
> 0.10 on the log scale. Use simulation to study the statistical properties of
> this experiment, assuming the standard error is 0.17.
>
> (a) Simulate 1000 independent replications of the experiment assuming that the
>     point estimate is normally distributed with mean 0.10 and standard
>     deviation 0.17.
>
> (b) For each replication, compute the 95% confidence interval. Check how many
>     of these intervals include the true parameter value.
>
> (c) Compute the average and standard deviation of the 1000 point estimates;
>     these represent the mean and standard deviation of the sampling
>     distribution of the estimated treatment effect.

TK

### 5.9, Coverage of confidence intervals after selection on statistical significance

> Take your 1000 simulations from Exercise 5.8, and select just the ones where
> the estimate is statistically significantly different from zero. Compute the
> average and standard deviation of the selected point estimates. Compare these
> to the result from Exercise 5.8.

TK

### 5.10, Inference for a ratio of parameters

> A (hypothetical) study compares the costs and effectiveness of two different medical treatments.
>
> * In the first part of the study, the difference in costs between treatments
>   A and B is estimated at $600 per patient, with a standard error of $400,
>   based on a regression with 50 degrees of freedom.
> * In the second part of the study, the difference in effectiveness is
>   estimated at 3.0 (on some relevant measure), with a standard error of 1.0,
>   based on a regression with 100 degrees of freedom.
> * For simplicity, assume that the data from the two parts of the study were
>   collected independently. Inference is desired for the incremental
>   cost-effectiveness ratio: the difference between the average costs of the
>   two treatments, divided by the difference between their average
>   effectiveness, a problem discussed further by Heitjan, Moskowitz, and
>   Whang (1999).
>
> (a) Create 1000 simulation draws of the cost difference and the effectiveness
>     difference, and make a scatterplot of these draws.
>
> (b) Use simulation to come up with an estimate, 50% interval, and 95% interval
>     for the incremental cost-effectiveness ratio.
>
> (c) Repeat, changing the standard error on the difference in effectiveness to
>     2.0.

TK

## 5.12, Randomization

> Write a function in R to assign $n$ items to treatment and control conditions
> under the following assignment procedures:
>
> * Independent random assignment. Each item is independently randomly assigned
>   to treatment or control with probabilities $p$ and $1 - p$.
> * Complete random assignment. The $n$ items are randomly partitioned into $np$
>   items that receive the treatment, and the other $n(1 - p)$ are assigned to
>   control.
> * Matched pairs. This is the simplest version of block random assignment. The
>   $n$ items come sequentially in $n/2$ pairs. Within each pair, one item is
>   randomly chosen for treatment and one for control. In other words,
>   $p = 0.5$.
>
> Write one R function, not three. Your function should have three inputs: $n$,
> $p$, and a code for which procedure to use. The output should be a vector of
> treatment assignments (1’s and 0’s). Hint: Your function likely won’t work for
> all combinations of $n$ and $p$. If it doesn’t, write it so that it throws an
> error and alerts the user.

TK