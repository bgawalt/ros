# Chapter 1: Overview

Key line from the chapter intro, which motivates this whole book club in the
first place: "It turns out there are many subtleties involved even with simple
linear regression—straight-line fitting."  Yeah!  Let's master some subtleties.

## Subsection rundown

### 1.1, The three challenges of statistics

The book comes out swinging by stating its own terms for "what is statistical
inference".  It's about generalization, which I will connect to regression:

1.  *Generalizing from sample to population.*  Regressions lets you identify an
    association between an attribute pair within your dataset, which you then
    want to turn into a claim about units *not* in your dataset.
2.  *Generalizing from treatment to control.*  The book connects this
    explicitly: run a regression to tell you how changing `X` *causes* a certain
    amount of change in `Y`. Most important near term is that the regression
    allows for controlling for factors *other* than the change in `X`.
3.  *Generalizing from observed measurements to the underlying constructs of
    interest.*  I don't know how to link that up!  Especially in areas like
    psychology where you never actually get direct measurement of the underlying
    construct.  Maybe regression, in more advanced forms where the model encodes
    uncertainty in `Y` as well as `X`, to allow for the fact that neither one
    is a direct measure of what we want to study? E.g., 
    [the measurement error model](https://statmodeling.stat.columbia.edu/2025/09/09/show-dont-tell-chatgpt-5-marginalizing-gelmans-measurment-error-model-in-stan/)

### 1.2, Why learn regression?

*  **Prediction**
*  **Exploring associations**
*  **Extrapolation.** The name for this one is potentially confusing. You *are*
   extrapolating to units outside your training set when you apply the model to
   new data for the sake of prediction. But the regression will mostly be
   *interpolating* across your sample data to arrive at that prediction.
*  **Causal inference.** Called out as "perhaps the most important use of
    regression."  I can't read this paragraph in any other way than "causal
    inference requires an experiment", but we'll see more in Part 5.

### 1.3, Some examples of regression

*  **The Xbox election survey** alludes to multilevel regression and
    poststratification, which is what I actually want to learn, but will not
    really get covered in this book.  Good to have a foundation, anyway.
*  **The Electric company** got used in a randomized trial to see the effects of
    the edutainment on reading ability.  Mostly notable for how visualizing the
    regression doesn't have to look like `y = mx + b`.
*  **Effect of UN peacekeeping** is an observational study that makes causal
    claims
*  **Effect of gun laws** is an observational study that makes causal claims

The book loves on the peacekeeping study and hates on the gun law study, though
they state that "\[w\]e don’t want to make too much of the differences between
these studies, which ultimately are of degree and not of kind."

The gun law one just seems thoughtless to them.  They crammed a kitchen sink of
predictors on top of not-that-many observed data (fifty states,
thirty predictor attributes).  They turned the crank and got a p-value and then
went hog wild claiming a causal effect. "\[T\]he result was that a respected
medical journal was induced to publish strong and poorly supported conclusions
taken from a messy set of aggregate trend data

The UN peacekeeping study gets praised for having a *thoughtful* process of
adding a hand-crafted predictor (how bad was the conflict) that directly
iterated on a simpler first-run model.

The difference is that the use of a disciplined process or workflow, vs.
pluggin' and chuggin', makes for more trustworthy conclusions.  It starts a
conversation instead of prematurely concluding one.