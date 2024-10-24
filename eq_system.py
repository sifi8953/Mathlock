import random
from typing import Self, TypeVar, Any
from collections.abc import Iterable, Generator

T = TypeVar("T")


def weighted_random(seq: Iterable[tuple[T, int]]) -> T:
    '''return a random item from the first element in the tuples in seq weighted by the second element in the tuples'''
    i = sum(w for _, w in seq)
    i = random.randrange(0, i)
    for t, w in seq:
        i -= w
        if i < 0:
            return t


def parse_float(x: str) -> float:
    '''convert string to float
    \n raises ValueError if unsuccessful'''
    try:
        return float(x)
    except ValueError:
        raise ValueError("please input a number")


class OpTreeExpr:
    '''represents a real expression'''

    var_str = "xyzabcduvw"  # characters to use as variable names
    # valid operations and their random weight
    opers = {"add": 10, "sub": 5, "mul": 10, "div": 2}
    const_range = (-5, 10)  # range of parts in constants
    val_range = (-50, 100)  # range of values of expression

    def __init__(self, op: str, *args: Any):
        self.op = op
        self.index: int | None = None
        self.val: float | None = None
        self.left: OpTreeExpr | None = None
        self.right: OpTreeExpr | None = None

        match self.op:
            case "var":  # variable
                self.index = args[0]
            case "const":  # constant
                self.val = args[0]
            case _:  # operator
                self.left = args[0]
                self.right = args[1]

    def transformations(self) -> Generator[Self, None, None]:
        if self.op in ("var", "const"):  # cannot be transformed
            return

        # combine constants
        if self.left.op == "const" and self.right.op == "const":
            yield OpTreeExpr("const", self(()))

    def __call__(self, var: tuple[float]) -> float:
        '''evaluates the expression'''
        match self.op:
            case "var":
                return var[self.index]
            case "const":
                return self.val
            case "add":
                return self.left(var) + self.right(var)
            case "sub":
                return self.left(var) - self.right(var)
            case "mul":
                return self.left(var) * self.right(var)
            case "div":
                return self.left(var) / self.right(var)

    def __str__(self) -> str:
        '''represent expression as a string'''
        match self.op:
            case "var":
                return OpTreeExpr.var_str[self.index]
            case "const":
                return self.val
            case "add":
                return f"{self.left} + {self.right}"
            case "sub":
                return f"{self.left} - {self.right}"
            case "mul":
                return f"{self.left:f} * {self.right:f}"
            case "div":
                return f"{self.left:f} / ({self.right})"

    def __format__(self, format_spec: str) -> str:
        '''f: wrap `str(self)` in parenthesis if necessary to use it as a factor'''
        s = str(self)
        if "f" in format_spec and (
            self.op in ("add", "sub")
            or (self.op == "const" and "-" in s)
        ):
            s = f"({s})"
        return s


class OpTreeEq:
    '''represents a real equation'''
    # valid operations and their random weight
    opers = {"add": 1, "mul": 1}
    root_range = (-5, 20)  # range of roots of equation

    def __init__(self, depth: int, roots: tuple[None | float]):
        self.left = OpTreeExpr()
        self.right: OpTreeExpr | None = None

    def __call__(self, var: tuple[float]) -> bool:
        '''returns wether var describes a solution'''
        return self.left(var) == self.right(var)

    def __str__(self):
        '''represents the equation as a string'''
        return f"{self.left} = {self.right}"


def get_eq(difficulty: int, **_):
    eq = OpTreeEq(difficulty // 2, difficulty)
    return f"Solve for x:\n\t{eq}\nx = ", lambda x: parse_float(x) == eq.root
