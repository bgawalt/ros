# Chapter 20: Observational studies with all confounders assumed to be measured

[(Return to README)](./README.md)

Chapter 18 already went over how randomization can be less than complete.  This
chapter takes that one step further: randomization can be so watered down that
it basically vanishes.  It "discusses methods for causal inference in the
presence of systematic pre-treatment differences between treatment and control
groups. A key difficulty is that there can be many pre-treatment variables with
mismatch, hence the need for adjustment on many variables."  The implication
here is that *if*, per the chapter title, all counfounders are assumed to be
measured, we can draw *some* kind of causal inference from a treatment (even if
that treatment is selected into/away from by subjects).


## Subsection rundown

### 20.1, The challenge of causal inference

The chapter opens with two examples of observational studies where the
regression coefficients *don't* lend themselves to causal inference.

1.  **Hypothetical example of zero causal effect but positive predictive
    comparison:**  if the treatment does nothing, but healthy patients sort into
    the treatment group (and sicker ones the control group), you get a positive
    coefficient if you fit a univariate model predicting patient health outcomes
    from patient treatment group assignment.

2.  **Hypothetical example of positive causal effect but zero positive
    predictive comparison:** if instead *sicker* patients sort preferentialy
    into the treatment group, then even a genuinely-helpful treatment can wind
    up looking inert (or bad).  "It is then possible to see equal average
    outcomes of patients in the two groups, with sick patients who received the
    treatment canceling out healthy patients who received the control."

The systematic nature of the sorting in these scenarios is important.  It's not
just bad luck that your two treatment groups are unbalanced w.r.t. patient
pre-treatment health status.  The sicker patients are systematically driven to
one group or the other, and resampling or increasing sample size won't fix the
imbalance that's inducing the coefficient-vs.-actual-effect mismatch.

The chapter introduces the term *confounding covariate* to describe the
pre-treatment predictor that drives the selection bias.  Omitting these
confounders from the model, leaving them as lurking variables, wrecks the
causal effect estimate (i.e., treatment indicator coefficient estimate).

The section closes out with algebra around omitted variable bias, where there's
a mechanism linking outcome $y$ to confounder $x$ and treatment indicator $z$,
as well as linking $x$ to $z$.  Both links are linear and additive, so the
book doesn't really dwell on the implications of the algebra: we know that's not
a realistic description of how the real-world values of $x$, $y$, and $z$
interrelate, so trying to draw out strong intuition for what "omitted variable
bias" looks like from this peculiar case is not really a good use of time.

### 20.2, Using regression to estimate a causal effect from observational data

In observational studies, the research design is nonexperimental, and you don't
directly manipulate any of the covariates used to predict the outcome.  "\[I\]f
we observe differences in average outcomes across these groups, we can't
separately attribute these differences to the treatment or the confounders --
the effect of the treatment is thus 'confounded' by these variables."

If you couldn't/didn't observe *all* the relevant confounders, none of the
techniques in this chapter will be fairly useless.

The motivating example in the section is to expand the Electric Company
education study from Chapter 19, now with more detail included.  Classrooms were
randomly given (or not-given) the Electric Company educational program to show
in-class.  But teachers who received the material could use it to either replace
or supplement their normal lesson plans.  That decision is nonrandom, and so
turns the study of "control vs. replace vs. supplement" into an observational
one.

The study includes pre-treatment test scores as a covariate.  If that were the
*only* basis on which teachers decided between "replace" and "supplement,"
then the decision satisfies "a form of the ignorability assumption discussed in
[Section 18.6](chapter18.md#186-properties-assumptions-and-limitations-of-randomized-experiments).
That's likely untrue, but, "the ignorability assumption can be a useful
starting point, especially in a setting such as this where pre-test score is
such a strong predictor of post-test score."

If we agree the ignorability assumption is satisfied (or just close enough to
being satisfied), there's still all the other assumptions from
[Section 11.1](chapter11.md#111-assumptions-of-regression-analysis) to worry 
about.  Later, this chapter introduces balance and overlap, a.k.a. *common
support*, that needs addressing before you can declare a regression coefficient
estimate a useful causal effect estimate.

### 20.3, Assumption of ignorable treatment assignment in an observational study

They compare the studies in this chapter with the block-randomized studies
in Chapter 18.  The difference is that in Ch. 18, the blocking attribute was,
"by design," the only covariate relevant to treatment assignment.  So it was
easy to be sure your model had all confounders included: there's only the one,
and it's what you used to block subjects into groups.  Now, we don't know for
sure whether we have the complete set of "blocking" confounders that drive
treatment assignment.

Actually incorporating confounders -- when there's lots of them; when they're
continuous -- lets you make use of the ignorability assumption, 

$$y^0, y^1 \perp z, x$$

but you have to build a parameteric model linking the three variables in all but
the simplest cases of $x$ and $z$.  (The chapter walks through a nonparametric
model for the simple case where $x$ is a single confounder that's a binary
indicator.)

### 20.4, Imbalance and lack of complete overlap

Ignorability is unsatisfied if treatment and control are not comparable.  If
that lack of comparability happens along an unobserved data axis, then nothing
in this chapter works.  But to repeat for like a fourth time: let's assume that
you *do* observe all attributes that serve as confounders to the treatment
indicator.  If you make that assumption, you can warp your observed data to make
treatment and control comparable again, and causal inference is revived.

Equation 20.3 describes what happens when you take sample averages of the
treatment and control group when the outcome also depends, quadratically, on a
confounder:

$$\theta = \bar{y}_1 - \bar{y}_0 - \beta_1\left(\bar{x}_1 - \bar{x}_0\right) - \beta_2\left(\bar{x^2_1} - \bar{x^2_0}\right)$$

To estimate $\theta$ correctly from a regression of $y$ on $(x, z)$, you need to
know to include both $x$ and $x^2$ as covariates in the model.  This is what
they mean by "\[i\]mbalance and lack of complete overlap are issues for causal
inference even if ignorability holds because they force us to rely more heavily
on model specification and less on direct support from the data."

They use the term *overlap* (a.k.a. *common support*) to talk about how
confounder value distributions compare across the treatment-control divide.
Visually:

![Caption of Figure 20.5 from page 392 of ROS: Lack of complete overlap in
distributions across treatment and control groups. Dashed lines indicate
distributions for the control group; solid lines indicate distributions for the
treatment group. (a) Two distributions with no overlap; (b) two distributions
with partial overlap; (c) a scenario in which the range of one distribution is a
subset of the range of the other.](./fig/part5/fig20_5_overlap.png)

When there's lack of complete overlap, "the data are inherently limited in what
they can tell us about treatment effects in the regions of nonoverlap."  Who
knows if there's just a magic interaction happening exactly in that spot of
covariate space where we see $x$'s for the treatment units but not the control.
Talking about those kinds of units means talking about your model (and modeling
assumptions) and not about anything gleaned from the study data itself.

Put another way, your model will let you extrapolate beyond the support of the
data (either for treatment units, control units, or both).  But by definition,
you can't check the fit outside the data support.  You're just hoping your model
is good enough, instead of doing any quality control.

### 20.5, Example: evaluating a child care program

The example compares a treated group of 290 premature, low-birth-weight babies
against a control group of 4,091 other babies.  A good dozen confounding
covariates are noted, and Fig 20.9 displays how greatly they vary between
groups:

![Figure 20.9 from ROS: "Imbalance in averages of confounding covariates across
treatment groups. Open circles represent absolute differences in means for the
unmatched groups standardized by the standard deviation in the treatment group.
Solid circles represent absolute differences in means for groups matched without
replacement standardized by the standard deviation in the treatment group.
Matching methods are described later in the chapter.
](./fig/part5/fig20_9_birth_covariates.png)

It makes sense that birth weight is the largest difference; it's literally the
treatment selection criteria.

They discuss how all the confounders have imbalance, but only some have lack of
complete overlap.  Birth weight, in particular, is capped in the treatment group
at 2500 grams, and so any treatment interaction trend beyond that is just
extrapolating from the fit model.

In general, they come just short of recommending dropping units from the control
group who fall outside treatment group support on 

(The outcome for this example is a cognitive ability test score, which is pretty
much an afterthought.  This chapter is all about the predictors, not the
outcomes.)

### 20.6, Subclassification and average treatment effects

TK

### 20.7, Propensity score matching for the child care example

TK

### 20.8, Restructuring to create balanced treatment and control groups

TK

### 20.9, Additional considerations with observational studies

TK


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer