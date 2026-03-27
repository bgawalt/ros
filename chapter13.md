# Chapter 13: Logistic regression

[(Return to README)](./README.md)

This chapter introduces two modifications to the linear regressions run so far:
a mechanism for bounding predictions such that they lie between 0 and 1, and a
model framework that interprets those predictions as probabilities over some
this-or-that outcome pair.  These modifications are will make stuff covered so
far -- fitting models, interpreting coefficients -- a bit more complicated.

## Subsection rundown

### 13.1, Logistic regression with a single predictor

When fitting the logistic regression, `stan_glm` doesn't output a `sigma`
coefficient estimate, like it did for linear regression.  "Logistic regression
has no separate variance term; its uncertainty comes from its probabilistic
prediction of binary outcomes."  The $y$ value is itself the reflection of
uncertainty.

The model of the probability that $y = 1$ looks like:

$$\text{logit}(z) = \log\left(\frac{z}{1 - z}\right)$$

$$\text{logit}^{-1}(z) = \frac{e^z}{1 + e^z} = \frac{1}{1 + e^-z}$$

$$\text{Pr}(y_i = 1) = \text{logit}^{-1}(X_i\beta)$$

calling the $X\beta$ term the linear predictor.  The change in predicted
probability you get from a fixed increase in the linear prediction depends on
the starting probability.  They do the arithmetic around what happens when the
linear predictor increases by 0.4; going from 0 to 0.4 is a jump from 50% to 60%
but going from 2.2 to 2.6 is only a jump from 90% to 93%.

### 13.2, Interpreting logistic regression coefficients and the divide-by-4 rule

You can, just as a simple default, choose the mean predictors value as the
baseline from which you assess how a predictor affects the output probability.
Plug in $\bar{x}$, get a baseline probability of $y = 1$, then see how that
changes when you increase $x_i$ from its mean value to mean-plus-one-unit.

The steepest part of the inverse logit is at 0, where its slope is $\beta/4$ for
the univariate linear predictor $\alpha + \beta x$.  The upshot is if you divide
a coefficient by four, you get a sense of how much a unit increase in that
predictor moves the predicted probability off of 0.5.

They touch on the log-odds-ratio interpretation of the logistic regression,
which is how I first learned it.  I agree that "the concept of odds can be
somewhat difficult to understand, and odds ratios are even more obscure."
And multiplicative effects on odds ratios are weirdest of all.  It really is
easier to just think in terms of the inverse logit curve squashing the
weighted-sum of the linear predictor into the [0, 1] range.

While there's no `sigma` any more, we do still get standard errors for each
coefficient estimate.  They work like usual: any value within $\pm 2$ of the
mean estimate is consistent with the data.  Don't try and use them as a
statistical significance filter, though, for the usual reasons: it's acting as a
classifier of "real/not real effect" that's too error prone.  Soft decisions
like "do we have certainty in this estimate" are different than hard decisions
of "this estimate is right, that one is wrong."

### 13.3, Predictions and comparisons

TK

### 13.4, Latent-data formulation

TK

### 13.5, Maximum likelihood and Bayesian inference for logistic regression

TK

### 13.6, Cross validation and log score for logistic regression

TK

### 13.7, Building a logistic regression model: wells in Bangladesh

TK

## Exercises

Plots and computation powered by [Chapter13.ipynb](./notebooks/Chapter13.ipynb)

### 13.1, Fitting logistic regression to data

> The folder NES contains the survey data of presidential preference and income
> for the 1992 election analyzed in Section 13.1, along with other variables
> including sex, ethnicity, education, party identification, and political
> ideology.
>
> (a) Fit a logistic regression predicting support for Bush given all these
>     inputs. Consider how to include these as regression predictors and also
>     consider possible interactions.
>
> (b) Evaluate and compare the different models you have fit.
>
> (c) For your chosen model, discuss and compare the importance of each input
>     variable in the prediction.

TK

### 13.2, Sketching the logistic curve

> Sketch the following logistic regression curves with pen on paper:
>
> (a) $\text{Pr}(y = 1) = \text{logit}^{-1}(x)$
> 
> (b) $\text{Pr}(y = 1) = \text{logit}^{-1}(2 + x)$
> 
> (c) $\text{Pr}(y = 1) = \text{logit}^{-1}(2x)$
> 
> (d) $\text{Pr}(y = 1) = \text{logit}^{-1}(2 + 2x)$
> 
> (e) $\text{Pr}(y = 1) = \text{logit}^{-1}(-2x)$

TK

### 13.3, Understanding logistic regression coefficients

> In Chapter 7 we fit a model predicting incumbent party’s two-party vote
> percentage given economic growth: vote = 46.2 + 3.1 * growth + error, where
> growth ranges from -0.5 to 4.5 in the data, and errors are approximately
> normally distributed with mean 0 and standard deviation 3.8. Suppose instead
> we were to fit a logistic regression,
> $\text{Pr}(\text{vote} > 50) = \text{logit}^{-1}(a + b \times \text{growth})$.
> Approximately what are the estimates of $(a, b)$?
>
> Figure this out in four steps: (i) use the fitted linear regression model to
> estimate Pr(vote > 50) for different values of growth; (ii) second, plot these
> probabilities and draw a logistic curve through them; (iii) use the
> divide-by-4 rule to estimate the slope of the logistic regression model;
> (iv) use the point where the probability goes through 0.5 to deduce the
> intercept. Do all this using the above information, without downloading the
> data and fitting the model. 

TK

### 13.4, Logistic regression with two predictors

> The following logistic regression has been fit:

```
            Median MAD_SD
(Intercept) -1.9    0.6
x            0.7    0.8
z            0.7    0.5
```

> Here, $x$ is a continuous predictor ranging from 0 to 10, and $z$ is a binary
> predictor taking on the values 0 and 1. Display the fitted model as two curves
> on a graph of $\text{Pr}(y = 1)$ vs. $x$.

TK

### 13.5, Interpreting logistic regression coefficients

> Here is a fitted model from the Bangladesh analysis predicting whether a
> person with high-arsenic drinking water will switch wells, given the arsenic
> level in their existing well and the distance to the nearest safe well:

```
stan_glm(formula = switch ~ dist100 + arsenic, family=binomial(link="logit"), data=wells)
             Median MAD_SD
(Intercept)   0.00   0.08
dist100      -0.90   0.10
arsenic       0.46   0.04
```

> Compare two people who live the same distance from the nearest well but whose
> arsenic levels differ, with one person having an arsenic level of 0.5 and the
> other person having a level of 1.0. You will estimate how much more likely
> this second person is to switch wells. Give an approximate estimate, standard
> error, 50% interval, and 95% interval, using two different methods:
>
> (a) Use the divide-by-4 rule, based on the information from this regression
>     output.
>
> (b) Use predictive simulation from the fitted model in R, under the assumption
>     that these two people each live 50 meters from the nearest safe well.

TK

### 13.6, Interpreting logistic regression coefficient uncertainties

> In Section 14.2, there are two models, `fit_4` and `fit_5`, with distance and
> arsenic levels as predictors along with an interaction term.  The model
> `fit_5` differed by using centered predictors. Compare the reported
> uncertainty estimates (mad sd) for the coefficients, and use for example the
> `mcmc_pairs` function in the `bayesplot` package to examine the pairwise joint
> posterior distributions. Explain why the mad sd values are different for
> `fit_4` and `fit_5`.

TK

### 13.7, Graphing a fitted logistic regression

> We downloaded data with weight (in pounds) and age (in years) from a random
> sample of American adults. We then defined a new variable:

`heavy <- weight > 200`

> and fit a logistic regression, predicting heavy from height (in inches):

```
stan_glm(formula = heavy ~ height, family=binomial(link="logit"), data=health)

              Median MAD_SD
(Intercept)  -21.51   1.60
height         0.28   0.02
```

> (a) Graph the logistic regression curve (the probability that someone is
>     heavy) over the approximate range of the data. Be clear where the line
>     goes through the 50% probability point.
>
> (b) Fill in the blank: near the 50% point, comparing two people who differ by
>     one inch in height, you’ll expect a difference of __ in the probability of
>     being heavy.

TK

### 13.8, Linear transformations

> In the regression from the previous exercise, suppose you replaced height in
> inches by height in centimeters. What would then be the intercept and slope?

TK

### 13.9, The algebra of logistic regression with one predictor

> You are interested in how well the combined earnings of the parents in a
> child’s family predicts high school graduation. You are told that the
> probability a child graduates from high school is 27% for children whose
> parents earn no income and is 88% for children whose parents earn $60,000.
> Determine the logistic regression model that is consistent with this
> information. For simplicity, you may want to assume that income is measured in
> units of $10,000.

TK

### 13.10, Expressing a comparison of proportions as a logistic regression

> A randomized experiment is performed within a survey, and 1000 people are
> contacted. Half the people contacted are promised a $5 incentive to
> participate, and half are not promised an incentive. The result is a 50%
> response rate among the treated group and 40% response rate among the control
> group.
> 
> (a) Set up these results as data in R. From these data, fit a logistic
>     regression of response on the treatment indicator.
> 
> (b) Compare to the results from Exercise 4.1.

TK

### 13.11, Building a logistic regression model

> The folder Rodents contains data on rodents in a sample of New York City
> apartments.
>
> (a) Build a logistic regression model to predict the presence of rodents (the
>     variable `rodent2` in the dataset) given indicators for the ethnic groups
>     (race). Combine categories as appropriate. Discuss the estimated
>     coefficients in the model.
>
> (b) Add to your model some other potentially relevant predictors describing
>     the apartment, building, and community district. Build your model using
>     the general principles explained in Section 12.6. Discuss the coefficients
>     for the ethnicity indicators in your model.

TK

### 13.12, Fake-data simulation to evaluate a statistical procedure

> When can we get away with fitting linear regression to binary data? You will
> explore this question by simulating data from a logistic regression,
> then fitting a linear regression, then looping this procedure to compute the
> coverage of the estimates.
>
> (a) You will be simulating independent binary data, $y_i; i = 1, \ldots, n$,
>     from the model,
>     $\text{Pr}(y_i = 1) = \text{logit}^{-1}(a + bx_i + \theta z_i)$, where the
>     $x_i$’s are drawn uniformly from the range (0, 100) and the $z_i$’s are
>     randomly set to 0 or 1. The “cover story” here is that $y$ represents
>     passing or failing an exam, $x$ is the score on a pre-test, and $z$ is a
>     treatment.  To do this simulation, you will need to set true values of
>     $a$, $b$, and $\theta$. Choose $a$ and $b$ so that 60% of the students in
>     the control group will pass the exam, with the probability of passing
>     being 80% for students in the control group who scored 100 on the midterm.
>     Choose $\theta$ so that the average probability of passing increases by 10
>     percentage points under the treatment. Report your values for $a$, $b$,
>     $\theta$ and explain your reasoning (including simulation code). It’s
>     not enough just to guess.
> 
> (b) Simulate $n = 50$ data points from your model, and then fit a linear
>     regression of $y$ on $x$ and $z$. Look at the estimate and standard error
>     for the coefficient of $z$. Does the true average treatment effect fall
>     inside this interval?
>
> (c) Repeat your simulation in (b) 10,000 times. Compute the coverage of the
>     normal-theory 50% and 95% intervals (that is, the estimates $\pm0.67$ and
>     1.96 standard errors).

TK