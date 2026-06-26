# Chapter 22: Advanced regression and multilevel models

[(Return to README)](./README.md)

This is the speedrun introduction to regression beyond linear models.  This is
what I've been looking forward to since the first page, and one of the major
reasons I kicked off this readthrough.

## Subsection rundown

### 22.1, Expressing the models so far in a common framework

Like Chris Pine said in "Spider-Verse," let's do this one more time:

$$y = a + bx + \text{error}$$

Or, repeating that several more times:

$$y_i = a + bx_i + \epsilon_i;~~~\epsilon_i \sim \mathcal{N}(0, \sigma^2), \text{for}~ i = 1,\ldots,n$$
$$y_i \sim \mathcal{N}(a + bx_i, \sigma^2)$$
$$y \sim \mathcal{N}(a + bx, \sigma^2I)$$

Then we upgraded from univariate regression, to multivariate regression:

$$y \sim \mathcal{N}(X\beta, \sigma^2I)$$

They set up the jargon term $u_i = X_i\beta$, the point-estimate prediction for
the $i$th example for a given coefficient vector.

Nonlinearity is introduced by adding columns to $X$ that are just themselves
nonlinear function of the existing/original columns.  This has some limitations.
"One cannot, for example, use linear regression to estimate the parameter
$\beta_2$ in the model $y = \beta_0 + \beta_1\sin(\beta_2 x) + \text{error}$."

One nice thing to come out of this retrospective, and which I'd picked up on
from the last two chapters, is the subtle insistence that the
"$ + \text{error}$" does not start with *probabilistic* error.  That's the first
thing we introduced on top of it, but that's not actually part of their base
case.  It's certainly the assumption that I make, given all the work I've done
with these tools in the past, so it's good to think about what things would be
like without it.

### 22.2, Incomplete Data

Chapter 17's approach to missing data was "just take an educated guess at the
value," which they especially encourage for "cleaning up small amounts of
missingness."  But rather than using two distinct operations (fill in the
blanks, then fit a model to the filled-in data), you can structure the model so
that it can handle/adjust to/learn from those missing elements.

Examples:

#### Survival analysis

If you're looking at what factors are associated with time-to-event (e.g.,
patient dies, civil war breaks out), for many units, the data will have been
published before that event occurred for the unit.  Variants can also correct
for rounded data, or for some units having, e.g., the age attribute measured in
months while others measured in years.

#### Measurement ereror

In $y = a + bx + \text{error}$, measurement error of the outcome "folds right
into" the error term.  Measurement error of the predictor, $x$, though: we
observe $x^*$, a fuzzing of the real value, $x^* = x + \nu$ for some zero-mean
error term.  That means:

$$\begin{align}
    y &= a + bx* + \epsilon \\
      &= a + b(x - \nu) + \epsilon \\
      &= a + bx + (\epsilon - b\nu)
\end{align}$$

That new noise process is very much correlated with our regression predictor;
regressing $y$ on $x^*$ doesn't return an unbiased estimate of $b$.

Correcting for this bias requires knowing the variance of $\nu$.  You can also
use a procedure very similar to the two-step approach used for instrumental
variables in Section 21.2.

### 22.3, Correlated errors and multivariate models

A motivating example: consider a situation where the error terms behind
consecutive units $\{(y_{i-1}, x_{i-1}), (y_i, x_i)\}$ are *not*
independent/uncorrelated.  Think a time series of data, where the error term
values are "sticky" from one time instant to the next:

$$y_t = X_y\beta + \epsilon_t,~~~
\epsilon_t \sim \mathcal{N}\left(\rho\epsilon_{t-1}, (1 - \rho^2)\sigma^2\right)$$

(The delicate specification of $\{\epsilon_t\}$ is so that the marginal variance
of each error term is $\sigma$.)

This setup gives you a multivariate regression with a non-diagonal covariance
matrix:

$$y \sim \mathcal{N}(X\beta, \Sigma), ~~~\Sigma_{ij} = \rho^{|i - j|}\sigma^2$$

You'll now need a special solver (or Stan/PyMC spec) to estimate the parameters,
but this is not especially exotic or difficult to specify.

> Modeling and inference for more complicated time series, spatial, etc., models
> proceeds the same way, in that any linear dependence structure for normally
> distributed errors can be expressed as a multivariate normal distribution on
> the errors.

This leads to an interesting question, that I don't know the answer to: how easy
is it to handle *non*-normal errors, with *non*-linear dependence structure?
Linear combinations of normals are themselves normals, which is how we're
getting the convenient "it's just another multivariate regression" behavior
here.  Maybe Stan/PyMC really do make it about as straightforward as this case.

## 22.4, Regularization for models with many predictors

We know what happens if you include too few predictors in a model.  You lose
ignorability for your less-than-fully-randomized causal inference, or you
increase your effect's standard error in your fully-randomized causal inference.
Your missing data imputation loses accuracy.  Predictive accuracy of the model
itself suffers.

Going the other way, though -- too *many* predictors -- introduces instability,
at least if you're "using least squares, maximum likelihood, or Bayesian
inference with noninformative priors".

Just chucking out predictors altogether is high-bias; you're insisting up front
you know which predictors should have zero influence on the prediction.

Instead, the book calls back to Section 12.7, where we used priors to regularize
the coefficient estimates.  The regularized horseshoe prior, in particular, let
us directly specify "I don't think the final model should put serious weight on
more than six predictors."


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer