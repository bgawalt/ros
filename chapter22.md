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

### 22.7, Nonparametric regression and machine learning

Nonparametric regression has no prespecified functional form for mapping the
predictors to the outcome.  These models can adapt arbitrarily well to any
data, limited just by the number of duplicate-predictor-value units.

To be of use, the nonparametric models need to avoid overfit (a term that is
only just now appearing in this book?!).  They come with some tuning parameters
that can require certain levels of smoothness.  Crossvalidation can help set
those tuning parameter values.

The crossover here between nonparametric regression and machine learning feels
mostly cultural.

#### Loess

This one's fun, because you can tune it in the limit to just fall back to
simple linear regression:

1.  Pick a tuning parameter, $f \in [0, 1]$, where values closer to 1 require
    more smoothness in the resulting functional form.  (A value of 1?  That's
    how you recover simple linear regression.)

2.  For each unit, fit a particular weighted linear regression based on the
    whole dataset.   (Call it "the main one".)   The weights for the regression
    decay with increasing distance of each unit from the main one.  A value of
    $f = 0$ ignores the other units entirely, and only fits the linear
    regression to the main one itself (or any duplicate-predictors lying on top
    of it).

They don't say how to *use* these $n$ weighted regressions, how to aggregate
them into a single predictor for new data.  Oh well.

#### Splines and Gaussian processes

For splines, you specify a set of $H$ basis functions, all of which are "locally
smooth."  These basis functions map predictors to outcome, and the overall
predictor for $x_{new}$ is just a weighted sum of the bases applied to
$x_{new}$.  The basis function family will make it clear what tuning parameters
are available.  The result looks very much like our "nonlinear predictor via
linear regression" hack, $y = \sum_{h=1}^N \beta_hb_h(x) + \text{error}$.

For Gaussian processes, the model looks like $y = g(x) + \text{error}$, where
$g(x)$ is a draw from a multivariate normal.  The correlation matrix of that
normal (i.e., its inverse covariance) has rows and columns corresponding to the
$n$ datapoints.  Element $(i, j)$ is a correlation value between 0 and 1, where
the exact value is a decreasing function of the distance between $x_i$ and
$x_j$.  The exact decay rates are the tuning parameters of the model.

They don't make it obvious how to use the Gaussian process model to make
predictions on new data.  Or even where $y_j$ enters the picture when fitting
the model.  They say that fitting the model will be slow, and I believe that's
because the sampling of $g(x)$ is going to involve the $O(n^3)$ operation of
inverting that correlation matrix.

#### Tree models and BART

Tree models are binary trees, where each non-leaf node has a split rule, and
each leaf provides a predicted value that's meant to match $\mathbb{E}[y | x]$.

A Bayesian additive regression tree (BART) is a sum over $J$ trees, with a prior
that sets guidance for how large a tree should be, and how varied/extreme its
leaf-values.  "The prior favors smaller trees and predictive components that are
near zero, thus keeping the fit smooth except to the extent that the data force
otherwise."

#### Machine learning meta-algorithms

Name checking a few other concepts, mostly with an eye towards how they can
wrap and aggregate several of the more-concrete models above.  Ensemble learning
(bagging and boosting, though they don't call it that) and genetic algorithms
get mentioned, and weirdly so does deep learning, despite it being a bad fit for
the category.

It closes by saying these are mostly about harnessing and learning from very
large amounts of data, to the point "that they can in practice require a large
sample to work well."  The reason the regression models from this book worked
on $n < 30$ datasets is the strict and minimal functional forms those linear
models induce.

### 22.8, Computational efficiency

They claim that the time it takes to fit a standard linear model is proportional
to the size of the data matrix, which, sure, 10 passes of stochastic gradient
descent will meet that claim.  The traditional method is more like $O(np^2)$,
for solving the normal equations of OLS.

They get into the computational aspects of `stan_glm`, which is based on
Hamiltonian Monte Carlo sampling.  In it, the sampler explores the
$D$-dimensional parameter space ($D = 3$ for the
$y \sim \mathcal{N}(a + bx, \sigma)$ univariate regression case) iteratively and
stochastically.

To check that the stochastic results are reliable, the fit is conducted
multiple times: multiple chains of iterative samples (usually four).  The
diagnostic read outs are

*  `Rhat`, the split-$\hat{R}$ convergence metric, comparing results from the
    different chains.  A value of 1 means converged; higher than 1 means the
    chains don't have great overlap yet in terms of which parts of the parameter
    space they've explored.

*  `n_eff`, the number of effective samples of each coefficient.  The iterative
    samples have some path dependence and drag.  Each sample is a function, in
    part, of the sample that came before.  So even though the default chain is
    4000 samples long, the number of effective samples depends on the 
    autocorrelation of the chain.

*  `mcse`, Monte Carlo standard error, additonal uncertainty you incur for each
    parameter by dint of using this stochastic approach.  It's "negligible in
    all the examples in this book."

Running the chains in parallel is a no-brainer way to speed things up.

And you can also ask `stan_glm` to just give you the mode of the posterior,
instead of exploring the whole space to get uncertainty estimates for each
coefficient or correlations between those coefficient samples.

> This optimization is as fast as maximum likelihood -- indeed, it can be
> faster, in that the prior distribution can make the optimization problem more
> stable -- and can be a good choice for problems where full Bayesian inference
> is too slow.

You do still get *some* uncertainty measurements from this mode-seeking use 
case, but the uncertainty ellipses are determined by approximating the posterior
mode with a multivariate normal distribution.


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### TK 22.1, Measurement error in $y$

> Simulate data $(x, y)_i, i = 1, \ldots, n$ from a linear regression model,
> $y = a + bx + \text{error}$, but suppose that the outcome $y$ is not observed
> directly, but instead we observe $v = y + \text{error}$, with independent
> measurement errors with mean zero.  Use simulations to understand the
> statistical properties of the observed-data regression of $v$ on $x$, compared
> to the desired regression of $y$ on $x$.

TODO

### TK 22.2, Measurement error in $x$

> Simulate data $(x, y)_i, i = 1, \ldots, n$ from a linear regression model,
> $y = a + bx + \text{error}$, but suppose that the predictor $x$ is not
> observed directly, but instead we observe $u = x + \text{error}$, with
> independent measurement errors with mean zero.  Use simulations to understand
> the statistical properties of the observed-data regression of $y$ on $u$,
> compared to the desired regression of $y$ on $x$.

TODO

### TK 22.3, Nonlinear modeling

> The folder `Golf` contains the dataset used in Section 22.6 and also an
> additional, larger dataset on golf putting, including putts of up to 75 feet
> in length.
>
> (a) Fit the two models in Section 22.6 to this new data.  Display the data and
>     fitted models, and comment on the fit.
>
> (b) Expand the geometry-based model to allow for the possibility that the putt
>     can be hit too short or too long. Tinker with the model as necessary to
>     get a reasonable fit to the larger dataset.

TODO

### TK 22.4, Nonlinear modeling

> In the absence of air resistance, a falling object has acceleration equal to
> the gravitational constant $g$, and so a dropped object will fall a distance
> $\frac{1}{2}gt^2$ during time $t$.
>
> For this exercise you will conduct an experiment to estimate the gravitational
> constant.  Using a yardstick, mark a set of heights on a wall, for example,
> 3, 4, 5, 6, and 7 feet off the ground.  At each height, drop a ball twice and
> measure the time it takes to fall.  Using these data and a measurement error
> model, fit a model in Stan to estimate $g$.

TODO

### TK 22.5, Smoothing and sample size

> Take a random sample of 1/10 of the data from the `Gay` folder and re-fit the
> loess and spline models to estimate the support for same-sex marriage and
> percentage of people who say they know at least one gay person.  Compare to
> the estimates from the full data shown in Figure 22.6.

TODO

### TK 22.6, Smoothing and sample size

> Repeating the previous exercise with different fractions of data subsampled,
> explore the behavior of loess and splines at their default settings as a
> function of sample size.

TODO

### TK 22.7, Nonparametric modeling of a continuous outcome

> Find data of interest to you with a continuous outcome and one continuous
> predictor and at least 100 data points.  Fit loess, spline, and BART and plot
> these along with the data. Discuss how these fitted models differ.  If the
> three fits are essentially identical, add some new (fake) points to the
> dataset to create differences between the three fitted models.

TODO 

### TK 22.8, Nonparametric modeling of a binary outcome

> Repeat the previous exercise, but with a binary outcome.  This could be a
> different example or simply a discretized version of the outcome variable in
> the previous exercise, as long as the discretization is of substantive
> interest and is not just an arbitrary cutpoint.

TODO

### TK 22.9, Visualizing a fitted nonparametric model in multiple dimensions

> Find data of interest to you with a continuous outcome and two continuous
> predictors and at least 100 data points.  Fit loess, spline, and BART.
> Consider different displays of the data and fitted model, such as
> three-dimensional plots or separate plots of $y$ vs. $x_1$ and $y$ vs. $x_2$.

TODO

### TK 22.10, Computational efficiency

> Perform fake-data experiments to study the speed of optimization and full
> Bayesian inference for logistic regression, following the example at the end
> of Section 22.8.  Make a graph on the log-log scale showing compute time as a
> function of sample size for a fixed number of predictors.

TODO