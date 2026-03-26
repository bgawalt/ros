"""Brian Gawalt's library for Regression and Other Stories."""

import textwrap

import arviz

from matplotlib import pyplot


def linregress_predict(lm, x_new: float) -> float:
  """Predict the outcome for `a + b*x_new` via the `stats.linregress` model."""
  return lm.intercept + lm.slope * x_new


def linregress_markdown(lm) -> str:
  """Return a Markdown table summarizing a `stats.linregress` model fit."""
  return textwrap.dedent(
    f"""\
    Coef.     | Mean | s.e.
    --------- | ---- | -----
    Intercept | {lm.intercept:0.2f} | {lm.intercept_stderr:0.2f}
    slope     | {lm.slope:0.2f} | {lm.stderr:0.2f}
    """
  )


def linregress_plot(
    ax: pyplot.Axes,
    lm,
    lo: float | None = None,
    hi: float | None = None,
    style: str = 'r-',
    label: str | None = None,
    ):
  """Adds `stats.linregress` model's trendline to a plot."""
  if lo is None:
    lo = 1.05 * ax.get_xlim()[0]
  if hi is None:
    hi = 0.95 * ax.get_xlim()[1]
  if lo >= hi:
    raise ValueError(f'lo must be less than hi (got lo = {lo}; hi = {hi})')
  ax.plot(
    [lo, hi],
    [linregress_predict(lm, lo), linregress_predict(lm, hi)],
    style,
    label=label,
  )
  return


def bambi_markdown(
    model_fit: arviz.data.inference_data.InferenceData,
    predictors: list[str]
    ) -> str:
  """Returns a Markdown table of the mean and s.e. for the linear model."""
  summ = arviz.summary(model_fit)
  sig_mu = summ["mean"]["sigma"]
  sig_se = summ["sd"]["sigma"]
  int_mu = summ["mean"]["Intercept"]
  int_se = summ["sd"]["Intercept"]
  out = textwrap.dedent(f"""\
    Coef.     | Mean   | s.e.
    --------- | ------ | ------
    sigma     | {sig_mu:0.2f} | {sig_se:0.2f}
    Intercept | {int_mu:0.2f} | {int_se:0.2f}
    """
  )
  just_len = max(len(p) for p in (predictors + ["Intercept",]))
  for pred in predictors:
    justname = pred.ljust(just_len)
    mu = summ["mean"][pred]
    se = summ["sd"][pred]
    out += f"{justname} | {mu:0.2f} | {se:0.2f}\n"
  return out