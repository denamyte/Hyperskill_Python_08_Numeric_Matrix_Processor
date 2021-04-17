from typing import List, Dict, Callable, Tuple
from mtx_op import MtxOp, Mtx2D


FChoice = Callable[[], None]
FTranspose = Callable[[Mtx2D], Mtx2D]


class UserIO:
    """ Input different matrix data and output the results of matrix operations """
    err_msg = 'The operation cannot be performed.'
    default_choice: FChoice = lambda: print(UserIO.err_msg)

    def __init__(self):
        self.result: str = ''
        self.main_choice_fun_dic: Dict[int, FChoice] = {
            0: lambda: None,
            1: self.add_matrices,
            2: self.multiply_matrix_by_scalar,
            3: self.multiply_matrices,
            4: self.transpose_matrices,
        }
        self.trans_choice_fun_dic: Dict[int, FTranspose] = {
            1: MtxOp.main_diagonal_reflection,
            2: MtxOp.side_diagonal_reflection,
            3: MtxOp.vert_line_reflection,
            4: MtxOp.horz_line_reflection,
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
            self.main_choice_fun_dic.get(choice, UserIO.default_choice)()

    @staticmethod
    def input_main_choice() -> int:
        return int(input('''\
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
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
            self.trans_choice_fun_dic.get(t_choice)(self.input_matrix())
        )

    @staticmethod
    def is_int(m: Mtx2D) -> bool:
        return all(all(x.is_integer() for x in row) for row in m)

    def input_2_matrices(self) -> Tuple[Mtx2D, Mtx2D]:
        return self.input_matrix('first '), self.input_matrix('second '),

    def input_matrix(self, mtx_ord='') -> Mtx2D:
        lines = self.input_int_row(mtx_ord)[0]
        print(f'Enter {mtx_ord}matrix:')
        m = [list(map(float, input().split(' '))) for _ in range(lines)]
        self.mtx_is_int = self.mtx_is_int and self.is_int(m)
        return m

    def input_int_row(self, mtx_ord='') -> List[int]:
        return list(map(int, input(f'Enter size of {mtx_ord}matrix: ').split(' ')))

    def input_constant(self) -> float:
        return float(input('Enter constant: '))

    def mtx_to_str(self, m: Mtx2D) -> str:
        """ Convert a matrix to a string representation"""
        num_map_fn = int if self.mtx_is_int else float
        return 'The result is:\n' + '\n'.join(' '.join(map(str, map(lambda x: round(x, 2), map(num_map_fn, row))))
                                              for row in m)
