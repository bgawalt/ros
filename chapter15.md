# Chapter 15: Other generalized linear models

[(Return to README)](./README.md)

This chapter kicks off with the term of art *link function.*  Just like the
inverse logit turned a weighted sum into $\text{Pr}(y = 1)$, link functions can
perform similar warps to predict "bounded or discrete data of different forms."

## Subsection rundown

### 15.1, Definition and notation

Four necessary ingredients, plus a set of optional ones, behind any generalized
linear model:

1.  Vector of outcome data, $y = (y_1, \ldots, y_n)$

2.  Matrix of predictors (one observation per row, one predictor per column) $X$
    and a vector of coefficients $\beta$, forming a linear predictor vector
    $X\beta$

3.  A link function $g$, yielding a vector of transformed data
    $\hat{y} = \text{E}(y | X, \beta) = g^{-1}(X\beta)$

4.  A data distribution, $\text{Pr}(y | \hat{y})$

5.  (Optional) other parameters like variances, overdispersions, and cutpoints,
    that apply to any of the above four ingredients

Some examples, byeond the linear and logistic regressions we've run so far:

*  **Poisson:** each outcome is a non-negative integer.  The link function is
    the logarithm, so $g^{-1}(z) = \exp(z)$.
*  **Negative binomial:** same outcomes and link function as Poisson regression, 
    but with an extra parameter to describe overdispersion, "variation in the 
    data beyond what would be predicted from the Poisson distribution alone."
*  **Logistic-binomial:** outcome $y_i$ is the number of successes observed
    out of $n_i$ attempts.  (They apologize for overloading $n_i$, number of
    tries for observation $i$, and $n$, the number of observations.)
    The link function is the logit, and the data distribution is the binomial.
*  **Beta-binomial:** Like logistic-binomial, but with an overdispersion
    parameter.
*  **Probit:** Like logistic regression, but replace the logit link function
    with the normal distribution's CDF.
*  **Multinomial logit/probit:** Extend the binary outcomes of logistic/probit
    models to categorical outcome.  These can be ordered or unordered
    categories.
*  **Robust:** the data distribution is given fatter tails than the usual
    normal distribution of the logistic regression.  The $t$ distribution is
    common here.

### 15.2, Poisson and negative binomial regression

#### Poisson model

The model:

$$y_i \sim \text{Poisson}\left(e^{X_i\beta}\right)$$

"The linear predictor $X_i\beta$ is the logarithm of the expected value of
measurement $y_i$." You should expect variation in the outcomes on the order of
$\sqrt{\text{E}(y)}$.

#### Overdispersion and underdispersion

If you look at your actual outcomes relative to the Poisson regression central
trend plus-or-minus that $\sqrt{\text{E}(y)}$ standard error, and see a bunch
of "outliers", you probably have overdispersion.  (Or, rarely, you see a 
too-tight clustering around the central trend, and you have underdispersion).

#### Negative binomial model for overdisperson

They don't go into the probability distribution or its sampling procedure, but,
they talk about how the negative binomial model brings in a reciprocal
dispersion parameter, $\phi > 0$, to set:

$$\text{sd}(y | x) = \sqrt{\text{E}(y | x) + \text{E}(y | x)^2/\phi}$$

As $\phi$ increases, we recover the original Poisson model.

#### Interpreting Poisson or negative binomial regression coefficients

The $X\beta$ linear predictor is being exponentiated, so $e^{\beta_j}$ gives you
the multiplicative effect on the expected change in $y_i$ when $x_i$ has a unit
increase in its $j$th predictor.

#### Exposure

Let's introduce the per-observation term $u_i$ to be the *exposure* of
observation $i$.  If we're observing count data, it can be useful to note the
absolute max value the count could have been: if you're modeling traffic
accidents at intersections as a function of intersection attribute, it can be
useful to use "number if cars that pass through the intersection" as that
intersection's exposure attribute.

$$y_i \sim \text{negative binomial}(u_i\theta_i, \phi),~~ \theta_i = e^{X_i\beta}$$

The equivalent term is *offset*, meaning, $\log(u_i)$.  The upshot is that
the $\beta$ coefficients now reflect change in outcomes per exposure unit per 
unit of predictor, rather than just outcomes per unit of predictor.

#### Including log(exposure) as a predictor in a Poisson or negative binomial regression

You can always just shove $\log(u_i)$ into one more column of $X$, and either
(a) force its coefficient to be 1, or (b) learn its coefficient value just like
any other predictor.  The float of (b) can make interpreting the other 
coefficients harder, but, it *could* allow for a better fit of model to data.

#### Differences between the binomial and Poisson or negative binomial models

If you have a natural limit on your outcomes, use a binomial model (which, when
$n_i = 1 \forall i$, is the logistic), and add overdispersion if needed.  
Otherwise, when the outcomes have no upper bound, use the log link function of
Poisson/negative binomial.  Though if the limit is much, much larger (like,
many orders of magnitude) than the expected outcome, you can use Poisson in that
case, too.

#### Example: zeroes in count data

A good way to check whether your estimated level of overdispersion matches the
data is to count zeros in the actual and predicted data.  Their example
(counting trapped roaches in apartments, where each apartment has an exposure
value of "number of days the traps were out") shows how Poisson regression does
bad on this front, but the negative binomial regression does okay.  (The NB
estimates many 1,000+ and even 1,000,000+ roach apartments, which never comes
close to being observed in the data.)

### 15.3, Logistic-binomial model

If you have many observations with identical predictors, all with binary
outcomes, you can bundle the identical-groups together as binomial outcomes
$y_i = k$ from $n_i$ trials.

The binomial distribution (like the Poisson) locks you into a strict
relationship between the mean and the variance.  They lay out a chi-squared test
you can use to see if the following standardized residuals:

$$\begin{align}
    z_i &= \frac{y_i - \hat{y}_i}{\text{sd}(\hat{y}_i)} \\
        &= \frac{y_i - \hat{y}_i}{\sqrt{n_i\hat{p}_i(1 - \hat{p}_i)}}
\end{align}$$

are distributed like a normal with zero mean and unit var  Teiance.

If they *aren't* distributed like a standard normal, then you have
overdispersion (or, very rarely, underdispersion).

They talk about how you can translate the binomial model's data matrix into
a binary logistic model instead, but, they then leave out what to do about
overdispersion in that case.  We had overdispersion in the count-data model,
and yet when we translate it to the equivalent binary-data model, the problem...
goes away?  They say, "Overdispersion at the level of the individual data points 
cannot occur in the binary model, which is why we did not introduce
overdispersed models in those earlier chapters."  But they don't talk about
what's eating the overdispersion sin by moving count data to binary data.

### 15.4, Probit regression: normally distributed latent data

Take the logistic regression model, and then swap the logistic distribution
for a normal distribution:

$$\text{Pr}(y_i = 1) = \Phi(X_i\beta)$$

or, in latent variable mode:

$$\begin{align}
    y_i &= \left\{\begin{align*}
        ~1 & ~\text{if}~z_i > 0 \\
        ~0 & ~\text{if}~z_i < 0,
    \end{align*}\right. \\
    z_i &= X_i\beta + \epsilon_i, \\
    \epsilon_i &\sim \mathcal{N}(0, 1),
\end{align}$$

where we freeze the variance of the $\epsilon$ RVs for identifiability.  (As
in Chapter 13, you can just scale that variance up and down alongside $\beta$
and get equivalent fits).

This has basically no effect on coefficient estimates w.r.t. using the logistic
instead, up to a 1.6x scaling factor.  There's... no reason to use it?

### 15.5, Ordered and unordered categorical regression

For $K$ ordered categorical outcomes, you can introduce coefficients
$c_j, j = 1, \ldots, K-1$ with the relationship:

$$\text{Pr}(y > j) = \text{logit}^{-1}(X\beta - c_j)$$

with $c_1 = 0$ frozen for the sake of identifiability.  These $c_j$ represent
cutpoints, defining boundaries between the $K$ ordinal-categorical zones claimed
over the linear predictor range.  The cutpoints are constrained to be strictly
increasing in $j$.

There are lots of ways to reparametrize this, especially in the univariate case.

And there are lots of ways to approach the problem other than the ordinal
logistic they fit as their example.  Use probit as the noise model instead of
logit.  Fit a linear regression, especially if $K$ is large and mostly high
entropy.  Fit a bunch of nested/sequential binary logistic regressions, one for
each this-category-or-higher cutoff.

The chapter ends by basically punting on what to do if you have *un*ordered
categorical outcomes.  They recommend fitting one model per category (which
definitely throws out information).

### 15.6, Robust regression using the $t$ model

The $t$ distribution's heavier tails means that coefficient estimates are less
sensitive to large-error observations, when used in a linear regression setting.

The logistric regression model can be swapped for the robit model, where the
noise applied to the linear predictor is a $t$ distribution with $\nu$ degrees
of freedom (and scaled so that it has unit variance;
$\epsilon_i \sim t_\nu(0, \sqrt{(\nu - 2)/\nu})$).  This allows for crazy Ivans,
where data can flip from 1 to 0 or vice versa no matter how far along the
central trend the predictors lie.

Robit regression leads to sharper sigmoids than the logistic model, since it
is happier to disregard the wacky outlier bitflips that the logistic model needs
to accommodate:

![From the book, Figure 15.7, whose caption reads "Hypothetical data to be
fitted using logistic regression: (a) a dataset with an “outlier” (the
unexpected y = 1 value near the upper left); (b) data simulated from a logistic
regression model, with no outliers. In each plot, the dotted and solid lines
show the fitted logit and robit regressions, respectively. In each case, the
robit line is steeper—especially for the contaminated data—because it
effectively downweights the influence of points that do not appear to fit the 
model](./fig/part3/fig15_07_robit.png)

Turns out robit and probit are linked: taking $\nu$ to infinity recovers the
probit model, and any value above $\nu = 7$ is basically indistinguishable from
probit.

### 15.7, Constructive choice models

They now repose the exact same regression operation (map input predictors to
output outcomes) as balancing incentives to reach a decision.  The version of
regression we've used so far is "a descriptive tool" for linking the outcome
and predictor variables.  They introduce here the choice model.

To build a choice model, you specify a value function, which defines a
particular preference value for each possible decision.  By convention, true
indifference to a decision option means the value function returns zero.
The value function considers both the decision option, plus the predictor terms
that describe the decider's situation at the time of the decision.

They look at the arsenic-well dataset again, and run a univariate regression to
predict "switched?" from "distance to nearest clean well (units: 100 m)".
The choice model gives every observed subject a triplet of random varaibles,
$(a_i, b_i, c_i)$ that determine:

*  $a_i$, the benefit of switching from an unsafe well to a safe one
*  $b_i + c_ix_i$, the cost of switching to a well $x_i$ distance away

They then say that $y_i = 1$, a switch for subject $i$, is dependent on those
random variables turning out the right way:

$$\text{Pr}(y_i = 1) = \text{Pr}(a_i > b_i + c_ix_i) = \text{Pr}\left(\frac{a_i - b_i}{c_i} > x_i\right)$$

If you define $d_i = (a_i - b_i)/c_i$, then you recover logistic regression if
the $d_i$ all follow a logistic distribution, and probit regression if they all
follow a normal distribution.  You never get to actually observe the RV triples
$(a_i, b_i, c_i)$ for subject $i$, only $(x_i, y_i)$.

This extends to multiple dimensions, and again, certain lucky breaks on how the
latent RVs are distributed means the model can recover familiar forms like
logistic or probit regression.

Fitting these requires more complicated software than the book is prepared to
introduce.

## 15.8, Going beyond generalized linear models

TK


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer