"""
Earth's orbit from Newton's law of gravity.

Question: If we only know Newton's law of gravitation and Earth's distance and
speed, can a computer predict that a year lasts about 365 days?

Physics used:
  Force of gravity: F = G*M*m / r^2, pointing toward the Sun
  So Earth's acceleration: a = -G*M * r_vector / r^3
  Solved with the "velocity Verlet" method, which keeps orbits stable
  (a simple method like Euler makes the planet slowly spiral away).
"""
import math
import matplotlib.pyplot as plt

GM_SUN = 1.327e20          # G times the Sun's mass, m^3/s^2
AU = 1.496e11              # Earth–Sun distance, m
V_EARTH = 29_780           # Earth's average orbital speed, m/s
DAY = 86_400               # seconds in a day
DT = 3600                  # time step: one hour


def acceleration(x, y):
    r = math.hypot(x, y)
    return -GM_SUN * x / r**3, -GM_SUN * y / r**3


def energy(x, y, vx, vy):
    """Energy per kilogram of Earth. It should stay constant if the simulation is good."""
    return 0.5 * (vx**2 + vy**2) - GM_SUN / math.hypot(x, y)


def simulate(days, speed=V_EARTH):
    x, y = AU, 0.0             # start to the right of the Sun
    vx, vy = 0.0, speed        # moving "up"
    ax, ay = acceleration(x, y)
    xs, ys = [x], [y]
    year_length = None
    e_start = energy(x, y, vx, vy)
    steps = int(days * DAY / DT)
    for step in range(1, steps + 1):
        # velocity Verlet
        x += vx * DT + 0.5 * ax * DT**2
        y_old = y
        y += vy * DT + 0.5 * ay * DT**2
        ax_new, ay_new = acceleration(x, y)
        vx += 0.5 * (ax + ax_new) * DT
        vy += 0.5 * (ay + ay_new) * DT
        ax, ay = ax_new, ay_new
        xs.append(x)
        ys.append(y)
        # one full orbit = crossing the starting line (y = 0, x > 0) again, going up
        if year_length is None and y_old < 0 <= y and x > 0:
            year_length = step * DT / DAY
    drift = abs(energy(x, y, vx, vy) - e_start) / abs(e_start) * 100
    return xs, ys, year_length, drift


if __name__ == "__main__":
    xs, ys, year, drift = simulate(days=400)
    print(f"Predicted length of a year: {year:.1f} days (real value: 365.25)")
    print(f"Energy changed by only {drift:.1e}% over the simulation (a good sign: energy should be conserved)")

    # What if Earth were 20% slower? It falls into an oval (elliptical) orbit.
    xs2, ys2, year2, _ = simulate(days=400, speed=V_EARTH * 0.8)
    print(f"With 20% less speed, the orbit becomes an oval and a year lasts {year2:.1f} days")

    plt.figure(figsize=(6, 6.8))
    plt.plot([x / AU for x in xs], [y / AU for y in ys], label="Earth (real speed)")
    plt.plot([x / AU for x in xs2], [y / AU for y in ys2], "--", label="Earth with 20% less speed")
    plt.plot(0, 0, "o", color="orange", markersize=14, label="Sun")
    plt.xlabel("x (AU)")
    plt.ylabel("y (AU)")
    plt.title("Orbits from Newton's law of gravity")
    plt.axis("equal")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=9)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("orbit.png", dpi=150)
    print("Saved the chart as orbit.png")
    plt.show()
