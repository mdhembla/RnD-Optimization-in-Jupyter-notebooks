## Optimizations in Jupyter Notebooks - R&D Project 
### CS 485 - Guide: Prof. Manas Thakur
This project was focused on exploring optimizations in Jupyter Notebooks. Python notebooks are
widely used for data science applications and in ML. Unlike standard programs, they offer a unique
challenge when attempting code optimization - the ability for user to execute code cells in any order.
Add to that the wide range of libraries and task-specific syntax characteristic of ML codes written
in python, a generalized optimizer is a tough ask - but this project aims to lay the foundation for
such a technique. We focus on data-science notebooks from popular kaggle competitions (obtained
using the ‘hotness’ metric) that use PyTorch and Tensorflow libraries. They are both widely used
for several ML tasks since tensors can support multimodal data - numerical/images/files etc.

In the scope of this project - I worked on understanding jupyter notebooks and the associated
metadata with each cell, compiling each cell to a corresponding python function that is called when
the cell is executed and maintaining a global symbol table that syncs variable values across cells. The
motivation for this is possibility of inter-cell optimizations by combining the cell-specific functions
using execution order trends and isolated/dependent cell analysis

