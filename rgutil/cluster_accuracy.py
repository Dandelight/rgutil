# Copyright (c) 2016, Members of the Paris Machine Learning for Data Science (MLDS) team, François Role, Stanislas Morbieu.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



"""
The :mod:`coclust.evaluation.external` module provides functions
to evaluate clustering or co-clustering results with external information
such as the true labeling of the clusters.

File imported from:

https://github.com/franrole/cclust_package/blob/v0.2.1/coclust/evaluation/external.py

"""


import numpy as np
from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment
from pgm import core_match


def cluster_accuracy(true_row_labels, predicted_row_labels):
    r"""Compute accuracy for Clustering algorithms.

    For a classification model, Accuracy(y, y') := \sum_{i=0}^{n-1} 1(y' = y)

    For a clustering model, we have

       Accuracy(y, y') := \max_{p \in P} \sum_{i=0}^{n-1} 1(perm(y) = y')

    where P is the set of all permutations of [1; K] where K is the number of clusters.

    Parameters
    ----------
    true_row_labels: array-like
        The true row labels, given as external information
    predicted_row_labels: array-like
        The row labels predicted by the model

    Returns
    -------
    float
        Best value of accuracy
    """

    cm = confusion_matrix(true_row_labels, predicted_row_labels)
    # 这一步没必要用PGM，因为是方阵，一次就够
    indices = core_match(_make_cost_m(cm))
    total = 0
    for row, column in indices:
        value = cm[row][column]
        total += value

    return (total * 1. / np.sum(cm))


def _make_cost_m(cm):
    """
    return max(cm) - cm
    """
    s = np.max(cm)
    return (- cm + s)
