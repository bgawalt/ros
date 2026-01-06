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
taken from a messy set of aggregate trend data."

The UN peacekeeping study gets praised for having a *thoughtful* process of
adding a hand-crafted predictor (how bad was the conflict) that directly
iterated on a simpler first-run model.

The difference is that the use of a disciplined process or workflow, vs.
pluggin' and chuggin', makes for more trustworthy conclusions.  It starts a
conversation instead of prematurely concluding one.

### 1.4,  Challenges in building, understanding, and interpreting regressions

"We can distinguish two different ways in which regression is used for causal
inference: estimating a relationship and adjusting for background variables."

Note that one author, Gelman, is adorably prickly about always saying "adjusting
for" when the typical jargon is "controlling for."  It's humbler!  And the
actual operation being performed is indeed humble.

#### (1/2) Regression to estimate a relationship of interest

You wan't to know the `m` in `y = mx + b`.  And of course this gets complicated,
where you think `m` will vary based on other covariates, like how `m` is
different for smokers and non-smokers when estimating the carcinogenic effect of
radon.

#### (2/2) Regression to adjust for differences between treatment and control groups

I really love Fig 1.8 for this:

![Hypothetical data with a binary treatment and a continuous pre-treatment variable. Treated units
are displayed with circles on the scatterplot, and controls are shown with dots. Overlaid is a fitted regression
predicting the outcome given treatment and background variable, with the estimated treatment effect being the
difference between the two lines.](./fig/fig1_8.png)

#### Introducing workflow

The final subsection here lays out the workflow cycle of regression analysis:

1.  Model building (i.e., stating a functional form like `y = mx + b`; start
    simple and add complexity on later loops)
2.  Model fitting, this is just the stats library of your choice
3.  Understanding model fits, where you especially use graphs and charts to
    explore where the model is succeeding and where failing and see if you get
    a hunch around why
4.  Criticism

I can add some perspective here: I know author Gelman from his blog.  The
reason I know his blog is that he's entering a third decade of trying popularize
the idea of criticism, always and everywhere.  It doesn't have to be a punitive,
flagellating slog, but if you avoid it, you wind up with the alternative of,
uhhhhhhhhhhhh, let's say, overconfident conclusions.  Blinding with science.

"No study is perfect.... The common theme is that we should recognize challenges
in extrapolation \[BG: I think of this more as the three kinds of generalization
described in 1.1\] and then work to adjust for them."

### 1.5, Classical and Bayesian inference

This is teasing an introduction to the holy war of Bayesians vs. Frequentists,
but cutely starts by talking about how really there are "various methodological
and philosophical frameworks."

> Common to all [BG: note, *all* not *either*!] these approaches are three
> concerns:
> 
> 1.  what information is being used in the estimation process,
> 2.  what assumptions are being made, and
> 3.  how estimates and predictions are interpreted, in a classical or Bayesian
>     framework

#### Information

There's the actual data you have as a CSV or whatever.  Then there's the
information about how it was collected, including how treatment attribute
values were assigned. And then "\[f\]inally, we typically have *prior
knowledge*" (emphasis in original), which is where the holy war comes in.

#### Assumptions

1.  Functional form of the model, a.k.a., the likelihood
2.  Data provenance, e.g., do we assume (if even just for the sake of
    simplification) the data were sampled randomly?
3.  Real-world relevance.  Are these measurements stable across time and across
    units of study?  Here's where that third and most taxing form of
    generalization comes in, "The interpretation of a regression of `y` on `x`
    depends also on the relation between the measured `x` and the underlying
    predictors of interest, and on the relation between the measured `y` and the
    underlying outcomes of interest.

#### Classical vs. Bayesian

The last two subsections introduce a classical analysis, where the uncertainty
interval for the estimated treatment effect is wide.  And then it's reanalyzed
in the Bayes style, adding in prior information stating a range of effect sizes
that it's reasonable to expect.  This narrows the range of possible effect
sizes.  Was that a good idea or not?  Impossible to say in a vacuum.

The reason the authors come down on the side of Bayes is that you can pretty
much recover the same answers that the classical result will give, by using
weakly- and non-informative ("flat") priors.  But you also get a handy and
easy way to explore other options with an actually-informative prior and see if
that "helps."

Measuring helpfulness is left implicit, but, it's down to "are the predictions
made by the model more or less correct," which necessarily means collecting more
data than you analyzed to craft this model.

### 1.6, Computing least squares and Bayesian regression

This is now just about what to type into what computer file.  The book uses R
(and [Stan](https://mc-stan.org/)); I will use Python (and... almost certainly
[PyStan](https://pystan.readthedocs.io/en/latest/)).

I will say that *I* know what Stan is doing there: it's doing Markov chain Monte
Carlo.  But this is not made explicit here; there is merely allusion to 
"producing simulations that enable you to express inferential and predictive
uncertainty (that is, estimates with uncertainties and probabilistic predictions
or forecasts)."

Pretty clear the book won't ever get into that: "Bayesian and simulation
approaches become more important when fitting regularized regression and
multilevel models. These topics are beyond the scope of the present book, but
once you are comfortable using simulations to handle uncertainty, you will be
well situated to learn and work with those more advanced models."

I started this whole thing to learn about those multilevel models, but, I will
take it on faith that the book is setting me up for success here later.  Or at
least, shading in subtleties that I wouldn't learn about jumping straight to
MRP.

## Exercises

### 1.2, Sketching a regression model and data

This one involves sketching data that powers a linear regression a la Fig 1.1b,
with two levels of residual standard deviation.  I sketched it in Matplotlib,
which you can see in [the Chapter01 notebook](./notebooks/Chapter01.ipynb):

![two scatter plots, one with 3x the residual std dev of the other](/fig/ex01_2.png)

### 1.9, A problem with linear models

> Consider the helicopter design experiment in Exercise 1.1.
> Suppose you were to construct 25 helicopters, measure their falling times, fit
> a linear model predicting that outcome given wing width and body length:
> 
>   `time = b_0 + b_1 * width + b_2 * length + error`
> 
> and then use the fitted model to estimate the values of wing width and body
> length that will maximize expected time aloft.
> 
> (a) Why will this approach fail?
> (b) Suggest a better model to fit that would not have this problem.

It'll fail because of the linearity of the model.  If either `b_j` parameter is
negative, you maximize time aloft by setting the width (or height) to zero.  If
either is positive, you maximize time aloft by make width (or height)
*infinite*.  Those are both degenerate answers.

I recommend adding synthetic predictor attributes for `width^2`, `height^2`, and
`width * height`, so that the model now has six `b_j` parameters to fit.  It's
still a "linear model," but it's linear over non-linear transformations of our
data.  You'll be able to fit parabolas that will allow for a non-degenerate
maximum.