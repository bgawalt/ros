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

TK


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

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

TK

### 5.2, Continuous probability simulation

> The logarithms of weights (in pounds) of men in the United States are
> approximately normally distributed with mean 5.13 and standard deviation 0.17;
> women’s log weights are approximately normally distributed with mean 4.96 and
> standard deviation 0.20. Suppose 10 adults selected at random step on an
> elevator with a capacity of 1750 pounds. What is the probability that their
> total weight exceeds this limit?

TK

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

TK

### 5.4, Demonstration of the Central Limit Theorem

> Let $x = x_1 + \ldots + x_{20}$, the sum of 20 independent uniform(0; 1)
> random variables. In R, create 1000 simulations of $x$ and plot their
> histogram. > What is the normal approximation to this distribution provided by
> the Central Limit Theorem? Overlay a graph of the normal density on top of the
> histogram. Comment on any differences between the histogram and the curve.

TK

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