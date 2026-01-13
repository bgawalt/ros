# Chapter 3: Some basic methods in mathematics and probability

Three motivations for the chapter:

1. Learn building blocks that can be used to construct "elaborate models"
2. Understand generic/abstract inference without looking at details of any
    particular model
3. Construct quick estimates for "small parts of problems -- before fitting a
    more elaborate model."

I do like (3); one failure mode I see a lot in ML work is people prematurely
reaching for expensive and finnicky and elaborate models, before attempting
simpler baselines.

## Subsection rundown

### 3.1, Weighted averages

"To take a weighted average, you have to use the right weights."  Seems obvious,
I'm sure there's constant high-profile goofs of this, though.

### 3.2, Vectors and matrices

Interesting that there's no caveat around the definition of vectors and
matrices.  No mention of what makes for a valid vector space, or that there are
such underlying, abstract rules.

That it spends half of page 36 on plugging different $x$'s into
"$\hat{y} = 46.3 + 3.0x$" is oddly elementary.  Were my undergrad books like
this?  I suppose it does lead into a statement of convention, that this book
will prefer stating multiple predictions as

$$\hat{y} = X\hat{\beta}$$

where matrix $X \in \mathbb{R}^{N \times p}$ has one example per row,
one predictor (feature) per column, and the model weights are a $p \times 1$
column vector.

### 3.3, Graphing a line

"Slope and intercept" are straight-up pre-algebra curricula, so I am now
getting a better sense of the audience of the book, or at least a meaningful
share: undergrads from disciplines where calculus is not a requirement.

I like the subtle change-of-variables that the switch from $1000 - 0.393x$ to
$241 - 0.393(x - 1950)$ represents.  This is going to be an important fact
about (generalized?) linear regression later, that additive scaling of an input
feature doesn't change that feature's model weight (0.393, here).

This is a mouthful, but it seems like a useful way to express the concept, so
I'll copy it down as a form of practice/recitation: "when comparing any two
years, we see a world record time that is, on average, 0.393 seconds per year
less for the more recent year."

### 3.4, Exponential and power-law growth and decline; logarithmic and log-log relationships

The world population growth model gets a caveat about how doubling every 50
years is "not an accurate description, just a crude approximation."  Linear
algebra didn't get the same courtesy that human-population studies does here!

I've worked out the semilog and log-log translations a bunch of times and it's
always fun.  So I won't try committing it to memory, I'll just have fun
re-deriving it if I ever need to.

(I hope this book talks about the difference between fitting a semilog/log-log
model directly, vs. fitting a slope and intercept to log-transformed data.)

### 3.5, Probability distributions

"\[T\]he *error term* \[emphasis theirs\] in the expression
$y = a + bx + \epsilon$" -- I think that's the first time we've seen that
expression?

Two steps to "describe the typical range of values of the outcome variable,
given the predictors": "predict the average outcome value given the predictors,"
and "summarize the variation in this prediction."

#### Mean and standard deviation of a probability distribution

A dog that didn't bark: in defining variance, the book doesn't mention the
difference between empirically estimating variance as

$$Var(x) = \frac{1}{N}\sum_{j=1}^N (x_j - \mu_j)^2$$

versus taking an the unbiased estimate with:

$$Var(x) = \frac{1}{N-1}\sum_{j=1}^N (x_j - \mu_j)^2$$

This pleases me, as my first data science job, I got in a minor disagreement
over my colleague calling the first one "wrong."  It's not wrong!  It's biased!
Those are different.  Sometimes bias is good.

#### Normal distribution

I wish I knew the technical criteria for "small" in terms of the central limit
theorem applying to "the sum of many small, independent random variables."
I am 99% sure that weirdo random variables drawn from mega-tail distributions
like the Cauchy break the CLT.

Just for the sake of my own clarity: the distribution of heights is not a normal
distribution:

![Figure 3.6(c), titled "heights of all adults (not a normal distribution)",
where the distribution looks like a hill with a somewhat gently sloped mesa
between 65 and 70 inches, and then bell curve tails outside that range.
Caption: "Heights of all adults in the United States, which have the form of a
mixture of two normal distributions, one for each sex."](./fig/fig03_06_height_distribution.png)

One outsized factor, sex, pushes it towards bimodality. But the
distribution of *the sample mean* of heights can still be normal.  Sometimes my
brain skips straight to that second sense of normality.  The heights aren't
normally distributed, but you can make a normal distribution out of them:

> There are many situations in which we can use the normal distribution to
> summarize uncertainty in estimated averages, differences, and regression
> coefficients, even when the underlying data do not follow a normal
> distribution.

Also, interesting! The word "Gaussian" does not appear until Chapter 11, when
used to talk about Gaussian processes.  And that's the only sense the word is
ever used in the book (eight appearances).  The bell curve is Normal, not
Gaussian, to this book.

#### Linear transformations

It was actually nice to see/be reminded how easy unit conversions (inches to
centimeters) are.  Just apply "2.54 cm/in" to the mean and standard deviation,
done.

I will do Exercise 3.6.

#### Mean and standard deviation of the sum of correlated random variables

Useful to include definition of correlation,

$$\rho_{uv} = \mathbb{E}\left[(u - \mu_u)(v - \mu_v)\right]/(\sigma_u\sigma_v)$$

but no hints yet on how to calculate that expectation.

Also just some useful cheat-sheet entries on the mean and standard deviation of
a linear combination of random variables $z = au + bv$:

*  $\mu_z = a\mu_u + b\mu_v$
*  $\sigma_z = \sqrt{a^2\sigma_u^2 + b^2\sigma_v^2 + 2ab\sigma_u\sigma_v}$

#### Lognormal distribution

"\[The lognormal distribution\] pulls in the values at the high end, compressing
the scale of the distribution."  Does it, though?  In Figure 3.8, there's more
mass on the right-hand side of the lognormal mode, than the symmetric normal
distribution.  That's "pulling in"?

![Figure 3.8, with two subplots titled "log weights of men (normal
distribution)" and "weights of men (lognormal distribution)". Caption: "Weights
of men (which approximately follow a lognormal distribution, as predicted from
the Central Limit Theorem from combining many small multiplicative factors),
plotted on the logarithmic and original scales."](./fig/fig03_08_lognormal_weight.png)

Also, I get that you can't get into every detail, but, a sentence about why
height is an aggregate of many additive factors but weight is and aggregate of
multiplicative factors would have been nice.

Between the lines: the book does not want readers to stress about whether any
particular random variable is Gaussian.  Transformations need a motivation other
than "now it looks more bell curvy."

#### Binomial distribution

Language is tricky: "independent of each other (that is, success in one shot is
not associated with ... probability of success for any other shot)."  There's
some undergrad-level-clever examples of like, uncorrelated variables, that very
much are dependent on each other.  So establishing what counts as "associated
with" is complicated.

#### Poisson distribution

Summarized as "can be used for count data;" with stay-tuned notices about
(a) checking its "fit to data" before definitely describing an RV as Poisson,
and (b) Section 15.2 will talk about accounting for "overdispersion".
(As a mechanical requirement of the distribution, Poisson RVs have variance
equal to their mean, but lots of empirical count datasets exhibit much larger
variances than that. Fix it!!)

#### Unclassified probability distributions

The heights example (a mixture of Gaussians) is a good one to call back to: you
can mix and match and combine all these, to the point that the set of
distributions worth considering is unenumerable.

Though here are some good named distributions that didn't get a mention above:
Laplacian, Cauchy, negative binomial, gamma, beta.  We Bought A Zoo.

#### Probability distributions for error

They're coyly introducing generalized regression here, when talking about how
the observed Bernoulli RVs can be better modeled with a latent "deterministic,
plus random error" RV behind it.

#### Comparing distributions

First off, wwwwwwhat is the placebo for "percutaneous coronary intervention"?
Do they gas you with propofol and then pretend to cut you open?  *Actually* cut
you open?

I like the "how many percentile points would the modal control person move up
if they became the model treatment person," and I hope we get into Q-Q plots for
charting this kind of comparison for quantiles starting anywhere from the
1st to the 99th percentile.

### 3.6 Probability modeling

Fun fact: my vote was decisive to an election, recently!  My congressional
district had a tie for second place in our weird open primary system.
Read all about it: https://en.wikipedia.org/wiki/Evan_Low#2024_U.S._House_of_Representatives_election

(There was a recount, some people were irritated by how it got kicked off, the
recount eliminated the tie.)

Anyway, the book talks about modeling the odds of a tied election two ways:

#### Using an empirical forecast

Yow, I am confused where this "use the PDF over $n$" as an approximation that
the (binary) election of $n$ voters is tied.  PDFs only reflect probability when
you integrate them over some range.  I guess this is like a rectangle of width
$1/n$ and height given by the PDF, but why that width and that height?

I guess they don't want to get into that kind of reasoning yet -- it is more of
a pure-play probability question, than a regression question.  But I dunno; I
think we'll need to answer stuff like this later.  Like when we make use of
a vote-total-predicting election model.

From my memories of Gelman's blog, I am *less* confused by earlier advice of
just calculating the odds the election lands between 49.9% and 50.1% and then
slicing up a uniform distribution over vote totals within to answer "will there
be a tie."  Maybe these are equivalent methods?

Reading for later:

*  [A new argument for estimating the probability that your vote will be decisive](https://statmodeling.stat.columbia.edu/2024/02/05/a-new-argument-estimating-the-probability-that-your-vote-will-be-decisive/), Feb 5, 2024
*  [What is the probability your vote will make a difference? \[pdf\]](https://sites.stat.columbia.edu/gelman/research/published/probdecisive2.pdf), April 2012, featuring co-author Nate Silver!

#### Using a reasonable-seeming but inappropriate probability model

I do like thinking about the Anscombe's-Quartet style switcharoo between
"every voter has probability $p$ of voting in favor" versus "the overall vote
share is $p$% in favor."  The paragraph calls this "\[s\]ome voters are almost
certainly going to choose one candidate, others are almost certainly on the
other side[...]."  Those voters aren't $p$% likely to vote in favor; they're
locked to 0% or 100%.

I had this discussion about this kind of "let's just say they're all $p$%
likely to be clicked, since population wide $p$% of them *are* clicked"
reasoning about Google's public web index nine years ago.  It's a strong
assumption!

The closing discussion about "\[t\]he key problem in the election example is
that the binomial model does not do a good job at capturing uncertainty \[in our
estimate of $p$, even granting we're allowed to model every voter as being
$p$% likely to vote in favor\]" is why I default to Bayesian inference over
probabilistic graphical models.  I know how to account for, and propagate,
uncertrainty like that; to let uncertainty in $p$ flow to our uncertainty in
probability-of-a-tie.

#### General lessons for probability modeling

"Ultimately we should check our probability models by their empirical
implications."  I agree, and work backwards from this.  Refuse any work where
there's no ability to check the model against empirical implication.  I am
$400K poorer this year due to this agreement.

I do hope we get to something more algorithmic than "a glance at Figure 3.6(c)"
to make goodness-of-fit decisions around what distributions we choose.


## Exercises

### 3.1, Weighted averages

> A survey is conducted in a certain city regarding support for increased
> property taxes to fund schools. In this survey, higher taxes are supported by
> 50% of respondents aged 18–29, 60% of respondents aged 30–44, 40% of
> respondents aged 45–64, and 30% of respondents aged 65 and up. Assume there is
> no nonresponse.

TK

### 3.2, Weighted averages

> Continuing the previous exercise, suppose you would like to estimate the
> proportion of all adults in the population who support higher taxes, so you
> take a weighted average as in Section 3.1. Give a set of weights for the four
> age categories so that the estimated proportion who support higher taxes for
> all adults in the city is 40%.

TK

### 3.3, Probability distributions

> Using R, graph probability densities for the normal distribution, plotting
> several different curves corresponding to different choices of mean and
> standard deviation parameters.

TK

### 3.4, Probability distributions

> Using a bar plot in R, graph the Poisson distribution with parameter 3.5.

### 3.5 Probability distributions

> Using a bar plot in R, graph the binomial distribution with $n = 20$ and
> $p = 0.3$.

### 3.6 Linear transformations

> A test is graded from 0 to 50, with an average score of 35 and a standard
> deviation of 10. For comparison to other tests, it would be convenient to
> rescale to a mean of 100 and standard deviation of 15.
> 
> (a) Labeling the original test scores as $x$ and the desired rescaled test
> score as $y$, come up with a linear transformation, that is, values of $a$ and
> $b$ so that the rescaled scores $y = a + bx$ have a mean of 100 and a standard
> deviation of 15.
>
> (b) What is the range of possible values of this rescaled score y?
>
> (c) Plot the line showing $y$ vs. $x$.

TK 

### 3.7 Linear transformations

> Continuing the previous exercise, there is another linear transformation
> that also rescales the scores to have mean 100 and standard deviation 15.
> What is it, and why would you not want to use it for this purpose?

TK

### 3.8 Correlated random variables

> Suppose that the heights of husbands and wives have a correlation
> of 0.3, husbands’ heights have a distribution with mean 69.1 and standard
> deviation 2.9 inches, and wives’ heights have mean 63.7 and standard deviation
> 2.7 inches. Let $x$ and $y$ be the heights of a married couple chosen at
> random. What are the mean and standard deviation of the average height,
> $(x + y)=2$?

TK