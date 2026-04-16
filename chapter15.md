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

$$begin{align}
    z_i &= \frac{y_i - \hat{y}_i}{\text{sd}(\hat{y}_i)} \
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

## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer