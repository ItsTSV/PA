import numba as nb
import numpy as np
import pandas as pd
import scipy as sp
import time


# Read data from csv file to pandas data frame, then transform it to numpy array so Numba can work with it
def read_data(filename):
    data = pd.read_csv(filename)
    data = data.iloc[:, 1:].values.astype(np.float64)
    return data


# Calculate similarity matrix
@nb.njit(parallel=True, fastmath=True)
def calculate_similarity_matrix(data):
    # Init similarity matrix
    S = np.zeros((data.shape[0], data.shape[0]))

    # Parallely calculate the
    for i in nb.prange(data.shape[0]):
        for j in range(data.shape[0]):
            S[i, j] = -np.linalg.norm(data[i] - data[j])

    # Calculate median (or perhaps min? I'll have to find out tomorrow, lol)
    median = np.median(S)

    # Add median value to diagonal
    for i in nb.prange(data.shape[0]):
        S[i, i] = median

    return S


@nb.njit(parallel=True, fastmath=True)
def run_affinity_propagation(similarity, max_iter=20, convergence_iter=3):
    # Create Responsibility (R) and Availability (A) matrices
    size = similarity.shape[0]
    R = np.zeros_like(similarity)
    A = np.zeros_like(similarity)

    for iteration in range(max_iter):
        print("Miluju PA")

    return R, A


if __name__ == '__main__':
    # Load data
    start = time.time()
    data = read_data('data/participants.csv')
    end = time.time()
    print(f"Loading done in {end - start} seconds")

    # Calculate similarity matrix
    start = time.time()
    S = calculate_similarity_matrix(data)
    end = time.time()
    print(f"Similarity matrix calculated in {end - start} seconds")

    # Run Affinity Propagation
    start = time.time()
    responsibility, availability = run_affinity_propagation(S)
    end = time.time()
    print(f"Affinity Propagation done in {end - start} seconds")

    print(f"Responsibility: {responsibility}")
    print(f"Availability: {availability}")
