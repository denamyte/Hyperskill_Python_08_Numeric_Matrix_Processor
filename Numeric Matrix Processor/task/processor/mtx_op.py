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

    @staticmethod
    def can_multiply_matrix_by_matrix(m1: Mtx2D, m2: Mtx2D) -> bool:
        return len(m1) > 0 and len(m1[0]) > 0 and len(m1[0]) == len(m2)

    @staticmethod
    def multiply_matrix_by_matrix(m1: Mtx2D, m2: Mtx2D) -> Mtx2D:
        m2_dr = MtxOp.main_diagonal_reflection(m2)
        # a row of m1 gets multiplied by every row of m2_dr, the result is a new matrix row
        return [[sum(v1 * v2 for v1, v2 in zip(m2_dr[m2_row_ind], m1_row)) for m2_row_ind in range(len(m2_dr))]
                for m1_row in m1]

    @staticmethod
    def side_diagonal_reflection(m: Mtx2D) -> Mtx2D:
        m = MtxOp.vert_line_reflection(m)
        m = MtxOp.main_diagonal_reflection(m)
        return MtxOp.vert_line_reflection(m)

    @staticmethod
    def main_diagonal_reflection(m: Mtx2D) -> Mtx2D:
        return [[m[row_i][col_i] for row_i in range(len(m))] for col_i in range(len(m[0]))]

    @staticmethod
    def vert_line_reflection(m: Mtx2D) -> Mtx2D:
        return [row[::-1] for row in m]

    @staticmethod
    def horz_line_reflection(m: Mtx2D) -> Mtx2D:
        return m[::-1]
