"""
Projectile motion: with and without air resistance.

Question: A ball is launched at some speed and angle. How far does it go?
And how much does air resistance change the answer, including the best launch angle?

Physics used:
  Without air: x = v*cos(a)*t, y = v*sin(a)*t - (1/2)*g*t^2  (exact formulas)
  With air:    drag force = -k * speed * velocity  (quadratic drag),
               solved step by step in small time steps (numerical simulation).
"""
import math
import matplotlib.pyplot as plt

G = 9.81          # gravity, m/s^2
DT = 0.001        # time step for the simulation, s


def no_drag(speed, angle_deg):
    """Exact answer from the kinematics formulas (no air resistance)."""
    a = math.radians(angle_deg)
    t_flight = 2 * speed * math.sin(a) / G
    distance = speed ** 2 * math.sin(2 * a) / G
    height = (speed * math.sin(a)) ** 2 / (2 * G)
    return distance, height, t_flight


def simulate(speed, angle_deg, k=0.0):
    """Step-by-step simulation. k is the drag constant (0 means no air).
    Returns lists of x and y positions."""
    a = math.radians(angle_deg)
    x, y = 0.0, 0.0
    vx, vy = speed * math.cos(a), speed * math.sin(a)
    xs, ys = [x], [y]
    while y >= 0:
        v = math.hypot(vx, vy)          # current speed
        ax = -k * v * vx                # drag slows it down horizontally
        ay = -G - k * v * vy            # gravity + drag vertically
        vx += ax * DT
        vy += ay * DT
        x += vx * DT
        y += vy * DT
        xs.append(x)
        ys.append(y)
    return xs, ys


def best_angle(speed, k):
    """Try every whole-number angle and return the one that goes farthest."""
    results = [(simulate(speed, angle, k)[0][-1], angle) for angle in range(1, 90)]
    distance, angle = max(results)
    return angle, distance


if __name__ == "__main__":
    speed = 30.0      # m/s (try changing this!)
    angle = 45.0      # degrees
    k = 0.005         # drag constant for a ball, 1/m (try 0.001 to 0.02)

    d, hmax, t = no_drag(speed, angle)
    print(f"Launch: {speed} m/s at {angle} degrees")
    print(f"Formula, no air:     distance {d:.1f} m, max height {hmax:.1f} m, time {t:.2f} s")

    xs, ys = simulate(speed, angle, k=0)
    print(f"Simulation, no air:  distance {xs[-1]:.1f} m  (should match the formula)")

    xd, yd = simulate(speed, angle, k=k)
    print(f"Simulation, with air: distance {xd[-1]:.1f} m, max height {max(yd):.1f} m")

    a_best, d_best = best_angle(speed, k)
    print(f"Best angle with air: {a_best} degrees ({d_best:.1f} m). Without air it is always 45.")

    plt.figure(figsize=(8, 4.5))
    plt.plot(xs, ys, label="No air resistance")
    plt.plot(xd, yd, label=f"With air resistance (k = {k})")
    plt.xlabel("Distance (m)")
    plt.ylabel("Height (m)")
    plt.title(f"Projectile launched at {speed:.0f} m/s, {angle:.0f}°")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("projectile.png", dpi=150)
    print("Saved the chart as projectile.png")
    plt.show()
