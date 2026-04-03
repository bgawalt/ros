"""Brian Gawalt's library for Regression and Other Stories."""

import itertools
import textwrap
import typing

from collections import abc

import arviz
import pandas

from matplotlib import pyplot


class DATFileParser:
  """Parses the non-CSV text files that seem built for R into Pandas."""

  def __init__(self, path: str):
    with open(path, 'rt') as infile:
      lines = infile.readlines()
    self._fields = tuple(f.strip('"') for f in lines[0].split())
    self._field_col = {field: i for i, field in enumerate(self._fields)}
    self._table = tuple(tuple(line.split()[1:]) for line in lines[1:])
    for row_id, row in enumerate(self._table):
      assert(len(row) == len(self._fields) for row in self._table), (
        f"Bad row length for row id {row_id}"
      )
    self._int_filters = {}
    self._float_filters = {}

  @property
  def fields(self) -> tuple[str, ...]:
    return self._fields
  
  def add_int_filter(self, field: str, filter: typing.Callable[[int], bool]):
    """Retain rows where the predicate is true for the given int field."""
    field_id = self._field_col[field]
    if field_id not in self._int_filters:
      self._int_filters[field_id] = []
    self._int_filters[field_id].append(filter)
  
  def add_float_filter(
      self,
      field: str,
      filter: typing.Callable[[float], bool]
      ):
    """Retain rows where the predicate is true for the given float field."""
    field_id = self._field_col[field]
    if field_id not in self._float_filters:
      self._float_filters[field_id] = []
    self._float_filters[field_id].append(filter)
  
  def _apply_filters(self, row: tuple[str, ...]) -> bool:
    for int_fid, filters in self._int_filters.items():
      val = int(row[int_fid])
      for filt in filters:
        if not filt(val):
          return False
    for float_fid, filters in self._float_filters.items():
      val = float(row[float_fid])
      for filt in filters:
        if not filt(val):
          return False
    return True
  
  def parse(
      self,
      int_fields: abc.Sequence[str],
      float_fields: abc.Sequence[str]
      ) -> tuple[pandas.DataFrame, dict[str, int]]:
    """Parse the DAT file into a DataFrame with the requested fields.
    
    Includes a counter for number of rows removed due to a field being "NA".
    """
    assert len(int_fields) == len(set(int_fields)), (
      "Duplicate field in `int_fields`")
    assert len(float_fields) == len(set(float_fields)), (
      "Duplicate field in `float_fields`")
    int_field_ids = tuple(self._field_col[field] for field in int_fields)
    float_field_ids = tuple(self._field_col[field] for field in float_fields)
    data = {field: [] for field in itertools.chain(int_fields, float_fields)}
    na_counts = {}
    for row_id, row in enumerate(self._table):
      if not self._apply_filters(row):
        continue
      updates = {}
      for fid, field in zip(int_field_ids, int_fields):
        if row[fid] == 'NA':
          na_counts[field] = na_counts.get(field, 0) + 1
          break
        try:
          val = int(row[fid])
        except ValueError:
          print(f'row_id {row_id} had non-int value for {field}')
          break
        updates[field] = val
      for fid, field in zip(float_field_ids, float_fields):
        if row[fid] == 'NA':
          na_counts[field] = na_counts.get(field, 0) + 1
          break
        try:
          val = float(row[fid])
        except ValueError:
          print(f'row_id {row_id} had non-float value for {field}')
          break
        updates[field] = val
      if len(updates) == len(data):
        for k, v in updates.items():
          data[k].append(v)
    return pandas.DataFrame(data=data), na_counts


def dataframe_describe_markdown(df: pandas.DataFrame) -> str:
    desc = df.describe()
    cols = desc.columns
    out = "|         | " + " | ".join(cols) + "\n"
    out += "--------- | " + " | ".join(['-' * len(col) for col in cols]) + '\n'
    quantities = [
        "count",
        "mean",
        "std",
        "min",
        "25%",
        "50%",
        "75%",
        "max",
    ]
    for q in quantities:
        bold_q = f'**{q}**'
        out += (
            f'{bold_q.ljust(9)} | ' +
            " | ".join(f'{desc[col][q]:0.2f}' for col in cols) +
            '\n'
        )            
    return out


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
    predictors: list[str],
    ) -> str:
  """Returns a Markdown table of the mean and s.e. for the linear model."""
  summ = arviz.summary(model_fit)
  just_len = max(max(len(name) for name in predictors), len('Intercept'))
  sig_mu = summ["mean"].get("sigma", float('nan'))
  sig_se = summ["sd"].get("sigma", float('nan'))
  int_mu = summ["mean"]["Intercept"]
  int_se = summ["sd"]["Intercept"]
  out = textwrap.dedent(f"""\
    {'Coef.'.ljust(just_len)} | Mean   | s.e.
    {'-' * just_len} | ------ | ------
    {'sigma'.ljust(just_len)} | {sig_mu:0.2f} | {sig_se:0.2f}
    {'Intercept'.ljust(just_len)} | {int_mu:0.2f} | {int_se:0.2f}
    """
  )
  for pred in predictors:
    justname = pred.ljust(just_len)
    mu = summ["mean"][pred]
    se = summ["sd"][pred]
    out += f"{justname} | {mu:0.2f} | {se:0.2f}\n"
  return out