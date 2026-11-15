"""
Solving equations a calculator can't solve directly: Newton's method vs bisection.

Example equation: x^3 - 2x - 5 = 0   (Newton himself used this one in 1669)
Also: computing sqrt(2) by solving x^2 - 2 = 0.

Bisection: keep cutting an interval in half. Slow but always works.
Newton's method: follow the tangent line to where it crosses zero:
    x_next = x - f(x) / f'(x)
Usually much faster: the number of correct digits roughly doubles each step.
"""
import matplotlib.pyplot as plt


def f(x):
    return x**3 - 2*x - 5


def df(x):          # derivative of f
    return 3*x**2 - 2


def newton(f, df, x, tol=1e-12, max_steps=50):
    history = [x]
    for _ in range(max_steps):
        x = x - f(x) / df(x)
        history.append(x)
        if abs(f(x)) < tol:
            break
    return x, history


def bisection(f, low, high, tol=1e-12, max_steps=100):
    if f(low) * f(high) > 0:
        raise ValueError("f(low) and f(high) must have opposite signs")
    history = []
    for _ in range(max_steps):
        mid = (low + high) / 2
        history.append(mid)
        if abs(f(mid)) < tol:
            break
        if f(low) * f(mid) < 0:
            high = mid
        else:
            low = mid
    return mid, history


if __name__ == "__main__":
    root_n, hist_n = newton(f, df, x=2.0)
    root_b, hist_b = bisection(f, 2.0, 3.0)
    print("Solving x^3 - 2x - 5 = 0")
    print(f"Newton:    x = {root_n:.12f} after {len(hist_n) - 1} steps")
    print(f"Bisection: x = {root_b:.12f} after {len(hist_b)} steps\n")

    print("Newton's steps (watch the correct digits double):")
    for i, x in enumerate(hist_n):
        print(f"  step {i}: {x:.15f}")

    sqrt2, hist_s = newton(lambda x: x*x - 2, lambda x: 2*x, x=1.0)
    print(f"\nsqrt(2) by Newton's method: {sqrt2:.15f} in {len(hist_s) - 1} steps")
    print(f"Python's own value:         {2 ** 0.5:.15f}")

    err_n = [max(abs(x - root_n), 1e-16) for x in hist_n]
    err_b = [max(abs(x - root_n), 1e-16) for x in hist_b]
    plt.figure(figsize=(8, 4.5))
    plt.semilogy(range(len(err_b)), err_b, "o-", markersize=3, label="Bisection")
    plt.semilogy(range(len(err_n)), err_n, "s-", label="Newton's method")
    plt.xlabel("Step")
    plt.ylabel("Error (log scale)")
    plt.title("How fast each method finds the root of x³ − 2x − 5")
    plt.legend()
    plt.grid(alpha=0.3, which="both")
    plt.tight_layout()
    plt.savefig("newton.png", dpi=150)
    print("Saved the chart as newton.png")
    plt.show()
