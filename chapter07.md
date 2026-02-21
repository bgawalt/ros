# Chapter 7: Linear regression with a single predictor

[(Return to README)](./README.md)

The book introduces the "simple (but not trivial)" case of univariate
regression.

## Subsection rundown

### 7.1, Example: predicting presidential vote share from the economy

We kick off with a univariate predictor of using economic growth to predict
presidential election vote share.  The prose is a bit vague about what's being
modeled, but its very first lines say "look at Figure 7.1," which does clear
everything up.

"\[W\]hat is impressive here is that this simple model does pretty well."

*  Note about the data: it covers US presidential elections from 1952 to 2012,
    sixteen data in total.
*  "To fit a line with zero intercept, y = bx, use the expression,
    `stan_glm(vote ~ -1 + growth)`; the -1 tells R to exclude the intercept or
    constant term from the fit."  This is not a great DSL!!  You have to learn
    it with folklore about the magic sigils that mean things like "no
    intercept".
*  "The interval is well separated from zero, indicating that, if the data had
    been generated from a model whose true slope is 0, it would be very unlikely
    to get an estimated slope coefficient this large."  That's impressive for
    only 16 elections.
*  On the other hand, "the linear model predicts the election outcome to within
    about 3.9 percentage points. Roughly 68% of the outcomes will fall between
    $\pm 3.9$ of the fitted line."
*  The "72% chance Clinton wins in 2016" prediction is just about where 538 was
    at the time.  Figure 7.3:

![A bell curve centered at 52.3 with standard deviation 3.9, it's mass
mostly between 45 and 60.  The x-axis of this probability mass function plot is
labeled "Clinton share of the two-party vote."  The area under the curve
starting from 50% and heading right is shaded grey and labeled "Predicted 72%
chance of Clinton victory."](./fig/fig07_3.png)

*  "Why not instead use the economic data to directly predict who wins the
    election?"
    *  dasf
    *  sdf

### 7.2, Checking the model-fitting procedure using fake-data simulation

TK

### 7.3, Formulating comparisons as regression models

TK

## Exercises

Plots and computation powered by [Chapter07.ipynb](./notebooks/Chapter07.ipynb)

### 7.1, Regression predictors

> In the election forecasting example of Section 7.1, we used inflation adjusted
> growth in average personal income as a predictor. From the standpoint of
> economics, it makes sense to adjust for inflation here. But suppose the model
> had used growth in average personal income, not adjusting for inflation. How
> would this have changed the resulting regression? How would this change have
> affected the fit and interpretation of the results?

TK

### 7.2, Fake-data simulation and regression

> Simulate 100 data points from the linear model, $y = a + bx + \text{error}$,
> with $a = 5$, $b = 7$, the values of x being sampled at random from a uniform
> distribution on the range [0, 50], and errors that are normally distributed
> with mean 0 and standard deviation 3.
>
> (a) Fit a regression line to these data and display the output.
> (b) Graph a scatterplot of the data and the regression line.
> (c) Use the text function in R to add the formula of the fitted line to the graph.

TK

### 7.3, Fake-data simulation and fitting the wrong model

> Simulate 100 data points from the model, $y = a + bx + cx^2 + \text{error}$,
> with the values of x being sampled at random from a uniform distribution on
> the range [0, 50], errors that are normally distributed with mean 0 and
> standard deviation 3, and $a$, $b$, $c$ chosen so that a scatterplot of the
> data shows a clear nonlinear curve.
>
> (a) Fit a regression line `stan_glm(y ~ x)` to these data and display the
> output.
>
> (b) Graph a scatterplot of the data and the regression line. This is the
> best-fit linear regression. What does “best-fit” mean in this context?

TK

### 7.4, Prediction

> Following the template of Section 7.1, find data in which one variable can be
> used to predict the other, then fit a linear model and plot it along with the
> data, then display the fitted model and explain in words as on page 95. Use
> the model to obtain a probabilistic prediction for new data, and evaluate that
> prediction, as in the last part of Section 7.1.

TK

### 7.5, Convergence as sample size increases

> Set up a simulation study such as in Section 7.2, writing the entire
> simulation as a function, with one of the arguments being the number of data
> points, $n$. Compute the simulation for $n = $10, 30, 100, 300, 1000, 3000,
> 10 000, and 30 000, for each displaying the estimate and standard error.
> Graph these to show the increasing stability as $n$ increases.

TK

### 7.6, Formulating comparisons as regression models

> Take the election forecasting model and simplify it by creating a binary
> predictor defined as $x = 0$ if income growth is less than 2% and $x = 1$ if
> income growth is more than 2%.
>
> (a) Compute the difference in incumbent party’s vote share on average,
> comparing those two groups of elections, and determine the standard error for
> this difference.
>
> (b) Regress incumbent party’s vote share on the binary predictor of income
> growth and check that the resulting estimate and standard error are the same
> as above.

TK

### 7.7, Comparing simulated data to assumed parameter values

> (a) Simulate 100 data points from the model, $y = 2 + 3x + \text{error}$, with
> predictors x drawn from a uniform distribution from 0 to 20, and with
> independent errors drawn from the normal distribution with mean 0 and standard
> deviation 5. Save $x$ and $y$ into a data frame called `fake`. Fit the model,
> `stan_glm(y ~ x, data=fake)`. Plot the data and fitted regression line.
>
> (b) Check that the estimated coefficients from the fitted model are reasonably
> close to the assumed true values. What does “reasonably close” mean in this context?

TK

### 7.8, Sampling distribution

> Repeat the steps of the previous exercise 1000 times (omitting the plotting).
> Check that the coefficient estimates are approximately unbiased, that their
> standard deviations in the sampling distribution are approximately equal to
> their standard errors, and that approximately 95% of the estimate $\pm 2$
> standard error intervals contain the true parameter values.

TK

### 7.9, Interpretation of regressions

> Redo the election forecasting example of Section 7.1, but switching $x$ and 
> $y$, that is, predicting economic growth given the subsequent election
> outcome. Discuss the problems with giving a causal interpretation to the
> coefficients in this regression, and consider what this implies about any
> causal interpretations of the original regression fit in the chapter.

TK