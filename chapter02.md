# Chapter 2: Data and measurement

[(Return to README)](./README.md)

The book is about fitting lines to data, and moving from there to prediction
and causal inference.  *This* chapter, though, is about "understanding where
your numbers are coming from."  Understanding by making graphs and charts.

## Subsection rundown

### 2.1, Examining where data come from

The Human Development Index is criticized as "pretty much a map of state income
with a mysterious transformation and a catchy name."  The point of the exercise
is to point directions to explore how it *isn't* just a recapitulation of state
income. "Income vs. GDP, maybe something there?"

Re: the partisanship vs. ideology example of Figure 2.3, "even very similar
measures can answer quite different questions."  (In 2008, income predicted
partisanship much better than it did ideology, among self reports of each.)

Not accounting for those "quite different questions" means you risk drawing
invalid conclusions from your regression analysis.

### 2.2, Validity and reliability

Measurement issues arise from:

*  quantifying a "real" thing, that's difficult to measure: foreign-born
population share, daily caloric intake
*  somewhat fuzzy, how many people do you trust, how large is your
vocabulary"
*  subjective concepts, like customer satisfaction

Validity of a measure (measuring process) is "giving the right answer on average
across a wide range of plausible scenarios."  You need some source of ground
truth (in at least some environment, if not the one you're studying) and
multiple measurements taken to assess validity.  Mostly this falls back to
"ground truth is what experts give as the right answer."

Reliable measuring processes give the same value on repeated measurements:
precision and stability.  "Inter-rater reliability" is mentioned as a way of
assessing reliability.

They close by saying they prefer to include selection and non-response biases
in the family of measurement issues.

All of these are of interest when considering "larger models [that connect]
measurements to underlying relationships of interest."  That's one of the key
forms of generalization trumpeted in Chapter 1.

### 2.3, All graphs are comparisons

#### Pt. 1, through "Grids of plots," inclusive

*  The redistricting model is interesting, there's a lot going on in terms of,
   why does the partisan-coding of the redistricting only affect the intercept,
   not the slope.  Clearly for a later chapter.
*  Kinda stuck with just two continuous values in your plots: `x1` and `y`.
   Everything else is discretized into colors or small-multiple rows and
   columns.
*  The call for rich captions falls in with the theme of the book: regression is
   story telling.  There's a big emphasis on prose, beginning-middle-end,
   narrative.  The graphs aren't necessarily succinct; you are meant to go big
   with them.

#### Pt. 2, "Applying graphical principles..." and on


*  "A graph can almost always be made smaller than you think and still be
   readable.  This then leaves room for more plots on a grid."
*  When discussing "three digits are usually enough because if more were
   necessary, we would subtract out the mean first": I do wish we had a word for
   the residual left when you subtract out a mean.  I think "the deviation"
   works, but it's not standard (hah!) jargon.  Even baseball sabremetrics has
   to resort to a mouthful of syllables to say "wins above replacement."
*  Here's Figure 15.6, used as an example of "\[an\] effective graph\[\]
   showing us what a fitted model is doing," an ordinal logistic regression
   model in this case:

![Six small multiples of an ordinal logistic regression predicting outcomes in
the set {1, 2, 3} for x-axis values running from zero to 100.  Each small
multiple shows a different dynamic between the x-value (just called "Value") and
what the model recovers: (1) perfect monotonicity between x and y value; 
(2) one fuzzy and one sharp cutpoint; (3) monotonic with one outlier; (4) only
1's and 3's in the y values; (5) almost only 3's; (6) erratic/noisy data
](./fig/fig15_6.png)

*  Here's Figure 10.9, used as an example of "graph\[ing\] sets of estimated
   parameters."  I think I would try to come up with a smaller, discrete set of
   y-axis scales instead of each one being *sui generis:*

![Nine small multiples, one for each predictor included in a models predicting
party identification.  The coefficient for each predictor is plotted as a time
series in each multiple, showing how its estimate changed with each election.
](./fig/fig10_9.png)

### 2.4, Data and analysis: trends in mortality rates

This is a memorable example for me, because it gave rise to a pithy expression
that bounces around my head: "45-54 year olds are older than they used to be."
Kind of a macabre etymology, but: still useful to keep in mind.

The study itself is known to me as the "deaths of despair" paper.

Also a fun memory for me: this dataset is named `AgePeriodCohort`, which is to
my mind the decomposition from hell.  I have never performed one, and they seem
daunting.

FWIW, I have a real hard time untangling the two identically-styled lines
apart in Figure 2.11(c):

![Figure 2.11(c) from ROS, showing two time series of death rate for 45-54
non-Hispanic white people. One is the raw death rate, the other is an expected
death rate you'd see based on the age distribution of peopl 45-54 each year.
They have identical upward trends starting from around 2003.
](./fig/fig02_11c.png)

Every time the lines cross, I have to guess which one is going which direction.
I can decipher it using Figs. 2.11(a) and (b), but like: just use two distinct
styles.  Dashed lines are free.

I think this example is neat, and worth discussing in the book.  But all the
juice is in the model that extrapolates an age distribution to an expected death
rate.  It's a regression model the book hasn't discussed fitting yet.  The
section concludes with "\[t\]hese graphs demonstrate the value of this sort of
data exploration," but it's not *just* data exploration.  It's a regression
model!


## Exercises

Plots and computation powered by [Chapter02.ipynb](./notebooks/Chapter02.ipynb)

### 2.3, Data processing

>  Go to the
> [folder `Names`](https://github.com/avehtari/ROS-Examples/tree/master/Names/data)
> and make a graph similar to Figure 2.8, but for girls.

Ta-daaaa:

![26 time series of the popularity of last letters among girls' names from
1880 to 2010; the top five are A, E, N, Y, and H, the only ones to finish
above 5% in the most recent yaer.](./fig/ex02_3.png)

### 2.7, Reliability and validity

> (a) Give an example of a scenario of measurements that have validity but not
> reliability.
>
> (b) Give an example of a scenario of measurements that have reliability but
> not validity.

When I take my kids' temperature with the ear thermometer, the thing I'm after
has validity.  But the measurements are unreliable.  We got in the habit of
always doing both ears, and they can vary by a full degree-Fahrenheit.
I suspect the forehead-blaster forehead thermometer checks they got at their
daycare in the immediate post-COVID years were even less reliable.

If you're trying to measure financial precarity, and you do so by asking for
copies of paystubs or tax returns or whatever: you will very reliably observe
your subjects' income.  But that may or may not be a valid reflection of
precarity.  Some people have family money they know they can fall back on; some
people are currently grad students and have reasonable certainty that high
income is coming soon.  Stuff like that.

### 2.9, Graphing parallel time series
>  The mortality data in Section 2.4 are accessible from this site at the U.S.
> Centers for Disease Control and Prevention: wonder.cdc.gov. Download mortality
> data from this source but choose just one particular cause of death, and then
> make graphs similar to those in Section 2.4, breaking down trends in death
> rate by age, sex, and region of the country.

I chose emphysema, and downloaded three separate datasets of "compressed
mortality", for the years 1968-1978; 1979-1998; and 1999-2016.

Mortality nationwide:

![Emphysema mortality for the full US, 1968-2016
](./fig/ex02_9_emphysema_all.png)

Mortality by sex:

![Emphysema mortality for the full US, 1968-2016, broken down by sex into 'M'
or 'F'
](./fig/ex02_9_emphysema_sex.png)

Mortality by age (as bucketed by the CDC):

Mortality by age:

![Emphysema mortality for the full US, broken down by age bucket, 1968-2016
](./fig/ex02_9_emphysema_age.png)

Mortality by age and region:

![Four small multiples of emphysema mortality, one for each of four major
census regions (west, midwest, northeast, south), broken down within each by
age bucket, 1968-2016](./fig/ex02_9_emphysema_region_age.png)