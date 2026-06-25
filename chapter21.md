# Chapter 21: Additional topics in causal inference

[(Return to README)](./README.md)

Closing out Part 5, this chapter goes into how to proceed if you want to weaken
the ignorability assumption.  They also introduce connections between the
causal effect estimates we've been making and "causal explorations or searches
for causes of patterns in observed data."

## Subsection rundown

### 21.1, Estimating causal effects indirectly using instrumental variables

Sometimes, you have a predictor in your observational study that is close enough
to random.  If this variable is predictive of the treatment of instrument, you
can call it the *instrument* that can help tease out a casual effect estimate
(even if the treatment assignment itself is confounded/nonrandom).  The catch
is that the instrument can't have any effect on the outcome, except by way of
its effect on the treatment (the *exclusion restriction*).

The example they have is a hypothetical study of "does watching Sesame Street
help kids learn their numbers."  Except actually enforcing random treatment --
making kids watch -- is impractical, and instead the randomization is on who is
*told* to watch Sesame Street.  If you just do the regression on the
"encouraged?" indicator, Chapter 19 style, that's an intent-to-treat estimate
(ITT).

This section goes into an alternative approach.  Call the amount actually
watched by each unit an intermediate potential outcome.  The study can only talk
about effects who would not have watched Sesame Street but for the
encouragement; the book calls them *compliers*.  Three other categories of unit:
*never-takers* (didn't watch if encouraged, wouldn't watch if not encouraged),
*always-takers* (would watch no matter what), and *defiers* (purposefully
does the opposite of the study proctor's instructions: watching if not
encouraged, and not watching if encouraged).  If you assume away the existence
of defiers, then only the compliers shed light on the treatment effect, since
they're the only kind of unit who gives us a view on both their potential
outcomes.  Running an analysis of the compliers gives the *complier average
causal effect (CACE)*.

Instrumental variable estimation, in its formal mode, builds up to the above
paragraph with four assumptions:

1.  **Ignorability of the instrument:**  Is there a predictor that's assigned
    randomly, or as-good-as-random?  If not, are all the potential confounders
    available to resurrect ignorability a la Chapter 20?

2.  **Monotonicity:** The instrument can only increase the odds of taking up the
    treatment.  This is the "assume there are no defiers in the study" part.

3.  **Nonzero association between instrument and treatment variable:** You can
    check for this right in the data.  Does the treatment group show higher
    rates of treatment uptake than the control group?

4.  **Exclusion restriction:** The encouragement has no further impact on the
    outcome outside of treatment uptake.  The exposure to Sesame Street has no
    stronger influence on numbers-learning just because you were encouraged to
    watch, is the assumption being made.  (And similarly, encouragement alone
    is not enough to affect the potential outcome if the subject never takes up
    the treatment.)

The section then goes God Mode and provides a table where we see not only the
potential outcomes with and without treatment uptake, but also the
complier/never-taker/always-taker indicator for each subject.  They boil it down
to calculating four ITT estimates across the four types of subject (complier et
al), plus the normal overall ITT estimate.  Equation 21.1 is the payoff:

$$\text{CACE} = \frac{\text{ITT}}{\mathbb{E}(T(z = 1)) - \mathbb{E}(T(z = 0))}$$

So just look up the treatment uptake rates in the two groups, and divide the
overall ITT by that rate difference to get the CACE.  The big takeaway here is
that if the instrument *isn't* an effective driver of uptake, then that
denominator becomes unstably small.  They step through how violations of each of
the four assumptions play out, and in all of them, a weak instrument makes
things much worse.

The software they write at the end to actually perform the CACE estimate for the
Sesame Street study is three steps:

1.  Find a coefficient for predicting uptake from `encouraged`
2.  Find a coefficient for predicting the outcome from `encouraged`
3.  Divide (2) by (1)

They promise a derivation of standard error for that ratio (called a *Wald
estimate*) is coming later.

### 21.2, Instrumental variables in a regression framework

That three step process I closed out immediately above in Section 21.1 gets an
algebraic representation:

$$y_i = \beta_0 + \beta_1T_i + \beta_2z_i + \epsilon_i$$
$$T_i = \gamma_0 + \gamma_1z_i + \nu_i$$

The ignorability assumptions requires $z_i$ to be uncorrelated with noise
factors $\epsilon_i$ and $\nu_i$.  The exclusion restriction requires $\beta_2$
to be zero.  The nonzero association and monotonicity assumptions require that
$\gamma_1$ be positive.

They note that there's no guarantees that $T$ is uncorrelated with $\epsilon$,
so you can't just grab the coefficient estimate and call that $\beta_1$.  You
don't have identifiability; $T$ could be collinear with some omitted variable
that's driving the outcome difference.

With some substitutions and term definitions:

$$y = (\beta_0 + \beta_1\gamma_0) + (\beta_1\gamma_1 + \beta_2)z + \text{error}$$
$$\delta_0 = \beta_0 + \beta_1\gamma_0$$
$$\delta_1 = \beta_1\gamma_1 + \beta_2$$
$$y = \delta_0 + \delta_1z + \text{error}$$
$$\Rightarrow \beta_1 = (\delta_1 - \beta_2)/\gamma_1$$

Estimating $\gamma_1$ is straightforward regression of $T$ on $z$ if $z$ is
"random enough" that we know it's not correlated with the $\nu$ error terms.
And estimating $\delta_1$ works the same way, by regressing $y$ against $z$.

As long as $\beta_2$ is zero -- the exclusion restriction! -- then you can back
out $\beta_1$ with two ignorability-assumption-hardened regressions on the
instrument $z$.

They implement this with *two-stage least squares*:

1.  Fit a model $M_1$ of `T ~ z` (feel free to include other covariates here, in
    addition to $z$)
2.  For each unit, calculate the predicted $T$ value based on $M_1$, `T'`
3.  Fit a model $M_2$ of `y ~ T'`; use the $M_1$ predictions as the input to
    $M_2$.  (If you included other covariates in step 1, include them here,
    too.)

The mean of the coefficient estimate will give you the CACE, but the standard
error you read out of the $M_2$ fit will *not* reflect a correct level of
uncertainty.  The calculation doesn't loop in uncertainty in the input `T'`,
even though we know the predictions from $M_1$ are noisy; nor does it consider
the correlation of $T$ with $\epsilon$.

You need to multiply the naive standard error by a ratio of:

*  **Numerator:** The root mean squared error when applying $M_2$ where the $T$
    values are the *actually observed* treatment-uptake values
*  **Denominator:** The root mean squared error when applying $M_2$ where the
    $T$ values are the predicted uptake values that $M_1$ provides

A bunch more caveats:

*  You need as many instruments as there are treatment variables to preserve
    identifiability.
*  Continuous valued treatments require a parametric assumption, or else it's
    the same situation of many treatments (the different "dosages") but only one
    instrument.
*  You better be real, real sure that the instrument satisfies the ignorability
    constraint!
*  Try to come up with ways to check the exclusion restriction.  Are there
    units that got the $z = 1$ instrument but *couldn't* have taken up the
    treatment, even if they wanted to?  That's a good source for checking the
    effect of encouragement on the outcome (and making sure it's nil).
*  What if compliers are just weirdos?  What if the CACE tells you something
    about compliers that doesn't apply to any of the other three classes of
    subject?

They close with a pair of paragraphs about the advanced topic of structural
equation models, of which instrumental variable models are a special case.
It includes this important line:

> \[E\]ven in a relatively simple instrumental variables model, the assumptions
> needed to identify causal effects are difficult to satisfy and largely
> untestable.

SEMs bring in even more assumptions (e.g., about conditional independence
structure, or "multivariate normality of errors"), which means even more
untestable modeling assumptions.

### 21.3, Regressoin discontinuity: known assignment mechanism but no overlap

There are times when you really do have perfect coverage of the confounders
that drive treatment group assignment, but still can't run the playbook from
Chapter 19 or 20.  A totally deterministic rule for assignment to the treatment
group like "any baby below 2.5 kg is treated; all babies above 2.5 kg aren't"
is not missing any hidden variables.  Instead, the trouble is zero overlap
between the two groups.

The regression discontinuity approach says to just zoom in on the subjects that
live quite close to the deterministic classification boundary.  They live in the
same general neighborhood, so comparability *probably* holds.  The book
highlights the tension between how wide that threshold of "close to the
boundary" is.  Too narrow, and you drop too much data to learn anything; too
wide, and you're losing comparability between the subgroups.

They walk through an example where Chilean elementary schools were given a test,
and schools with low average scores were given an intervention to improve
things.  "Low" was defined by some threshold, which the data translates as the
zero point of a pretreatment predictor $x$, to give a regression model for
predicting next year's test scores ($y$):

$$y = \beta_0 + \tau z + \beta_1 * x + \text{error}$$

where $z$ is 0 when $x$ is negative and 1 otherwise.  The actual range of $x$
covers -20 to 40, but they restrict to just -5 to 5 as their comparability
window.  (That cuts data volume: they throw away two-thirds of the subjects this
way.)  When they fit this model, they see an estimate of $\tau$ that's 2 with a
standard error of 1.  Though by the time they add some richer pre-treatment
predictors and interactions, that shifts to 1.5 with a s.e. of 1.5.

They talk about how hanging any causal inference on this regression requires
"an assumption that no confounders vary discontinuously across the threshold."

There's a related case, the fuzzy discontinuity, where the strict deterministic
treatment assignment rule is occasionally violated.  On the one hand, cool!, we
get some overlap back.  But on the other, worse hand, oof!, now we have lost the
ignorability assumption.  The violation cases are probably distinct in some way,
which means you need a way to adjust for whatever confounder is now producing
the group selection.

They relate fuzzy regression disconuity conceptually to instrumental variables. 
The strict deterministic assignment rule is the encouragement.  The same four
assumptions need checking: ignorable instrument (which you get by setting a
sufficiently narrow window around the discontinuity boundary), the exclusion 
restriction, monotonicity (no defiers!), and a predictive link between
encouragement and treatment.  If you have all four, you can produce a CACE.

Turns out the Chilean schools example is fuzzy, *very* fuzzy.  "\[A\]bout 39% of
those who were defined as eligible did not receive the program."

### 21.4, Identification using variation within or between groups

#### Comparisons within groups using varying-intercept ("fixed effects") models

They ask us to imagine groups where (a) there are unobserved/unobservable
characteristics, (b) that are common/constant across all members of the group,
and (c) we can take multiple measures from the group.  This let's us adjust for
those unobserved, unspecified characteristics -- which vary a lot *between*
groups -- to learn about a relationship we can/do observe.

They immediately tie this to twin studies.  Two twin babies will have many, many
things in common, that they don't share with any old other random pair of twins.
Family structure, prenatal care, lots of hereditary factors: all held in common.
"In essence, then, each twin acts as a counterfactual for his or her sibling."

To harness this, run the regression where each group (e.g., twin pair) gets its
own intercept term:

$$y_{ij} = \beta_0 + \tau z_{ij} + \alpha_i + \epsilon_{ij}$$

where $z_{ij}$ is the treatment predictor for the $j\text{th}$ subject drawn
from the $i\text{th}$ group.  You can also predict the deviation from the group
mean, which works fine when all group sizes are two, but introduces more
uncertainty when you are estimating the group mean from the data itself.

For causal inference:

1.  You'll need to include within-group means of the treatment variable as a
    group-level predictor, to try and adjust coarsely for confounders.  (If you
    think you actually have all the group-level confounder values in your
    dataset, use those.)

2.  You need non-trivial variation in the treatment variable within each group.
    You can't study effects of low birth weight using a twin study if twins are
    always the same birth weight.

One especially prominent use case of varying-intercept models are panel data,
where the same person is measured repeatedly over some time.  This can hit a
snag if you adjust for the subject's covariates as measured at each time, since
some of those are downstream of earlier treatment values.  But ruling out any
possibly-post-treatment predictor can wind up leaving you with too few
predictors to justify ignorability.

#### Comparisons within and between groups: difference-in-differences estimation

The treatment-control comparison looks at changes in outcomes across groups.
Difference-in-differences brings in another dimension of outcome variation,
like time.  The hope is that this adjusts for differences between these groups.
Don't just compare outcomes in treat vs. control; there could be selection bias.
Don't just compare pre-treat measure of the outcome attribute vs. post-treat
outcome for the treated group; who knows what else happened alongside the
treatment that explains the gap.  Instead, compare the pre-post change among
treated units to pre-post change among controls.  That's
difference-in-differences.

In algebra:

$$y_i = \beta_0 + \beta_1z_i + \beta_2P_i + \tau z_iP_i + \epsilon_i$$

where $$P_i$$ is a time period for subject $i$, taking on 0 for pre-exposure
and 1 for post-exposure measurements.  Treat and control get their own
intercepts, plus their own slopes w.r.t. the passage of time.

This works even if you only see each subject for only one of the time periods --
*if* you assume the sampling at each time instant was from a common
distribution.

If you do see every subject in both time periods, you have dependence between
units of the regression, which you can fix by predicting the difference instead:

$$d_i = \alpha + \tau z_i + \nu_i$$

**NOTE!!** This is *not* how Equation 21.9 puts it; I think they have a typo and
put in $P_i$ instead of $z_i$.

### 21.5, Causes of effects and effects of causes

Part 5 of the book has focused on the effects of causes: when you take this
pill, does it cause anything notable to happen?  Except in almost every
situation, people want to know causes of effects: something notable happened,
what caused it?  We don't have a great statistical toolset for that, not in
Part 5 anyway.

They add some mathy looking bits about it -- to say an outcome is notable, is to
say you have some model of what the outcome *should* have been.  That model can
be formalized, and the notable outcome can be looked at through the lens of that
model:

*  Maybe the we're missing a causal variable driving a potential-outcomes model
    this whole time, where the variable is selecting one or the other outcome,
    and just so happens to be favoring one class.  Conditioning on the current
    set of predictors, plus that potential outcomes framework, explains away
    the notability of the outcomes.

*  Or, and it's hard to say how different this really is from the prior version,
    maybe we have ignored or omitted an important additional attribute from the
    current set of predictors.  Looking at the current notable outcome could
    point us toward a new candidate predictor (or two, or three) that including
    them would reset our model.  The outcome wouldn't be so notable or
    surprising any more; the effect was explained away.

They stress that there's no way to pin down unique answers.  I think this is
synonymous with saying this kind of investigation can lend itself to weak
theories and wild guesses, just grab the first thing that makes the residuals
go away.  Our model checking, like LOO-CV, can sort of help with this, but we
really are HARKing here.

This is one of the most important sections in the book.


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer