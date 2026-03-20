# Chapter 12: Transformations and regression

[(Return to README)](./README.md)

The intro talks about *standardization*, which "connects to 'regression to the
mean'" by putting predictors and outcomes on a shared zero-mean, unit-variance
scale.  And it also talks about "logarithmic and other transformations... in
order to get more understandable models and better predictions."

## Subsection rundown

### 12.1, Linear transformations

#### Scaling of predictors and regression coefficients

Units matter!  A regression coefficient describes the expected change in the
output given an increase in its predictor by "one unit".  But the same attribute
can be expressed in small units (inches of distance) or large ones (miles) and
that is going to dictate the scale of coefficient you get.

Linear transformations of predictors or outcome don't affect the model fit or
predicted values.  But they "can improve interpretability of coefficients and
make a fitted model easier to understand."  (Unsaid: they can also make the
numerical operations run during the model fit procedure go smoother.)

#### Standardization using z-scores

Linearly transform your predictors into versions with zero mean and unit
variance.  That makes unit changes in the predictor correspond to moving up or
down by one standard deviation:

> This is helpful because standard deviations can be seen as a measure of
> practical significance; in this case, a difference in one standard deviation
> on the input scale is a meaningful difference in that it roughly reflects a
> typical difference between the mean and a randomly drawn observation.

Standardization like this requires you have reliable values of the mean and
standard deviation for each predictor.  Maybe you estimate that from your data;
we call using the sample means and standard deviations "$z$-scoring".
Or maybe your data are too thin for that....

#### Standardization using an externally specified population distribution

If your data is too thin for that, look up good values of mean and standard
deviation to use from some other authority.  One benefit of *not* using
sample statistics is that it makes it easier to compare estimates of, e.g.,
coefficients.  (You just directly compare them.)

#### Standardization using reasonable scales

You can also just be a normal human being and use the same units everyone does:
inches, dollars, years, etc.  Maybe you adjust them a bit, to keep coefficients
on a "human" scale, like picking "thousands of dollars" to express a personal
income predictor.  Work backwards from what you want "one unit" to mean when
your coefficients express "change in expected outcome per change by one unit."

### 12.2, Centering and standardizing for models with interactions

TK

### 12.3, Correlation and “regression to the mean”

TK

### 12.4, Logarithmic transformations

TK

### 12.5, Other transformations

TK

### 12.6, Building and comparing regression models for prediction

TK

### 12.7, Models for regression coefficients

TK


## Exercises

Plots and computation powered by [Chapter12.ipynb](./notebooks/Chapter12.ipynb)

### 12.1 Plotting linear and quadratic regressions

> The folder `Earnings` has data on weight (in pounds), age (in years), and
> other information from a sample of American adults. We create a new variable,
> `age10 = age/10`, and fit the following regression predicting weight:

```
            Median MAD_SD
(Intercept) 148.7   2.2
age10         1.8   0.5

Auxiliary parameter(s):
      Median MAD_SD
sigma 34.5    0.6
```

> (a) With pen on paper, sketch a scatterplot of weights versus age (that is,
>     weight on y-axis, age on x-axis) that is consistent with the above
>     information, also drawing the fitted regression line. Do this just given
>     the information here and your general knowledge about adult heights and
>     weights; do not download the data.
>
> (b) Next, we define `age10_sq = (age/10)^2` and predict weight as a quadratic
> function of age:

```
            Median MAD_SD
(Intercept) 108.0    5.7
age10        21.3    2.6
age10sq      -2.0    0.3

Auxiliary parameter(s):
      Median MAD_SD
sigma 33.9    0.6
```

> Draw this fitted curve on the graph you already sketched above.

TK

### 12.2, Plotting regression with a continuous variable broken into categories

> Continuing Exercise 12.1, we divide age into 4 categories and create
> corresponding indicator variables, `age18_29`, `age30_44`, `age45_64`, and
> `age65_up`. We then fit the following regression:

```
   stan_glm(weight ~ age30_44 + age45_64 + age65_up, data=earnings)

            Median MAD_SD
(Intercept) 147.8    1.6
age30_44TRUE  9.6    2.1
age45_64TRUE 16.6    2.3
age65_upTRUE  7.5    2.7

Auxiliary parameter(s):
      Median MAD_SD
sigma 34.1    0.6
```

> (a) Why did we not include an indicator for the youngest group, `age18_29`?
>
> (b) Using the same axes and scale as in your graph for Exercise 12.1, sketch
>     with pen on paper the scatterplot, along with the above regression
>     function, which will be discontinuous.

TK

### 12.3, Scale of regression coefficients

> A regression was fit to data from different countries, predicting the rate of
> civil conflicts given a set of geographic and political predictors. Here are
> the estimated coefficients and their $z$-scores (coefficient divided by
> standard error), given to three decimal places:
> 
> 
> |                      | Estimate | $z$-score |
> | -------------------- | -------- | --------- |
> | Intercept            |   -3.814 |   -20.178 |
> | Conflict before 2000 |    0.020 |     1.861 |
> | Distance to border   |    0.000 |     0.450 |
> | Distance to capital  |    0.000 |     1.629 |
> | Population           |    0.000 |     2.482 |
> | % mountainous        |    1.641 |     8.518 |
> | % irrigated          |   -0.027 |    -1.663 |
> | GDP per capita       |   -0.000 |    -3.589 |
> 
> Why are the coefficients for distance to border, distance to capital,
> population, and GDP per capita so small?

TK

### 12.4, Coding a predictor as both categorical and continuous

> A linear regression is fit on a group of employed adults, predicting their
> physical flexibility given age. Flexibility is defined on a 0–30 scale based
> on measurements from a series of stretching tasks. Your model includes age in
> categories (under 30, 30–44, 45–59, 60+) and also age as a linear predictor.
> Sketch a graph of flexibility vs. age, showing what the fitted regression
> might look like.

TK

### 12.5, Logarithmic transformation and regression

> Consider the following regression:
>
> $$\log(weight) = -3.8 + 2.1 \log(height) + \text{error}$$
> 
> with errors that have standard deviation 0.25. Weights are in pounds and
> heights are in inches.
> 
> (a) Fill in the blanks: Approximately 68% of the people will have weights
>     within a factor of and of their predicted values from the regression.
>
> (b) Using pen and paper, sketch the regression line and scatterplot of
>     log(weight) versus log(height) that make sense and are consistent with the
>     fitted model. Be sure to label the axes of your graph.

TK

### 12.6, Logarithmic transformations

> The folder `Pollution` contains mortality rates and various environmental
> factors from 60 U.S. metropolitan areas (see McDonald and Schwing, 1973). For
> this exercise we shall model mortality rate given nitric oxides, sulfur
> dioxide, and hydrocarbons as inputs. This model is an extreme
> oversimplification, as it combines all sources of mortality and does not
> adjust for crucial factors such as age and smoking. We use it to illustrate
> log transformations in regression.
>
> (a) Create a scatterplot of mortality rate versus level of nitric oxides. Do
>     you think linear regression will fit these data well? Fit the regression
>     and evaluate a residual plot from the regression.
>
> (b) Find an appropriate transformation that will result in data more
>     appropriate for linear regression. Fit a regression to the transformed
>     data and evaluate the new residual plot.
>
> (c) Interpret the slope coefficient from the model you chose in (b).
>
> (d) Now fit a model predicting mortality rate using levels of nitric oxides,
>     sulfur dioxide, and hydrocarbons as inputs. Use appropriate
>     transformations when helpful. Plot the fitted regression model and
>     interpret the coefficients.
> 
> (e) Cross validate: fit the model you chose above to the first half of the
>     data and then predict for the second half. You used all the data to
>     construct the model in (d), so this is not really cross validation, but it
>     gives a sense of how the steps of cross validation can be implemented.

TK

### 12.7, Cross validation comparison of models with different transformations of outcomes

> When we compare models with transformed continuous outcomes, we must take into
> account how the nonlinear transformation warps the continuous variable. Follow
> the procedure used to compare models for the mesquite bushes example on page
> 202.
>
> (a) Compare models for earnings and for log(earnings) given height and sex as
>     shown on pages 84 and 192. Use earnk and log(earnk) as outcomes.
>
> (b) Compare models from other exercises in this chapter.

TK

### 12.8, Log-log transformations

> Suppose that, for a certain population of animals, we can predict log weight
> from log height as follows:
> 
> *  An animal that is 50 centimeters tall is predicted to weigh 10 kg.
> *  Every increase of 1% in height corresponds to a predicted increase of 2% in
>     weight.
> * The weights of approximately 95% of the animals fall within a factor of 1.1
>     of predicted values.
>
> (a) Give the equation of the regression line and the residual standard
>     deviation of the regression.
>
> (b) Suppose the standard deviation of log weights is 20% in this population.
>     What, then, is the R2 of the regression model described here?

TK

### 12.9, Linear and logarithmic transformations

> For a study of congressional elections, you would like a measure of the
> relative amount of money raised by each of the two major-party candidates in
> each district. Suppose that you know the amount of money raised by each
> candidate; label these dollar values $D_i$ and $R_i$. You would like to
> combine these into a single variable that can be included as an input variable
> into a model predicting vote share for the Democrats. Discuss the advantages
> and disadvantages of the following measures:
>
> (a) The simple difference, $D_i - R_i$
>
> (b) The ratio, $D_i/R_i$
> 
> (c) The difference on the logarithmic scale, $\log D_i - \log R_i$
> 
> (d) The relative proportion, $D_i/(D_i + R_i)$

TK

### 12.10, Special-purpose transformations

> For the congressional elections example in the previous exercise, propose an
> idiosyncratic transformation as in the example on page 196 and discuss the
> advantages and disadvantages of using it as a regression input.

TK

## 12.11, Elasticity

> An economist runs a regression examining the relations between the average
> price of cigarettes, $P$, and the quantity purchased, $Q$, across a large
> sample of counties in the United States, assuming the functional form,
> $logQ = \alpha + \beta \log P$. Suppose the estimate for $\beta$ is -0.3.
> Interpret this coefficient.

TK

### 12.12, Sequence of regressions

> Find a regression problem that is of interest to you and can be performed
> repeatedly (for example, data from several years, or for several countries).
> Perform a separate analysis for each year, or country, and display the
> estimates in a plot as in Figure 10.9.

TK

### 12.13,  Building regression models

> Return to the teaching evaluations data from Exercise 10.6. Fit regression
> models predicting evaluations given many of the inputs in the dataset.
> Consider interactions, combinations of predictors, and transformations, as
> appropriate. Consider several models, discuss in detail the final model that
> you choose, and also explain why you chose it rather than the others you had
> considered.

TK

### 12.15, Models for regression coefficients

> Using the Portuguese student data from the `Student` folder, repeat the
> analyses in Section 12.7 with the same predictors, but using as outcome the
> Portuguese language grade rather than the mathematics grade.

TK