# Chapter 14: Working with logistic regression

[(Return to README)](./README.md)

Now that we can fit logistic regressions, we can build on them with:

*  better ways to visualize the models,
*  better interpretation of coefficients, including under linear transformation
    and interactions of features,
*  making probabilistic predictions with the models, and aggregating those
    predictions into average predictive comparisons that work as model
    summaries,
*  better evaluation methods, using binned residual plots and predictive errors,
*  better handling of sparse, discrete data.


## Subsection rundown

### 14.1, Graphing logistic regression and binary data

When $y$ is binary, scatter plotting $y$ vs. $x$ doesn't really work any more.
The dots wind up too piled on top of each other.  For univariate data, consider
binning by $x$ and plotting the proportion of $y = 1$ (i.e., mean of $y$) in
each bin.  For 2-D data, consider scatter plotting $x_2$ vs. $x_1$, with
different color dots for depending on $y$'s value.

### 14.2, Logistic regression with interactions

The arsenic-wells example from Chapter 13 is revisited, this time adding an
interaction term between distance to nearest clean well and local well's
arsenic level.  The coefficients for non-interaction/pure-linear terms are
interpreted by plugging in the mean values of one-or-both predictors and using
the divide-by-four rule to describe what a unit change in a particular predictor
(or the intercept) does to predicted probability of switching, in terms of
percentage point shift.

The interaction term interpretation is interesting.  For each predictor, they
describe how a unit increase in *that* predictor changes the *other* predictor's
coefficient:

> Looking from one direction, for each additional unit of arsenic, the value
> −0.18 is added to the coefficient for distance.... Looking at it the other
> way, for each additional 100 meters of distance to the nearest well, the value
> −0.18 is added to the coefficient for arsenic.

When the predictor inputs are centered to be zero-mean, this makes no difference
to the predictor coefficients (though does change the intercept).  It makes it
a bit easier to do the coefficients, now that mean values don't need plugging in
to interpret the coefficients' impact on predicted probability of switching.

They look at LOO log score differences when the interaction term is, vs. isn't,
included in the model, and find that the two models are fairly equivalently
accurate on the held-out samples.

When they add a predictor for education level (on an ordinal scale of grades
completed, divided by four to bring into a more typical order of magnitude) and
a binary predictor for "are you in any community associations", they find a
low-s.e. coefficient around education and a medium-high-s.e. for association,
and so just keep the education predictor "for clarity and stability." (The
association estimate was also of a counterintuitive sign, which I think really
sunk it, in combo with the s.e. width.) The LOO comparison *probably* favors
inclusion of the new predictors, but with wide uncertainty.

Because the education coefficient's s.e. was so narrow, they try out 
interactions between education and local arsenic level, and find pretty
decent coefficient estimates for them.  They then repeat the interpretation
routine for these two interaction coefficients.  (The inputs have all been
centered.)  When they compare this model, with education plus two education
interactions, to one that omits education level, they definitely find
improvement in LOO scores.

### 14.3, Predictive simulation

They fit a simpler arsenic well switch model, just based on distance to the
nearest clean well, and reach into the individual coefficient samples to
produce (a) a graph of a few random curves implied by some of the coefficient
pairs, (b) predictions on ten new subjects, which can be aggregated across the
4,000 simulations into single probability-of-switching estimates.

### 14.4, Average predictive comparisons on the probability scale

TK

### 14.5, Residuals for discrete-data regression

TK

### 14.6, Identification and separation

TK


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer