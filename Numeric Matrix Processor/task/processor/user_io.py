import math
from typing import List, Dict, Callable, Union, Iterable
from mtx_op import MtxOp
from mtx_2d import Mtx2D
from mtx_view import MatrixView

FChoice = Callable[[], None]
FTranspose = Callable[[Mtx2D], Mtx2D]


class UserIO:
    """ Input different matrix data and output the results of matrix operations """
    err_msg = 'The operation cannot be performed.'
    no_inverse = "This matrix doesn't have an inverse."
    default_choice: FChoice = lambda: print(UserIO.err_msg)

    def __init__(self):
        self.result: str = ''
        self.main_choice_fn_dic: Dict[int, FChoice] = {
            0: lambda: None,
            1: self.add_matrices,
            2: self.multiply_matrix_by_scalar,
            3: self.multiply_matrices,
            4: self.transpose_matrices,
            5: self.calculate_determinant,
            6: self.invert_matrix
        }
        self.trans_choice_fn_dic: Dict[int, FTranspose] = {
            1: MtxOp.main_diagonal_transposition,
            2: MtxOp.side_diagonal_transposition,
            3: MtxOp.vert_line_transposition,
            4: MtxOp.horz_line_transposition,
        }
        self.mtx_is_int = True
        self.main()

    def main(self):
        choice = -1
        while choice != 0:
            self.mtx_is_int = True
            if self.result:
                print(self.result, end='\n\n')
            choice = self.input_main_choice()
            self.main_choice_fn_dic.get(choice, UserIO.default_choice)()

    @staticmethod
    def input_main_choice() -> int:
        return int(input('''\
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit
Your choice: '''))

    @staticmethod
    def input_transpose_choice() -> int:
        return int(input('''
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line
Your choice: '''))

    def add_matrices(self):
        matrices = self.input_2_matrices()
        self.result = UserIO.err_msg if not MtxOp.can_add_matrices(*matrices) \
            else self.mtx_to_str(MtxOp.sum_of_matrices(*matrices))

    def multiply_matrix_by_scalar(self):
        m = self.input_matrix()
        scalar = self.input_constant()
        self.mtx_is_int = self.mtx_is_int and scalar.is_integer()
        self.result = self.mtx_to_str(MtxOp.multiply_matrix_by_scalar(m, scalar))

    def multiply_matrices(self):
        matrices = self.input_2_matrices()
        self.result = UserIO.err_msg if not MtxOp.can_multiply_matrix_by_matrix(*matrices) \
            else self.mtx_to_str(MtxOp.multiply_matrix_by_matrix(*matrices))

    def transpose_matrices(self):
        t_choice = self.input_transpose_choice()
        self.result = self.mtx_to_str(
            self.trans_choice_fn_dic.get(t_choice)(self.input_matrix())
        )

    def calculate_determinant(self):
        m = self.input_matrix()
        self.result = UserIO.err_msg if len(m) != len(m[0]) \
            else (int if self.mtx_is_int else float)(MatrixView(m).determinant())

    def invert_matrix(self):
        m = self.input_matrix()
        inverse = MtxOp.invert_matrix(m)
        if inverse:
            self.mtx_is_int = self.is_int(inverse)
        self.result = self.mtx_to_str(inverse) if inverse else self.no_inverse

    @staticmethod
    def is_int(m: Mtx2D) -> bool:
        return all(all(x.is_integer() for x in row) for row in m)

    def input_2_matrices(self) -> (Mtx2D, Mtx2D):
        return self.input_matrix('first '), self.input_matrix('second '),

    def input_matrix(self, mtx_ord='') -> Mtx2D:
        lines = self.input_int_row(mtx_ord)[0]
        print(f'Enter {mtx_ord}matrix:')
        m = [list(map(float, input().split(' '))) for _ in range(lines)]
        self.mtx_is_int = self.mtx_is_int and self.is_int(m)
        return m

    @staticmethod
    def input_int_row(mtx_ord='') -> List[int]:
        return list(map(int, input(f'Enter size of {mtx_ord}matrix: ').split(' ')))

    @staticmethod
    def input_constant() -> float:
        return float(input('Enter constant: '))

    def mtx_to_str(self, m: Mtx2D) -> str:
        """ Convert a matrix to a string representation"""
        num_map_fn = int if self.mtx_is_int else float
        return 'The result is:\n' + '\n'.join(' '.join(UserIO.convert_row(row, num_map_fn)) for row in m)

    @staticmethod
    def convert_row(row: List[Union[float, int]], num_map_fn) -> Iterable[str]:
        return map(lambda x: '0' if x == 0 else str(x), map(num_map_fn, row))
