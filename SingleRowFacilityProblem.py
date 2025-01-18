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


# Calculate distance between two devices based on d(pi1, pi2) equation3
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
    # Generate permutation
    perm = [a for a in range(1, n) if a != pref]
    skip = False
    skip_val = None
    skip_idx = 0

    for p in it.permutations(perm):
        if skip:
            if skip_idx < len(p) and p[skip_idx] == skip_val:
                continue
            else:
                dist = calculate_total_distance([0, pref] + list(p), widths, matrix)
                if dist > best_dist.value:
                    skip_idx = int(dist) % len(p)
                    skip_val = p[skip_idx]
                else:
                    if dist < best_dist.value:
                        best_dist.value = dist
                        for i, val in enumerate([0, pref] + list(p)):
                            best_perm[i] = val
        else:
            dist = calculate_total_distance([0, pref] + list(p), widths, matrix)
            if dist > best_dist.value:
                skip_idx = int(dist) % len(p)
                skip_val = p[skip_idx]
            else:
                if dist < best_dist.value:
                    best_dist.value = dist
                    for i, val in enumerate([0, pref] + list(p)):
                        best_perm[i] = val


if __name__ == "__main__":
    # Read data
    size, widths, matrix = read_file("data/srflp.txt")

    # Mp
    manager = mp.Manager()
    best_dist = manager.Value('d', 10000.0)
    best_perm = manager.Array('i', range(size))

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
