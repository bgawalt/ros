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

## 3.1, Weighted averages

"To take a weighted average, you have to use the right weights."  Seems obvious,
I'm sure there's constant high-profile goofs of this, though.

## 3.2, Vectors and matrices

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

## 3.3, Graphing a line

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

## 3.4, Exponential and power-law growth and decline; logarithmic and log-log relationships

The world population growth model gets a caveat about how doubling every 50
years is "not an accurate description, just a crude approximation."  Linear
algebra didn't get the same courtesy that human-population studies does here!

I've worked out the semilog and log-log translations a bunch of times and it's
always fun.  So I won't try committing it to memory, I'll just have fun
re-deriving it if I ever need to.

(I hope this book talks about the difference between fitting a semilog/log-log
model directly, vs. fitting a slope and intercept to log-transformed data.)

