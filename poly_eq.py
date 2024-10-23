from itertools import zip_longest
from random import randint

ROOT_MIN = -6
ROOT_MAX = 6

def get_poly(degree:int = 2, **_):
    roots = random_roots(degree)
    eq = poly_string(poly_from_roots(roots)) + " = 0"
    return f"Solve for x:\n\t{eq}\nx = ", lambda x: parse_int(x) in roots

def parse_int(x: str) -> int:
    try:
        return int(x)
    except ValueError:
        raise ValueError("please input a number")

def poly_from_roots(roots: list[int]):
    factors = []
    for root in roots:
        factors.append([-root,1])
    return poly_prod(*factors)
    
#returns sum of two polynomials
def poly_add(p1:list[int], p2:list[int]) -> list[int]:
    return list(map(sum,zip_longest(p1, p2, fillvalue = 0)))
    
#sum of any number of polynomials
def poly_sum(*polynomials:list[int]):
    res = [0]
    for p in polynomials:
        res = poly_add(res, p)
    return res

#returns product of two polynomials
def poly_mult(p1:list[int], p2:list[int]): 
    polynomials = []
    for exponent, coeff1 in (enumerate(p1, 0)):
        current_poly = [0] * exponent 
        for coeff2 in p2:
            current_poly.append(coeff1 * coeff2)
        polynomials.append(current_poly)
    
    return poly_sum(*polynomials)

#returns product of any number of polynomials
def poly_prod(*factors:list[int]):
    res = [1]
    for p in factors:
        res = poly_mult(res, p)
    return res
    
#returns string of a polynomial expression from a list of its coefficients, e.g [c,b,a] -> "ax^2 + bx + c"
def poly_string(polynomial: list[int]) -> str:
    poly_string = " "
    for exponent, coeff in reversed(list(enumerate(polynomial, 0))):
        poly_string += f"{coeff}x^{exponent} + "
    poly_string = poly_string.replace("+ -", "- ").replace("x^1", "x").replace("x^0", "").replace(" 1x", " x").replace(" + 0x", "")[:-3]
    return poly_string.strip()

#returns a list of "degree" length of random integers between ROOT_MIN AND ROOT_MAX
def random_roots(degree:int) -> list[int]:
    roots = []
    for i in range(degree):
        roots.append(randint(ROOT_MIN,ROOT_MAX))
    return roots
    

