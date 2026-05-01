# Chapter 17: Poststratification and missing-data imputation

[(Return to README)](./README.md)

Fitting a regression model is an intermediate step (not least because you
usually fit a *sequence* of models until you have one you like), and this
chapter is about two things you can that sandwich the coefficient-generating
step of model fitting:

1.  Missing-data analysis: pre-process your data to make them more amenable to
    regression (or other statistical) analysis
2.  Poststratification: make predictions about a new dataset that varies
    substantially from the one that built this model

## Subsection rundown

### 17.1, Poststratification: using regression to generalize to a new population

If your existing observations are not a representative sample of the population
of interest, you can't just take blunt averages over the sample and hope to get
good estimates of what holds in genpop.  But a regression model can help, if it
learns a generally-valid mapping from predictor values to outcome-of-interest.
The composition of the training data might be off, but the rule it learns to
predict outcomes might not be, and you can apply the rule to genpop and come out
okay.

To poststratify by attribute $A$, (1) you need each observation's $A$ value,
and (2) the prevalence of each $A$ value in the population of interest.
Do this for each of your attributes $A_i$, and then you can:

1.  Assemble the full cross-product table of the attribute prevalance (i.e.,
    how many people have gender X, age bucket Y, and party identification Z)
2.  Fit the regression of outcome from attributes
3.  Apply the fit model to get expectated values for each entry in the
    postratification table in (1)
4.  Weight each predicted value of expected value and take the weighted sum to
    get the expectation of the average outcome value in the general population

Some complications, though.  The prevalence value in the poststrat table of (1)
are usually themselves statistical estimates, with their own uncertainties and
unreliability.

### 17.2, Fake-data simulation for regression and poststratification

They make up a fake table of census values for population counts binned by
sex, age, and ethnicity.  (They point out that their mechanism implies that
membership across these categories are statistically independent from each
other, which is not true in the real world.)

They set up a non-response rate, also based on a simple multiplicative model
that has a similar "the categories are independent/non-intersectional" mood.
They sample 1,000 people, proportional to the made-up census bucket counts,
filtering out non-responders.

They synthesize binary outcomes for each sampled person according to an
underlying logistic model.  Then they fit a model to that fake data, and
apply it to the poststrat table to get a mean estimate and standard error (by
pulling out the individual MCMC coefficient iterates).

### 17.3, Models for missingness

"Missing data arise in almost all Example: serious statistical analyses\[, but
we discuss\] some relatively simple approaches that can often yield reasonable
results."

Four main ways data are missing:

1.  Missing completely at random.  If this is true of your data, then there's no
    bias introduced by just throwing away rows that have missing elements.

2.  Missing at random.  (But not *completely* at random!)  Whether or not an
    element is missing is derived, up to a random factor, entirely from
    other observed attributes.  As long as your model adjusts for all the
    attributes that drive missingness, throwing out rows won't introduce bia.

3.  Missing due to unobserved predictors.  If some un-noted aspect of your data
    subjects is driving missingness, then you can't use it in your regression,
    and now either missinginess "must be explicitly modeled" or else you just
    throw out the missing-elements rows and accept some amount of bias.

4.  Missing due to the missing value itself.  They give an example of high
    income respondents, out of modesty, declining to answer a "what is your
    income" question.  If you bring in more predictors, maybe you eventually
    get enough ability to predict the self-censoring attribute to make it more
    like "missing at random."  But it's not looking good for you, if you're
    here.

There's no good way to know which bucket your data falls into.  It's like a
close cousin of the omitted variable bias; you can't rule out some unobserved
(and so, unadjusted-for) factor is driving missingness.  The cope is to just
include as many predictors as possible and hope missingness is now at random.

### 17.4, Simple approaches for handling missing data

*  **Complete-case analysis:** just throw away units missing any data.  This
    breaks when:
    *  the complete cases are systematically different than the incomplete ones,
        which would mean the rule you learn is biased w.r.t. the overall unit
        population
    *  there are enough predictors that the cumulative chances of having *none*
        of them missing drops to near zero, completely trashing your sample size

*  **Available-case analysis:** if you have multiple aspects you want to study,
    take one subset of the sample at a time, where each subset excludes only the
    units that are missing an attribute necessary for that aspect.  (So, subsets
    don't include complete-cases only, but do have standards for excluding at
    least some.)  A special case is when the researcher just tosses a predictor
    entirely because it's just missing too often.  But:
    *  As with complete-case analysis, if there's systematic difference between
        units that are missing an attribute and those that aren't, then you get
        a biased analysis for that aspect
    *  Each aspect is studied with a different subset of the sample, and so
        might not be consistent with each other.  Like depending on nonresponse
        to certain attributes, some aspect studies may have units that are
        Blacker or whiter than the other subsets used for other aspects studies.
    *  Omitting predictors, even frequently missing ones, can cause you to
        violate assumptions needed for analyses like causal inference.

*  **Nonresponse weighting:** if complete-case analysis throws out a bunch of
    units, can you just reweight the remaining units and restore
    representativeness?  They provide a guide for doing this if exactly one
    predictor has missing values: build a model that predicts nonresponse of
    that one flaky predictor, toss out incomplete cases, and reweight the
    remaining complete-cases by (the inverse of) their predicted "Pr{present}"
    scores.

*  **Simple missing data approaches that retain all the data:** why not just
    fill in the missing data and pretend they're all complete-case units?
    This is loading in a lot of undeserved certainty; if you just replace the
    missing elements with a single value, you're acting like there's no
    uncertainty to your guessed-at imputation.  But here's some options:
    *  **Mean imputation:** each missing value gets the mean of all the
        non-missing values for that predictor.  This lowers the observed
        variance of that predictor, and pulls its correlations will all other
        predictors and the output towards zero.
    *  **Last value carried forward:** the example use case they have in mind
        for this are where a pre-treatment predictor is measured.  If the
        post-treatment outcome is never recorded, just impute it as whatever the
        pre-treatment measure was.  Because real data has reversion-to-the-mean
        effects, and this imputation can't ape that, you can wind up with
        distortions.  This is especially bad if the outcome is missing more
        often in the treatment group vs. the control group or vice versa.
    *  **Using information from related observations:** if you want to know
        something about a subject's father, but he doesn't fill in the survey,
        why not ask the mother for the information in her survey, and then use
        that to make the subject case-complete?  This might help, but also,
        maybe there's distortions in how correctly and under what conditions the
        mother's response is given.
    *  **Imputation based on logical rules:** if earnings is unreported, but
        hours-worked is reported as zero, sure, just impute earnings as also
        zero.

### 17.5, Understanding multiple imputation

Single values make it hard to convey uncertainty, so for each missing element,
impute multiple values.  Like, if you fit a Bayesian regression to generate
missing elements from observed elements, then you have our usual posterior
predictive distribution to draw sample imputations from.

Multiple imputation leaves you with $M$ distinct datasets, each made up of
complete cases.  Models fit to predict the outcome on a single dataset $m$,
$m = 1, \ldots, M$, have "internal" uncertainty in model parameters, the sort of
standard errors we've been looking at for ten chapters.  And now, newly, there's
"external" uncertainty, which is how the estimates vary across the $M$ imputed
datasets.

For a scalar coefficient $\beta$, we get estimate $\hat{\beta}_m$ with standard
error $\text{se}_m$ from dataset $m$, and we get an overall estimate by
averaging them: $\hat{\beta} = \frac{1}{M}\sum_{i=1}^M \hat{\beta}_m$.

$$se_\beta = \sqrt{W + \left(1 + \frac{1}{M}\right)B}$$

$$W := \frac{1}{M}\sum_{m=1}^M \text{se}_m^2$$

$$B := \frac{1}{M - 1} \sum_{m=1}^M \left(\hat{\beta}_m - \hat{\beta}\right)^2$$

#### Simple random imputation

If you're missing elements for a particular predictor $x_j$, just fill in those
blanks by randomly sampling $x_j$ values that *aren't* missing.  But this not
that smart, and will make weird imputations that don't make sense paired with
the other predictor values.

Like if "total earnings" is your imputation target, and "wage earnings" is a
predictor, simple random imputation will happily pick a total earnings from the
observed value set that's less than this unit's wage earnings.

#### Random regression imputation

Smarter would be to use the existing predictors to predict the missing value.
That way you will get more sensible value pairs across the units of the
imputed datasets.

Make sure to use the posterior-predict approach, where you bring draw on the
spread/uncertainty of the model coefficients when making predictions.  
Otherwise, if you just take the expected value or point prediction, the imputed
values will be too-low-variance relative to the observed/true values.

The book emphasizes that you're just going for predictive accuracy with this
imputing model.  You don't have to have the predictors make sense in terms of
their relationship to the output, just so long as they make for better
predictions.  (I.e., good prediction due to reverse-causality is fine.)

They walk through a case where prediction benefits from the two-step process of
(a) use a logistic regression to decide "is the value zero, or not", then
(b) decide "what is the value for this" as trained on the non-zero-value-having
cases.

#### Multivariate imputation

When more than one predictor is allowed to be missing from a case, the routine
approach is to grab an off-the-shelf multiple-outputs regression modeler.  They
say that these tend to default to assuming multivariate normal or $t$
distributions governing the set of missing values.  "\[T\]his automatic approach
is easy enough that it can be a good place to start."

They conclude by recommending iterative regression imputation:

1.  Start by completing the data matrix with simple random imputation.
2.  Loop over each predictor $j$ that needs imputation:
    *  fit an imputation model for $j$ with whatever the current matrix looks
        like currently, starting from the simple randoms of (1)
    *  replace $j$'s missing values with the imputation model you just trained
    *  move on to $j+1$, now using the somewhat-smarter-imputations for $j$ as
        the basis of $j+1$'s imputation model
3.  Repeat (2) a bunch of times (ten, in their example)

Model checking is hard here.  Histograms of imputed vs. observed values are
useful.

### 17.6, Nonignorable missing-data models

Sometimes the missingness of the data is itself a powerful signal that bears on
your question of interest.  "Age at event" models don't have outcomes for
units where the event hasn't happened yet.  But that it hasn't happened yet for
those units is valuable info; you have a lower bound on the age.  Certainly just
throwing out those observations is suboptimal.

They don't go into how to handle these, they're just planting the seeds right
now.


## Exercises

Plots and computation powered by [Chapter17.ipynb](./notebooks/Chapter17.ipynb)

### 17.1, Regression and poststratification

> Section 10.4 presents some models predicting weight from height and other
> variables using survey data in the
> [folder `Earnings`](https://github.com/avehtari/ROS-Examples/tree/master/Earnings/data).
> But these data are not representative of the population. In particular, 62% of
> the respondents in this survey are women, as compared to only 52% of the
> general adult population. We also know the approximate distribution of heights
> in the adult population: normal with mean 63.7 inches and standard deviation 
> 2.7 inches for women, and normal with mean 69.1 inches and standard deviation
> 2.9 inches for men.
>
> (a) Use poststratification to estimate the average weight in the general
>     population, as follows:
> 
> > (i) fit a regression of linear weight on height and sex;
> >
> > (ii) use `posterior_epred` to make predictions for men and women for each
> >     integer value of height from 50 through 80 inches;
> > 
> > (iii) poststratify using a discrete approximation to the normal
> >     distribution for heights given sex, and the known proportion of men and
> >     women in the population.
>
>    Your result should be a set of simulation draws representing the population
>    average weight. Give the median and mad sd of this distribution: this
>    represents your estimate and uncertainty about the population average
>    weight.
>
> (b) Repeat the above steps, this time including the `height:female`
>     interaction in your fitted model before poststratifying.
>
> (c) Repeat (a) and (b), this time performing a regression of log(weight) but
>     still with the goal of estimating average weight in the population, so you
>     will need to exponentiate your predictions in step (ii) before
>     poststratifying.

In fitting the regression model, I'll decline to $z$-scale or standardize the
data.  The gender indicator is binary, and the height indicator is on the order
of "dozens", so, there shouldn't be much numerical concern about fitting a good
model.  The two predictors are within a factor of like 60 of each other; not
great, not terrible.

In assembling the postratification table, the heights considered cover 99.998%
of people (assuming those normal approximations to height distributions).

Here's the dataset I loaded:

|         | weight | height | male
--------- | ------ | ------ | ----
**count** | 1789.00 | 1789.00 | 1789.00
**mean**  | 156.31 | 66.59 | 0.38
**std**   | 34.62 | 3.84 | 0.48
**min**   | 80.00 | 57.00 | 0.00
**25%**   | 130.00 | 64.00 | 0.00
**50%**   | 150.00 | 66.00 | 0.00
**75%**   | 180.00 | 70.00 | 1.00
**max**   | 342.00 | 82.00 | 1.00

And here's the model fit for `weight ~ height + male`:

Coef.     | Mean    | s.e.
--------- | ------- | ------
sigma     |   28.70 |  0.48
Intercept | -107.30 | 16.18
height    |    3.89 |  0.25
male      |   11.80 |  1.97

Note that this is not a model with especially high predictive accuracy.  That
`sigma` value is "accuracy to within $\pm52$ pounds.

The result: I predict the average weight in the overall population is
156.3 lbs., with a standard error of 0.7 lbs.

For the model `weight ~ height + male + height:male`, I get coefficient
estimates of:

Coef.       | Mean   | s.e.
----------- | ------ | ------
sigma       |  28.60 | 0.48
Intercept   | -61.39 | 21.15
height      |   3.18 | 0.33
male        | -96.80 | 32.56
height:male |   1.61 | 0.48

The `sigma` parameter has changed... not at all.

And so the estimated population average weight hasn't, either: 156.2 lbs, with a
standard error of 0.7.

For part (c), the `log(weight) ~ height + male` model gives:

Coef.     | Mean   | s.e.
--------- | ------ | ------
sigma     | 0.17 | 0.00
Intercept | 3.37 | 0.10
height    | 0.03 | 0.00
male      | 0.08 | 0.01

for an estimate of (154.0 lbs, se 0.7).

The `log(weight) ~ height + male + height:male` model gives:

Coef.       | Mean   | s.e.
----------- | ------ | ------
sigma       | 0.17 | 0.00
Intercept   | 3.54 | 0.13
height      | 0.02 | 0.00
male        | -0.32 | 0.19
height:male | 0.01 | 0.00

For an estimate of (153.9 lbs, se 0.65).
