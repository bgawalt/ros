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

### 19.7, Intermediate outcomes and causal paths

Opening of this section emphasizes that the randomized experiment is a black
box: treatment values go in, outcomes come out, we link the two with a
regression analysis.  We can get these SATEs, but we aren't left with much room
to establish a mechanism to explain the pathway from "treatment applied" to
"expected outcome increases."

One thing you *can't* do: run the model twice, once with just pre-treatment
covariates, again with pre- and post-treatment covariates, and take the
difference between the SATEs found in each case.  If the treatment affects the
values of the post-treatment covariates, then you're necessarily skewing
the covariate distributions between the treat and control groups.

> The regression adjusting for the intermediate outcome thus implicitly compares
> unlike groups \[...\] and underestimates the treatment effect, because the
> treatment group in this comparison is made up of lower-\[valued outcomes\],
> on average.

They put forward the technique of principal stratification: dividing up the
subjects into categories based on their intermediate potential outcomes.
But you don't get to observe the counterfactual intermediate outcome, so instead
you're just making educated guesses as to what they would have been.  That's no
longer a clean, randomized experiment, it's an analysis of observational data
like before.

They say to keep an eye out for *instrumental variable* techniques, coming in
Chapter 21.

This chapter closes by looping back to trying to draw casual inferences from
regression analysis of observational studies.  It's all tripped up by the fact
that asking "how much would a unit increase in covariate $x_i$, and only $x_i$,
*cause* the output to increase?" assumes $x_i$ can be treated independently from
the other covariates.  If there's no data, or if in the real world, no one ever
sees an increased $x_i$ without seeing an increased $x_j$, the question is
asking about the outcome of an impossible input.  If an increase in $i$ requires
an increase in $j$, then the change in the outcome can't be traced back to
either covariate shift in isolation.

This applies to the randomized-experiment-with-intermediate-outcome case because
the post-treatment covariate has this same "no one sees a bigger $z$ without a
bigger post-intermediate output $q$" phenomenon that made causal interpretaion
of observational study coefficients a non-starter.


## Exercises

Plots and computation powered by [Chapter19.ipynb](./notebooks/Chapter19.ipynb)

### 19.4, Pre-test and post-test

> 100 students are given a pre-test, then a treatment or control is randomly
> assigned to each, then they get a post-test.  Given the following regression
> model:
>
> $$\text{post\_test} = a + b \cdot \text{pre\_test} + \theta \cdot z + \text{error},$$
>
> where $z = 1$ for treated units and 0 for controls.  Further suppose that
> `pre_test` has mean 40 and standard deviation 15.  Suppose $b = 0.7$ and
> $\theta = 10$ and the mean for `post_test` is 50 for the students in the
> control group. Further suppose that the residual standard deviation of the 
> regression is 10.
>
> (a) Determine a.
>
> (b) What is the standard deviation of the post-test scores for the students in
>     the control group?
>
> (c) What are the mean and standard deviation of the post-test scores in the
>     treatment group?

$$a = 50 - b \mathcal{E}(\text{pre_test}) = 22$$
$$\text{sd}\left(y^C) = 0.7 \cdot 15 + 10 = 20.5$$
$$\bar{y^T} = a + b \mathcal{E}(\text{pre_test}) + 10 = 60$$

and the standard deviation of the post-test scores in the treatment group
matches that of the control group, 20.5.

### 19.6, Sketching the regression model for causal inference

> Assume that linear regression is appropriate for the regression of an outcome,
> $y$, on treatment indicator, $z$, and a single confounding covariate, $x$.
> With pen on paper, sketch hypothetical data (plotting $y$ versus $x$, with
> treated and control units indicated by circles and dots, respectively) and
> regression lines (for treatment and control group) that represent each of the
> following situations:
>
> (a) No treatment effect,
> 
> (b) Constant treatment effect,
>
> (c) Treatment effect increasing with $x$.

![Three scatter plots in a row, all on x-axes ranging from 0 to 10.  Control
data in all three is forty points with x values uniform between 0 and 10, and
y values trending down as 20 - 3x, plus normally distributed noise of standard
deviation 2.  Each plot has its own treatment data points as well, where
(a) looks just like control, (b) looks like control translated upwards by 6
units, and (c) looks like the same 2-unit SD noise around a trend of 26 - 2x
](./fig/part5/ex19_06_sketches.png)

### 19.7, Linearity assumptions and causal inference

> Consider a study with an outcome, $y$, a treatment indicator, $z$, and a
> single confounding covariate, $x$. Draw a scatterplot of treatment and control
> observations that demonstrates each of the following:
>
> (a) A scenario where the difference in means estimate would not capture the
>     true treatment effect but a regression of $y$ on $x$ and $z$ would yield
>     the correct estimate.
>
> (b) A scenario where a linear regression would yield the wrong estimate but a
>     nonlinear regression would yield the correct estimate.

For part (a), when the $x$ covariates are not distributed similarly across
treatment and control, diff-in-means can give you a misleading answer.
I simulated an experiment where the treatment effect is -0.5, but the outcomes
are positively correlated with $x$.  And if the treat group has the
higher-than-average $x$ values, then the result can be a wash.

Here's what my data looked like:

![Scatter plot where the control series is solid blue dots, trending upwards
over an x range of 0 to 1, with y ranging from 0 to 1.  The treatment group
ranges over an x range of 0.5 to 1.5, and the y also ranges from 0 to 1 (because
the treatment itself causes a -0.5 intercept shift).](./fig/part5/ex19_07a.png)

The diff-in-means estimate of the effect is -0.05, ten times less than the true
value.

When I run the regression, `y ~ x + z`, though:

Coef.     | Mean   | s.e.
--------- | ------ | ------
sigma     |   0.10 | 0.01
Intercept |  -0.00 | 0.02
x         |   1.06 | 0.04
z         |  -0.57 | 0.03

Not quite exact (sample size here is 100 points total), but much much closer
than a 10x underestimate.

For part(b), the treatment is a constant +10, but the outcome $y$ rises as the
square of the covariate $x$ under both treatment conditions.  If we also get
a skewed sample -- in this case, treatment units only cover [2, 6] while control
saw the full [0, 10] range -- then ignoring the quadratic component of $x$
gives a bad SATE.

Here's the data:

![In solid dots, a somewhat noisy parabola that looks like y = x^2 from 0 to 10.
In hollow dots (treatment), the same noisy parabola lifted upwards by 10 units,
but only covering the range from 2 to 6](./fig/part5/ex19_07b.png)

The model `y ~ x + z` gives an underestimate of the treatment effect:

Coef.     | Mean   | s.e.
--------- | ------ | ------
sigma     |   5.92 | 0.42
Intercept | -13.29 | 1.55
x         |   9.49 | 0.26
z         |   2.51 | 1.21

But using the true model, `y ~ x + x^2 + z`, gives an accurate estimate:

Coef.     | Mean  | s.e.
--------- | ----- | ------
sigma     |  1.14 | 0.09
Intercept |  0.76 | 0.41
x         | -0.26 | 0.21
x2        |  1.02 | 0.02
z         |  9.81 | 0.28

### 19.8, Messy randomization

> The
> [folder `Cows` contains data](https://github.com/avehtari/ROS-Examples/tree/master/Cows)
> from an agricultural experiment that was conducted on 50 cows to estimate the
> effect of a feed additive on 6 outcomes related to the amount of milk fat
> produced by each cow.
>
> Four diets (treatments) were considered, corresponding to different levels of
> the additive, and three variables were recorded before treatment assignment:
> lactation number (seasons of lactation), age, and initial weight of the cow.
>
> Cows were initially assigned to treatments completely at random, and then the
> distributions of the three covariates were checked for balance across the
> treatment groups; several randomizations were tried, and the one that produced
> the "best" balance with respect to the three covariates was chosen.  The
> treatment depends only on fully observed covariates and not on unrecorded
> variables such as the physical appearances of the cows or the times at which
> the cows entered the study, because the decisions of whether to re-randomize
> are not explained.
>
> We shall consider different estimates of the effect of additive on the mean
> daily milk fat produced.
>
> (a) Consider the simple regression of mean daily milk fat on the level of
>     additive.  Compute the estimated treatment effect and standard error, and
>     explain why this is not a completely appropriate analysis given the
>     randomization used.
>
> (b) Add more predictors to the model. Explain your choice of which variables
>     to include.  Compare your estimated treatment effect to the result from
>     (a).
>
> (c) Repeat (b), this time considering additive level as a categorical
>     predictor with four levels.  Make a plot showing the estimate (and
>     standard error) of the treatment effect at each level, and also showing
>     the inference from the model fit in part (b).

Loaded the `Cows` data, using the codebook as a guide to what columns to
extract (and how to generate the `milk_fat` outcome):

|         | age | lactation | initial_weight | level | milk | fat | milk_fat
--------- | --- | --------- | -------------- | ----- | ---- | --- | --------
**count** | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00 | 50.00
**mean**  | 42.16 | 2.38 | 1258.06 | 0.15 | 59.54 | 3.58 | 213.09
**std**   | 18.59 | 1.32 | 181.21 | 0.11 | 9.36 | 0.48 | 45.38
**min**   | 21.00 | 1.00 | 900.00 | 0.00 | 40.24 | 2.65 | 130.81
**25%**   | 26.25 | 1.00 | 1118.75 | 0.10 | 53.11 | 3.27 | 179.85
**50%**   | 37.00 | 2.00 | 1266.50 | 0.15 | 59.52 | 3.46 | 207.32
**75%**   | 49.00 | 3.00 | 1369.00 | 0.20 | 66.66 | 3.91 | 248.43
**max**   | 95.00 | 6.00 | 1656.00 | 0.30 | 76.60 | 4.96 | 328.63

For part (a), I fit the model `milk_fat ~ level`, and get back:

Coef.     | Mean   | s.e.
--------- | ------ | ------
sigma     |  44.37 | 4.59
Intercept | 194.43 | 10.50
level     | 124.45 | 56.23

The `sigma` value is basically identical to the standard deviation of `milk_fat`
in the dataframe description above.  So that's bad news; the `level` treatment
is not a good explainer all on its own.

For part (b), I fit the model
`milk_fat ~ level + age + lactation + initial_weight`, including the three
pre-treatment predictors (and left all the post-treatment ones out of the
dataframe parsing) and get back:

Coef.          | Mean   | s.e.
-------------- | ------ | ------
sigma          |  36.22 | 3.80
Intercept      |  45.81 | 45.72
level          | 106.85 | 46.66
age            |  -2.15 | 1.06
lactation      |  31.23 | 14.06
initial_weight |   0.13 | 0.05

The new `sigma` parameter is an actual improvement, though, not by all that
much.  The standard error of `level` has dropped, which is nice, but again, not
that much.  Adjusting for pre-treatment predictors has also shrunk the mean
estimate for the effect of the treatment.

For part (c), I made a new string column, `level_cat`, just as a can't-lose
form of discretizing the `level` treatment variable.  I then fit the model
`milk_fat ~ C(level_cat) + age + lactation + initial_weight`, and got:

Coef.             | Mean  | s.e.
----------------- | ----- | ------
sigma             | 37.02 |  4.07
Intercept         | 42.52 | 48.55
C(level_cat)[0.1] | 17.52 | 15.08
C(level_cat)[0.2] | 25.48 | 15.39
C(level_cat)[0.3] | 32.70 | 16.06
age               | -2.16 |  1.13
lactation         | 31.64 | 14.75
initial_weight    |  0.13 |  0.05

Man!!  The `sigma` parameter got worse by doing this.  Oh well.

Here's the plots, with the linear effect of (b) as dashed grey lines.  All
coefficient uncertainties represent $\pm 2$ standard errors.

![Plots of the C(level_cat) coefficients from the above table.  The dashed grey
overlay of the linear effect underestimates the categorical answers for levels
0.1 and 0.2 but matches up perfectly with the mean of 0.3
](./fig/part5/ex19_08_effects.png)

### 19.10, Estimating causal effects

> The folder Congress has election outcomes and incumbency for U.S. Incumbency
> advantage congressional election races in the 1900s.
>
> (a) Take data from a particular year, t, and estimate the effect of incumbency
>     by fitting a regression of $v_{i,t} , the Democratic share of the
>     two-party vote in district $i$, on $v_{i,t-2} (the outcome in the previous
>     election, two years earlier), $I_{it}$ (the incumbency status in district
>     $i$ in election $t$, coded as 1 for Democratic incumbents, 0 for open
>     seats, -1 for Republican incumbents), and $P_{it}$ (the incumbent party,
>     coded as 1 if the sitting congressmember is a Democrat and -1 if he or she
>     is a Republican). In your analysis, include only the districts where the
>     congressional election was contested in both years (if you are interested
>     in missing-data imputation for these elections, see Exercise 17.10), and
>     do not pick a year ending in 2. District lines in the United States are
>     redrawn every 10 years, and district election outcomes $v_{it}$ and
>     $v_{i,t-2}$ are not comparable across redistrictings, for example, from
>     1970 to 1972.
>
> (b) Plot the fitted model and the data, and discuss the political
>     interpretation of the estimated coefficients.
>
> (c) What assumptions are needed for this regression to give a valid estimate
>     of the causal effect of incumbency? In answering this question, define
>     clearly what is meant by incumbency as a “treatment variable.”

TK