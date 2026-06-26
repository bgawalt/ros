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

### TK 21.1, Instrumental variables

> The following study is performed at a university.  Students are sent emails
> encouraging them to click on a university website.  Each student is randomly
> assigned to one of two sites: a site with encouragement to vote in the
> upcoming student government election, and a neutral site with study tips.  The
> students are then followed up to see if they voted. Define $y = 1$ if the
> student voted or 0 otherwise; define u = 1 if the student was assigned to the
> encouragement site or 0 if he or she was assigned to the neutral site; define
> $v = 1$ if the student actually accessed the site (which can be checked using
> unique identifiers) or 0 if he or she never clicked on the link.
>
> (a) From which of the following regressions or pair of regressions can we
>     compute the instrumental variables estimate of the effect of accessing the
>     site on voting?
>
>    * Regression of $y$ on $u$.
>    * Regression of $y$ on $v$.
>    * Regression of $y$ on $u$ and $v$.
>    * Regression of $y$ on $u$, and the regression of $v$ on $u$.
>    * Regression of $y$ on $v$, and the regression of $v$ on $u$.
>
> (b) What assumptions are required for the instrumental variables estimate to
>     be reasonable in this case?  Do these assumptions seem plausible here?

TODO

### TK 21.2, Instrumental variables, simulating a population

> The goal of this exercise is to simulate data consistent with the assumptions
> of the instrumental variables procedure described in Section 21.1.  You will
> also evaluate the properties of different approaches to estimating the
> complier average causal effect (CACE).
>
> To help conceptualize the type of data that might be consistent with the
> instrumental variable assumptions, consider a hypothetical randomized
> encouragement design.  In particular, imagine a study in which 1000 students
> entering any undergraduate degree program in the sciences in a major
> university are randomly assigned to one of two conditions.  One group is
> encouraged via an email from the chair of their department to participate in a
> one-week math boot camp just before the start of their first semester.
> Students in the other group are also allowed to participate but receive no
> special encouragement.  These students would have had to discover on their own
> the existence of the program on the university website.  The running variable
> is test score on the final exam for a required math course, and the outcome
> variable $y$ that you will simulate below represents the difference between
> that score and the threshold for passing.  Thus a negative value for a student
> reflects the fact that the student would not be eligible for that course.
>
> Generate data for a sample of 1000 individuals consistent with the IV
> assumptions discussed in this chapter. Follow the guidelines below.
>
> (a) Simulate compliance status.  Assume that 25% of individuals are compliers,
>     60% are never-takers, and 15% are always-takers. Generate $d^0$ and $d^1$
>     vectors to reflect this. You can also generate a vector indicating
>     compliance type, $c$, if that is helpful.
>
> (b) Which compliance group has been omitted from consideration?  What
>     assumption does that imply?
>
> (c) Simulate the potential outcomes in a way that meets the following
>     criteria:
>
>    * The exclusion restriction is satisfied.
>    * The average effect of $z$ on $y$ for the compliers is 4.
>    * The average $y(z = 0)$ for never-takers is 0; the average $y(z = 0)$
>        for compliers is 3; the average $y(z = 0)$ for always-takers is 6.
>    * The residual standard deviation is 1 for everyone in the sample
>        (generated independently for each potential outcome).
>
> (d) Calculate the sample average treatment effect (SATE; average effect of $z$
>     on y for the people in the experiment) for each of the compliance groups.
>
> (e) What is another name for the SATE for the compliers?
>
> (f) Calculate the intent-to-treat (ITT) effect using your simulated data.
>
> (g) Put $T^0, T^1, y^0, y^1$ into one dataset called `dat_full`. You can also
>     include a variable, $c$, indicating compliance group if you created one.

TODO

### TK 21.3, Instrumental variables, playing the role of the experimenter

> Now switch to the role of the researcher.  Pretend that you ran the experiment
> described in the previous exercise. Generate a binary indicator $z$ for to
> indicate who was to be encouraged to participate in the program. The
> probability of encouragement should be 0.5.

TODO

### TK 21.4, Instrumental variables, understanding which potential outcome manifests as an observed outcome

> Use `dat_full` from the previous exercise to create a dataset that the
> researcher would actually get to see given the $z$ you just generated.  This
> observed dataset should only have $T$, $z$, and $y$ in it.  Call it `dat_obs`.

TODO

### TK 21.5, Instrumental variables, inference

> Given the simulated `dat_obs`:
>
> (a) Estimate the percentage of compliers, never-takers, and always-takers,
>     assuming that there are no defiers.
>
> (b) Perform the naive regression estimate of the effect of the treatment on
>     the outcome.  What is another name for this type of analysis?
>
> (c) Estimate the intent-to-treat on the treated (ITT) effect.
>
> (d) Estimate the complier average causal effect (CACE) by dividing the ITT
>     estimate by the estimated percentage of compliers in the sample.
>
> (e) Estimate the CACE by fitting two-stage regression as in Section 21.1.
>
> (f) Estimate the CACE and its standard error using brms.

TODO

### TK 21.6, Instrumental variables, assumptions

> Continuing Exercises 21.2–21.5:
>
> (a) Describe the assumptions required for the instrumental variables procedure
>     to give a good estimate of the treatment effect.  We have generated data
>     that satisfy these assumptions.  Suppose instead you were handed data from
>     the study described above.  Comment on the plausibility of each of the
>     required assumptions in that setting.
>
> (b) Suppose that the data-generating process above included a covariate that
>     predicted both $z$ and $y$. Which of the assumptions described in (a)
>     would that change and how?
>
> (c) Suppose that the above directions were amended as follows: "The average of
>     $y^0$ for never-takers is 0; the average of $y^0$ for compliers is 3; the
>     average of $y^0$ for always-takers is 6; the average of $y^1$ for
>     never-takers is 2."  Which of the assumptions of instrumental variables
>     would that violate?
>
> (d) How would you alter the simulation to violate the monotonicity assumption?
>
> (e) How might one alter the administration of this program to preclude the
>     existence of always-takers? Does this raise ethical questions?

TODO

### TK 21.7, Instrumental variables, evaluating statistical properties when the assumptions hold

> Simulate a sampling distribution for any of the estimators used in Exercise
> 21.5.  Which of these estimators is unbiased?  For each, also report the
> standard deviation of the sampling distribution and compare to the standard
> error computed in Exercise 21.5.

TODO

### TK 21.8, Instrumental variables, evaluating statistical properties when the assumptions are violated

> Simulate a sampling distribution for any of the estimators used in Exercise
> 21.5 in one of the worlds implied in Exercise 21.6.  What happens to the
> properties of these estimators when the required assumptions do not hold?

TODO

### TK 21.9, Regression discontinuity

> Take the Chile schools example from Section 21.3 and perform a series of
> analyses using different subsetting ranges.  Plot the estimate $\pm$ standard
> error as a function of the subsetting range.  As the width of the range
> increases, the standard error should go down, but there should be more of a
> concern about the use of the estimate for causal inference, given the lack of
> overlap.

TODO

### TK 21.10, Regression discontinuity

> Suppose you are trying to evaluate the effect of a new procedure for coronary
> bypass surgery that is supposed to help with the postoperative healing
> process.  The new procedure is risky, however, and is rarely performed in
> patients who are over 80 years old.
>
> Data for this (hypothetical) example are displayed in Figure 21.4.
>
> (a) Does this seem like an appropriate setting in which to implement a
>     regression discontinuity analysis?
>
> (b) The folder `Bypass` contains data for this example: `stay` is the length
>     of hospital stay after surgery, `age` is the age of the patient, and `new`
>     is the indicator for whether the new surgical procedure was used.
>     Preoperative disease severity (`severity`) was unobserved by the
>     researchers, but we have access to it for illustrative purposes.  Can you
>     find any evidence using these data that the regression discontinuity
>     design is inappropriate?
>
> (c) Estimate the treatment effect using a regression discontinuity estimate
>     (ignoring) severity.  Estimate the treatment effect in any way you like,
>     taking advantage of the information in severity.  Explain the discrepancy
>     between these estimates.

TODO

### TK 21.11, Regression discontinuity, setting up an artificial world

> This assignment simulates hypothetical data collected on women who gave birth
> at any one of several hospitals in disadvantaged neighborhoods in New York
> City in 2010.  We are envisioning a government policy that makes health care
> available for pregnant women, new mothers, and their children though 2 years
> post-birth.  This program is only available for women in households with
> income below $20,000 at the time they gave birth.  The general question of
> interest is whether this program increases a measure of child health at age 3.
> You will generate data for a sample of 1000 individuals.
>
> For this assignment we make the unrealistic assumption that everyone who is
> eligible for the program participates and no one participates who is not
> eligible.  This is an example of a "clean" or "sharp" regression discontinuity
> design.
>
> (a) Simulate the "assignment variable" (sometimes referred to as the running
>     variable, forcing variable, or rating), income, in units of thousands of
>     dollars.  Call the variable `income`.  Try to create a distribution that
>     mimics the key features of the data displayed in Figure 21.5.
>
> (b) Create an indicator for program eligibility for this sample. Call this
>     variable `eligible`.
>
> (c) Simulate outcomes for World A.  Generate the potential outcomes for health
>     assuming linear models for both $\mathbb{E}(y^0|x)$ and
>     $\mathbb{E}(y^1|x)$.  This health measure should have a minimum possible
>     score of 0 and maximum possible score of 30.  The expected treatment
>    effect for everyone should be 4; in other words, $\mathbb{E}(y^1-y^0|x)$
>    should be 4 at all levels of $x$.  The residual standard deviation of each
>    potential outcome should be 1.
>
>    Save two datasets: (1) `fullA` should have the assignment variable and both
>    potential outcomes and (2) `obsA` should have the assignment variable, the
>    eligibility variable, and the observed outcome.
>
> (d) Simulate outcomes for World B. Generate the potential outcomes for health
>     assuming a linear model for $\mathbb{E}(y^0|x)$ and a quadratic model for
>     $\mathbb{E}(y^1 |x)$.  The treatment effect at the threshold (the level of
>     $x$ that determines eligibility) should be 4.  The residual standard
>    deviation of each potential outcome should be 1.  Creating this
>    data-generating process may be facilitated by using a transformed version
>    of your income variable that subtracts out the threshold value.
>
>    Save two datasets: (1) `fullB` should have the assignment variable and both
>    potential outcomes and (2) `obsB` should have the assignment variable, the
>    eligibility variable, and the observed outcome.

TODO

### TK 21.12, Regression discontinuity analysis

> Now you will act as a researcher and analyze the data created in the previous
> exercise.
>
> (a) Plot your data!  Make two scatterplots of observed health vs. income, one
>     corresponding to each world.  In each, plot eligible participants in red
>     and non-eligible participants in blue.
>
> (b) Estimate the treatment effect for World A and World B using all the data.
>     Now we will estimate effects in a number of different ways.  Each model
>     should include reported income and eligible as predictors.  In each case
>     use the model fit to report the estimate of the effect of the program at
>     the threshold level of income.
>
>    i. Fit a linear model to the full dataset. Do not include an interaction.
>
>    ii. Fit a linear model to the full dataset, including an interaction
>       between income and eligible.
>
>    iii. Fit a model that is quadratic in income and includes an interaction
>       between both income terms and eligible; that is, allow the shape of the
>       relationship to vary between treatment and control groups.
>
> (c) Fit the same models using the data from World B.
>
> (d) Fit the same models using the data from World A but restricting the sample
>     to those with incomes between $16,000 and $24,000.
>
> (e) Fit the same models using the data from World B but restricting the sample
>     to those with incomes between $16,000 and $24,000.
>
> (f) Comment on the differences in the estimates from the previous four parts
>     of this exercise.
>
> (g) Provide a causal interpretation of your favorite estimate above.

TODO

### TK 21.13, Regression discontinuity assumptions

> What are the three most important assumptions for the causal estimates in the
> previous exercise?

TODO

### TK 21.14, Thinking harder about regression discontinuity

> Consider the scenario of Exercise 21.11.
>
> (a) A colleague now points out that some women may have incentives in these
>     settings to misreport their actual income.  Plot a histogram of reported
>     income and look for anything that might support such a claim.  What
>     assumption is called into question if women are truly misreporting in this
>     manner?
>
> (b) Another colleague points out that several other government programs such
>     as food supplements and Head Start have the same income threshold for
>     eligibility. How might this knowledge impact your interpretation of your
>     results?

TODO

### TK 21.15, Intermediate outcomes

> In Exercise 19.10, you estimated the effect of incumbency on votes for
> Congress.  Now consider an additional variable: money raised by the
> congressional candidates.  Assume this variable has been coded in some
> reasonable way to be positive in districts where the Democrat has raised more
> money and negative in districts where the Republican has raised more.
>
> (a) Explain why it is inappropriate to include money as an additional input
>     variable to "improve" the estimate of incumbency advantage in the
>     regression in Exercise 19.10.
>
> (b) Suppose you are interested in estimating the effect of money on the
>     election outcome.  Set this up as a causal inference problem (that is,
>     define the treatments and potential outcomes).
>
> (c) Explain why it is inappropriate to simply estimate the effect of money
>     using instrumental variables, with incumbency as the instrument.  Which of
>     the instrumental variables assumptions would be reasonable in this example
>     and which would be implausible?
>
> (d) How could you estimate the effect of money on congressional election
>     outcomes?
>
> See Campbell (2002) and Gerber (2004) for more on this topic.

TODO

### TK 21.16, Difference-in-differences estimation

> Consider the Electric Company example from Chapter 19, estimating a separate
> treatment effect in each grade. What is the difference-in-differences estimate
> here?  Explain why the regression estimate used in that chapter is a better
> choice.

TODO