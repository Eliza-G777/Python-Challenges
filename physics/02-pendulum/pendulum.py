"""
The pendulum: when does the textbook formula stop working?

The formula taught in school, T = 2*pi*sqrt(L/g), assumes small swings.
This program simulates a real pendulum at different starting angles and
measures its period, so you can see how far the formula is off for big swings.

Physics used:
  Angular acceleration = -(g / L) * sin(theta)   (the exact equation)
  The formula uses sin(theta) ≈ theta, which is only true for small angles.
"""
import math
import matplotlib.pyplot as plt

G = 9.81      # m/s^2
L = 1.0       # pendulum length in metres
DT = 0.0005   # time step, s


def formula_period(length):
    return 2 * math.pi * math.sqrt(length / G)


def simulated_period(start_angle_deg, length=L):
    """Release the pendulum from rest and time one full swing.
    A quarter swing ends when it first passes the bottom (theta = 0)."""
    theta = math.radians(start_angle_deg)
    omega = 0.0          # angular speed
    t = 0.0
    while theta > 0:
        alpha = -(G / length) * math.sin(theta)
        omega += alpha * DT          # semi-implicit Euler: update speed first,
        theta += omega * DT          # then position (keeps the swing stable)
        t += DT
    return 4 * t                     # four quarter swings make one period


if __name__ == "__main__":
    t_formula = formula_period(L)
    print(f"Pendulum length {L} m. Formula period: {t_formula:.3f} s\n")
    print("Start angle | Simulated period | Formula error")

    angles = list(range(5, 176, 5))
    periods = []
    for a in angles:
        p = simulated_period(a)
        periods.append(p)
        if a in (5, 15, 30, 45, 60, 90, 120, 150, 170):
            error = (p - t_formula) / p * 100
            print(f"{a:>8}°   | {p:>12.3f} s   | {error:>8.1f} %")

    plt.figure(figsize=(8, 4.5))
    plt.plot(angles, periods, "o-", markersize=3, label="Simulated (exact equation)")
    plt.axhline(t_formula, color="gray", linestyle="--", label="Formula 2π√(L/g)")
    plt.xlabel("Starting angle (degrees)")
    plt.ylabel("Period (s)")
    plt.title("Bigger swings take longer: where the small-angle formula breaks")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("pendulum.png", dpi=150)
    print("\nSaved the chart as pendulum.png")
    plt.show()
