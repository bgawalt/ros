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

### 18.5, Using additional information in experimental design

You can split your subjects into disjoint blocks, and then perform different
randomization within each block.  The book examples splits 16 subjects into
four blocks of 4, grouped by age.  The younger blocks get a lower allotment of
$z = 1$, with the extras going to the older blocks.

You can untangle this design in the later analysis.  Instead of just taking
simple means of the treatment and control outcomes, calculate effects within
each block, then average over the blocks.  One implementation of this is to
fit a regression with indicators of block ID as predictors.

When blocking is done as a function of a predictor thought to have substantial
correlation/linkage to the outcome, the within-block treatment estimates will
be more precise.

When blocks are all of size 2, that's matching.  You pair up each subject with
another subject that's quite similar (the most similar?).  If the two subjects
wind up having similar potential outcomes (just like their pre-treatment
predictors were similar), you get very nice efficiency gains.

Occasionally, the blocking/grouping is not something you can practically
control.  Maybe for practical reasons, you have to treat an entire neighborhood
of subjects identically.  Or maybe you think that treating one subject will mean
the treatment "rubs off" on nearby neighbors in ways that wash out your
treatment effect estimate, and so need to bundle group assignment by site or
neighborhood.

If you're treating at the group level, just make the groups the subject of
analysis.  Make the outcome an aggregate of within-group outcomes.

### 18.6, Properties, assumptions, and limitations of randomized experiments

A rundown of different attributes and pitfalls associated with different
randomization schemes.

#### Ignorability

Completely randomized experiments have no link between treatment assignment and
either potential outcome value.  It's totally random; treatment assignment is
statistically independent of all subject attributes.  When this independence
assumption holds, then on average, the treatment and control groups will be
balanced.  *On average!*  There will still be imbalance between the groups in
terms of any of the subject attributes, for any one study.

Note that this independence only applies to *pre-treatment* predictors.  Any
predictors measured after the treatment is/isn't applied are no longer
guaranteed to be independent of $z$.  

> In general, the relevant cutoff time is when the treatment is assigned, not
> when it is implemented, because people can adjust their behavior based on the
> anticipation of a treatment to which they have been assigned.

Applying ignorability to block-randomized experiments means the treatment is now
merely *conditionally* independent of the potential outcomes, given the block
ID.  In the example where older blocks got more treatment allotments, and we
know age is associated with potential outcome values, there's not full-on
independence between treatment and potential outcomes.  But condition on the
block ID, and independence is restored, because assignment is random within each
block.

When the blocking is now pairwise matching, it can get tough to just include
an indicator for each of the $n/2$ blocks.  The book says wait until Chapter 20,
when multilevel models will help analyze these situations.  You don't have to;
you can just take a simple difference in means and get an unbiased estimate.
But the multilevel model will let you make a similar estimate with less
variance.

#### Efficiency

When the treatment and control groups are basically similar, the less variance
you have to worry about when estimating the treatment effect.  Ideally, the
similarity would hold for the potential outcome distributions in the two
groups, but you can hope that if they're similar in pre-treatment predictor
values, then the potential outcomes will also be similar.

Blocking is supposed to help with this.  The blocks are all built around
corralling similar units together, so that randomization within the block makes
for even apportionment of each "type" of subject between treatment group.

Adjusting to pre-treatment predictors (both the ones that established whatever
blocking your design used, plus the rest) will only serve to reduce the
standard error in your treatment effect estimate.  Even without blocking, if
you do collect useful-for-blocking predictors pre-treatment, a regression using
those attributes will (probably) recover a lot of the explanatory power, and
you will efficiently estimate the treatment effect.

#### Stable unit treatment value assumption (SUTVA): no interference among units and no hidden versions of the treatment

This assumption is that the outcome seen for subject $i$ is a function *only*
on treatment $z_i$.  It doesn't change when $z_j,~j\ne i$ changes.  As well,
SUTVA implies that the treatment is the same for all subjects in the treatment
group.  They give a lot of examples of how easy it is to break this assumption
in practice.  This links back to our "involuntary blocking" at the end of 
Section 18.5, where you just randomize at the neighborhood/metro area/site
level, and treat those natural blocks as the new individual units of study.

#### External validity: Difficulty of extrapolating to new individuals and situations

Randomized experiments get their "gold standard" reputation because of their
internal validity.  But external validity is harder.

*  Studies will seek out particular kinds of subjects.  For ethical or
    cost-effectiveness reasons, they want to maximize power by amping up
    expected effect size, as discussed in Chapter 16.

*  Particular kinds of subjects will seek out studies to join, rather than
    getting subjects volunteering purely at random.

*  Joining a study will cause participants to change their behavior, called the
    Hawthorne effect.  Scientists are measuring you!  You will change up your
    patterns in anticipation of the measurement.  Or if you know you're in the
    control group, you may try to do what the treatment group is doing anyway,
    now that you know that's an option (and a potentially beneficial one).

*  Researchers doing measurements, if they know a subject's treatment status,
    consciously or unconsciously change up their measuring habits as a function
    that status.

*  Your treatment subjects might refuse the treatment, either altogether, or
    halfway through.  Your control subjects might get bored and walk away before
    they can have their outcome measured.  Noncompliance works against the
    benefits of randomization by introducing a selection bias.


## Exercises

Plots and computation powered by [Chapter18.ipynb](./notebooks/Chapter18.ipynb)

### 18.4, Average treatment effects

> The table below describes a hypothetical experiment on 8 people.  Each row of
> the table gives a participant and her pre-treatment predictor $x$, treatment
> indicator $z$, and potential outcomes $y^0$ and $y^1$.
> 
> |    | $x$ | $z$ | $y^0$ | $y^1$
> ---- | --- | --- | ----- | -----
> Anna |   3 |   0 |     5 |  5
> Beth |   5 |   0 |     8 | 10
> Cari |   2 |   1 |     5 |  3
> Dora |   8 |   0 |    12 | 13
> Edna |   5 |   0 |     4 |  2
> Fala |  10 |   1 |     8 |  9
> Geri |   2 |   1 |     4 |  1
> Hana |  11 |   1 |     9 | 13
> 
> (a) Give the average treatment effect in the sample, the average treatment
>     effect among the treated, and the estimated treatment effect based on a
>     simple comparison of treatment and control.
>
> (b) Simulate a new completely randomized experiment on these 8 people; that
>     is, resample $z$ at random with the constraint that equal numbers get the
>     treatment and the control.  Report your new randomization and give the
>     corresponding answers for (a).

With the original group assignments:

*  **Average treatment effect:** 0.12
*  **Average treatment effect among the treated:** 0.0
*  **Simple comparison of treatment and control:** -0.75

Reshuffled to $z = \{0, 0, 0, 0, 1, 1, 1, 1\}$ (dumb luck!):

*  **Average treatment effect:** 0.12  (doesn't depend on $z$)
*  **Average treatment effect among the treated:** 0.0  (sheer luck)
*  **Simple comparison of treatment and control:** -1.25

Reshuffled again to $z = \{0, 1, 1, 0, 0, 0, 1, 1\}$

*  **Average treatment effect among the treated:** 0.25
*  **Simple comparison of treatment and control:** -0.5

### 18.5, Potential outcomes

> The table below describes a hypothetical experiment on 2400 people. Each row
> of the table specifies a category of person, as defined by his or her
> pre-treatment predictor $x$, treatment indicator $z$, and potential outcomes
> $y^0$, $y^1$. For simplicity, we assume unrealistically that all the people
> in this experiment fit into these eight categories.
> 
> Category | # people in category | $x$ | $z$ | $y^0$ | $y^1$
> -------- | -------------------- | --- | --- | ----- | -----
> 1 | 300 | 0 | 0 |  4 | 6
> 2 | 300 | 1 | 0 |  4 | 6
> 3 | 500 | 0 | 1 |  4 | 6
> 4 | 500 | 1 | 1 |  4 | 6
> 5 | 200 | 0 | 0 | 10 | 12
> 6 | 200 | 1 | 0 | 10 | 12
> 7 | 200 | 0 | 1 | 10 | 12
> 8 | 200 | 1 | 1 | 10 | 12
> 
> In making the table we are assuming omniscience, so that we know both $y^0$
> and $y^1$ for all observations. But the (non-omniscient) investigator would
> only observe $x$, $z$, and $y^z$ for each unit. For example, a person in
> category 1 would have $x =0, z=0, y =4$, and a person in category 3 would have
> $x =0, z=1, y =6$.
>
> (a) What is the average treatment effect in this sample of 2400 people?
> 
> (b) Another summary is the mean of $y$ for those who received the treatment
>     minus the mean of $y$ for those who did not. What is the relation between
>     this summary and the average treatment effect (ATE)?
>
> (c) Is it plausible to believe that these data came from a completely
>     randomized experiment? Defend your answer.
> 
> (d) For these data, is it plausible to believe that treatments were assigned
>     using randomized blocks conditional on given $x$? Defend your answer.

(a) The ATE is 2.00.

(b) The different in mean outcomes is 1.31.  When the $z$ values are randomly
    assigned, this value will eventually converge to the ATE.  Under random
    assignment, there's no systematic difference in the $y^0$ as a function of
    our study observing them.  So the mean of the factual in the control group
    is an unbiased estimate of the mean of the *counter*factual in the treatment
    group.

This seems plausibly a completely randomized experiment.  There's no imbalance
in $x$ values between treatment and control, nor in the category sizes.  If
this was from blocking conditional on $x$, we'd expect to see some difference in
$z$ values across the levels of $x$ -- that's the whole point of randomized
block designs.