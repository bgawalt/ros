# Chapter 10: Linear regression with multiple predictors

[(Return to README)](./README.md)

Three challenges of moving to multiple-predictor models:

1.  what predictors to include/omit,
2.  how to interpret the fit coefficient values and their interdependencies,
3.  constructing new predictors from an existing set to capture nonlinearity.

## Subsection rundown

### 10.1, Adding predictors to a model

I get that they've pushed it into the next chapter, but it's interesting that
they talk about using the single binary predictor to predict kid IQ, and then
using the single continuous predictor, and in neither case provide a sense of
how good a job the model is doing.  When they do combine the two into a model
that leverages both predictors, they *do* include median and mad sd for the
$\sigma$ error parameter.  (It's also a bit unfortunate that the coefficients
are the same whether the predictor is used in the univariate or the multivariate
model.)

### 10.2, Interpreting regression coefficients

"Change predictor $k$ while leaving the others constant" doesn't work when
"the others" are linked to $k$; in their examples, where you have some
predictors that are polynomials over other predictors.

They fall back to first principles on interpreting coefficients:

1.  *Predictive interpretation:* the coefficient $\beta_k$ tells you how much to
    expect the average output to change between two groups that differ by one
    unit in predictor $k$, while holding all other predictors constant.
2.  *Counterfactual interpretation:* the causal inference case, where you're
    saying "if I changed predictor $k$ to be one unit higher in this individual,
    I should expect the output for this individual to be $\beta_k$ higher."

They say be careful with the counterfactual interpretation; don't even use the
common gentler rewording of "a change in $k$ is associated with a $\beta_k$
change in $y$":

> From the data alone, a regression only tells us about comparisons between
> units, not about changes within units.

Taking this seriously means you have to use the word "comparing" when describing
what $\beta_k$ means, in a much longer sentence than you want to have to use.

> \[Our guidelines prescribe\] an awkward way to put things, which helps explain
> why people often prefer simpler formulations such as “a change of 1 in $x_k$
> causes, or is associated with, a change of $\beta_k$ in $y$”—but those sorts
> of expressions can be terribly misleading. You just have to accept that
> regression, while a powerful data-analytic tool, can be difficult to
> interpret.

### 10.3, Interactions

By their notation, an interaction is like `height:weight`, which means

`y ~ height:weight`

translates to a model of

$$y = \beta_0 + \beta_1 * \text{height} * \text{weight} + \text{error}$$

Their example is more typical, where the individual predictors are included as
well as their interaction.  And since one of their predictors is binary, the
result is like fitting two univariate regressions on the two subsets of the
data, split on the binary variable value.

Their advice for looking for interaction candidates: "the first place we
typically look for them is with predictors that have large coefficients when
not interacted."

### 10.4, Indicator variables

TK

### 10.5, Formulating paired or blocked designs as a regression problem

TK

### 10.6, Example: uncertainty in predicting congressional elections

TK

### 10.7, Mathematical notation and statistical inference

TK

### 10.8, Weighted regression

TK

### 10.9, Fitting the same model to many datasets

TK

## Exercises

Plots and computation powered by [Chapter10.ipynb](./notebooks/Chapter10.ipynb)

### 10.1, Regression with interactions

> Simulate 100 data points from the model,
> $y = b_0 + b_1x + b_2z + b_3xz + error$, with a continuous predictor $x$ and a
> binary predictor $z$, coefficients $b = \{1, 2, -1, -2\}$, and errors drawn
> independently from a normal distribution with mean 0 and standard deviation 3,
> as follows. For each data point $i$, first draw $z_$i$ , equally likely to
> take on the values 0 and 1. Then draw $x_i$ from a normal distribution with
> mean $z_i$ and standard deviation 1. Then draw the error from its normal
> distribution and compute $y_i$.
> 
> (a) Display your simulated data as a graph of $y$ vs. $x$, using dots and
>     circles for the points with $z = 0$ and $1$, respectively.
>
> (b) Fit a regression predicting $y$ from $x$ and $z$ with no interaction. Make
> a graph with the data and two parallel lines showing the fitted model.
> 
> (c) Fit a regression predicting $y$ from $x$, $z$, and their interaction. Make
> a graph with the data and two lines showing the fitted model.

TK

### 10.2, Regression with interactions

> Here is the output from a fitted linear regression of outcome $y$ on
> pre-treatment predictor $x$, treatment indicator $z$, and their interaction:
> 
> `            Median MAD_SD`
> `(Intercept) 1.2    0.2`
> `x           1.6    0.4`
> `z           2.7    0.3`
> `x:z         0.7    0.5`
> 
> `Auxiliary parameter(s):`
> `      Median MAD_SD`
> `sigma 0.5 0.0`
> 
> (a) Write the equation of the estimated regression line of $y$ on $x$ for the
>     treatment group, and the equation of the estimated regression line of $y$
>     on $x$ for the control group.
> 
> (b) Graph with pen on paper the two regression lines, assuming the values of
>     $x$ fall in the range (0, 10). On this graph also include a scatterplot of
>     data (using open circles for treated units and dots for controls) that are
>     consistent with the fitted model.

TK

### 10.3, Checking statistical significance

> In this exercise and the next, you will simulate two variables that are
> statistically independent of each other to see what happens when we run a
> regression to predict one from the other. Generate 1000 data points from a
> normal distribution with mean 0 and standard deviation 1 by typing
> `var1 <- rnorm(1000,0,1)` in R. Generate another variable in the same way
> (call it var2). Run a regression of one variable on the other. Is the slope
> coefficient “statistically significant”? We do not recommend summarizing
> regressions in this way, but it can be useful to understand how this works,
> given that others will do so.

TK

### 10.4, Simulation study of statistical significance

> Continuing the previous exercise, run a simulation repeating this process 100
> times. This can be done using a loop. From each simulation, save the $z$-score
> (the estimated coefficient of `var1` divided by its standard error). If the
> absolute value of the $z$-score exceeds 2, the estimate is “statistically
> significant.”
> 
> To perform this computation, we start by creating an empty vector of
> $z$-scores filled with missing values (NAs). Another approach is to start with
> `z_scores <- numeric(length=100)`, which would set up a vector of zeroes. In
> general, however, we prefer to initialize with NAs, because then when there is
> a bug in the code, it sometimes shows up as NAs in the final results, alerting
> us to the problem. Here is code to perform the simulation:
> 
> `  z_scores <- rep(NA, 100)`
> `  for (k in 1:100) {`
> `    var1 <- rnorm(1000, 0, 1)`
> `    var2 <- rnorm(1000, 0, 1)`
> `    fake <- data.frame(var1, var2)`
> `    fit <- stan_glm(var2 ~ var1, data=fake)`
> `    z_scores[k] <- coef(fit)[2] / se(fit)[2]`
> `  }`
> 
> How many of these 100 $z$-scores exceed 2 in absolute value, thus achieving
> the conventional level of statistical significance?

TK

### 10.5, Regression modeling and prediction

> The folder `KidIQ` contains a subset of the children and mother data discussed
> earlier in the chapter. You have access to children’s test scores at age 3,
> mother’s education, and the mother’s age at the time she gave birth for a
> sample of 400 children.
> 
> (a) Fit a regression of child test scores on mother’s age, display the data
>     and fitted model, check assumptions, and interpret the slope coefficient.
>     Based on this analysis, when do you recommend mothers should give birth?
>     What are you assuming in making this recommendation?
> 
> (b) Repeat this for a regression that further includes mother’s education,
>     interpreting both slope coefficients in this model. Have your conclusions
>     about the timing of birth changed?
> 
> (c) Now create an indicator variable reflecting whether the mother has
>     completed high school or not. Consider interactions between high school
>     completion and mother’s age. Also create a plot that shows the separate
>     regression lines for each high school completion status group.
> 
> (d) Finally, fit a regression of child test scores on mother’s age and
>     education level for the first 200 children and use this model to predict
>     test scores for the next 200. Graphically display comparisons of the
>     predicted and actual scores for the final 200 children.

TK

### 10.6, Regression models with interactions:

> The folder `Beauty` contains data (use file `beauty.csv`) from Hamermesh and
> Parker (2005) on student evaluations of instructors’ beauty and teaching
> quality for several courses at the University of Texas. The teaching
> evaluations were conducted at the end of the semester, and the beauty
> judgments were made later, by six students who had not attended the classes
> and were not aware of the course evaluations.
> 
> (a) Run a regression using beauty (the variable `beauty`) to predict course
>     evaluations (`eval`), adjusting for various other predictors. Graph the
>     data and fitted model, and explain the meaning of each of the coefficients
>     along with the residual standard deviation. Plot the residuals versus
>     fitted values.
> 
> (b) Fit some other models, including beauty and also other predictors.
>     Consider at least one model with interactions. For each model, explain the
>     meaning of each of its estimated coefficients.
> 
> See also Felton, Mitchell, and Stinson (2003) for more on this topic.

TK

### 10.7, Predictive simulation for linear regression

> Take one of the models from the previous exercise.
> 
> (a) Instructor A is a 50-year-old woman who is a native English speaker and
> has a beauty score of -1. Instructor B is a 60-year-old man who is a native
> English speaker and has a beauty score of -0.5. Simulate 1000 random draws of
> the course evaluation rating of these two instructors. In your simulation,
> use `posterior_predict` to account for the uncertainty in the regression
> parameters as well as predictive uncertainty.
> 
> (b) Make a histogram of the difference between the course evaluations for A
>     and B. What is the probability that A will have a higher evaluation?

TK

### 10.8, How many simulation draws

> Take the model from Exercise 10.6 that predicts course evaluations from beauty
> and other predictors.
> 
> (a) Display and discuss the fitted model. Focus on the estimate and standard
>     error for the coefficient of beauty.
> 
> (b) Compute the median and mad sd of the posterior simulations of the
>     coefficient of beauty, and check that these are the same as the output
>     from printing the fit.
> 
> (c) Fit again, this time setting `iter = 1000` in your `stan_glm` call. Do
>     this a few times in order to get a sense of the simulation variability.
> 
> (d) Repeat the previous step, setting `iter = 100` and then `iter = 10`.
> 
> (e) How many simulations were needed to give a good approximation to the mean
>     and standard error for the coefficient of beauty?

TK

### 10.9, Collinearity

> Consider the elections and economy example from Chapter 7.
> 
> (a) Create a variable that is collinear to the economic growth predictor in
>     the model. Graph the two predictors to confirm that they are collinear.
> 
> (b) Add this new predictor to the model, in addition to economic growth. Fit
>     the regression and report what happens.
> 
> (c) Create a variable that is nearly collinear to the economic growth
>     predictor, with a 0.9 correlation between the two variables. Fit the
>     regression predicting election outcome given economic growth and this new
>     predictor you have created, and again describe and explain what happens.

TK

### 10.10, Regression with few data points and many predictors

> Re-fit the elections and economy example from Chapter 7, adding several
> economic predictors such as unemployment rate in the year of the election,
> inflation rate in the year of the election, etc. Discuss the difficulties in
> interpretation of the fitted model.

TK