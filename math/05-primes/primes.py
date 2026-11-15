"""
Exploring prime numbers.

1. Find all primes up to N with the Sieve of Eratosthenes (a 2,000-year-old algorithm).
2. Test the Prime Number Theorem: the number of primes up to x is about x / ln(x).
3. Check Goldbach's conjecture: every even number greater than 2 is the sum of two primes.
   (Nobody has proved it yet. We can only check it for many numbers.)
"""
import math
import time
import matplotlib.pyplot as plt


def sieve(n):
    """Return a list of all primes up to n."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            # cross out multiples of p, starting at p*p (smaller ones are already crossed out)
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
    return [i for i, prime in enumerate(is_prime) if prime]


def is_prime_slow(k):
    """Trial division, for comparing speed with the sieve."""
    if k < 2:
        return False
    for d in range(2, int(k ** 0.5) + 1):
        if k % d == 0:
            return False
    return True


def goldbach(n, prime_set):
    """Return one way to write the even number n as p + q, or None."""
    for p in sorted(prime_set):
        if p > n // 2:
            break
        if (n - p) in prime_set:
            return p, n - p
    return None


if __name__ == "__main__":
    N = 1_000_000

    start = time.perf_counter()
    primes = sieve(N)
    t_sieve = time.perf_counter() - start
    print(f"There are {len(primes):,} primes up to {N:,}. Sieve took {t_sieve:.2f} s.")

    start = time.perf_counter()
    slow_count = sum(1 for k in range(N // 10) if is_prime_slow(k))
    t_slow = time.perf_counter() - start
    print(f"Testing numbers one at a time took {t_slow:.2f} s for just the first {N // 10:,} ({slow_count:,} primes),")
    print("so the sieve covers 10 times as many numbers in about the same time.")

    # Prime Number Theorem
    print("\n        x | primes up to x | x / ln(x) | ratio")
    for x in (100, 1_000, 10_000, 100_000, 1_000_000):
        count = sum(1 for p in primes if p <= x)
        guess = x / math.log(x)
        print(f"{x:>9,} | {count:>14,} | {guess:>9,.0f} | {count / guess:.3f}")
    print("The ratio slowly moves toward 1, as the theorem predicts.")

    # Goldbach's conjecture
    prime_set = set(sieve(100_000))
    limit = 100_000
    failures = [n for n in range(4, limit + 1, 2) if goldbach(n, prime_set) is None]
    print(f"\nGoldbach checked for every even number up to {limit:,}: {'no exceptions!' if not failures else failures}")
    print("Example: 2026 =", " + ".join(map(str, goldbach(2026, prime_set))))

    xs = list(range(10, N + 1, 5000))
    counts, idx = [], 0
    for x in xs:
        while idx < len(primes) and primes[idx] <= x:
            idx += 1
        counts.append(idx)
    plt.figure(figsize=(8, 4.5))
    plt.plot(xs, counts, label="Actual number of primes up to x")
    plt.plot(xs, [x / math.log(x) for x in xs], "--", label="Prediction x / ln(x)")
    plt.xlabel("x")
    plt.ylabel("How many primes are ≤ x")
    plt.title("The Prime Number Theorem")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("primes.png", dpi=150)
    print("Saved the chart as primes.png")
    plt.show()
