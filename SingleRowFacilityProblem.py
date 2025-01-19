import itertools as it
import multiprocessing as mp
import time as t


# Open file and read data
def read_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        w = list(map(int, lines[1].strip().split()))
        m = [[int(x) for x in line.strip().split()] for line in lines[2:]]

    return n, w, m


# Calculate distance between two devices based on d(pi1, pi2) equation
def calculate_distance(permutation, widths, i, j):
    # Base of the equation
    device1 = permutation[i]
    device2 = permutation[j]
    distance = (widths[device1] + widths[device2]) / 2

    # The sum part
    for k in range(i, j + 1):
        distance += widths[permutation[k]]

    return distance


# Calculate total distance of a permutation
def calculate_total_distance(permutation, widths, matrix):
    total_distance = 0
    for i in range(0, len(permutation)):
        for j in range(i + 1, len(permutation)):
            # Get devices so no indexing hell happens and matrix is correctly used
            device1 = permutation[i]
            device2 = permutation[j]
            if device1 > device2:
                device1, device2 = device2, device1

            add_distance = matrix[device1][device2] * calculate_distance(permutation, widths, i, j)
            total_distance += add_distance

    return total_distance


# Branch and bound algorithm for Single Row Facility Location Problem
def branch_and_bound_srflp(pref, n, matrix, widths, best_dist, best_perm):
    # Generate permutation without preferred device
    perm = [a for a in range(1, n) if a != pref]

    # Function that estimates lower bound (based on which will the branches be cut)
    def lower_bound(partial_perm, remaining):
        bound = 0
        # Cost of already existing part of the permutation
        for i in range(len(partial_perm)):
            for j in range(i + 1, len(partial_perm)):
                device1 = partial_perm[i]
                device2 = partial_perm[j]
                if device1 > device2:
                    device1, device2 = device2, device1
                bound += matrix[device1][device2] * calculate_distance(partial_perm, widths, i, j)

        # Estimated cost of the rest of the permutation
        for i, device in enumerate(remaining):
            for j in range(i + 1, len(remaining)):
                device1 = remaining[i]
                device2 = remaining[j]
                if device1 > device2:
                    device1, device2 = device2, device1
                bound += matrix[device1][device2] * (widths[device1] + widths[device2]) / 2

        return bound

    for p in it.permutations(perm):
        full_perm = [0, pref] + list(p)
        remaining = [x for x in range(n) if x not in full_perm]

        # Compute lower bound, cut the branch if it's bigger than the best distance
        lb = lower_bound(full_perm, remaining)
        if lb >= best_dist.value:
            continue

        # If it's not bigger, calculate the total distance and check if it's the best one
        dist = calculate_total_distance(full_perm, widths, matrix)
        if dist < best_dist.value:
            best_dist.value = dist
            for i, val in enumerate(full_perm):
                best_perm[i] = val


if __name__ == "__main__":
    # Read data
    size, widths, matrix = read_file("data/srflp.txt")

    # Init multiprocessing and shared variables
    manager = mp.Manager()
    best_dist = manager.Value('d', float("inf"))
    best_perm = manager.Array('i', range(size))

    # Start with 8 processes, measure time (it's slow, cuz it's Python :/)
    start = t.time()
    with mp.Pool(processes=8) as p:
        p.starmap(
            branch_and_bound_srflp,
            zip(range(1, size), it.repeat(size), it.repeat(matrix), it.repeat(widths), it.repeat(best_dist),
                it.repeat(best_perm))
        )
    end = t.time()

    # Output
    print(f"Best permutation: {list(best_perm)}")
    print(f"Best distance: {best_dist.value}")
    print(f"Time: {end - start} seconds")
