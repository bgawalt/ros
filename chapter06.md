# Chapter 6: Background on regression modeling

[(Return to README)](./README.md)

"At a purely mathematical level," the book wants you to use regression for
prediction and/or comparison.  Comparison has a special case where you're
comparing treatment and control outcomes to estimate a causal effect.

## Subsection rundown

### 6.1, Regression models

Jargon check: in the "basic regression model" expression

$$y = a + bx + \text{error}$$

"The quantities $a$ and $b$ are *coefficients* or, more generally, *parameters*
of the model."

The book is going to focus on four extensions of that basic model:
additional predictors, nonlinear models (like log-transforming $y$ and $x$),
nonadditive models (e.g., you have a term for the product of two other
predictors), and generalized linear models (wrap the basic model in an
activation function).

This means *not* focusing on the listed extensions of nonparametric models,
multilevel models, and measurement error models.

### 6.2, Fitting a simple regression to fake data

Hm, ok. Is there a Python replacement that will work with their example usage
of `rstanarm`?  A short Google search suggests
[Bambi](https://github.com/bambinos/bambi).  But I dislike both Pandas and
the "`y ~ x`" way of describing models, so... we'll see what I go with.

(Looked it up: the `arm` in `rstanarm` is short for "applied regression
modeling.")

The section describes fitting a model to $(x, y)$ data where $x$ is the integers
1 through 20.  The output $y$ is:

$$y_i + 0.2 + 0.3x_i + \mathcal{N}(0, 0.5)$$

They report median and madsd numbers for their estimates of the slope and
intercept, as well as for the residual noise's standard deviation.  They also
plot the line of best fit on top of the twenty datapoints.

They note that their estimates are close to the original scalars they used to
generate the data, when you take into account the reported madsd uncertainties.

### 6.3, Interpret coefficients as comparisons, not effects

They fit a linear model predicting a person's income from their height and their
gender.  There's a lot of residual uncertainty; $R^2$ is 0.1.

They don't want to use the word "effect" when talking about the predictive
impact of height on income.  They want to save that word for situations where
there's a treatment or intervention driving the predictor's value.  In this
example, "what is observed is an observational pattern, that taller people in
the sample have higher earnings on average. These data allow between-person
comparisons, but to speak of effect of height is to reference a hypothetical
within-person comparison."

When doing those comparisons, they word it as:

*  "the average difference in earnings, comparing two people of the same sex but
    one inch different in height, is $600."
*  "when comparing two people with the same height but different sex, the man’s
    earnings will be, on average, $10 600 more than the woman’s in the fitted
    model."

### 6.4, Historical origins of regression

Lol, okay, this section opens with a literal "Webster's defines 'regression'
as...." 

One thing I'll say about this scatterplot from Galton about mother and daughter
heights:

![A scatterplot of Mother's Height (inches) on the x-axis and Adult Daughter's
Height (inches) on the y-axis.  There's a wide cloud of dots in the middle,
tilted up at about 45 degrees.  The regression model predictive line has a
noticeably shallower slope than that, more like 30 degrees
upward.](./fig/fig06_3.png)

That line of best fit is not what you'd get if you used principal component
analysis to find the direction in 2D space that captures most of the variance.
I don't know why or when we'd prefer one slope or the other (the PCA vs. the
OLS), though I guess it is encoded in the loss function used to train the model.
Galton illustrated this with this famous oval:

![Same mother-daughter chart axes, albeit in old timey 1900s style. There's an
oval drawn like you would for the original scatterplot's PCA/covariance, plus
lines for predicting mother from daughter, predicting daughter from mother, and
the actual major axis of the covariance
oval.](./fig/ch06_galton_smoothed_correlation.png)

### 6.5, The paradox of regression to the mean

They discuss how "regression to the mean" is a view on the general phenomenon
of a sort of conservation of variance.  If you disassemble the basic equation
$y = a + bx + \text{error}$,

*  If $b$ is less than one (as in the Galton heights case), then the $a + bx$
    predictions have less variance than the original $x$'s did...
*  ... but then you add in some variance from the error term, and so $y$ winds
    up with the same total variance as $x$.

With midsentence markup frome me:

> Regression to the mean thus will always arise in some form whenever
> predictions are imperfect in a stable environment.  The imperfection of the
> prediction [the error term in the basic equation -bg] induces variation, and
> regression in the point prediction [that $b$ be less than 1 -bg] is required
> in order to keep the total variation constant.

They break this down further in the fake-data scenario where student test
performance is based solely on their inherent talent, plus a noise factor.
If you predict final exam score from midterm exam score, you get regression to
the mean (you get a slope $b$ of 0.5).  By construction, there's no causal
effect here, even though the story lends itself to one:

> [A] student who scores very well on the midterm is likely to have been
> somewhat lucky and also to have a high level of skill, and so in the final
> exam it makes sense for the student to do better than the average but worse
> than on the midterm.

The skill effect is still there, but the luck is different every time.  So you
should guess that some of the observed input level will disappear in the output,
just by drawing a different luck/error term.  They warn you not to get fooled
by the "regression fallacy" which doesn't take this phenomenon into account.

They conclude by rephrasing the regression fallacy as a comparison against a
bogus alternative -- daughters should be the same height as their mothers,
final exam scores should exactly match midterm scores.

## Exercises

TK