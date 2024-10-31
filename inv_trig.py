import random
import re

const_range = (-5, 10)

type RealConst = tuple[float, float]  # a + b pi
type LinExpr = tuple[RealConst, RealConst]  # a x + b
type TrigExpr = tuple[bool, LinExpr]  # sin/cos(f)
type TrigEq = tuple[TrigExpr, TrigExpr]  # f = g
type TrigAns = tuple[LinExpr, LinExpr]  # f or g


def generate_lin_expr() -> LinExpr:
    '''generate a linear expression with no multiples of pi'''
    x = float(random.randint(*const_range)), 0
    c = float(random.randint(*const_range)), 0
    return x, c


def real_str(x: RealConst) -> str:
    '''represent a real number as a string'''
    if x[1] == 0:
        return f"{x[0]:g}"  # a
    elif x[0] == 0:
        if x[1] == 1:
            return f"π"  # pi
        elif x[1] == -1:
            return f"-π"  # -pi
        else:
            return f"{x[1]:g}π"  # b*pi
    elif x[1] == 1:
        return f"{x[0]:g} + π"  # a+pi
    elif x[1] == -1:
        return f"{x[0]:g} - π"  # a-pi
    elif x[1] < 0:
        return f"{x[0]:g} - {-x[1]:g}π"  # a-b*pi
    else:
        return f"{x[0]:g} + {x[1]:g}π"  # a+b*pi


def lin_expr_str(x: LinExpr) -> str:
    '''represent a linear expression as a string'''
    if x[0][1]:
        return f"({real_str(x[0])})x + {real_str(x[1])}"  # (a + b pi)x + c + d pi
    else:
        return f"{real_str(x[0])}x + {real_str(x[1])}"  # a x + c


def generate_trig_expr() -> TrigExpr:
    '''generate a trig function with linear input'''
    return random.random() < 0.5, generate_lin_expr()


def trig_expr_str(x: TrigExpr) -> str:
    '''represent a trig expression as a string'''
    return f"{'sin' if x[0] else 'cos'}({lin_expr_str(x[1])})"


def generate_trig_eq() -> TrigEq:
    '''generate a random trigonometric equation'''
    while True:
        l = generate_trig_expr()
        r = generate_trig_expr()
        # make sure solutions exist
        if abs(l[1][0][0]) != abs(r[1][0][0]):
            return l, r


def trig_eq_str(x: TrigEq) -> str:
    '''represent a trig equation as a string'''
    return f"{trig_expr_str(x[0])} = {trig_expr_str(x[1])}"


def trig_to_cos(x: TrigExpr) -> TrigExpr:
    '''apply sin(x) = cos(pi-x) if possible'''
    sin, ((a, b), (c, d)) = x
    if sin:
        # sin(x) = cos(0.5 pi - x)
        # sin((a + b pi) x + (c + d pi)) = cos((-a + -b pi) x + (-c + (0.5 - d) pi))
        return (not sin, ((-a, -b), (-c, 0.5-d)))
    else:
        return x


def solve_trig_eq(x: TrigEq) -> TrigAns:
    '''get all solutions to trigonometric equation'''
    _, ((la, lb), (lc, ld)) = trig_to_cos(x[0])
    _, ((ra, rb), (rc, rd)) = trig_to_cos(x[1])

    if lb or rb:
        raise ValueError("cannot handle pi as a factor for x")

    # (la + lb pi) x + (lc + ld pi) = (ra + rb pi) x + (rc + rd pi) + 2 pi n
    # la x + (lc + ld pi) = ra x + (rc + rd pi) + 2 pi n
    # (la - ra) x = ((rc - lc) + (rd - ld) pi) + 2 pi n
    # x = ((rc - lc)/(la - ra) + (rd - ld)/(la - ra) pi) + 2/(la - ra) pi n
    ans1 = ((rc - lc)/(la - ra), (rd - ld)/(la - ra)), (0.0, 2/(la - ra))

    # (la + lb pi) x + (lc + ld pi) = -((ra + rb pi) x + (rc + rd pi)) + 2 pi n
    # (la + lb pi) x + (lc + ld pi) = (-ra + -rb pi) x + (-rc + -rd pi) + 2 pi n
    # la x + (lc + ld pi) = -ra x + (-rc + -rd pi) + 2 pi n
    # (la + ra) x = ((-rc - lc) + (-rd - ld) pi) + 2 pi n
    # x = ((-rc - lc)/(la + ra) + (-rd - ld)/(la + ra) pi) + 2/(la + ra) pi n
    # x = (-(rc + lc)/(la + ra) + -(rd + ld)/(la + ra) pi) + 2/(la + ra) pi n
    ans2 = (-(rc + lc)/(la + ra), -(rd + ld)/(la + ra)), (0.0, 2/(la + ra))

    return ans1, ans2


def parse_rational(x: str, default: float) -> float:
    '''interpret string as float or quotient of floats'''
    if "/" in x:
        a, b = x.split("/")
        return float(a) / float(b)
    elif x.strip():
        return float(x)
    else:
        return default


def parse_solution(x: str) -> LinExpr:
    '''interpret string as one case of a trigonometric solution'''
    # a + b pi + (c + d pi) n
    a, b, c, d = 0.0, 0.0, 0.0, 0.0

    x = x.replace("-", "+-").strip().lstrip("+")  # replace subtraction with addition of negative
    x: str = re.sub("-\\s+", "-", x)  # remove spaces between negative sign and number

    for t in x.split("+"):
        if "pi" in t:
            t = t.replace("pi", " ")
            if "n" in t:
                t = t.replace("n", " ")
                d += parse_rational(t, 1)
            else:
                b += parse_rational(t, 1)
        else:
            if "n" in t:
                t = t.replace("n", " ")
                c += parse_rational(t, 1)
            else:
                a += parse_rational(t, 0)

    return (a, b), (c, d)


def parse_solutions(x: str) -> TrigAns:
    '''interpret string as both cases of a trigonometric solution'''
    try:
        v1, v2 = x.split(",")
        return parse_solution(v1), parse_solution(v2)
    except ValueError:
        raise ValueError("please answer in the form 'a + b pi + c n + d pi n, ...'")


def standardise(x: LinExpr) -> LinExpr:
    '''converts all equivalent solutions to the same representation'''
    (a, b), (c, d) = x

    if c < 0 or (c == 0 and d < 0):
        c = -c
        d = -d

    if c:
        n = a // c
        a = a - c * n
        b = b - d * n
    elif d:
        n = b // d
        a = a - c * n
        b = b - d * n

    return (a, b), (c, d)


def validate_one(x: LinExpr, y: LinExpr) -> bool:
    '''compare one case of trigonometric solutions'''
    (xa, xb), (xc, xd) = standardise(x)
    (ya, yb), (yc, yd) = standardise(y)

    # add leniency
    xa = round(xa, 5)
    xb = round(xb, 5)
    xc = round(xc, 5)
    xd = round(xd, 5)
    ya = round(ya, 5)
    yb = round(yb, 5)
    yc = round(yc, 5)
    yd = round(yd, 5)

    return xa == ya and xb == yb and xc == yc and xd == yd


def validate(a: TrigAns, b: TrigAns) -> bool:
    '''compare both cases of trigonometric solutions'''
    return (
        (validate_one(a[0], b[0]) and validate_one(a[1], b[1]))
        or (validate_one(a[0], b[1]) and validate_one(a[1], b[0]))
    )


def get_inv_trig(**_):
    eq = generate_trig_eq()
    ans = solve_trig_eq(eq)
    return f"Find all values of x for integers n such that\n\t{trig_eq_str(eq)}\nx1, x2 = ", lambda x: validate(parse_solutions(x), ans)
