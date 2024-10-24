import random
from typing import Self, TypeVar
from collections.abc import Iterable

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
    opers = {"add": 10, "mul": 10, "neg": 5, "inv": 2}
    const_range = (-5, 10)  # range of parts in constants
    val_range = (-50, 100)  # range of values of expression

    def __init__(
        self,
        op: str | None = None,
        left: Self | None = None,
        right: Self | None = None,
        val: float | None = None,
        depth: int = 0
    ):
        '''`op`: operation of expression, randomized if `None`
        \n `left`: first argument of operation if it takes at least one argument
        \n `right`: second argument of operation if it takes at least two arguments
        \n `val`: value of constant if const operation or variable number if var operation
        \n `depth`: maximum depth of randomized expressions.'''

        self.op = op or ("const" if random.random() < 2 ** -depth else weighted_random(OpTreeExpr.opers.items()))
        self.val = None
        self.left = None
        self.right = None

        match self.op:
            case "var":  # variable
                self.val = val or 0
            case "const":  # constant
                self.val = val
                while self.val is None or self.val == 0:  # don't allow zero constants
                    self.val = float(random.randint(*OpTreeExpr.const_range))
            case "add" | "mul":  # binary operators
                self.left = left or OpTreeExpr(depth=depth-1)
                self.right = right or OpTreeExpr(depth=depth-1)
            case _:  # unary operators
                self.left = left or OpTreeExpr(depth=depth-1)

    def __call__(self, var: tuple[float]) -> float:
        '''evaluates the expression'''
        match self.op:
            case "var":
                return var[self.val]
            case "const":
                return self.val
            case "add":
                return self.left(var) + self.right(var)
            case "mul":
                return self.left(var) * self.right(var)
            case "neg":
                return -self.left(var)
            case "inv":
                return 1/self.left(var)

    def __str__(self) -> str:
        '''represent expression as a string'''
        match self.op:
            case "var":
                return OpTreeExpr.var_str[self.val]
            case "const":
                return f"{self.val:g}"
            case "add":
                return f"{self.left} + {self.right}"
            case "mul":
                return f"{self.left:f} * {self.right:f}"
            case "neg":
                return f"-{self.left:f}"
            case "inv":
                return f"1/({self.left})"

    def __format__(self, format_spec: str) -> str:
        '''f: wrap `str(self)` in parenthesis if necessary to use it as a factor'''
        s = str(self)
        if "f" in format_spec and (
            self.op in ("add", "neg")
            or (self.op == "const" and "-" in s)

        ):
            s = f"({s})"
        return s


class OpTreeEq:
    '''represents a real equation'''
    # valid operations and their random weight
    opers = {"add": 1, "mul": 1}
    root_range = (-5, 20)  # range of roots of equation

    def __init__(self, depth: int, iters: int, root: None | float = None):
        '''`depth`: maximum depth of expressions
        \n `iters`: number of expression to combine
        \n `root`: root of equation, randomized if `None`'''
        while True:
            self.root = root or float(random.randint(*OpTreeEq.root_range))
            self.left = OpTreeExpr("var", val=0)
            self.right = OpTreeExpr("const", val=root)

            for _ in range(iters):
                op = weighted_random(OpTreeEq.opers.items())
                expr = OpTreeExpr(depth=depth)

                if random.random() < 0.5:  # randomize the order
                    self.left = OpTreeExpr(op, self.left, expr)
                else:
                    self.left = OpTreeExpr(op, expr, self.left)

                if random.random() < 0.5:  # randomize the order
                    self.right = OpTreeExpr(op, self.right, expr)
                else:
                    self.right = OpTreeExpr(op, expr, self.right)

            try:
                t = self(self.root)
                f = self(self.root+1)
            except ZeroDivisionError:
                continue
            else:
                if t and not f:
                    break

    def __call__(self, *var: float) -> bool:
        '''returns wether var describes a solution'''
        return self.left(var) == self.right(var)

    def __str__(self):
        '''represents the equation as a string'''
        return f"{self.left} = {self.right}"


def get_eq(difficulty: int, **_):
    eq = OpTreeEq(difficulty // 2, difficulty)
    return f"Solve for x:\n\t{eq}\nx = ", lambda x: parse_float(x) == eq.root
