def hungarian(cost_matrix):
    import copy
    matrix = copy.deepcopy(cost_matrix)
    size = len(matrix)

    # Row Reduction
    for row in range(size):
        min_value = min(matrix[row])
        for col in range(size):
            matrix[row][col] -= min_value

    # Column Reduction
    for col in range(size):
        min_value = min(matrix[row][col] for row in range(size))
        for row in range(size):
            matrix[row][col] -= min_value

    # Greedy Star Zeroes
    starred = [[False] * size for _ in range(size)]
    covered_rows = [False] * size
    covered_columns = [False] * size

    for row in range(size):
        for col in range(size):
            if (
                matrix[row][col] == 0
                and not covered_rows[row]
                and not covered_columns[col]
            ):
                starred[row][col] = True
                covered_rows[row] = True
                covered_columns[col] = True

    # Extract Assignment
    assignment = []
    for row in range(size):
        if True in starred[row]:
            col = starred[row].index(True)
        else:
            col = matrix[row].index(min(matrix[row]))
        assignment.append((row, col))

    return assignment


if __name__ == '__main__':
    costs = [
        [4, 1, 3],
        [2, 0, 5],
        [3, 2, 2]
    ]

    print(hungarian(costs))
