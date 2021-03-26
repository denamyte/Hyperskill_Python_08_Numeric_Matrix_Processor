from typing import List
from mtx_op import MtxOp, Mtx2D


class UserIO:
    """ Input different matrix data and output the results of matrix operations """

    def __init__(self):
        self.result: str = ''
        self.main()

    def main(self):
        self.stage1()
        print(self.result)

    def stage1(self):
        mtx_ar = [self.input_matrix() for _ in range(2)]
        self.result = 'ERROR' if not MtxOp.can_add_matrices(*mtx_ar) \
            else self.mtx_to_str_i(MtxOp.sum_of_matrices(*mtx_ar))

    def input_matrix(self) -> Mtx2D:
        lines = self.read_int_row()[0]
        return [list(map(float, input().split(' '))) for _ in range(lines)]

    def read_int_row(self) -> List[int]:
        return list(map(int, input().split(' ')))

    def mtx_to_str_i(self, m: Mtx2D) -> str:
        """ Convert a matrix to a string representation using int values """
        return '\n'.join(' '.join(map(str, map(int, row))) for row in m)
