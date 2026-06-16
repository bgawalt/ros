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

TK

### 20.3, Assumption of ignorable treatment assignment in an observational study

TK

### 20.4, Imbalance and lack of complete overlap

TK

### 20.5, Example: evaluating a child care program

TK

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