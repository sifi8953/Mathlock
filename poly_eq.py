from itertools import zip_longest
from random import randint

ROOT_MIN = -5
ROOT_MAX = 5


def get_poly(degree: int = 2, difficulty: int = 1, **_):
    roots = random_ints(degree, ROOT_MIN * difficulty, ROOT_MAX * difficulty)
    eq = randomize_eq(poly_from_roots(roots))
    return f"Find all roots for the equation:\n\t{eq}\nx = ", lambda x: parse_ints(x) == set(roots)


def get_poly_div(degree: int = 2, difficulty: int = 1, **_):
    roots = random_ints(degree + 1, ROOT_MIN * difficulty, ROOT_MAX * difficulty)
    eq = f"{poly_string(poly_from_roots(roots))} = 0"
    revealed_roots = []
    for i in range(1):
        revealed_roots.append(roots[i])
    
    for root in revealed_roots:
        roots.remove(root)
    return f"An equation has the known roots {revealed_roots}, find all remaining roots for the equation:\n\t{eq}\nx = ", lambda x: parse_ints(x) == set(roots)


def randomize_eq(p):
    eq_left = p
    coeffRange = max(eq_left)
    eq_right = random_ints(len(p), -coeffRange, coeffRange)
    eq_left = poly_add(eq_left, eq_right)
    eq = f"{poly_string(eq_left)} = {poly_string(eq_right)}" 
    return eq


def parse_ints(x: str) -> set[int]:
    try:
        return set([int(i) for i in x.split(',')])
    except ValueError:
        raise ValueError("Please input only numbers")


def poly_from_roots(roots: list[int]):
    factors = []
    for root in roots:
        factors.append([-root, 1])
    return poly_prod(*factors)


def poly_add(p1: list[int], p2: list[int]) -> list[int]:
    '''returns sum of two polynomials'''
    return list(map(sum, zip_longest(p1, p2, fillvalue=0)))


def poly_sum(*polynomials: list[int]):
    '''sum of any number of polynomials'''
    res = [0]
    for p in polynomials:
        res = poly_add(res, p)
    return res


def poly_mult(p1: list[int], p2: list[int]):
    '''returns product of two polynomials'''
    polynomials = []
    for exponent, coeff1 in (enumerate(p1, 0)):
        current_poly = [0] * exponent
        for coeff2 in p2:
            current_poly.append(coeff1 * coeff2)
        polynomials.append(current_poly)

    return poly_sum(*polynomials)


def poly_prod(*factors: list[int]):
    '''returns product of any number of polynomials'''
    res = [1]
    for p in factors:
        res = poly_mult(res, p)
    return res


def poly_string(polynomial: list[int]) -> str:
    '''returns string of a polynomial expression from a list of its coefficients, e.g [c,b,a] -> "ax^2 + bx + c"'''
    poly_string = " "
    for exponent, coeff in reversed(list(enumerate(polynomial, 0))):
        poly_string += f"{coeff}x^{exponent} + "
    poly_string = poly_string.replace("+ -", "- ").replace("x^1", "x").replace("x^0","").replace(" 1x", " x").replace(" + 0x", "")[:-3]
    return poly_string.strip()


def random_ints(amount: int, min: int, max: int) -> list[int]:
    '''returns a list of "amount" length of random integers between ROOT_MIN AND ROOT_MAX'''
    roots = []
    for i in range(amount):
        roots.append(randint(min, max))
    return roots

