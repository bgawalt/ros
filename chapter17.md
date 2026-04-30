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

## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer