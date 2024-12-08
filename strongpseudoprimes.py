import argparse
import math
import time


def print_progressbar(segment, start_time, resolution):
    """
    Prints a progress bar, unrelated to strong pseudoprimes or primality testing
    """
    progress = segment // (resolution // 20)
    print(
        f"\r[{'=' * progress}{' ' * (20 - progress)}]  {((segment / resolution) * 100):.2f}% {time.time() - start_time:.2f}s",
        end="")


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

    for a in range(2, min(n - 1, math.floor(2 * (math.log(n) ** 2)))):
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


def search_for_strong_pseudoprimes(base, bound, progress_resolution):
    """
    Searches for strong pseudoprimes for a given base below a given bound.
    :param base: The base to search
    :param bound: The upper bound, essentially the amount of numbers to check (only odd numbers larger than 2)
    :param progress_resolution: The resolution of the progress bar
    :return:
    """
    print(f"{'-' * 60}")
    print(f"Searching for strong pseudoprimes to base {base} below {bound}")
    print(f"{'-' * 60}")
    start_time = time.time()
    segment_size = bound / progress_resolution
    current_segment = 1
    strong_pseudoprimes = []
    for n in range(3, bound, 2):
        if is_strong_pseudoprime(n, base):
            print(f"\r\33[K{n}\n", end="")
            strong_pseudoprimes.append(n)
            print_progressbar(current_segment, start_time, progress_resolution)
        elif n > (current_segment - 1) * segment_size:
            print_progressbar(current_segment, start_time, progress_resolution)
            current_segment += 1
    print(f"\r\33[K{'-' * 60}")
    print(f"Found {len(strong_pseudoprimes)} strong pseudoprimes to base {base} below {bound} in {time.time() - start_time:.2f}s")
    return strong_pseudoprimes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base', type=int, help='The base to search for strong pseudoprimes', default=2)
    parser.add_argument('-c', '--count', type=int, help='The upper bound to search for strong pseudoprimes, essentially the amount of numbers to check',
                        default=100000)
    parser.add_argument('-r', '--resolution', type=int, help='The resolution of the progress bar', default=10000)
    args = parser.parse_args()

    search_for_strong_pseudoprimes(max(args.base, 2), max(args.count, 5), max(args.resolution, 20))
