import re
import random
from typing import Self, TypeVar
from collections.abc import Iterable

T = TypeVar("T")

#             ( -?      a )             ( a+bi  |   a-bi | b=0 | a=0 )  ( -?      b       i )
#               v       v                  v         v      v     v       v       v       v
COMPLEX_RE = "^(-?\\s*[0-9]+)?\\s*((?<!^)\\+(?!$)|(?=-)|(?<=^)|(?=$))\\s*(-?\\s*[0-9]*\\s*i)?$"


def weighted_random(seq: Iterable[tuple[T, int]]) -> T:
    '''return a random item from the first element in the tuples in seq weighted by the second element in the tuples'''
    i = sum(w for _, w in seq)
    i = random.randrange(0, i)
    for t, w in seq:
        i -= w
        if i < 0:
            return t


def complex_str(z: complex) -> str:
    '''represent a complex number as a string'''
    if z.imag == 0:
        return f"{z.real:g}"  # a
    elif z.real == 0:
        if z.imag == 1:
            return f"i"  # i
        elif z.imag == -1:
            return f"-i"  # -i
        else:
            return f"{z.imag:g}i"  # bi
    elif z.imag == 1:
        return f"{z.real:g} + i"  # a+i
    elif z.imag == -1:
        return f"{z.real:g} - i"  # a-i
    elif z.imag < 0:
        return f"{z.real:g} - {-z.imag:g}i"  # a-bi
    else:
        return f"{z.real:g} + {z.imag:g}i"  # a+bi


def parse_complex(z: str) -> complex:
    '''convert string to complex number
    \n raises ValueError if unsuccessful'''
    z = z.strip()
    match = re.match(COMPLEX_RE, z)
    if z and match:
        a = (match.group(1) or "0")
        b = (match.group(3) or "0").rstrip("i").strip() or "1"
        if b == "-":
            b = "-1"
        a, b = float(a), float(b)
        return complex(a, b)
    else:
        raise ValueError("please answer in the form 'a+bi'")


class OpTreeC:
    '''represents a complex expression'''

    # valid operations and their random weight
    opers = {"add": 10, "sub": 5, "mul": 10, "div": 2, "conj": 1, "abs": 1, "re": 1, "im": 1}
    const_range = (-5, 10)  # range of parts in constants
    val_range = (-50, 100)  # range of values of expression

    def __init__(self, depth: int):
        '''construct a random expression at most `depth` operations deep'''
        # chance to be leaf node
        self.op: str = "const" if random.random() < 2 ** -depth else weighted_random(OpTreeC.opers.items())
        self.val: complex | None = None
        self.left: OpTreeC | None = None
        self.right: OpTreeC | None = None

        while True:
            match self.op:
                case "const":  # constant
                    self.val = random.randint(*OpTreeC.const_range) + 1j * random.randint(*OpTreeC.const_range)
                case "add" | "sub" | "mul" | "div":  # binary operators
                    self.left = OpTreeC(depth-1)
                    self.right = OpTreeC(depth-1)
                case _:  # unary operators
                    self.left = OpTreeC(depth-1)

            try:
                # make sure no division by zero occurs
                z = self()
            except ZeroDivisionError:
                continue
            else:
                # make sure the parts are small integers
                if (
                    z.real.is_integer() and z.imag.is_integer()
                    and OpTreeC.val_range[0] <= z.real <= OpTreeC.val_range[1]
                    and OpTreeC.val_range[0] <= z.imag <= OpTreeC.val_range[1]
                ):
                    self.val = z
                    break

    def __call__(self) -> complex:
        '''evaluates the expression'''
        match self.op:
            case "const":
                return self.val
            case "add":
                return self.left() + self.right()
            case "sub":
                return self.left() - self.right()
            case "mul":
                return self.left() * self.right()
            case "div":
                return self.left() / self.right()
            case "conj":
                return self.left().conjugate()
            case "abs":
                return abs(self.left())
            case "re":
                return complex(self.left().real, 0)
            case "im":
                return complex(0, self.left().imag)

    def __str__(self) -> str:
        '''represent expression as a string'''
        match self.op:
            case "const":
                return complex_str(self.val)
            case "add":
                return f"{self.left} + {self.right}"
            case "sub":
                return f"{self.left} - {self.right}"
            case "mul":
                return f"{self.left:f} * {self.right:f}"
            case "div":
                return f"{self.left:f} / ({self.right})"
            case "conj":
                return f"conj({self.left})"
            case "abs":
                return f"|{self.left}|"
            case "re":
                return f"Re({self.left})"
            case "im":
                return f"Im({self.left})"

    def __format__(self, format_spec: str) -> str:
        '''f: wrap `str(self)` in parenthesis if necessary to use it as a factor'''
        s = str(self)
        if "f" in format_spec and (
            self.op == ("add", "sub")
            or (self.op == "const" and "-" in s or "+" in s)
        ):
            s = f"({s})"
        return s


def get_complex(difficulty: int, **_):
    c = OpTreeC(difficulty)
    return f"Evaluate\n\t{c}\n= ", lambda x: parse_complex(x) == c.val
