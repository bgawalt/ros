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

TK

## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer