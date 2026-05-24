# Chapter 19: Causal inference using regression on the treatment variable

[(Return to README)](./README.md)

Just like my intro to last chapter, this chapter opens with the difference
between for predicting differences you expect to see *between* units and
differences you expect to see when applying/withholding a treatment
*to the same* unit.

> More generally, causal inference can be viewed as a special case of prediction
> in which the goal is to predict what *would have happened* under different
> treatment options.

That's neat!  In terms of, how do you test this.  The most obvious, and only,
thing that occurs to me is (a) fit the regression to the randomized experiment
data, (b) make predictions on a new/held-out set of randomized experiment data.
I suppose that's not so different than what we were doing to evaluate models in
earlier chapters, but it *feels* different to have the model first, *then* set
the value of treatment predictor $z$, before applying the model to those
predictors (one of which has a value you controlled!).


## Subsection rundown

### 19.1, Pre-treatment covariates, treatments, and potential outcomes

The three sorts of measurments made of each datum $i$:

*  **Pre-treatment measurements, a.k.a. covariates:** $x_i$, an optional vector.
    But as we saw in the last chapter, having and using these can reduce both
    bias and variance in our estimate of the average treatment effect.
*  **Treatment:** $z_i$, a binary indicator, 1 if the unit received the
    treatment or 0 if the unit is in the control group.
*  **Outcome measurement:** $y_i$, with special labels $y_i^1$ and $y_i^0$
    (the potential outcomes notation) defining $y_i$'s recorded value depending
    on what group $i$ was in.

Nothing special there, basically what we've been saying this whole time, albeit
with more emphasis on the $z_i$ "special" covariate.  (I have been using
"predictors" a lot for the values used to predict the outcome, a term which
seems purposefully missing here.)

### 19.2, Example: the effect of showing children an educational television show

In 1970, education researchers showed early elementary schoolers
["The Electric Company"](https://en.wikipedia.org/wiki/The_Electric_Company),
then later measured their reading ability.  They compared them to a control
group of classrooms that were not shown the program in class.  The unit of study
was one classroom at a time, where $n = 192$ classrooms.

Figure 19.3 does not make it look like the treatment was a huge win; the
difference in means in Grades 1 and 2 are pointing in the right direction, but
are very small relative to the overall variation in (classroom) outcomes:

![A 2x4 grid of bar-chart histograms, where the x-axis of each runs from 45 to
120 and represents a classroom's average reading score, and bar height
indicates number of classrooms with that score.  The top row are control
classes and the bottom are treatment classes.  Each column reflects Grades 1
then 2, 3, and 4.  Big black vertical bars show the mean of each histogram.
Reading score distributions rise in mean and shrink in variance as grade
increases, for both treat and control. The means for Grades 3 and 4 are
basically identical between treat and control; the means for Grades 1 and 2 show
a ~10 point gain, but the standard deviations of each histogram is between 10
and 15.](./fig/part5/fig19_03_elec_co_hists.png)

The study was designed with matched pairs: each school in the study had two
classrooms participate (the two with the worst reading scores), with treatment
applied at random between those two classes.  The book says that this points
towards using a multilevel model to account for those school effects at the
pairwise level, but that will have to wait for a more advanced book.

The section ends with simple estimates of the treatment effect,

1.  taking the overall SATE, averaging over all four grades
2.  calculating the difference of group-means within each grade, which is
    a good idea (a) because the study design randomizes within each grade, just
    by dint of the pairing, and (b) the obvious difference in pre- and
    post-treatment test measures between the grades.  "The effect varies enough
    by grade that it would not make sense to try to estimate a single treatment
    effect averaging over the four grades."

### 19.3, Including pre-treatment predictors

Each classes' mean reading test score, measured pre-treatment, is used as the
sole covariate in their regression analysis.  This is what they were talking
about earlier about how a multilevel model would be useful: there's no
covariate for school right now, even though the units all share a school with
other units, and that's a source of explainable variance in the outcome.

The inclusion of the pre-treatment reading test score has the nice and typical
benefit of reducing uncertainty in the estimate of the causal effect, like we
saw in the last chapter.  They go out of their way to say that including the
covariate in the analysis offers the upside chance to reduce both variance and
bias.

They also devote two paragraphs to reemphasize: just comparing before to after
will lead you astray.  There is no good reason to think that "test score before
treatment is applied" is a good estimate of "post-study test score you'd get had
you not applied the treatment"; it's neither low-bias nor low-variance.

They discuss the *gain score* framework, where instead of modeling

$$y_i = \alpha + \tau z_i + \beta x_i + \text{error}$$

you define $g_i := y_i - x_i$ and model:

$$g_i = \alpha + \tau z_i + \text{error}$$

This is the same as locking $\beta$ to a value of 1, which can reduce variance
in estimating $\tau$ via introducing bias (i.e., a strong prior).

This closing paragraph threw me:

> Another motivation for use of gain scores is the desire to interpret effects
> on changes in the outcome rather than the effect on the outcome on its own.
> Compare this interpretation to the interpretation of a treatment effect
> estimate from a model that adjusts for the pre-test; in this case we could
> interpret an effect on the outcome for those with the same value of the
> pre-test. The difference between these interpretations is subtle.

That subtlety is lost on me.  Closest I can get is, the gain score version is
saying "comparisons between two units can ignore pre-treatment predictor
values"?

### 19.4, Varying treatment effects, interactions, and poststratification

You can absolutely add an interaction term between covariate(s) and treatment.
That does leave you with a more complicated set of coefficients to interpret.
The model is now:

$$y_i = \alpha + \tau_1 z_i + \beta x_i + \tau_2 z_i x_i + \text{error}$$

where the treatment effect is $\tau_1 + \tau_2 x$.  Except $x$ varies from
unit to unit.  They go through a worked example using the Electric Company data
to show that if you take the mean over $i$ of 

$$\frac{1}{n}\sum_{i=1}^n \tau_1 + \tau_2 x_i$$

you get the same mean and standard error as estimating the treatment effect with
no interaction (but yes, with the covariate term $\beta x_i$).

> In general, for a linear regression model, the estimate obtained by including
> the interaction, and then averaging over the data, reduces to the estimate
> with no interaction.  The motivation for including the interaction is thus to
> get a better idea of how the treatment effect varies with pre-treatment
> predictors, not to simply estimate an average effect.

The poststratification alluded to in this subsection title means

1.  fitting a model with interaction terms for covariates $x_{ij}$, 
    $j = 1 \ldots p$
2.  estimating the regression model
    $y \sim \alpha + \beta_0 z + \sum_j \beta_i x_{ij} + \sum_j \beta_{jz} x_{ij} z_i$
3.  deriving the treatment effect, $\beta_0 + \sum_j \beta_{jz} x_{ij}$ (i.e.,
    plug $z = 0$ and $z = 1$ into the regression formula above and take the
    diff),
4.  plug the means of $x_{\cdot j}$, $\mu_j$, to yield the population average
    treatment effect: $\beta_0 + \sum_j \beta_{jz} \mu_j$.

Those means, $\mu_j$, come from some outside source of info on the distribution
of covariate values in the population of interest.  The result of
poststratification applied here is to give a population average treatment
effect estimate, and when a Bayesian regression framework is used for the
estimates, the individual MCMC draws can be used to provide an uncertainty
interval around that mean estimate.

### 19.5, Challenges of interpreting regression coefficients as treatment effects

This is kind of confusing, because their example in this section (where naive
interpretation of the regression coefficient as a treatment effect steers you
wrong) is not an analysis of a randomized experiment, but an analysis of
many results from randomized experiments.

In this case, different studies decided their operating parameters (i.e.,
covariate values) in a vacuum.  There was no overarching randomization of *all*
design parameters; only the treatment/control split within each study was
randomized.  So studies finding a strong effect might have been conducted in
areas where researchers were more likely to set the covariates to particular
values, and now you have risk of committing the omitted-variable fallacy.

This feels like a weird thing to include.  It's useful as an example, but most
of the causal inference material assumes we're working at the single-study
level.  We just went over the crucial importance of randomization all last
chapter, so this actually-an-observational-study example seems like a weird
digression.

### 19.6, Do not adjust for post-treatment variables

The reason not to: those post-treatment variables are likely influenced by
the treatment variable's value.  This breaks the conditional independence
assumptions, that the two potential outcome values are independent of the
treatment value, given the other covariates.

I'm lost here, too.  I feel like earlier sections either didn't mention, or
didn't hit hard enough for me to notice, why it's bad that "the coefficient of
$z$ represents a comparison of families that differ fundamentally in their
underlying characteristics."

I bet there's a Bayes Ball diagram that would clear this right up, but this book
doesn't get that deep into the Bayes Weeds.  My attempt at drawing the Bayes net
the authors are thinking of didn't get me anywhere.

Best I can do for this is to say that the counterfactual intermediate outcome
acts as an omitted variable, which was fatal in the example in Section 19.5
above.

Googling around got me this blog post:

https://statmodeling.stat.columbia.edu/2009/07/05/disputes_about/

which doesn't bring any clarity, but that's because it winds up being much more
equivocal about whether you should/shouldn't include the post-treatment info in
the analysis.  The link in the post-script says you're better off skipping it if
your analysis is just going to be regression (you *could* back out causal
treatment effect estimates even with the intermediate covariates in the
regression model, but I guess it's hard?).  But it also says if you're using a
more complicated model, sure, go ahead and include the intermediate output's
mechanisms as part of it.


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer