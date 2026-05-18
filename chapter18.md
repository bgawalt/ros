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

### 18.7,  Before-after comparisons

> The
> [folder `Sesame`](https://github.com/avehtari/ROS-Examples/tree/master/Sesame/data)
> contains data from an experiment in which a randomly selected group of
> children was encouraged to watch the television program Sesame Street and the
> randomly selected control group was not.
>
> (a) The goal of the experiment was to estimate the effect on child cognitive
>     development of watching more Sesame Street. In the experiment,
>     encouragement but not actual watching was randomized. Briefly explain why
>     you think this was done. Think of practical as well as statistical
>     reasons.
>
> (b) Suppose that the investigators instead had decided to test the
>     effectiveness of the program simply by examining how test scores changed
>     from before the intervention to after.  What assumption would be required
>     for this to be an appropriate causal inference?  Use data on just the
>     control group from this study to examine how realistic this assumption
>     would have been.
>
> We return to this example in Chapter 21.

(a) Randomizing the actual watching would have meant having some reliable way of
    making sure the subject followed through with the prescribed watch time.
    This is expensive if you need to set up a monitoring protocol at the
    home of each subject.  Or it drives down participation if you require
    subjects to come on-site for monitoring the watch-time.  (The first one
    is gonna drive down participation, too.)  And finally, in terms of
    estimating effects in the real world, the general population is not going to
    have any kind of monitoring set up.  So your design should reflect your
    actual research question: what would happen if we encouraged more families
    to watch Sesame Street?

(b) To just do a pre-post design, you'd have to assume that absent the
    intervention, test scores would remain the same.  This is implausible!
    For one thing, families and schools want kids to learn, and will try and
    get them to be smarter in ways that will show up in improved test scores,
    even without being told to watch Sesame Street.

We can see that this doesn't hold by scatterplotting the post-intervention test
scores against pre-intervention test scores, just among the control group.
In general, they go up!  They aren't even noisily clustered around the dashed
line where `pre = post`.  (These two particular tests are chosen because they're
of interest in Exercise 18.8.)

![Two subplots of scatterplots.  At left, blue dots show 'Letters post-test
score' on the y-axis and 'Letters pre-test score' on the x-axis.  At right, red
dots show 'Numbers post-test score' on the y-axis and 'Numbers pre-test score'
on the x-axis.  There are dashed grey lines of equality on each subplot; each
subplot goes from 0 to 58 on each axis.  In general, dots tend to fall above the
dashed line of equality](./fig/part5/ex18_07_ctrlgroup.png)

### 18.8, Evaluating an encouragement design

> Return to the Sesame Street example from the previous exercise. Did
> encouragement (the variable viewenc) lead to an increase in post-test scores
> for letters (`postlet`) and numbers (`postnumb`)?  Fit an appropriate model to
> address this question.

I fit the Letters test model with

```
postlet ~ encour + regular + sex + age + viewcat + setting + prelet + prenumb + peabody
```

and get the coefficients:

Coef.     | Mean  | s.e.
--------- | ----- | ------
sigma     |  9.22 | 0.42
Intercept | -8.29 | 6.04
encour    |  1.16 | 1.45
regular   |  2.06 | 2.37
sex       |  1.05 | 1.22
age       |  0.01 | 0.11
viewcat   |  3.66 | 0.86
setting   |  1.78 | 1.34
prelet    |  0.44 | 0.10
prenumb   |  0.25 | 0.10
peabody   |  0.14 | 0.05

So, no, I don't see strong evidence that the treatment (coded as the `encour`
predictor, where 0 is control and 1 is treatment) definitely or substantially
improved test scores.  The mean is small compared to the residual noise
(`sigma`), and its standard error is large compared to the mean.

(I didn't do any scaling of the predictors, so they can't be especially compared
to each other on a consistent basis.)

I fit the Numbers test model with

```
postnumb ~ encour + regular + sex + age + viewcat + setting + prelet + prenumb + peabody
```

Similar results for the `encour` coefficient:

Coef.     | Mean  | s.e.
--------- | ----- | ------
sigma     |  8.80 | 0.41
Intercept | -7.45 | 5.67
encour    |  0.45 | 1.39
regular   |  2.46 | 2.20
sex       |  0.81 | 1.15
age       |  0.15 | 0.10
viewcat   |  2.44 | 0.80
setting   |  1.80 | 1.29
prelet    |  0.09 | 0.10
prenumb   |  0.52 | 0.09
peabody   |  0.11 | 0.04

The evidence of a useful treatment effect is even weaker here.

But.  We haven't actually talked about how to pose these models.  I'm just
dumping all these predictors in the top of a meat grinder and turning the crank.

### 18.12, Simulating potential outcomes

> In this exercise, you will simulate an intervention study with a
> pre-determined average treatment effect.  The goal is for you to understand 
> the potential outcome framework, and the properties of completely randomized
> experiments through simulation.
>
> The setting for our hypothetical study is a class in which students take two
> quizzes.  After quiz 1 but before quiz 2, the instructor randomly assigns half
> the class to attend an extra tutoring session.  The other half of the class
> does not receive any additional help.  Consider the half of the class that
> receives tutoring as the treated group.  The goal is to estimate the effect of
> the extra tutoring session on average test scores for the retake of quiz 1.
> Assume that the stable unit treatment value assumption is satisfied.
>
> (a) Simulating all observed and potentially observed data (omniscient mode).
>     For this section, you are omniscient and thus know the potential outcomes
>     for everyone.  Simulate a dataset consistent with the following
>     assumptions.
>
> > i. The average treatment effect on all the students, $\tau$, equals 5.
> >
> > ii. The population size, $N$, is 1000.
> >
> > iii. Scores on quiz 1 approximately follow a normal distribution with mean
> >     of 65 and standard deviation of 3.
> >
> > iv. The potential outcomes for quiz 2 should be linearly related to the
> >     pre-treatment quiz score. In particular they should take the form,
> >
> > $$y^0 = \beta_0 + \beta_1x + 0 + \epsilon^0,$$
> > $$y^1 = \beta_0 + \beta_1x + \tau + \epsilon^1,$$
> >
> > where the intercept $\beta_0 = 10$ and the slope $\beta_1 = 1.1$.  Draw the
> > errors $\epsilon^0$ and $\epsilon^1$ independently from normal distributions
> > with mean 0 and standard deviations 1.
>
> (b) Calculating and interpreting average treatment effects (omniscient mode).
>     Answer the following questions based on the data-generating process or
>     using your simulated data.
>
> > i. What is your interpretation of $\tau$?
> >
> > ii. Calculate the sample average treatment effect (SATE) for your simulated
> >     dataset.
> > 
> > iii. Why is SATE different from $\tau$?
> >
> > iv. How would you interpret the intercept in the data-generating process
> >     for $y^0$ and $y^1$?
> >
> > v. How would you interpret $\beta_1$?
> >
> > vi. Plot the response surface versus $x$. What does this plot reveal?
>
> (c) Random assignment (researcher mode).  For the remaining parts of this
>     exercise, you are a mere researcher!  Return your goggle of omniscience
>     and use only the observed data available to the researcher; that is, you
>     do not have access to the counterfactual outcomes for each student.
>     Using the same simulated dataset generated above, randomly assign students 
>     to treatment and control groups. Then, create the observed dataset, which
>     will include pre-treatment scores, treatment assignment, and observed $y$.
>
> (d) Difference in means (researcher mode).
>
> > i. Estimate SATE using a difference in means.
> >
> > ii. Is this estimate close to the true SATE?  Divide the difference between
> >     SATE and estimated SATE by the standard deviation of the observed
> >     outcome, $y$.
> >
> > iii. Why is $\hat{\text{SATE}}$ different from SATE and $\tau$?
>
> (e) Researcher view: linear regression.
>
> > i. Now you will use linear regression to estimate SATE for the observed data
> >     created as above.  With this setup, you will begin to better understand
> >     some fundamental assumptions crucial for the R homework assignments in
> >     the following chapters.
> >
> > ii. What is gained by estimating the average treatment effect using linear
> >     regression instead of the mean difference estimate from above?
> >
> > iii. What assumptions do we need to make in order to believe this estimate?
> >     Given how you generated the data, do you believe these assumptions have
> >     been satisfied?

#### 18.12(b)

$\tau$ is the difference the treatment makes, on average.  When a subject is
given the treatment, their score on the next test should be expected to rise by
5 points above the original test score.

The SATE is 5.02, which is close to $\tau$'s value of 5, plus some sampling
error.

The intercept term, $\beta_0$, is the amount that you should expect every
student's score to rise between the pre-test and the post-test.  Everyone's
spent an additional few months in class, and in expectation, that will increase
everyone's scores by 10 points.

The slope term, $\beta_1$, is how much a student's score is expected to increase
as a function of their pre-test score.  That it's 1.1 indicates that everyone is
expected to do 10% better than their pre-test value, on top of the 10 points
gain that applies universally.  That 10% means that students who did well on the
first test, will gain more absolute points (in expectation) than the students
who scored lower.  Kind of a compound interest, rich get richer thing.

The response surface shows that, adjusting for pre-treatment test score, the
treatment effect $\tau$ is clearly shifting post-treatment test scores up.
There's basically no overlap between the two clouds for the $y^0$ and $y^1$
potential outcomes:

![Scatterplot. x-axis: Pre-test score, 50 to 80.  y-axis: Post-test score, 70 to
100.  Two high-eccentricity elliptical clouds, tilting upwards at a roughly 45
degree angle, are plotted, with x values between 55 and 72, save a few outliers.
In magenta, treatment outcomes have a vertical range of 75 to 95.  In cyan,
lower than the other, control outcomes have a vertical range of 70 to 90.
](./fig/part5/ex18_12b_responsesurface.png)

#### 18.12(d)

The estimated SATE is 4.7, versus our earlier omniscient SATE of 5.0.  If
$s_y$ is the sample standard deviation of $y$, that's a difference of $0.08s_y$.
This is a close estimate.

$\tau$, SATE, and $\hat{\text{SATE}}$ are all different due to sampling, with
the last link (from SATE to estimated SATE) being due to the random assignment
of treat/control.  With SATE we had access to all potential outcomes; now, we
have some sampling noise around which ones wound up in treatment and control.
Also, we have half as much data going into the means of the treatment and
control outcomes, so standard errors of those mean estimates are also quite
a bit wider.

#### 18.12(e)

When I fit the model `y ~ x + z`, I get the coefficient estimates:

Coef.     | Mean  | s.e.
--------- | ----- | ------
sigma     |  0.99 | 0.02
Intercept | 10.28 | 0.71
x         |  1.09 | 0.01
z         |  4.98 | 0.07

These coefficients are all bang-on accurate relative to the true values I coded
into the simulation.

By using linear regression, I am making it *much* easier to incorporate (a) more
pre-treatment predictors, and (b) richer expressions of the treatment (like,
different dosages or different durations or different exposures, per subject).

To believe these estimates, I need to assume that $z$ and $x$ are independent of
each other, which I definitely do in this case.  I believe the PRNG I rolled is
sufficiently chaotic that $z$ and $x$ can't be predicted from each other.

### 18.13, Varying treatment effect

> Now you will explore a situation where treatment effect varies by a known
> covariate.
>
> (a) Simulate data from the following response surface and plot both curves,
>
>  $$y^0 = \beta_0^0 + \beta_1^0x + \epsilon^0,$$
>  $$y^1 = \beta_0^1 + \beta_1^1x + \epsilon^1,$$
>
>  where $\beta_0^0 = 35$, $\beta_1^0 = 0.6$, $\beta_0^1 = 15$,
>     $\beta_1^1 = 1$, and $\epsilon^0$ and $\epsilon^1$ are drawn independently
>     from normal distributions with mean 0 and standard deviation 1.
>
> (b) Comment on your findings. In particular, there is no longer a $\tau$
>     included in the data-generating process. Is there still a sample average
>     treatment effect? What is it? How do you interpret the average treatment
>     effect in this setting?
>
> (c) Is the treatment effect the same for all students? If not, is there a
>     pattern to the way it varies?  Why should you care about variation in the
>     treatment effect?
>
> (d) Plot the response surface versus $x$. What does this plot reveal,
>     particularly as compared to the plot from the previous question?

Here's the response surface for $N = 1000$ data points,
$x ~ \mathcal{N}(65, 3)$:

![Similar to the above repsonse surface scatter plot, though now, the magenta
Treatment cloud tilts upwards more than the cyan Control cloud does.  They very
slightly overlap for pre-test scores below 60.](./fig/part5/ex18_13_varied_effect.png)

Again, the treatment outcomes are consistently higher than the control outcomes.
There is indeed a SATE -- we can calculate it at 5.92 points this time.

But the treatment clearly varies.  When the pre-test score is below 62 or so, we
start to see some overlap, where control outcomes exceed treatment outcomes.
In the previous exercise, that basically never happened.

We care about this because if this treatment is going to become a standard
practice, we need to make sure everyone understands whether we're saying the
treatment achieves its average lift by affecting everyone basically to the same
degree, or if the gains are concentrated in one group or another.  Knowing how
the treatment effect varies tells us what follow-up treatments to look for next:
like, for *this* treatment, it's telling us that we should target the next
treatment to students who are currently scoring lower than average.

### 18.14, Completely randomized experiment

> In a completely randomized experiment, the number of treatment and control
> units is decided in advance, and each unit has the same probability of being
> assigned to receive the treatment.  This exercise extends Exercise 18.12 by
> comparing the same estimates with respect to both bias and efficiency.
>
> You will operationalize these properties by appealing to randomization-based
> inference.  Therefore you will create a randomization distribution (similar to
> a sampling distribution) for each estimate.  This distribution only considers
> the variability in estimates that would manifest as a result of the randomness
> in who is assigned to receive the treatment.
>
> (a) Simulate the dataset from Exercise 18.12.  You will use this as your
>     observed data.
>
> (b) Now create a randomization distribution for each estimate by following
>     these steps:
>
> > i. Create a vector of length 10,000 for each estimate to save these
> >     estimates across simulated datasets. These could be named, for instance,
> >     `dm_res` and `ols_res`.
> >
> > ii. For the $r^{\text{th}}$ simulated draw, generate a new treatment
> >     assignment vector using the `rbinom()` or `sample()` function in R.
> >     Use it to generate a new outcome vector, recalling that
> >     $y = (1 - z) y^0 + z y^1$.
> >
> > iii. Apply each of the estimates (difference in means and linear regression
> >     with the one covariate) to the newly generated dataset. Save each
> >     estimate as the rth item in the results vector.
> >
> > iv. Repeat 10 000 times.
>
> (c) We will use these estimates to create a Monte Carlo estimate of a
>     randomization distribution for each of these estimates for the sample
>     average treatment effect.
>
> (d) Plot the randomization distribution for each of the two estimates:
>     difference in means and regression.  Either overlay the plots (with
>     different colors for each) or make sure the x-axis range on both plots is
>     the same. Also add vertical lines (using different colors) for the SATE
>     and the mean of the randomization distribution.
>
> (e) Use these distributions to calculate the bias of each of these two
>     methods.  What is the difference between methods with respect to bias?
>
> (f) Use these distributions to calculate the efficiency of each of these two
>     methods. What is the difference between methods with respect to
>     efficiency?
>
> (g) Re-run the simulation by first generating data as in Exercise 18.12 but
>     with a zero coefficient for the pre-treatment score. Does the zero
>     coefficient lead to a different bias and efficiency estimate compared to
>     when the coefficient for pre-treatment score was at 1.1 from before?

Yup, regression that includes the pre-treatment predictor is much more
sample efficient than the difference-of-means that just hopes the pre-treatment
predictors cancel out eventually:

![Two overlapping and slightly transparent histograms of estimated treatment
effect sizes.  In blue, the difference of means treatment effect estimator has
a much wider spread, from 4.6 to 5.4.  In red, there's a tighter spread between
4.9 and 5.2.  The SATE has a vertical black line at 5.06.
](./fig/part5/ex18_14_histograms.png)

When we zero out the effect of the pre-treatment predictor, the diff-of-means
method is just as efficient as the regression method:

![Same as the immediately preceding figure, but now the histograms are both
concentrated in the same 4.9 to 5.2 range
](./fig/part5/ex18_14g_hist_no_pretest.png)

### 18.15, Randomized block design with interactions

> In a randomized block design, randomization occurs separately within blocks,
> and the ratio of treatment to control observations is allowed to vary across
> blocks.  And, as always, the underlying treatment effect can vary across
> blocks.
>
> For this exercise, you will simulate datasets for a randomized block design
> that includes sex as a blocking variable.  You will then estimate the average
> treatment with two estimates: one that accounts for the blocking structure and
> one that does not.  You will compare the bias and efficiency of these
> estimates. We will walk you through this in steps.
> 
> (a) First simulate the blocking variable and potential outcomes. In
>     particular:
> 
> *  Generate sex as a blocking variable, with 30% female and 70% male.
> *  Generate y0 and y1 with the following features:
>    *  The intercept of the regression of $y$ on treatment indicator, block
>          indicator, and their interaction, is 70.
>    *  The residual standard deviation is 1.
>    *  Treatment effect varies by block: the average treatment effect is 7 for
>          women and 3 for men. Further assume that men and women have no 
>          average difference under the control.
>
> (b) Calculate the sample average treatment effect (SATE) overall and for each
>     block.
>
> (c) Now create a function for assigning the treatment.  In particular, within
>     each block create different assignment probabilities:
>
>  $$\text{Pr}(z = 1 | \text{male}) = 0.6,$$
>  $$\text{Pr}(z = 1 | \text{female}) = 0.4.$$
>
> (d) Generate the treatment and create a vector for the observed outcomes
>     implied by that treatment.  We will use this to create a randomization
>     distribution for two different estimates for the SATE. Take 100,000 draws
>     from that distribution.
>
> (e) Plot the Monte Carlo estimate of the randomization distribution for each
>     of the two estimates: difference in means and regression.  Either overlay
>     the plots (with different colors for each) or make sure the x-axis on both
>     plots is the same.
>
> (f) Calculate the bias and efficiency of each estimate.  Also calculate the
>     root mean squared error.
>
> (g) Consider the estimate that ignores the blocking. Why is it biased?  Is the
>     efficiency meaningful here?  Why did we ask you to calculate the root mean
>     squared error?
>
> (h) Describe one possible real-life scenario where treatment assignment
>     probabilities or treatment effects vary across levels of a covariate.
>
> (i) How could you use a regression to estimate the treatment effects
>     separately by group?  Calculate estimates for our original sample and
>     treatment assignment.

The SATE estimates:

*  SATE: 4.22
*  SATE for men: 3.07
*  SATE for women: 7.09

When calculating from the factual outcomes only, and re-drawing the $z$
assingments 100 times, we get the histograms:

![Two histograms of estimated treatment effect, running from 3.5 to 4.5 on the
x-axis.  In cyan, the diff-of-means estimates are spread from 3.6 to 4.4.  In
magenta, the regression estimates range from 4.0 to just under 4.5.  The actual
SATE is 4.3, which the magenta histogram is centered around (but the cyan
histogram isn't).](./fig/part5/ex18_15_histograms.png)

*  Difference of means: mean 4.02, std. dev. 0.20
*  Regression: mean 4.30, std. dev. 0.15

So the difference-of-means approach is about one standard error away from SATE
(which is not bad; it covered the spread).  The regression method, though,
is much closer in expectation, and also lower variance.

If I fit the model `y ~ x + z + x:z`, I get:

Coef.     | Mean  | s.e.
--------- | ----- | ------
sigma     |  0.95 | 0.06
Intercept | 70.26 | 0.19
x         | -0.16 | 0.24
z         |  6.92 | 0.34
x:z       | -4.17 | 0.39

This looks good to me!  It's recovering the residual noise level, plus the
intercept term, exactly.  The default treatment effect (where $x$ is 0) is the
value of 7 that we coded in part (a).  It's got an effect on the gender
predictor that is basically nil, but that is because it's moved that (important)
effect into the interaction term `x:z`.  For male subjects, the effect of $z$ is
reduced from 7 to 3, just like we coded into the data synthesis.