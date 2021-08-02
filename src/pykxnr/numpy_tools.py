import numpy as np


def pad_to_dense(M, value=0):
    """Appends the minimal required amount of zeroes at the end of each 
     array in the jagged array `M`, such that `M` looses its jaggedness."""

    maxlen = max(len(r) for r in M)

    padded = np.empty((len(M), maxlen))
    padded.fill(value)

    for row, values in enumerate(M):
        padded[row, :len(values)] = values

    return padded
