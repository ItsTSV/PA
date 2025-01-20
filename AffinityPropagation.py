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
    # Init similarity matrix and helper variables
    n_samples = data.shape[0]
    S = np.zeros((n_samples, n_samples))
    non_diagonal_values = [0]

    # Parallely calculate the similarity matrix
    for i in nb.prange(n_samples):
        for j in range(i + 1):
            S[i, j] = -np.sum((data[i] - data[j]) ** 2)
            S[j, i] = S[i, j]

    # Find minimum non-diagonal value
    for i in range(n_samples):
        for j in range(n_samples):
            if i != j:
                non_diagonal_values.append(S[i, j])

    minimum = np.min(np.array(non_diagonal_values))
    for i in nb.prange(n_samples):
        S[i, i] = minimum

    return S


@nb.njit(parallel=True, fastmath=True)
def run_affinity_propagation(similarity, max_iter=1):
    # Init matrices
    size = similarity.shape[0]
    R = np.zeros_like(similarity)
    A = np.zeros_like(similarity)
    C = np.zeros_like(similarity)

    for iteration in range(max_iter):
        # Update responsibility matrix R -- First equation
        for i in nb.prange(size):
            for k in range(size):
                max_val = -np.inf
                for k_ in range(size):
                    # Working with k_, not k! I kept debugging this goddamned miss for like two hours -_-
                    if k != k_ and A[i, k_] + similarity[i, k_] > max_val:
                        max_val = A[i, k_] + similarity[i, k_]
                R[i, k] = similarity[i, k] - max_val

        # Update availability matrix -- Second and Third equations
        for i in nb.prange(size):
            for k in range(size):
                sum_val = 0.0
                for i_ in range(size):
                    if i != i_:
                        sum_val += max(0, R[i_, k])
                if i != k:
                    A[i, k] = min(0, R[k, k] + sum_val)
                else:
                    A[i, k] = sum_val

        # Update criterion matrix -- track if it changes
        final = True
        for i in nb.prange(size):
            for j in range(size):
                new_val = A[i, j] + R[i, j]
                if new_val != C[i, j]:
                    final = False
                C[i, j] = new_val

        # If it does not change, we're done, yey.
        if final:
            break

    return C


def run_clustering(C):
    # Dictionary to store clusters and number of rows
    clusters = {}
    rows = C.shape[0]

    # Find clusters
    for row in range(rows):
        # Maximum element -- cluster_id
        cluster_id = int(np.argmax(C[row]))

        # If cluster_id is not in the dictionary, add it
        if cluster_id not in clusters:
            clusters[cluster_id] = []

        # And append the cluster. Finally.
        clusters[cluster_id].append(row)

    return clusters


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
    criterion = run_affinity_propagation(S)
    end = time.time()
    print(f"Affinity Propagation done in {end - start} seconds")

    # Run Clustering
    start = time.time()
    clusters = run_clustering(criterion)
    end = time.time()
    print(f"Clustering done in {end - start} seconds")

    print("Criterion matrix:\n", criterion)
    print("Clusters:\n", clusters)
