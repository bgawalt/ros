# Chapter 18: Causal inference and randomized experiments

[(Return to README)](./README.md)

The regressions run so far in the book have all been interpreted as a
comparison: what difference in output do we expect *between* a subject with
predictor value $x_i = 0$ and one with the value $x_i = 1$.  Now, we get to
focus on the special cases where the regression admits the interpretation:
what *change* in output *to* a subject whose predictor rises from
$x_i = 0 \rightarrow x_i = 1$.

## Subsection rundown

### 18.1, Basics of causal inference

They introduce a running example built around a fake data simulation of a
dietary intervention.  Since we know the exact rules of data generation, it's
easy to check how well each causal inference approach works.  Eight subjects
split evenly between treatment and control, where the treatment group is going
to take fish oil supplements for a year, after which everyone gets their
systolic blood pressure checked.

Some jargon is introduced, where the fish oil example makes for easier
explanations:

*  We say predictor $z$ is the treatment indicator, where $z = 0$ (no fish oil)
    is the control-group indicator and $z = 1$ (yes fish oil) is the treated
    group
*  Every subject $i$ has two *potential outcomes*, $y_i^0$ and $y_i^1$, which
    are the outcomes you'd see if subject $i$ was in control or treatment
*  Subject $i$ really was in one of those two groups in historical reality, and
    so the potential outcome that matches their actual group is called the
    *factual state* (and the other potential outcome is the *counterfactual
    state*).
*  You can staple these together into a single expression for the observed
    outcome for subject $i$: $y_i = y_i^0(1 - z_i) + y_i^1z_i$.
*  Every subject has (an unobserved) *causal effect* that is usually something
    like $\tau_i = y_i^1 - y_i^0$, but sometimes are nonlinear functions of the
    potential outcomes.

They name and emphasize the fundamental problem of causal inference: you only
get to observe (at most) one of the potential outcomes, for any given subject.
(You observe neither for every future would-be subject who wasn't in this
study.)  Even close proxies for the counterfactual state are noisy.  (I.e., you
can measure pre-fish blood pressure, but that measurement is not the same as
what the subject's blood pressure would actually be a year later; lots can
change about a subject's life over the course of a year that would affect the
counterfactual state value.)

Crossover trials are designed to repeatedly apply (or withhold) the treatment
from each subject multiple times, measuring outputs frequently.  They to try and
build up a sense of per-subject effects, isolated from the treatment effect.
You do still have to worry about long-lasting effects from
treatment/withholding, though.

Extending to multiple treatments can mean making $z$ an integer or
real-valued predictor, like size of the fish oil pills, when the "multiple
treatments" are ordinal/numeric.  If they're unordered, the book says you should
get into multilevel modeling, with one set of group effects per treatment.
And if the multiple treatments can be given concurrently, you can either bucket
all the cross-product combinations as separate treatments, or model them
individually as treatments $z_i$, along with their interactions.

### 18.2, Average causal effects

Since we don't have access to both potential outcomes for every sample subject,
let alone the population, we have to settle for estimates based on the factual 
outcomes.  This has the families:

*  **Sample average treatment effect (SATE):** If $\tau_i = y_i^1 - y_i^0$, then
    $\mathbb{E}[\tau] = \mathbb{E}[y^1] - \mathbb{E}[y^0].  The sample averages
    of the treated and untreated outcomes give us good estimates of that
    expectation.

*  **Conditional average treatment effect (CATE):** You can also make the above
    expectations conditional on pre-treatment predictors $x$:
    $\mathbb{E}[\tau | x] = \mathbb{E}[y^1 | x] - \mathbb{E}[y^0 | x]$.
    Fit regression models to the treatment and control groups and put them to
    use.

*  **Population average treatment effect (PATE):** You may be interested in what
    your study's data implies about a larger population of interest.  If the
    sample is a representative/random draw from that popular, then cool, the
    SATE estimate is an unbiased estimate of the PATE.  Otherwise, you'll have
    to apply some postratification-style methods to retarget the SATE estimate
    to the actual demographics of the general population.

All these estimates hit snags if there's selection bias among who gets either
particular $z$ grouping.  You can hope that pre-treatment predictors correct for
this selection bias (or, sampling variance, if the imbalance between the two
groups is just bad luck) when used in a regression model.  But maybe not!

### 18.3, Randomized experiments

Randomize the treatment/control assignment to reduce risk of selection bias.
(Your subjects may still later get a veto, but, you can at least try at the
design stage to keep the two groups balanced.)

Every unit has the same chance of getting a particular $z$ value as every other
unit.  Take your vector that's half $z = 0$ and half $z = 1$, of length equal to
your sample size, shuffle it, and that shuffled vector is the treatment
assignment for each subject $i$.

Sometimes this works fine at keeping representative balance between the two
groups, but not always (especially at low sample sizes).  "Randomization ensures
balance on average but not in any given sample, and imbalance can be large when
sample size is small."

### 18.4, Sampling distributions, randomization distributions, and bias in estimation

This section reads a lot like Chapters 4 and 16: averages of random sampling
gives unbiased estimates of population means, with variance in those estimates
dropping with larger sample sizes.  The one addition this time is that for our
case, balance in the pre-treatment predictor attributes of the subjects can
also directly lower the variance of treatment effect estimates.  The balancing
act -- blocking, matching, etc. -- attentuates one source of variation and so
narrows the eventual standard error of the estimate.  A lower $\sigma$ in the
numerator $\sigma/\sqrt{n}$.


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer