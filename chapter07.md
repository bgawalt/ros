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
    *  Too many hopelessly close cases, where collapsing a 50-50 race into a
        hard binary won/lost would introduce a kind of quantization noise
    *  In somewhat close cases, where there's consensus around who's very likely
        to win, you want to provide odds of an upset.
    *  Too many too-easy landslide cases, where vote margin prediction just is
        the more interesting thing to predict.
    *  "In any of these cases, a prediction of the vote share is more
        informative than simply predicting the winner."
*  And then the familiar sad stinger, declaring that multilevel modeling "is
    beyond the scope of this book."

### 7.2, Checking the model-fitting procedure using fake-data simulation

The fake data simulation uses the actual economic growth numbers as $x$ values,
then simulates random $y$ outcomes centered on the model coefficients with
the same residual standard deviation.

They repeat the simulation 1000 times to check coverage rates of the "real"
coefficient values used to generate the fake data.  "The coverage is a bit low,
in part because $\pm 1$ and $\pm 2$ are standard error bounds for the normal
distribution, but with a sample size of only 16, our inferences should use the
$t$ distribution with 14 degrees of freedom."

### 7.3, Formulating comparisons as regression models

"\[W\]e show how simple averages and comparisons can be interpreted as special
cases of linear regression."  I love when things are special cases of
linear regression!  Like
[all of these common statistical tests:](https://lindeloev.github.io/tests-as-linear/)

!["Cheat sheet" of how many statistical tests are actually linear models, from
the above lindeloev.github link](./fig/ch07_linear_tests_cheat_sheet.png)

This section introduces the jargon "indicator variable, which is a predictor
that equals 1 or 0 to indicate whether a data point falls into a specified
category."

The comparisons they pose as regression:

*  "Estimating the mean is the same as regressing on a constant term," i.e.,
    only $y$ and an intercept term, no $x$.  I do think there would be a payoff
    now if the book had earlier talked about the optimization routine that
    leads to coefficient estimation.  Why does OLS on zero predictors produce 
    the output mean?  What objective function would produce an output median?
    I wonder if it's because using the minimization framework lends itself too
    much to frequentissm, and would need to be walked back in order to introduce
    the Bayesian approach next chapter.
*  "Estimating a difference is the same as regressing on an indicator variable,"
    i.e., all the $x$s are 0 or 1.

Coming attraction: "In Section 10.4 we discuss the use of indicator variables in
regression models with multiple predictors."


## Exercises

Plots and computation powered by [Chapter07.ipynb](./notebooks/Chapter07.ipynb)

### 7.1, Regression predictors

> In the election forecasting example of Section 7.1, we used inflation adjusted
> growth in average personal income as a predictor. From the standpoint of
> economics, it makes sense to adjust for inflation here. But suppose the model
> had used growth in average personal income, not adjusting for inflation. How
> would this have changed the resulting regression? How would this change have
> affected the fit and interpretation of the results?

Without inflation adjustment, you'd see a rearrangement of the $x$ values.
But I don't know in advance if that would make the data more or less well-fit
by a straight line.  I will just look up the inflation data and find out:

![Two scatterplot series regressing incumbent party vote share in presidential
elections against recent changes in personal income, with (blue) and without
(red) adjusting for inflation](./fig/ex07_1a_inflation.png)

It's a worse fit:

![Same pair of red and blue scatterplots, now with linear models fit to them and
displayed as dashed lines](./fig/ex07_1b_models.png)

The coefficient of determination (i.e., share of explained variance) is 58% when
adjusting for inflation and only 3% when you don't.

### 7.2, Fake-data simulation and regression

> Simulate 100 data points from the linear model, $y = a + bx + \text{error}$,
> with $a = 5$, $b = 7$, the values of x being sampled at random from a uniform
> distribution on the range [0, 50], and errors that are normally distributed
> with mean 0 and standard deviation 3.
>
> (a) Fit a regression line to these data and display the output.
>
> (b) Graph a scatterplot of the data and the regression line.
>
> (c) Use the text function in R to add the formula of the fitted line to the graph.

LinRegress results:

*  **Slope:** 6.97
*  **Slope stderr:** 0.02
*  **Intercept:** 5.82
*  **Intercept stderr:** 0.65
*  **RValue:** 1.00
*  **PValue:** 0.00

![Scatterplot of fake data as requested in the problem, along with the line of
best fit overlaid](./fig/ex07_2_fake_data.png)

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

I put the parabola vertex at $x = 25$ and set the parabola's y-axis intercept
to match the max $y$ value in Exercise 5.2, with:

$$a = 350,~b=-25,~c=0.5$$

LinRegress results:

*  **Slope:** -0.18
*  **Slope stderr:** 0.66
*  **Intercept:** 145.17
*  **Intercept stderr:** 18.84
*  **RValue:** -0.03
*  **PValue:** 0.78

![Scatterplot of a convex parabola and a dashed line that crosses it about a
third the way up its full height](./fig/ex07_3_fake_parabola.png)

### 7.5, Convergence as sample size increases

> Set up a simulation study such as in Section 7.2, writing the entire
> simulation as a function, with one of the arguments being the number of data
> points, $n$. Compute the simulation for $n =$ 10, 30, 100, 300, 1000, 3000,
> 10 000, and 30 000, for each displaying the estimate and standard error.
> Graph these to show the increasing stability as $n$ increases.

$n$ | $\hat{b}$ | std. err
--- | --------- | --------
10 | 4.0 | 0.83
30 | 2.8 | 0.42
100 | 2.7 | 0.27
300 | 3.2 | 0.16
1000 | 3.0 | 0.09
3000 | 3.0 | 0.05
10,000 | 3.0 | 0.03
30,000 | 3.0 | 0.02

![A trio of line plots, with the y axis "Slope estimate, +/- 1 std err" between
2.4 and 4.9, and the x-axis "Sample size" on a log scale from 7 to 3x10^4. 
The three lines form a green band that stars very wide, from 3.1 to 4.8, and
narrows to almost exactly 3](./fig/ex07_5_fake_data_slopes.png)

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

With the direct method of (a), I find an average difference of 5.5% with a
standard error of 2.3%.  When I use the linear regression method of (b), I get
a slope of 5.5% and a standard error of 2.5%.  Those are close enough that I
trust it's working, and I chalk up the difference to the linear regression
package probably making use of a genuine $t$-distribution with $n - 2$ degrees
of freedom.

### 7.7, Comparing simulated data to assumed parameter values

> (a) Simulate 100 data points from the model, $y = 2 + 3x + \text{error}$, with
> predictors x drawn from a uniform distribution from 0 to 20, and with
> independent errors drawn from the normal distribution with mean 0 and standard
> deviation 5. Save $x$ and $y$ into a data frame called `fake`. Fit the model,
> `stan_glm(y ~ x, data=fake)`. Plot the data and fitted regression line.
>
> (b) Check that the estimated coefficients from the fitted model are reasonably
> close to the assumed true values. What does “reasonably close” mean in this
> context?

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