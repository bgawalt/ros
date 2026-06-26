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

### 22.4, Regularization for models with many predictors

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

### 22.5, Multilevel or hierarchical models

Often, units can be bundled together, and often those bundles can themselves be
bundled.  This gets called multilevel or hierarchical modeling.  It's been
name-checked a lot in earlier chapters as a useful tool!

Examples of hierarchical data:

*  **Nested:**
    *  a test score from each student, a school for each student, a district for
        each school, a state for each district
    *  a district for each likely voter, a state for each district
*  **Non-nested:**
    *  a test score from each student, who has a grade level, and a school
    *  a vote-share outcome for each election, each of which takes place in a
        certain state and in a certain year

If you have lots of data, you can just fit this kind of structure directly,

```
y ~ x + factor(state) + x:factor(state)
```

If you have low data volumes, though, you'll need to partially pool coefficient
estimates.  Stabilize your coefficient estimates for any one state by assuming
that state's coefficents are at least somewhat similar to the coefficients for
the other 49 states.

I don't know how non-nested pooling should work, if you have interactions
between group indicators.  If I want to regularize my estimates for Wyoming in
1996, how much should I make (Wyoming, 1996) look like every other state in
1996, vs. make it look like Wyoming in every other year?  And how do I specify
that, in Stan/PyMC?

### 22.6, Nonlinear models, a demonstration using Stan

Linear modeling, we've got on lock.  Our approach to nonlinear modeling, though,
has been kind of hack: you just define a new predictor as nonlinear transform
on one or more initial predictors, then rerun the linear modeling playbook.
But not every nonlinear transformation can be addressed this way, like we posed
with the model above, $y = \beta_1\sin(\beta_2x) + \text{error}$.  "Such models
can be fit with maximum likelihood or Bayesian methods using Stan."

The example model they fit: a set of about 6,000 golf puts at various distances,
rounded to the nearest foot, giving a set of $(n, x, y)$ triples, for $x$ as
distance and $y$ being the number sunk.  There's $J$ such triples.

To fit a logistic regression to this, or really any, univariate data, your Stan
spec looks like:

```
data {
  int J;
  int n[J];
  vector[J] x;
  int y[J];
}
parameters {
  real a;
  real b;
}
model {
  y ~ binomial_logit(n, a + b*x);
}
```

The resulting estimates for `a ` and `b` wind up with narrow credible intervals.

That's the linear model.  This section is about *non*linear model.  They build
one up from first principles:

1.  Every ball is hit towards the hole, at some angle.  That angle has zero mean
    (i.e., dead on target) and some standard deviation $\sigma$.  The golfer
    never hits the ball too hard or too soft given the distance, it's strictly
    about getting the angle right.  Call that noisy angle a normal RV.
2.  The ball is of radius $r$ (1.68 inches) and the hole is of radius $R$ (4.25
    inches).
3.  For the ball to land in the hole, the entire ball must land within the
    radius $R$.  That means the angle must be sufficiently shallow that the
    angle is less than $\sin^{-1}\left((R - r) / x\right)$.  (I don't know why
    it's not enough for the center of the ball to pass over the $R$-hole, but
    "the whole ball lands in the hole" is the way they went here.)
4.  If the angle is a normal $\mathcal{N}(0, \sigma)$, you can back out the
    probability of landing in the hole as
    $2\Phi\left(\sin^{-1}\left(\frac{R - r}{x}\right) / \sigma\right)$ - 1.

That $\sigma$ parameter is the only one to fit in this model.  (The logistic
regression had two, slope and intercept.)  In Stan, this looks like:

```
data {
  int J;
  int n[J];
  vector[J] x;
  int y[J];
  real r;
  real R;
}
parameters {
  real<lower=0> sigma;
}
model {
  vector[J] p = 2*Phi(asin((R-r) ./ x) / sigma) - 1;
  y ~ binomial(n, p);
}
```

The model is fit, and the result is a very narrow band around 1.5 degrees for
$\sigma$.

For goodness-of-fit checking, they superimpose each model over the data:

![Figure 22.4 Logistic regression and custom geometry-based model fit to the
golf-putting data. The custom model fits better, which is particularly
impressive, given that it contains only one parameter and the logistic
regression has two.](./fig/part6/fig22_6_golf.png)

Without putting any numbers to it, they declare that the nonlinear model "fits
the data much better."

## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer