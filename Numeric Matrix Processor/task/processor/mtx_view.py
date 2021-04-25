from typing import List
from mtx_op import Mtx2D


class MatrixView:
    """
    A special class containing a 2D matrix as well as information
    about available rows and columns of the matrix. "Availability" of
    particular rows and columns means that only those rows and columns
    of the matrix will be used in calculations.

    The class allows to calculate the determinant of a matrix.
    """

    def __init__(self, mtx: Mtx2D, rows: List[int] = None, cols: List[int] = None):
        self.mtx = mtx
        if rows and cols:
            self.visible_rows = rows
            self.visible_cols = cols
        else:
            self.visible_rows = list(range(len(mtx)))
            self.visible_cols = list(range(len(mtx[0])))

    def decrease_mtx_size(self, ex_row: int, ex_col: int):
        """
        Create an instance of MatrixView from an existing one, by taking away
        one row and one column from the visible rows and columns
        """
        rows = self.visible_rows[:]
        cols = self.visible_cols[:]
        rows.remove(ex_row)
        cols.remove(ex_col)
        return MatrixView(self.mtx, rows, cols)

    def determinant(self) -> float:
        m, vr, vc = self.mtx, self.visible_rows, self.visible_cols
        if len(vr) == 1:
            return m[vr[0]][vc[0]]
        if len(vr) == 2:  # [0][0] * [1][1] - [0][1] * [1][0]
            return m[vr[0]][vc[0]] * m[vr[1]][vc[1]] - m[vr[0]][vc[1]] * m[vr[1]][vc[0]]

        determ, sign, exclude_row = .0, 1, vr[0]
        for exclude_col in vc:
            cross_value = m[exclude_row][exclude_col]
            if cross_value != 0:
                determ += sign * cross_value * self.decrease_mtx_size(exclude_row, exclude_col).determinant()
            sign *= -1

        return determ
