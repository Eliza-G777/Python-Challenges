"""
Estimating pi with random numbers (the Monte Carlo method).

Idea: throw random darts at a 1-by-1 square. A quarter circle of radius 1
fits inside it, with area pi/4. So the fraction of darts that land inside
the quarter circle is about pi/4, and pi ≈ 4 * (darts inside) / (all darts).

Math question: how fast does the estimate improve as we throw more darts?
Theory says the error shrinks like 1 / sqrt(n): 100 times more darts
gives only about 10 times more accuracy.
"""
import math
import random
import matplotlib.pyplot as plt

random.seed(7)   # makes the "random" results repeatable; remove it to get new ones


def estimate_pi(n):
    inside = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1:
            inside += 1
    return 4 * inside / n


if __name__ == "__main__":
    sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
    errors = []
    print("Darts       | Estimate of pi | Error")
    for n in sizes:
        est = estimate_pi(n)
        err = abs(est - math.pi)
        errors.append(err)
        print(f"{n:>11,} | {est:>14.6f} | {err:.6f}")

    # Picture of 3,000 darts
    xs = [random.random() for _ in range(3000)]
    ys = [random.random() for _ in range(3000)]
    hit = [x * x + y * y <= 1 for x, y in zip(xs, ys)]

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 5))
    left.scatter([x for x, h in zip(xs, hit) if h], [y for y, h in zip(ys, hit) if h], s=3, label="Inside")
    left.scatter([x for x, h in zip(xs, hit) if not h], [y for y, h in zip(ys, hit) if not h], s=3, label="Outside")
    left.set_aspect("equal")
    left.set_title(f"3,000 darts: pi ≈ {4 * sum(hit) / len(hit):.3f}")
    left.legend(loc="upper right")

    right.loglog(sizes, errors, "o-", label="Actual error")
    right.loglog(sizes, [1.6 / math.sqrt(n) for n in sizes], "--", label="Theory: about 1/√n")
    right.set_xlabel("Number of darts")
    right.set_ylabel("Error (log scale)")
    right.set_title("More darts, smaller error")
    right.legend()
    right.grid(alpha=0.3, which="both")

    plt.tight_layout()
    plt.savefig("pi_estimate.png", dpi=150)
    print("Saved the chart as pi_estimate.png")
    plt.show()
