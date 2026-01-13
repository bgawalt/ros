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