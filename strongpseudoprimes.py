import math


def is_strong_probable_prime(n, a):
    """
    An iteration of the Miller-Rabin primality test

    Parameters
    ----------
    n : int
        The number to test
    a : int
        The base, i.e. a number in the range 2 to n-2 which is used in the test

    Returns
    -------
    bool
        True if n is a strong probable prime, False if it is definitely composite
    """
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1
    x = pow(a, d, n)

    for i in range(s):
        y = pow(x, 2, n)
        if y == 1 and x != 1 and x != n - 1:
            return False
        x = y

    if x != 1:
        return False
    return True


def is_prime(n, skip_base=None):
    """
    The Miller-test

    Parameters
    ----------
    n : int
        The number to test
    skip_base : int
        A base to skip, useful when it's a known liar.

    Returns
    -------
    bool
        True if n is prime, False if it is definitely composite (assuming the GRH is true)
    """
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1

    for a in range(2, min(n - 1, math.floor(2*(math.log(n) ** 2)))):
        if a == skip_base:
            continue

        x = pow(a, d, n)

        for i in range(s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y

        if x != 1:
            return False

    return True

def is_strong_pseudoprime(n, a):
    # 1. check if n is a strong probable prime with the Miller-Rabin test
    if is_strong_probable_prime(n, a):
        # 2. check if it's a prime with the Miller-test, skipping base a since n is known to be SPP to base a
        return not is_prime(n, a)
    return False

def search_for_strong_pseudoprimes(base, count):
    for n in range(3, count, 2):
        if is_strong_pseudoprime(n, base):
            print(f"{n} is a strong pseudoprime to base {base}", end="\n\r")

# Find all strong pseudoprimes to base 2 below 100 000
search_for_strong_pseudoprimes(2, 100000)