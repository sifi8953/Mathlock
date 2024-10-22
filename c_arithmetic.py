import re
import random
from typing import Self, TypeVar
from collections.abc import Iterable

T = TypeVar("T")

#             ( -?      a )             ( a+bi  |   a-bi | b=0 | a=0 )  ( -?      b       i )
#               v       v                  v         v      v     v       v       v       v
COMPLEX_RE = "^(-?\\s*[0-9]+)?\\s*((?<!^)\\+(?!$)|(?=-)|(?<=^)|(?=$))\\s*(-?\\s*[0-9]*\\s*i)?$"


def weighted_random(seq: Iterable[tuple[T, int]]) -> T:
    i = sum(w for _, w in seq)
    i = random.randrange(0, i)
    for t, w in seq:
        i -= w
        if i < 0:
            return t


def complex_str(z: complex) -> str:
    if z.imag == 0:
        return f"{z.real:g}"
    elif z.real == 0:
        if z.imag == 1:
            return f"i"
        elif z.imag == -1:
            return f"-i"
        else:
            return f"{z.imag:g}i"
    elif z.imag == 1:
        return f"{z.real:g} + i"
    elif z.imag == -1:
        return f"{z.real:g} - i"
    elif z.imag < 0:
        return f"{z.real:g} - {-z.imag:g}i"
    else:
        return f"{z.real:g} + {z.imag:g}i"


def parse_complex(z: str) -> complex:
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
    opers = {"add": 10, "mul": 10, "neg": 5, "inv": 2, "conj": 1, "abs": 1, "re": 1, "im": 1}
    const_range = (-5, 10)
    val_range = (-50, 100)

    def __init__(self, depth: int):
        self.op: str = "const" if random.random() < 2 ** -depth else weighted_random(OpTreeC.opers.items())
        self.val: complex | None = None
        self.left: OpTreeC | None = None
        self.right: OpTreeC | None = None

        while True:
            match self.op:
                case "const":  # constant
                    self.val = random.randint(*OpTreeC.const_range) + 1j * random.randint(*OpTreeC.const_range)
                case "add" | "mul":  # binary operators
                    self.left = OpTreeC(depth-1)
                    self.right = OpTreeC(depth-1)
                case _:  # unary operators
                    self.left = OpTreeC(depth-1)

            try:
                z = self()
            except ZeroDivisionError:
                pass
            else:
                if (z.real.is_integer() and z.imag.is_integer()
                        and OpTreeC.val_range[0] <= z.real <= OpTreeC.val_range[1]
                        and OpTreeC.val_range[0] <= z.imag <= OpTreeC.val_range[1]
                    ):
                    self.val = z
                    break

    def group_terms(self, op: str) -> list[Self]:
        if self.op == op:
            return self.left.group_terms(op) + self.right.group_terms(op)
        else:
            return [self]

    def __call__(self) -> complex:
        match self.op:
            case "const":
                return self.val
            case "add":
                return self.left() + self.right()
            case "mul":
                return self.left() * self.right()
            case "neg":
                return -self.left()
            case "inv":
                return 1/self.left()
            case "conj":
                return self.left().conjugate()
            case "abs":
                return abs(self.left())
            case "re":
                return complex(self.left().real, 0)
            case "im":
                return complex(0, self.left().imag)

    def __str__(self) -> str:
        match self.op:
            case "const":
                return complex_str(self.val)
            case "add":
                return "(" + ") + (".join(map(str, self.group_terms("add"))) + ")"
            case "mul":
                return "(" + ") * (".join(map(str, self.group_terms("mul"))) + ")"
            case "neg":
                return f"-({self.left})"
            case "inv":
                return f"1/({self.left})"
            case "conj":
                return f"conj({self.left})"
            case "abs":
                return f"|{self.left}|"
            case "re":
                return f"Re({self.left})"
            case "im":
                return f"Im({self.left})"


def get_complex(depth: int):
    c = OpTreeC(depth)
    return f"Evaluate\n\t{c}\n= ", lambda x: parse_complex(x) == c.val
