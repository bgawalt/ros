# Chapter 14: Working with logistic regression

[(Return to README)](./README.md)

Now that we can fit logistic regressions, we can build on them with:

*  better ways to visualize the models,
*  better interpretation of coefficients, including under linear transformation
    and interactions of features,
*  making probabilistic predictions with the models, and aggregating those
    predictions into average predictive comparisons that work as model
    summaries,
*  better evaluation methods, using binned residual plots and predictive errors,
*  better handling of sparse, discrete data.


## Subsection rundown

### 14.1, Graphing logistic regression and binary data

When $y$ is binary, scatter plotting $y$ vs. $x$ doesn't really work any more.
The dots wind up too piled on top of each other.  For univariate data, consider
binning by $x$ and plotting the proportion of $y = 1$ (i.e., mean of $y$) in
each bin.  For 2-D data, consider scatter plotting $x_2$ vs. $x_1$, with
different color dots for depending on $y$'s value.

### 14.2, Logistic regression with interactions

TK

### 14.3, Predictive simulation

TK

### 14.4, Average predictive comparisons on the probability scale

TK

### 14.5, Residuals for discrete-data regression

TK

### 14.6, Identification and separation

TK


## Exercises

Plots and computation powered by [ChapterK.ipynb](./notebooks/ChapterK.ipynb)

### K.x, Exercise italic title

> The problem statement

The answer