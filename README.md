# Notes on "Regression and Other Stories"

I organized a reading group for
["Regression and Other Stories"](https://avehtari.github.io/ROS-Examples/) a
statistics textbook by Andrew Gelman, Jennifer Hill, and Aki Vehtari. This repo
contains my notes on the reading, chapter by chapter, as well as any demo
scripts I wrote to explore the material.

The book is built around the programming language R, but I will be using Python
throughout, esp. Jupyter notebooks.


## Chapter Notes

* Part 1: Fundamentals
    *  [Chapter 1](./chapter01.md): Overview
    *  [Chapter 2](./chapter02.md): Data and measurement
    *  [Chapter 3](./chapter03.md): Some basic methods in mathematics and probability
    *  [Chapter 4](./chapter04.md): Statistical inference
    *  [Chapter 5](./chapter05.md): Simulation
* Part 2: Linear Regression
    *  [Chapter 6](./chapter06.md): Background on regression modeling
    *  [Chapter 7](./chapter07.md): Linear regression with a single predictor
    *  [Chapter 8](./chapter08.md): Fitting regression models
    *  [Chapter 9](./chapter09.md): Prediction and Bayesian inference


## Jupyter

I set up a virtual environment for running a notebook server locally.

Setup the environment with:

```shell
$ python3 -m venv venv/jupyter
```

Installed Jupyter with:

```shell
$ cd ~
$ source venv/jupyter/bin/activate
$ pip3 install jupyter
$ pip3 install matplotlib
```

Ran the backend (always from the root dir of this repo) with:

```shell
$ source ~/venv/jupyter/bin/activate; \
cd ~/ros; \
jupyter notebook --port 9999
```

I use that manually-specific port to avoid colliding with Pelican (my
static-site blogging software) on :8888.

More details: https://docs.jupyter.org/en/latest/running.html
