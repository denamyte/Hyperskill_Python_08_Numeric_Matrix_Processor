from typing import List

Mtx2D = List[List[float]]


class MtxOp:
    """
    Check if an operation can be performed on matrices,
    perform different matrix operations.
    """

    @staticmethod
    def can_add_matrices(m1: Mtx2D, m2: Mtx2D) -> bool:
        return len(m1) > 0 and len(m1) == len(m2) and len(m1[0]) == len(m2[0])

    @staticmethod
    def sum_of_matrices(m1: Mtx2D, m2: Mtx2D) -> Mtx2D:
        return [[a + b for (a, b) in zip(row1, row2)] for (row1, row2) in zip(m1, m2)]

    @staticmethod
    def multiply_matrix_by_scalar(m: Mtx2D, scalar: float) -> Mtx2D:
        return [[x * scalar for x in row] for row in m]
