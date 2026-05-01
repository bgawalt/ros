"""Brian Gawalt's library for Regression and Other Stories."""

import csv
import itertools
import textwrap
import typing

from collections import abc

import arviz
import numpy
import pandas

from matplotlib import pyplot
from scipy import stats


class PRNGBuilder:
  """Build new numpy default RNGs from seed phrases."""

  def __init__(self, base_seed: str):
    self._base_seed = base_seed
  
  def new(self, seed: str) -> numpy.random.Generator:
    seed_int = abs(hash(self._base_seed + seed) % (2 **32))
    return numpy.random.default_rng(seed_int)


_HIBBS_DAT = '''year growth vote inc_party_candidate other_candidate
1952 2.4 44.6 "Stevenson" "Eisenhower"
1956 2.89 57.76 "Eisenhower" "Stevenson"
1960 .85 49.91 "Nixon" "Kennedy"
1964 4.21 61.34 "Johnson" "Goldwater"
1968 3.02 49.60 "Humphrey" "Nixon"
1972 3.62 61.79 "Nixon" "McGovern"
1976 1.08 48.95 "Ford" "Carter"
1980 -.39 44.70 "Carter" "Reagan"
1984 3.86 59.17 "Reagan" "Mondale"
1988 2.27 53.94 "Bush, Sr." "Dukakis"
1992 .38 46.55 "Bush, Sr." "Clinton"
1996 1.04 54.74 "Clinton" "Dole"
2000 2.36 50.27 "Gore" "Bush, Jr."
2004 1.72 51.24 "Bush, Jr." "Kerry"
2008 .1 46.32 "McCain" "Obama"
2012 .95 52.00 "Obama" "Romney"'''


# https://www.investopedia.com/inflation-rate-by-year-7253832
_HIBBS_INFLATION = {
  1952: 0.8,
  1956: 3,
  1960: 1.4,
  1964: 1,
  1968: 4.7,
  1972: 3.4,
  1976: 4.9,
  1980: 12.5,
  1984: 3.9,
  1988: 4.4,
  1992: 2.9,
  1996: 3.3,
  2000: 3.4,
  2004: 3.3,
  2008: 0.1,
  2012: 1.7,
}


# From FRED's US UNRATE, https://fred.stlouisfed.org/series/UNRATE
# Always the Nov 1 entry.
_HIBBS_UNEMP = {
  1952: 2.8,
  1956: 4.3,
  1960: 6.1,
  1964: 4.8,
  1968: 3.4,
  1972: 5.3,  
  1976: 7.8,
  1980: 7.5,
  1984: 7.2,
  1988: 5.3,
  1992: 7.4,
  1996: 5.4,
  2000: 3.9,
  2004: 5.4,
  2008: 6.8,
  2012: 7.7,
}


# From FRED's US Interest Rate, Discount rate; always the Nov. 1 entry.
# https://fred.stlouisfed.org/series/INTDSRUSM193N
_HIBBS_INTEREST = {
  1952: 1.75,
  1956: 3.00,
  1960: 3.00,
  1964: 3.62,
  1968: 5.25,
  1972: 4.50,
  1976: 5.43,
  1980: 11.47,
  1984: 8.83,
  1988: 6.50,
  1992: 3.00,
  1996: 5.00,
  2000: 6.00,
  2004: 3.00,
  2008: 1.25,
  2012: 0.75,
}


def hibbs_df(
    with_inflation: bool = False,
    with_unemp: bool = False,
    with_interest: bool = False
    ) -> pandas.DataFrame:
  """Returns the Hibbs election-economy dataset."""
  votes = []
  years = []
  growths = []
  infls = []
  unemps = []
  inters = []
  for line in _HIBBS_DAT.split('\n')[1:]:
    spline = line.split()
    year = int(spline[0])
    years.append(year)
    growths.append(float(spline[1]))
    votes.append(float(spline[2]))
    if with_inflation:
      infls.append(_HIBBS_INFLATION[year])
    if with_unemp:
      unemps.append(_HIBBS_UNEMP[year])
    if with_interest:
      inters.append(_HIBBS_INTEREST[year])
    
  data = {
    'year': years,
    'growth': growths,
    'vote': votes,
  }
  if with_inflation:
    data['inflation'] = infls
  if with_unemp:
    data['unemp'] = unemps
  if with_interest:
    data['interest'] = inters

  return pandas.DataFrame(data=data)


def census_df() -> pandas.DataFrame:
  with open('/home/bgawalt/ros/datasets/census_age_race_sex.csv') as csvfile:
    rows = list(csv.DictReader(csvfile))
  ages = []
  males = []
  races = []
  counts = []
  for row in rows:
    race_sex = row['race_sex']
    sprace_sex = race_sex.split('_')
    assert len(sprace_sex) == 2
    race, sex = sprace_sex
    races.append(race)
    males.append(1 if sex == 'male' else 0)
    ages.append(row['age'])
    counts.append(int(row['count'].replace(',', '')))
  return pandas.DataFrame(data={
    'race': races,
    'age': ages,
    'male': males,
    'counts': counts,
  })


class DATFileParser:
  """Parses the non-CSV text files that seem built for R into Pandas."""

  def __init__(self, path: str):
    with open(path, 'rt') as infile:
      lines = infile.readlines()
    self._fields = tuple(f.strip('"') for f in lines[0].split())
    self._field_col = {field: i for i, field in enumerate(self._fields)}
    self._table = tuple(tuple(line.split()[1:]) for line in lines[1:])
    for row_id, row in enumerate(self._table):
      assert len(row) == len(self._fields), (
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


def dataframe_describe_markdown(
    df: pandas.DataFrame,
    columns: abc.Sequence[str] = list()
    ) -> str:
    """Describes a DataFrame with a Markdown table.
    
    If you pass in a non-empty set of column names, the table will only describe
    those columns.  (If you leave it empty, it assumes you want all columns
    described.)
    """
    desc = df.describe()
    cols = columns if columns else desc.columns
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
  int_mu = summ["mean"].get("Intercept", float('nan'))
  int_se = summ["sd"].get("Intercept", float('nan'))
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


def bambi_flatten(
    model_fit: arviz.data.inference_data.InferenceData,
    predictors: abc.Sequence[str],
    num_chains: int = 4,
    ) -> dict[str, tuple[float]]:
  """Returns coefficent samples of the form {pred: (coefs, ...)}."""
  out = {pred: [] for pred in predictors}
  for chain in range(num_chains):
    sims = model_fit.posterior.sel(chain=chain).to_dataframe()
    for _, row in sims.iterrows():
      for pred in predictors:
        out[pred].append(row[pred])
  return {k: tuple(v) for k, v in out.items()}


def plot_ridge(
    ax: pyplot.Axes,
    model_fit: arviz.data.inference_data.InferenceData,
    predictors: abc.Sequence[str],
    num_chains: int = 4,
    color: str = 'b',
    ):
  flat = bambi_flatten(model_fit, predictors, num_chains)
  bell_height = 0.7
  for i, pred in enumerate(predictors):
    vals = flat[pred]
    kde = stats.gaussian_kde(vals)
    mu = numpy.mean(vals)
    se = numpy.std(vals)
    xs = numpy.arange(mu - 3 * se, mu + 3 * se, 0.01)
    ys_raw = kde.evaluate(xs)
    scale = bell_height / max(ys_raw)
    ys = i + scale * ys_raw

    iqr = numpy.quantile(vals, [0.25, 0.75])
    iqr_xs = numpy.arange(iqr[0], iqr[1], 0.01)
    iqr_ys_raw = kde.evaluate(iqr_xs)
    iqr_ys = i + scale * iqr_ys_raw
    ax.fill_between(iqr_xs, [i for _ in iqr_xs], iqr_ys, color=color, alpha=0.3)
    ax.plot([min(xs), max(xs)], [i, i], linestyle='-', color=color)
    ax.plot(
      [mu, mu],
      [i, i + scale * (kde.evaluate(mu)[0])],
      linestyle='-',
      color=color
    )
    ax.plot(xs, ys, linestyle='-', color=color)
  ax.set_yticks([i for i in range(len(predictors))], predictors)
  ax.grid()
  ax.axvline(x=0, linestyle='--', color='k', zorder=100, alpha=0.5)
  ax.set_axisbelow(True)
  ax.set_xlabel('Coefficient estimate')
  ax.set_ylim(-0.2, len(predictors) - 1 + bell_height + 0.2)