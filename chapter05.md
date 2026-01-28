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

TK

## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer