from typing import List, Dict, Callable, Tuple
from mtx_op import MtxOp, Mtx2D


class UserIO:
    """ Input different matrix data and output the results of matrix operations """
    err_msg = 'The operation cannot be performed.'

    def __init__(self):
        self.result: str = ''
        self.fun_dic: Dict[int, Callable[[], None]] = {
            0: lambda: None,
            1: self.add_matrices,
            2: self.multiply_matrix_by_scalar,
            3: self.multiply_matrices
        }
        self.main()

    def main(self):
        choice = -1
        while choice != 0:
            if self.result:
                print(self.result, end='\n\n')
            choice = self.input_choice()
            self.fun_dic.get(choice, lambda: print(UserIO.err_msg))()

    @staticmethod
    def input_choice() -> int:
        return int(input('''\
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
0. Exit
Your choice: '''))

    def add_matrices(self):
        matrices = self.input_2_matrices()
        self.result = UserIO.err_msg if not MtxOp.can_add_matrices(*matrices) \
            else self.mtx_to_str(MtxOp.sum_of_matrices(*matrices))

    def multiply_matrix_by_scalar(self):
        m = self.input_matrix()
        scalar = self.input_constant()
        self.result = self.mtx_to_str(MtxOp.multiply_matrix_by_scalar(m, scalar))

    def multiply_matrices(self):
        matrices = self.input_2_matrices()
        self.result = UserIO.err_msg if not MtxOp.can_multiply_matrix_by_matrix(*matrices) \
            else self.mtx_to_str(MtxOp.multiply_matrix_by_matrix(*matrices))

    def input_2_matrices(self) -> Tuple[Mtx2D, Mtx2D]:
        return self.input_matrix('first '), self.input_matrix('second '),

    def input_matrix(self, mtx_ord='') -> Mtx2D:
        lines = self.input_int_row(mtx_ord)[0]
        print(f'Enter {mtx_ord}matrix:')
        return [list(map(float, input().split(' '))) for _ in range(lines)]

    def input_int_row(self, mtx_ord='') -> List[int]:
        return list(map(int, input(f'Enter size of {mtx_ord}matrix: ').split(' ')))

    def input_constant(self) -> float:
        return float(input('Enter constant: '))

    @staticmethod
    def mtx_to_str(m: Mtx2D, num_map_fn=float) -> str:
        """ Convert a matrix to a string representation using a specific number mapping function """
        return 'The result is:\n' + '\n'.join(' '.join(map(str, map(num_map_fn, row))) for row in m)
