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


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer