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


def random_roots(n: int, rand_range: tuple[int, int]) -> tuple[int, ...]:
    '''returns a tuple of `n` random numbers within the range `rand_range`'''
    return tuple(random.randint(*rand_range) for _ in range(n))


def tuple_replace(t: tuple[Any, ...], i: int, v: Any) -> tuple[Any, ...]:
    '''returns the tuple `t` but with item `i` replaced by `v`'''
    return t[:i] + (v,) + t[i+1:]


def parse_float(x: str) -> float:
    '''convert string to float
    \n raises ValueError if unsuccessful'''
    try:
        return float(x)
    except ValueError:
        raise ValueError("please input a number")


def parse_tuple(x: str) -> tuple[float]:
    '''convert string to tuple of floats
    \n raises ValueError if unsuccessful'''
    try:
        return tuple(parse_float(f) for f in x.split(","))
    except ValueError:
        raise ValueError("please answer in the form 'a, b, c, ...'")


class OpTreeExpr:
    '''represents a real expression'''

    var_str = "xyzabcduvw"  # characters to use as variable names
    opers = {"add": 10, "sub": 5, "mul": 10, "div": 2}  # valid operations and their random weight

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
        '''yields slightly modified but equivalent expressions'''

        if self.op in ("var", "const"):  # cannot be transformed
            return

        # combine constants
        if self.left.op == "const" and self.right.op == "const":
            x: float = self(())
            if x.is_integer():
                yield OpTreeExpr("const", x)

        # commutative
        if self.op in ("add", "mul"):  # a +* b
            yield OpTreeExpr(self.op, self.right, self.left)  # b +* a

        # associative
        if self.op in ("add", "mul") and self.op == self.left.op:  # (a +* b) +* c
            yield OpTreeExpr(  # a +* (b +* c)
                self.op,
                self.left.left,
                OpTreeExpr(self.op, self.left.right, self.right)
            )
        if self.op in ("add", "mul") and self.op == self.right.op:  # a +* (b +* c)
            yield OpTreeExpr(  # (a +* b) +* c
                self.op,
                OpTreeExpr(self.op, self.left, self.right.left),
                self.right.right
            )

        # right distributive
        if self.op in ("mul", "div") and self.left.op in ("add", "sub"):  # (b +- c) */ a
            yield OpTreeExpr(  # (b */ a) +- (c */ a)
                self.left.op,
                OpTreeExpr(self.op, self.left.left, self.right),
                OpTreeExpr(self.op, self.left.right, self.right)
            )

        # left distributive
        if self.op == "mul" and self.right.op in ("add", "sub"):  # a * (b +- c)
            yield OpTreeExpr(  # (a * b) +- (a * c)
                self.right.op,
                OpTreeExpr(self.op, self.left,  self.right.left),
                OpTreeExpr(self.op, self.left, self.right.right)
            )

        # right distributive
        if self.op in ("add", "sub"):
            left = OpTreeExpr("mul", OpTreeExpr("const", 1), self.left)  # 1 * left
            right = OpTreeExpr("mul", OpTreeExpr("const", 1), self.right)  # 1 * right
            for l, r in ((self.left, self.right), (self.left, right), (left, self.right), (left, right)):
                if l.op in ("mul", "div") and l.op == r.op and l.right == r.right:  # (b */ a) +- (c */ a)
                    yield OpTreeExpr(  # (b +- c) */ a
                        l.op,
                        OpTreeExpr(self.op, l.left, r.left),
                        r.right
                    )

        # left distributive
        if self.op in ("add", "sub"):
            left = OpTreeExpr("mul", self.left, OpTreeExpr("const", 1))  # left * 1
            right = OpTreeExpr("mul", self.right, OpTreeExpr("const", 1))  # right * 1
            for l, r in ((self.left, self.right), (self.left, right), (left, self.right), (left, right)):
                if l.op == "mul" and l.op == r.op and l.left == r.left:  # (a * b) +- (a * c)
                    yield OpTreeExpr(  # a * (b +- c)
                        l.op,
                        l.left,
                        OpTreeExpr(self.op, l.right, r.right)
                    )

        yield from (OpTreeExpr(self.op, l, self.right) for l in self.left.transformations())  # transform left
        yield from (OpTreeExpr(self.op, self.left, r) for r in self.right.transformations())  # transform right

    def __call__(self, var: tuple[float]) -> float:
        '''evaluates the expression'''
        match self.op:
            case "var":
                if self.index < len(var) and var[self.index] is not None:
                    return var[self.index]
                else:
                    raise ValueError("too few variables")
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
                return str(self.val)
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

    def __eq__(self, other: Self) -> bool:
        if self.op != other.op:
            return False
        elif self.op == "var":
            return self.index == other.index
        elif self.op == "const":
            return self.val == other.val
        else:
            return self.left == other.left and self.right == other.right


class OpTreeEq:
    '''represents a real equation'''

    const_range = (-5, 10)  # range of parts in constants

    def __init__(self, depth: int, iters: int, roots: tuple[None | float, ...], outermost: bool = True):
        if not outermost and random.random() < 2 ** -depth:  # chance to be leaf node

            root_dict = {i: x for i, x in enumerate(roots) if x is not None}
            if root_dict and random.random() < 0.5:  # 50% chance to use a root
                i, x = random.choice(tuple(root_dict.items()))
                self.left = OpTreeExpr("var", i)
                self.right = OpTreeExpr("const", x)

                if random.random() < 0.5:  # swap sides
                    self.left, self.right = self.right, self.left
            else:
                x = 0
                while x == 0:
                    x = random.randint(*OpTreeEq.const_range)
                self.left = OpTreeExpr("const", x)
                self.right = OpTreeExpr("const", x)

        else:
            while True:
                op = weighted_random(OpTreeExpr.opers.items())
                left_eq = OpTreeEq(depth - 1, 0, roots, outermost=False)
                right_eq = OpTreeEq(depth - 1, 0, roots, outermost=False)
                self.left = OpTreeExpr(op, left_eq.left, right_eq.left)
                self.right = OpTreeExpr(op, left_eq.right, right_eq.right)

                # don't check sub-expressions
                if not outermost:
                    break

                # make sure roots is a root and it isn't true for all values of some variable
                if self(roots) and not all(self(tuple_replace(roots, i, v+1)) for i, v in enumerate(roots) if v is not None):
                    break

        if outermost:
            self.transform(iters)

    def transform(self, iters: int) -> None:
        '''slightly modifies both sides iters times but remains equivalent'''
        for _ in range(iters):
            t = tuple(self.left.transformations())
            if t:
                self.left = random.choice(t)
            t = tuple(self.right.transformations())
            if t:
                self.right = random.choice(t)

    def __call__(self, var: tuple[float, ...]) -> bool:
        '''returns wether var describes a solution'''
        try:
            return self.left(var) == self.right(var)
        except ZeroDivisionError:
            return False

    def __str__(self):
        '''represents the equation as a string'''
        return f"{self.left} = {self.right}"


class OpTreeEqSys:
    '''represents a system of real equations'''
    root_range = (-5, 10)  # range of roots

    def __init__(self, depth: int, iters: int, eqs: int):
        roots = random_roots(eqs, OpTreeEqSys.root_range)
        while True:
            self.eqs = [OpTreeEq(depth, iters, roots) for _ in range(eqs)]

            # make sure roots is a root and it isn't true for all values of a variable
            if self(roots) and not any(self(tuple_replace(roots, i, v+1)) for i, v in enumerate(roots) if v is not None):
                break

    def __call__(self, var: tuple[float, ...]) -> bool:
        '''returns wether var describes a solution'''
        return all(eq(var) for eq in self.eqs)

    def __str__(self):
        '''represents the system as a string'''
        return "\n".join(str(eq) for eq in self.eqs)


def get_eq(difficulty: int, **_):
    eq = OpTreeEqSys(difficulty, difficulty, 1)
    return f"Solve for x:\n\t{eq}\nx = ", lambda x: eq((parse_float(x),))


def get_eq_sys(difficulty: int, var_count: int, **_):
    eq = OpTreeEqSys(difficulty, difficulty, var_count)
    return f"Find a solution:\n\n{eq}\n\n{', '.join(OpTreeExpr.var_str[:var_count])} = ", lambda x: eq(parse_tuple(x))
