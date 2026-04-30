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


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer