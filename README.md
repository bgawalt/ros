# Notes on "Regression and Other Stories"

I organized a reading group for
["Regression and Other Stories"](https://avehtari.github.io/ROS-Examples/) a
statistics textbook by Andrew Gelman, Jennifer Hill, and Aki Vehtari. This repo
contains my notes on the reading, chapter by chapter, as well as any demo
scripts I wrote to explore the material.

The book is built around the programming language R, but I will be using Python
throughout, esp. Jupyter notebooks.

## Chapter Notes

*  [Chapter 1](./chapter01.md): Overview
*  [Chapter 2](./chapter02.md): Data and measurement
*  [Chapter 3](./chapter03.md): Some basic methods in mathematics and probability

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
$ source venv/jupyter/bin/activate
$ jupyter notebook --port 9999
```

I use that manually-specific port to avoid colliding with Pelican (my
static-site blogging software) on :8888.

More details: https://docs.jupyter.org/en/latest/running.html
