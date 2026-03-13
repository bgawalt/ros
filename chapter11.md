# Chapter 11: Assumptions, diagnostics, and model evaluation

[(Return to README)](./README.md)

## Subsection rundown

### 11.1, Assumptions of regression analysis

TK

### 11.2, Plotting the data and fitted model

TK

### 11.3, Residual plots

TK

### 11.4, Comparing data to replications from a fitted model

TK

### 11.5, Example: predictive simulation to check the fit of a time-series model

TK

### 11.6, Residual standard deviation σ and explained variance $R^2$

TK

### 11.7, External validation: checking fitted model on new data

TK

### 11.8, Cross validation

TK

## Exercises

Plots and computation powered by [Chapter11.ipynb](./notebooks/Chapter11.ipynb)

### 11.1, Assumptions of the regression model

> For the model in Section 7.1 predicting presidential vote share from the
> economy, discuss each of the assumptions in the numbered list in Section 11.1.
> For each assumption, state where it is made (implicitly or explicitly) in the
> model, whether it seems reasonable, and how you might address violations of
> the assumptions.

TK

### 11.2, Descriptive and causal inference

> (a) For the model in Section 7.1 predicting presidential vote share from the
>     economy, describe the coefficient for economic growth in purely
>     descriptive, non-causal terms.
>
> (b) Explain the difficulties of interpreting that coefficient as the effect of
>     economic growth on the incumbent party’s vote share.

TK

### 11.3, Coverage of confidence intervals: Consider the following procedure:

> *  Set $n = 100$ and draw n continuous values $x_i$ uniformly distributed
>    between 0 and 10. Then simulate data from the model
>    $y_i = a + bx_i + \text{error}_i$, for $i = 1, \ldots, n$, with $a = 2$,
>    $b = 3$, and independent errors from a normal distribution.
>
> *  Regress $y$ on $x$. Look at the median and mad sd of $b$. Check to see if
>    the interval formed by the median $\pm 2$ mad sd includes the true value,
>    $b = 3$.
> *  Repeat the above two steps 1000 times.
>
> (a) True or false: the interval should contain the true value approximately
>     950 times. Explain your answer.
>
> (b) Same as above, except the error distribution is bimodal, not normal. True
>     or false: the interval should contain the true value approximately 950
>     times. Explain your answer.

TK

### 11.4, Interpreting residual plots

> Anna takes continuous data $x_1$ and binary data $x_2$, creates fake data
> $y$ from the model, $y = a + b_1x_1 + b_2x_2 + b_3x_1x_2 + \text{error}$, and
> gives these data to Barb, who, not knowing how the data were constructed, fits
> a linear regression predicting $y$ from $x_1$ and $x_2$ but without the
> interaction. In these data, Barb makes a residual plot of $y$ vs. $x_1$, using
> dots and circles to display points with $x_2 = 0$ and $x_2 = 1$, respectively.
> The residual plot indicates to Barb that she should fit the interaction model.
> Sketch with pen on paper a residual plot that Barb could have seen after
> fitting the regression without interaction.

TK

### 11.5, Residuals and predictions

> The folder `Pyth` contains outcome $y$ and predictors $x_1, x_2$ for 40 data
> points, with a further 20 points with the predictors but no observed outcome.
> Save the file to your working directory, then read it into R using
> `read.table()`.
>
> (a) Use R to fit a linear regression model predicting $y$ from $x_1, x_2$,
>     using the first 40 data points in the file. Summarize the inferences and
>     check the fit of your model.
>
> (b) Display the estimated model graphically as in Figure 11.2.
>
> (c) Make a residual plot for this model. Do the assumptions appear to be met?
>
> (d) Make predictions for the remaining 20 data points in the file. How
>     confident do you feel about these predictions?
>
> After doing this exercise, take a look at Gelman and Nolan (2017, section
> 10.4) to see where these data came from.

TK

### 11.6, Fitting a wrong model

> Suppose you have 100 data points that arose from the following model:
> $y = 3 + 0.1 x_1 + 0.5 x_2 + \text{error}$, with independent errors drawn from
> a $t$ distribution with mean 0, scale 5, and 4 degrees of freedom. We shall
> explore the implications of fitting a standard linear regression to these
> data.
>
> (a) Simulate data from this model. For simplicity, suppose the values of $x_1$
>     are simply the integers from 1 to 100, and that the values of $x_2$ are
>     random and equally likely to be 0 or 1. In R, you can define
>     `x_1 <- 1:100`, simulate `x_2` using `rbinom`, then create the linear
>     predictor, and finally simulate the random errors in `y` using the `rt`
>     function. Fit a linear regression (with normal errors) to these data and
>     see if the 68% confidence intervals for the regression coefficients (for
>     each, the estimates $\pm 1$ standard error) cover the true values.
>
> (b) Put the above step in a loop and repeat 1000 times. Calculate the
>     confidence coverage for the 68% intervals for each of the three
>     coefficients in the model.

TK

### 11.7, Correlation and explained variance

> In a least squares regression with one predictor, show that $R^2$ equals the
> square of the correlation between $x$ and $y$.

TK

### 11.8, Using simulation to check the fit of a time-series model

> Find time-series data and fit a first-order autoregression model to it. Then
> use predictive simulation to check the fit of this model as in Section 11.5.

TK

### 11.9, Leave-one-out cross validation

> Use LOO to compare different models fit to the beauty and teaching evaluations 
> example from Exercise 10.6:
>
> (a) Discuss the LOO results for the different models and what this implies, or
>     should imply, for model choice in this example.
>
> (b) Compare predictive errors pointwise. Are there some data points that have
>     high predictive errors for all the fitted models?

TK

### 11.10, K-fold cross validation

> Repeat part (a) of the previous example, but using 5-fold cross validation:
>
> (a) Randomly partition the data into five parts using the `sample` function in
>     R.
>
> (b) For each part, re-fitting the model excluding that part, then use each
>     fitted model to predict the outcomes for the left-out part, and compute
>     the sum of squared errors for the prediction.
>
> (c) For each model, add up the sum of squared errors for the five steps in
>     (b). Compare the different models based on this fit.

TK