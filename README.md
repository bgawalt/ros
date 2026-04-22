# Notes on "Regression and Other Stories"

I organized a reading group for
["Regression and Other Stories"](https://avehtari.github.io/ROS-Examples/) a
statistics textbook by Andrew Gelman, Jennifer Hill, and Aki Vehtari. This repo
contains my notes on the reading, chapter by chapter, as well as any demo
scripts I wrote to explore the material.

The book is built around the programming language R, but I will be using Python
throughout, esp. Jupyter notebooks.


## Chapter Notes

*  Part 1: Fundamentals
    *  [Chapter 1](./chapter01.md): Overview
    *  [Chapter 2](./chapter02.md): Data and measurement
    *  [Chapter 3](./chapter03.md): Some basic methods in mathematics and probability
    *  [Chapter 4](./chapter04.md): Statistical inference
    *  [Chapter 5](./chapter05.md): Simulation
*  Part 2: Linear Regression
    *  [Chapter 6](./chapter06.md): Background on regression modeling
    *  [Chapter 7](./chapter07.md): Linear regression with a single predictor
    *  [Chapter 8](./chapter08.md): Fitting regression models
    *  [Chapter 9](./chapter09.md): Prediction and Bayesian inference
    *  [Chapter 10](./chapter10.md): Linear regression with multiple predictors
    *  [Chapter 11](./chapter11.md): Assumptions, diagnostics, and model evaluation
    *  [Chapter 12](./chapter12.md): Transformations and regression
*  Part 3: Generalized linear models
    *  [Chapter 13](./chapter13.md): Logistic regression
    *  [Chapter 14](./chapter14.md): Working with logistic regression
    *  [Chapter 15](./chapter15.md): Other generalized linear models


## Jupyter and Bambi

The exercises I completed were done using
[Bambi](https://bambinos.github.io/bambi/) as the Bayesian inference engine,
inside [Jupyter](https://jupyter.org/) notebooks.

Originally I could skate by with a virtualenv and `pip install`ing Bambi, but,
when I upgraded to Python 3.14 I got bit by some C++ compiler bugs.  I had to
bite the bullet and use
[Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
instead.

The steps I took were guided by the above Conda link, and looked like:

Download the [Miniconda mini-installer](https://docs.anaconda.com/miniconda/)
for
[my Linux (well, WSL) OS](https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install):

```
$ curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Run that downloaded installer:

```
$ bash ~/Miniconda3-latest-Linux-x86_64.sh
```

Which responded with (among lots of other text):

> Miniconda3 will now be installed into this location:
> /home/bgawalt/miniconda3

From there, I set up the Conda environment for this project:

```
$ conda create --name ros_conda scipy numpy jupyter matplotlib
$ conda install -c conda-forge bambi
```

That last line was from the Bambi "Getting Started" guide.  (I tried just
stuffing `bambi` into that list of args alongside `scipy` and `numpy` but that
didn't work.  But the second line did, so, cool.)

Back when I was on Python 3.10 and using flat virtualenvs and `pip` to install
the Bambi module, I needed to install `g++` and `python3-dev` in order for
the NUTS chain sampler to run at tolerable speed:

```shell
$ sudo apt-get update
$ sudo apt install python3-dev
$ sudo apt install g++
```

This made chain sampling go 100x faster.  These are still around, but, I suspect
they're now ignored in favor of what's been compiled inside the Conda
environment.

When it's time to write more exercises, I launch the Jupyter backend
(always from the root dir of this repo) with:

```shell
$ conda activate ros_conda; \
cd ~/ros; \
jupyter notebook --port 9999
```

I use that manually-specific port to avoid colliding with Pelican (my
static-site blogging software) on :8888.

More details: https://docs.jupyter.org/en/latest/running.html
