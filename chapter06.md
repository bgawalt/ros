# Chapter 6: Background on regression modeling

[(Return to README)](./README.md)

"At a purely mathematical level," the book wants you to use regression for
prediction and/or comparison.  Comparison has a special case where you're
comparing treatment and control outcomes to estimate a causal effect.

## Subsection rundown

### 6.1, Regression models

Jargon check: in the "basic regression model" expression

$$y = a + bx + \text{error}$$

"The quantities $a$ and $b$ are *coefficients* or, more generally, *parameters*
of the model."

The book is going to focus on four extensions of that basic model:
additional predictors, nonlinear models (like log-transforming $y$ and $x$),
nonadditive models (e.g., you have a term for the product of two other
predictors), and generalized linear models (wrap the basic model in an
activation function).

This means *not* focusing on the listed extensions of nonparametric models,
multilevel models, and measurement error models.

### 6.2, Fitting a simple regression to fake data

Hm, ok. Is there a Python replacement that will work with their example usage
of `rstanarm`?  A short Google search suggests
[Bambi](https://github.com/bambinos/bambi).  But I dislike both Pandas and
the "`y ~ x`" way of describing models, so... we'll see what I go with.

(Looked it up: the `arm` in `rstanarm` is short for "applied regression
modeling.")

The section describes fitting a model to $(x, y)$ data where $x$ is the integers
1 through 20.  The output $y$ is:

$$y_i + 0.2 + 0.3x_i + \mathcal{N}(0, 0.5)$$

They report median and madsd numbers for their estimates of the slope and
intercept, as well as for the residual noise's standard deviation.  They also
plot the line of best fit on top of the twenty datapoints.

They note that their estimates are close to the original scalars they used to
generate the data, when you take into account the reported madsd uncertainties.

### 6.3, Interpret coefficients as comparisons, not effects

They fit a linear model predicting a person's income from their height and their
gender.  There's a lot of residual uncertainty; $R^2$ is 0.1.

They don't want to use the word "effect" when talking about the predictive
impact of height on income.  They want to save that word for situations where
there's a treatment or intervention driving the predictor's value.  In this
example, "what is observed is an observational pattern, that taller people in
the sample have higher earnings on average. These data allow between-person
comparisons, but to speak of effect of height is to reference a hypothetical
within-person comparison."

When doing those comparisons, they word it as:

*  "the average difference in earnings, comparing two people of the same sex but
    one inch different in height, is $600."
*  "when comparing two people with the same height but different sex, the man’s
    earnings will be, on average, $10 600 more than the woman’s in the fitted
    model."

### 6.4, Historical origins of regression

Lol, okay, this section opens with a literal "Webster's defines 'regression'
as...." 

One thing I'll say about this scatterplot from Galton about mother and daughter
heights:

![A scatterplot of Mother's Height (inches) on the x-axis and Adult Daughter's
Height (inches) on the y-axis.  There's a wide cloud of dots in the middle,
tilted up at about 45 degrees.  The regression model predictive line has a
noticeably shallower slope than that, more like 30 degrees
upward.](./fig/fig06_3.png)

That line of best fit is not what you'd get if you used principal component
analysis to find the direction in 2D space that captures most of the variance.
I don't know why or when we'd prefer one slope or the other (the PCA vs. the
OLS), though I guess it is encoded in the loss function used to train the model.
Galton illustrated this with this famous oval:

![Same mother-daughter chart axes, albeit in old timey 1900s style. There's an
oval drawn like you would for the original scatterplot's PCA/covariance, plus
lines for predicting mother from daughter, predicting daughter from mother, and
the actual major axis of the covariance
oval.](./fig/ch06_galton_smoothed_correlation.png)

### 6.5, The paradox of regression to the mean

They discuss how "regression to the mean" is a view on the general phenomenon
of a sort of conservation of variance.  If you disassemble the basic equation
$y = a + bx + \text{error}$,

*  If $b$ is less than one (as in the Galton heights case), then the $a + bx$
    predictions have less variance than the original $x$'s did...
*  ... but then you add in some variance from the error term, and so $y$ winds
    up with the same total variance as $x$.

With midsentence markup frome me:

> Regression to the mean thus will always arise in some form whenever
> predictions are imperfect in a stable environment.  The imperfection of the
> prediction [the error term in the basic equation -bg] induces variation, and
> regression in the point prediction [that $b$ be less than 1 -bg] is required
> in order to keep the total variation constant.

They break this down further in the fake-data scenario where student test
performance is based solely on their inherent talent, plus a noise factor.
If you predict final exam score from midterm exam score, you get regression to
the mean (you get a slope $b$ of 0.5).  By construction, there's no causal
effect here, even though the story lends itself to one:

> [A] student who scores very well on the midterm is likely to have been
> somewhat lucky and also to have a high level of skill, and so in the final
> exam it makes sense for the student to do better than the average but worse
> than on the midterm.

The skill effect is still there, but the luck is different every time.  So you
should guess that some of the observed input level will disappear in the output,
just by drawing a different luck/error term.  They warn you not to get fooled
by the "regression fallacy" which doesn't take this phenomenon into account.

They conclude by rephrasing the regression fallacy as a comparison against a
bogus alternative -- daughters should be the same height as their mothers,
final exam scores should exactly match midterm scores.


## Exercises

Plots and computation powered by [Chapter06.ipynb](./notebooks/Chapter06.ipynb)

### 6.2, Programming fake-data simulation

> Write an R function to: (i) simulate $n$ data points from the model, 
> $y = a + bx + \text{error}$, with data points $x$ uniformly sampled from the
> range (0, 100) and with errors drawn independently from the normal
> distribution with mean 0 and standard deviation $\sigma$; (ii) fit a linear
> regression to the simulated data; and (iii) make a scatterplot of the data
> and fitted regression line. Your function should take as arguments, $a$, $b$,
> $n$, $\sigma$, and it should return the data, print out the fitted regression,
> and make the plot. Check your function by trying it out on some values of $a$,
> $b$, $n$, $\sigma$.

Two sample runs,

*  At left, $a = 30$, $b = 0.25$, $n = 200$, $\sigma = 15$
*  At right, $a=80$, $b = -0.9$, $n = 35$, $\sigma = 4$

![Two scatterplots with blue dots, side by side, both with x and y axes that
each go from 0 to 100. At left, the title reads: "Slope: [0.16, 0.30];
Intercept: [28.1, 36.4]", the blue dots are labeled "N = 200" and are spread
across the bottom 2/3rds of the space.  At right, the title reads:
"Slope: [-0.96, -0.87]; Intercept: [79.0, 83.9]", the blue dots are labeled
"N = 35" and are on a tight stripe across the space.  Both have lines
across them indiciating their linear regression fit and each fit has a wider
pale red stripe encoding some of the model uncertainty.](./fig/ex06_2_demo_regression.png)

### 6.3, Variation, uncertainty, and sample size

> Repeat the example in Section 6.2, varying the number of data points, $n$.
> What happens to the parameter estimates and uncertainties when you increase
> the number of observations?

Four repeats of \[$a = 30$, $b = 0.25$, $\sigma = 15$\] with larger sample
sizes (each is its own resampling, they aren't telescoping sets):

![Same basic layout as the above-left figure, repeated four times in a 2 x 2
grid; the uncertainty around the line of best fit gets narrower.  Slope
uncertainty goes: [0.11, 0.4] at n = 50, [0.22, 0.43] at n = 100, [0.22, 0.43]
at n = 200, and [0.21, 0.32] at n = 400.  Intercept uncertainty goes [23.6, 39.2],
[20.5, 33.4], [24.4, 31.8], [27.6, 33.9]](./fig/ex06_3_larger_samples.png)

### 6.4, Simulation study

> Perform the previous exercise more systematically, trying out a sequence of
> values of $n$, for each simulating fake data and fitting the regression to
> obtain estimate and uncertainty (median and mad sd) for each parameter. Then
> plot each of these as a function of $n$ and report on what you find.

These are also repeats of the \[$a = 30$, $b = 0.25$, $\sigma = 15$\] generating
process. The sample sizes used were [10, 20, 40, 80, 160, 320, 640, 1280].

The thick gray bar indicates the max-likelihood estimate of each parameter
for the largest sample, so that we can see whether it's covered by earlier
samples (it is).  

![Two side-by-side semilog plots.  At left, slope's y-axis goes from 0 to 0.8;
its initial uncertainty is [0.2, 0.8] and slowly tightens to [0.21, 0.27].
At right, intercept's y-axis goes from just below 0 to 45; its initial
uncertainty is [0, 34] tightening to [29, 31].](./fig/ex06_4_uncertainty.png)

### 6.5, Regression prediction and averages

> The heights and earnings data in Section 6.3 are in the folder `Earnings`.
> Download the data and compute the average height for men and women in the
> sample.
> 
> (a) Use these averages and fitted regression model displayed on page 84 to
>     get a model-based estimate of the average earnings of men and of women in
>     the population.
> 
> (b) Assuming 52% of adults are women, estimate the average earnings of adults
>     in the population.
> 
> (c) Directly from the sample data compute the average earnings of men, women,
>     and everyone.  Compare these to the values calculated in parts (a) and
>     (b).

Predicted average earnings for each category:

| Category | Model   | Sample   |
| -------- | ------- | -------- |
| Men      | $26.7K  | $30.1K   |
| Women    | $12.7K  | $15.8K   |
| All      | $19.4K  | $21.1K   |

### 6.6 Selection on x or y,

> (a) Repeat the analysis in Section 6.4 using the same data, but just analyzing
>     the observations for mothers’ heights less than the mean. Confirm that the
>     estimated regression parameters are roughly the same as were obtained by
>     fitting the model to all the data.
> 
> (b) Repeat the analysis in Section 6.4 using the same data, but just analyzing
>     the observations for daughters’ heights less than the mean. Compare the
>     estimated regression parameters and discuss how they differ from what was
>     obtained by fitting the model to all the data.
> 
> (c) Explain why selecting on daughters’ heights had so much more of an effect
>     on the fit than selecting on mothers’ heights.

Fitting the model to three editions of the dataset (note that my linear model
is different that what their `stan_glm` version produced, and also the datasets
don't seem identical?):

| Subsample       | Intercept (in.) | Mother's Height |
| --------------- | --------------- | --------------- |
| All records     | 33.0 +/- 1.4    | 0.46 +/- 0.02   |
| Short mothers   | 37.8 +/- 3.1    | 0.38 +/- 0.05   |
| Short daughters | 49.6 +/- 1.4    | 0.17 +/- 0.02   |

Graphically:

![A football-shaped cloud of light scatterplot dots, with Mother's Height on
the x-axis and Daughter's Height on the y-axis.  Both axes run from 50 in. to
75 in, though most of the dots are between 55 and.  The three slope-intercept
lines from the table are drawn, in cyan, yellow, and magenta.](./fig/ex06_6_mother_daughter.png)

### 6.7, Regression to the mean

> Gather before-after data with a structure similar to the mothers’ and
> daughters’ heights in Sections 6.4 and 6.5. These data could be performance of
> athletes or sports teams from one year to the next, or economic outcomes in
> states or countries in two successive years, or any other pair of measurements
> taken on a set of items. Standardize each of the two variables so it has a
> mean of 0 and standard deviation of 1.
> 
> (a) Following the steps of Section 6.4, read in the data, fit a linear
>     regression, and plot the data and fitted regression line.
> 
> (b) Repeat the above steps with fake data that look similar to the data you
>     have gathered.

Drawing from my work
[on The LombardoTron](https://github.com/bgawalt/lombardotron/commit/5bf17f5b762cd926211ea96659e698788e87c6bd),
I exported a CSV of IDP-league fantasy football points earned by NFL players
who earned at least 20 points in both the 2023 and 2024 seasons.  And would you
look at that: when I fit a linear model on the log-log scale, we see regression
to the mean.

$$\log(\hat{y}) = 1.8 + 0.59 \log(x)$$
$$\Rightarrow \hat{y} = 6x^{0.59}$$


![Scatter plot with log-log axes labeled "Total IDP Score for 2023" (x axis)
and "... for 2024" (y axis), both running from 2^4 to 2^9.  The 739 blue dots
representing each player-performance are uniformly spread, though they make
a kind of acute isoceles triangle shape, point northeast -- narrowing by a
factor of three (again, log scale) between low-score and high-score regions.
A red line is overlain labeled "log(y) ~ 1.8 + 0.59 log(x)](./fig/ex06_07_nfl_idp.png)


### 6.8, Regression to the mean with fake data

> Perform a fake-data simulation as in Section 6.5, but using the flight school
> example on page 89. Simulate data from 500 pilots, each of whom performs two
> maneuvers, with each maneuver scored continuously on a 0–10 scale, that each
> pilot has a true ability that is unchanged during the two tasks, and that the
> score for each test is equal to this true ability plus independent errors.
> Further suppose that when pilots score higher than 7 on the scale during the
> first maneuver, that they get praised, and that scores lower than 3 on the
> first maneuver result in negative reinforcement. Also suppose, though, that
> this feedback has no effect on performance on the second task.
> 
> (a) Make a scatterplot with one dot for each pilot, showing score on the
>     second maneuver vs. score on the first maneuver. Color the dots blue for
>     the pilots who got praised, red for those who got negative reinforcement,
>     and black for the other cases.
>
> (b) Compute the average change in scores for each group of pilots. If you did
>     your simulation correctly, the pilots who were praised did worse, on
>     average, and the pilots who got negative reinforcement improved, on
>     average, for the second maneuver. Explain how this happened, given that
>     your data were simulated under a model in which the positive and negative
>     messages had no effects.

With a generative distribution of:

*  Pilot ability is uniform between 1.5 and 8.5,
*  Score on any particular maneuver is "ability, plus noise of
    $\mathcal{N}(0, 1)$, truncated to cap all noise within [-2.4, 2.4],
*  And then an overall clamp applied to keep all manuever scores between 0 and
    10,

the negative-reinforcement group saw an average change of +0.6 points, and the
praised group saw an average change of -0.6 points.

![A rectangle-turned-diagonal stripe of scatterplot points, colored as
instructed for this exercise.  X- and y-axes run from 0 to 10 and are labelled
"First/Second maneuver score".  There is a dashed cyan line denoting the linear
model fit.](./fig/ex06_8_fake_pilots.png)