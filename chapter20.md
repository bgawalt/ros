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
subset of the range of the other.](./fig/part5/fig20_05_overlap.png)

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
](./fig/part5/fig20_09_birth_covariates.png)

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

The chapter has stressed a few times how weird it feels to rely on extrapolation
from a fit model when faced with imbalance between treatment and control.  So
this section asks, what can be done nonparametrically.  They break the above
example out into mother's-education indicator blocks and look at between group
differences in average outcomes within each block.  They concede this is bad; it
makes the ignorability assumption even though it's clear important covariates
are omitted from consideration.  Also, they could only conduct this because they
had discrete buckets of units to compare, and bucketizing a continuous covariate
in a similar way throws out information.

Once they have estimates for the effect in each bucket, they derive an average
treatment effect (a weighted average, where the weights are total baby count
across both treatment groups).

Circling back to "should we throw out control group data to address incomplete
overlap with the training group," they introduce the term *average effect of the
treatment on the treated (ATT)*.  Only certain babies are eligible for the
treatment, so the comparison should be between treated babies and control group
babies that meet the criteria.

They repeat the earlier subcategory bucketing, and find ATT by taking the same
weighted average, but with weights that are only baby counts from the treatment
buckets.  (ATC does the same thing, but with baby counts in the control
buckets.)

They close with:

> We can think of the estimate of the effect of the treatment on the treated as
> a poststratified version of the estimate of the average causal effect. As the
> methods we discuss in this section rely on more and more covariates, it can be
> more attractive to apply methods that estimate the effect of the treatment on
> the treated while avoiding explicit stratification on all potential treatment
> effect modifiers, as we discuss next.

If you make your buckets the crossproduct of a bunch of different attributes,
your unit counts will wind up too low to say anything useful.

### 20.7, Propensity score matching for the child care example

Matching: if there's systematic difference between treatment and control, then
try and restore balance by matching each treatment unit with a most-similar
control unit.  *Propensity score matching* is the version they walk through
here.  It's a five step process.

#### Step 1: Defining the confounders and estimand

1.  What covariates are required to satisfy ignorability?  Maybe you have to
    rely on conventional choices of what to include, based on prior work in your 
    field.  Or maybe there's few enough on record that you can just use them
    all.

2.  Are you estimating ATT?  ATC?  Average treatment effect on some third
    population beyond treatment and control?  Call whatever group you're going
    to try and balance towards the *inferential group.*

At this point, I am a little wrongfooted by the introduction of ATT and ATC.
It seems like they're just saying "an interaction between $z$ and $x$" without
actually acknowledging that that's what they're recommending.

#### Step 2: Estimating the propensity score

Fit a binary classifier that turns the covariates above into a probability of
being in the treatment group:

$$\text{Pr}(z = 1) = \text{logit}^{-1}(\beta \cdot x)$$

They promise checking the success of this model fit effort will come later.

The predictions you get out of this classifier are the propensity scores, i.e.,
the propensity for a unit to have wound up in the inferential group, as a
function of the confounder covariates.

#### Step 3: Matching to restructure data

Once you have the model, score every unit in treat and control.  Then (when your
estimand in Step 1 is ATT, and so you inferential group is "treatment") just
pair every treat unit with the control unit that has the closest propensity
score.

This matching can be done with or without replacement.  Matching *with*
replacement is recommended, while noting that it increases variance of
estimates.  (You might oversample the same control unit a lot, and your estimate
now is overly reliant on the weird aspects of that one oversampled control
unit.)

#### Step 4: Diagnostics for balance and overlap

Like in Fig 20.9, once you have your matched dataset, you can look at
differences in mean values between treat and control for each confounder
(standardized for continuous confounders, left as means for binary confounders).

You can also plot histograms of the propensity scores for treat and control,
pre- and post-matching routine:

![sdf](./fig/part5/fig20_14_propensity.png)

You can use the support range of propensity scores to throw away more data:
only include treat units that fall in the propensity range of the control units.

You should loop here: if the balance diagnostics are bad, go back and upgrade
the classifier of Step 2.

#### Step 5: Estimating a treatment effect using the restructured data

Run a regression.

The coefficient for the treatment variable is going to be off somewhat: "the
propensity score has been estimated from the data is not reflected in our
calculations. This issue has no perfect solution to date and is currently under
investigation by researchers in this field."  The standard errors are going to
be too narrow because you're working off the same data twice.

### 20.8, Restructuring to create balanced treatment and control groups

Some things to consider in general, beyond the specifics of matching to restore
balance between treatment and control:

#### Step 1: Estimands and confounders

*  **Defining the population of interest:** Make sure your estimand target
    matches the research goals.  Unless you genuinely don't have a way to match
    treat units with comparable control units -- then maybe fall back to a less
    specific estimand than ATT.

*  **Choosing covariates:** Maybe you have too few covariates to assume
    ignorability; that's bad and you should flag it.  Or you have too *many*
    covariates.  We saw how to include them all and regularize the model fit,
    but you can also just pre-prune the covariate list for simplicity.
    Definitely drop any post-treatment predictors.  You should also hold off on
    covariates that strongly correlate to $z$ but not $y$ (and seek out the
    ones that *do* strongly predict $y$).

#### Step 2: Calculating distance metrics: finding observations with different treatments that are similar in their pre-treatment characteristics

The propensity score is *a* distance metric, but you can try other ones, too.
Mahalanobis distance is encouraged, though it "defines proximity based on what
are arguably specialized neighborhoods of the covariate space."

They talk about some ironies of the propensity score classifier.  If it does a
perfect job -- gives every treat unit a score of 1 and every control a score of
0 -- it's totally useless as a matching function.  And in situations where
randomization has worked perfectly, then you can't fit a classifier at all.
Plus you get dumb matches from the linearity and additivity: two matched units
can be very different in their covariates while still having identical
propensity scores, because the wild swings cancel out overall.

This all reinforces my longstanding sense that unsupervised learning ("what
counts as two units being close across this $N$ dimensional manifold") is hard
to evaluate and no one knows how to do it.

#### Step 3: Restructuring the data

*  **Matching algorithms:** So many choices, beyond just with-or-without
    replacement.  You can do many-to-one matching, where some treat units get
    many control units matched to it, based on some distance threshold.  You
    can do a Gale-Shapley style optimal matching.  You can do greedy algorithms
    in various different orderings of which treat gets matched first.

*  **Matching as weighting scheme:** The restructuring used above is like 0-1
    weighting: control units are either selected as a treat match, or aren't.
    But you can pick different weight assignment schemes.  (They tend to
    correspond to some matching algorithm or other; the book goes into how
    caliper matching would work for controls that fall within the distance
    thresholds of multiple treats.)

*  **Inverse probability weighting:** Instead of using the propensity score for
    hard matching, warp them into per-unit weights.  Different warps apply to
    different estimands.
    *  **ATE**: Treats get a weight of $1/\hat{p}$; controls get a weight of
        $1/(1 - \hat{p})$.
    *  **ATT**: Treats get a weight of 1; controls get a weight of
        $\hat{p} / (1 - \hat{p})$.
    *  **ATC**: Treats get a weight of $(1 - \hat{p}) / \hat{p}$; controls get a
        weight of 1.

When weighting, be careful you don't assign degenerately large weights to some
few units that wind up defining the whole model fit.

#### Step 4: Diagnostics: Balance and overlap

It's not useful to look at histograms of propensity scores for treat and control
and see if they are similar.  A model that's pure randomness can generate good
histogram similarity and be useless for propensity score matching.

Use standard techniques (e.g., LOO-CV) to test the propensity score model's fit.

Go back and fix the propensity score model as needed, but don't tweak it just so
that your treatment effect estimate is made stronger/more publishable.

#### Step 5: Estimating the treatment effect using restructured data

Right, run the regression now.  Don't worry about the pairing off; the point is
not to have matched pairs that are meaningfully linked, but to have two groups
that in aggregate are comparable.

### 20.9, Additional considerations with observational studies

If you have an observational study, the first step to drawing causal inferences
from it is to imagine its controlled-experiment counterpart:

*  **Define the treatment/exposure variable:**  Which predictor is the one that
    you'd manipulate in an actual randomized experiment, if you could?

*  **Define the control counterfactual state:** When a unit is
    untreated/unexposed, what does it do instead?

*  **Temporal ordering:** Make sure your outcome comes after the treatment, and
    that you don't adjust for post-treatment predictors.  And also: make sure
    that if all data is collected at some time instant, but many of the
    attributes are about values at some past instant -- are you sure that's
    being measured right?  You want the subject's education level *before* the
    treatment, not the level at time of measurement.  I love their call out of
    how humans are smart and will change up their behavior in anticipation of
    a treatment/exposure that hasn't happened yet; attributes that are
    technically pre-treatment are in fact caused by the coming treatment.

Imagining a randomized experiment that corresponds to your observational data
can help clarify which attributes should be included as predictors, included as
outcomes, or purposefully ignored.


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)


### TK 20.2, Constructed Example: observational studies

> The folder Lalonde contains data from an observational LaLonde study
> constructed by LaLonde (1986) based on a randomized experiment that evaluated
> the effect on earnings of a job training program called National Supported
> Work.  The constructed observational study was formed by replacing the
> randomized control group with a comparison group formed using data from two
> national public-use surveys: the Current Population Survey (CPS) and the Panel
> Study of Income Dynamics.
>
> Dehejia and Wahba (1999) used a subsample of these data to evaluate the
> potential efficacy of propensity score matching.  The subsample they chose
> removes men for whom only one pre-treatment measure of earnings is observed.
> There is evidence in the economics literature that adjusting for earnings from
> only one pre-treatment period is insufficient to give a good approximation to
> ignorability.  This exercise replicates some of Dehejia and Wahba’s findings
> based on the CPS comparison group.
>
> (a) Estimate the treatment effect from the experimental data in two ways:
>     (i) a simple difference in means between treated and control units, and
>     (ii) a regression-adjusted estimate (that is, a regression of outcomes on
>     the treatment indicator as well as predictors corresponding to the
>     pre-treatment characteristics measured in the study).
>
> (b) Now use a regression analysis to estimate the causal effect from Dehejia
>     and Wahba’s subset of the constructed observational study.  Examine the
>     sensitivity of the model to model specification, for instance, by
>     excluding the employed indicator variables or by including interactions.
>     How close are these estimates to the experimental benchmark?
>
> (c) Now estimate the causal effect from the Dehejia and Wahba subset using
>     propensity score matching. Do this by first trying several different
>     specifications for the propensity score model and choosing the one that
>     you judge to yield the best balance on the most important covariates.
>     Perform this propensity score modeling without looking at the estimated
>     treatment effect that would arise from each of the resulting matching
>     procedures.  For the matched dataset you construct using your preferred
>     model, report the estimated treatment effects using the
>     difference-in-means and regression-adjusted methods described in part (a)
>     of this exercise. How close are these estimates to the experimental
>     benchmark (about $1800)?
>
> (d) Assuming that the estimates from (b) and (c) can be interpreted causally,
>     what causal effect does each estimate? What populations are we making
>     inferences about for each of these estimates?
>
> (e) Redo both the regression and the matching exercises, excluding the
>     variable for earnings in 1974, which is two time periods before the start
>     of this study. How important does the earnings-in-1974 variable appear to
>     be in terms of satisfying the ignorability assumption?

TODO

### TK 20.3, Understanding the difference between average treatment effect in the treated and control groups

> Create a hypothetical dataset in which the average treatment effect on the
> treated and controls (ATT and ATC) are clearly different.  What are the
> distinguishing characteristics of this dataset?

TODO

### TK 20.4, Exploring the properties of observational data under a linear model

> The goal of this exercise is to learn how to simulate a few different types of
> observational causal structures and evaluate the properties of different
> approaches to estimating the treatment effect through linear regression.
>
> (a) Simulate data from 1000 people.  First we want to simulate the underlying
>     data from the joint distribution of a continuous pre-treatment predictor
>     or covariate $x$, a binary treatment variable $z$, and continuous
>     potential outcomes $y^0, y^1$. The data-generating process is
>     $p(x, z, y_0, y_1) = p(x)p(z|x)p(y^0, y^1|z, x)$.
>
>    i. Start by simulating the values of $x$ from a normal distribution with
>         mean 0 and standard deviation 1.
>
>    ii. What role does x play in the data-generating process?
>
>    iii. The next step is to simulate $z$ from $p(z|x) = \text{binomial}(p)$,
>         where the vector of probabilities can vary across observations. Come
>         up with a strategy for generating the vector $z$ conditional on $x$
>         that forces you to create be explicit about how these probabilities
>         are conditional on $x$.  An inverse logit function is one approach but
>         there are others.  Make sure that $x$ is strongly associated with $z$
>         and that the vector of probabilities used to draw $z$ does not go
>         below 0.05 or above 0.95 for the values of $x$ in the data.
>
>    iv. The last step is to simulate $y^0, y^1$ given $x$ and $z$.  Construct a
>         model for simulating the two potential outcomes with appropriate
>         conditioning on $z$ and $x$ with the following stipulations:
>
>    *  Make sure that $\mathbb{E}(y^1|x) - E(y^0 | x) = 5$.
>    *  Make sure that $x$ has a linear and strong relationship with the
>          outcome.
>    * Finally, set your error term to have a standard deviation of 1 and allow
>         the residual standard deviation to be different for the same person
>         across potential outcomes.
>
>    v. Create a data frame containing your simulated $x, z, y^0, y^1$, and save
>         it for use later.
>
>    vi. Calculate the sample average treatment effect and save it for use
>         later.
>
>    vii. Create a data frame with the observed data, $x, z, y$.
>
> (b) Play the role of the applied researcher.  Pretend someone handed you the
>     observed data generated above and asked you to estimate the treatment
>     effect.  You will try two approaches: difference in means and regression.
>
>    i. Estimate the treatment effect using a difference in mean outcomes across
>         treatment groups.
>
>    ii. Estimate the treatment effect using a regression of the outcome on the
>         treatment indicator and covariate.
>
>    iii. Create a scatterplot of observed $y$ vs. $x$ using red dots for
>         treatment and blue for control observations.  If you were the
>         researcher, would you be comfortable using linear regression with no
>         interaction in this setting?
>
> (c) Play the role of the statistician studying the properties of estimates.
>
>    i. Create a scatterplot of both potential outcomes vs. $x$, using red dots
>         for values of $y^1$ and blue dots for $y^0$. Does linear regression
>         with no interaction seem like a reasonable model to estimate causal
>         effects for the observed data? Why or why not?
>
>    ii. Find the bias of each of the estimates calculated by the researcher in
>         (b) relative to the sample average treatment effect computed using all
>         the potential outcomes.
>
>    iii. Think harder about the practical importance of the bias by dividing
>         this estimate by the standard deviation of the observed outcome $y$.
>
>    iv. Find the bias of each of the estimates by creating a randomization
>         distribution for each.  When creating randomization distributions,
>         remember to be careful to keep the original sample the same, only
>         varying treatment assignment and the observed outcome.

TODO

### TK 20.5, Simulating observational data under a nonlinear model

> Now we’ll explore what happens when we fit a wrong model in an observational
> study in a simple problem with a single pre-treatment predictor.
>
> (a) Simulate the data. Create an R function called `sim_nlin()` that does the
>     following:
>
>    i. The predictor $x$ should be drawn from a uniform distribution between 0
>         and 2.
>
>    ii. Treatment assignment should be drawn from the following binomial where
>         $\mathbb{E}(z|x) = p = \text{logit}^{-1}(-2 + x^2)$. Save the $p$
>         vector for use later.
>
>    iii. The response surface (model for $y^0, y^1$) should be drawn from the
>         following distributions:
>         $y^0 = x + \epsilon_0, y1 = 2x + 3x^2 + \epsilon_1$, where the error
>         terms are independent and normally distributed, each with mean 0 and
>         standard deviation 1.
>
>    iv. Make sure the returned dataset has a column for the probability of
>         treatment assignment as well.
>
>    v. Simulate a dataset called `data_nlin` with sample size 1000.
>
> (b) Make the following plots:
>
>    i. Overlaid histograms of the probability of assignment.
>
>    ii. A scatterplot of observed $y$ vs. $x$ using red dots for treatment and
>         blue for control observations.
>
>    iii. A scatterplot of both potential outcomes vs. $x$, using red dots for
>         values of $y^1$ and blue dots for $y^0$.  Does linear regression with
>         no interactions seem like a reasonable model to estimate causal
>         effects for the observed data?  Why or why not?
>
> (c) Create randomization distributions to investigate the properties of each
>     of three estimates with respect to the sample average treatment effect:
>     (1) difference in means, (2) linear regression of the outcome on the
>     treatment indicator and $x$, (3) linear regression of the outcome on the
>     treatment indicator, $x$, and $x^2$.
>
> (d) Calculate the standardized bias (bias divided by the standard deviation of
>     $y$) of these estimates relative to the sample average treatment effect.

TODO

### TK 20.6, Observational data with multiple covariates

> (a) Simulate from
>     $p(x_1, x_2, x_3, z, y^0, y^1) = p(x_1, x_2, x_3)p(z|x_1, x2, x3)p(y^0, y^1|z, x_1, x_2, x_3)$.
>
>    i. Simulate the predictors x1; x2; x3 to be independent of each other.
>
>    ii. Make sure that the probability of being treated is between 0.05 and
>         0.95 for each person and that there is a reasonable amount of overlap
>         across the treatment and control groups.
>
>    iii. Generate the response surface as in the following:
>
>    $$y^0 = x1 + x2 + x3 + \epsilon_0$$
>    $$y1 = x1 + x2 + x3 + 5 + \epsilon_1$$
>
>   with independent errors normally distributed with mean 0 and standard
>   deviation 1.
>
> (b) Create randomization distributions for (1) a regression that adjusts for
>     only one of the three covariates and (2) a regression estimate that
>     adjusts for all three covariates. Evaluate the standardized bias of these
>     estimates relative to the sample average treatment effect (SATE).
>
> (c) Repeat the above but $x_1$, $x_2$, and $x_3$ generated with a dependence
>     structure.
>
> (d) Repeat the above but with a nonlinear response surface.

TODO

### TK 20.7, Propensity score matching

> Perform your own propensity score analysis using the IHDP childcare data in
> the folder Childcare discussed in Section 20.5. Follow all of the steps and
> report back in your findings.

TODO

### TK 20.8, Weighted estimate of treatment effect

> Perform an inverse estimated probability of treatment weighting (IPTW)
> analysis for the IHPD problem. Make sure to check balance and overlap.

TODO

### TK 20.9, Propensity score matching

> Decide on a balance metric for the covariates in the IHPD problem.  Try out a
> variety of propensity score approaches, varying the propensity score models
> and method for restructuring, including weighting by inverse estimated
> probability of treatment.  Find at least eight approaches that satisfy your
> balance criteria. Comment on the variation in your estimates.

TODO

### TK 20.10, Inverse estimated probability of treatment weighting and other estimates

> Figure 20.15 displays hypothetical data from an observational study with one
> confounder.
>
> (a) Determine the weights (normed and unnormed) for estimating the average
>     treatment effect for the treated units (ATT) and the sample size in the
>     ATT pseudo-population.
>
> (b) Check for balance in the covariate and potential outcomes in the
>     reweighted sample.
>
> (c) Calculate the ATT in this example using the potential outcomes.
>
> (d) Estimate the ATT in this example using the reweighted data.
>
> (e) Show the equivalency between weighting for ATT in this example and the
>     stratification weights discussion in Section 20.6.
>
> (f) Repeat all of the above for the average treatment effect for the control
>     units (ATC).

TODO