"""
Keeping a water tank at the right level: on/off control vs a PID controller.

Question: A village water tank drains as people use water, and a pump refills it.
How should the pump decide how hard to work, so the level stays steady?

Two strategies:
  On/off (like a fridge thermostat): pump at full power when low, off when high.
  PID controller (used in drones, cruise control, factories):
    pump power = Kp*error + Ki*(sum of past errors) + Kd*(how fast the error is changing)
    error = target level - current level
"""
import matplotlib.pyplot as plt

AREA = 2.0          # tank floor area, m^2
PUMP_MAX = 0.02     # pump's full flow, m^3/s
TARGET = 1.5        # wanted water level, m
DT = 1.0            # one-second steps
MINUTES = 60


def usage(t):
    """Water drawn by the village (m^3/s): more in the morning rush (minutes 20–40)."""
    return 0.012 if 1200 <= t < 2400 else 0.006


def run(controller):
    level, t = 0.5, 0.0
    times, levels, powers = [], [], []
    state = {"integral": 0.0, "last_error": TARGET - level, "pump_on": True}
    while t < MINUTES * 60:
        power = controller(level, state)                 # 0 = off, 1 = full
        power = max(0.0, min(1.0, power))
        inflow = power * PUMP_MAX
        level += (inflow - usage(t)) / AREA * DT          # volume change ÷ area = height change
        level = max(level, 0.0)
        times.append(t / 60)
        levels.append(level)
        powers.append(power * 100)
        t += DT
    return times, levels, powers


def on_off(level, state):
    if level < TARGET - 0.05:
        state["pump_on"] = True
    elif level > TARGET + 0.05:
        state["pump_on"] = False
    return 1.0 if state["pump_on"] else 0.0


def pid(level, state, kp=10.0, ki=0.05, kd=20.0):
    """Gains chosen by testing many combinations (try changing them!)."""
    error = TARGET - level
    state["integral"] += error * DT
    state["integral"] = max(-50, min(50, state["integral"]))   # stop it growing forever
    derivative = (error - state["last_error"]) / DT
    state["last_error"] = error
    return kp * error + ki * state["integral"] + kd * derivative


def summary(name, times, levels, powers):
    settled = [abs(l - TARGET) for t, l in zip(times, levels) if t > 10]
    switches = sum(1 for a, b in zip(powers, powers[1:]) if (a == 0) != (b == 0))
    print(f"{name:<8} | average distance from target {sum(settled) / len(settled) * 100:.1f} cm | "
          f"largest {max(settled) * 100:.1f} cm | pump switched on/off {switches} times")


if __name__ == "__main__":
    t1, l1, p1 = run(on_off)
    t2, l2, p2 = run(pid)
    print(f"Target level {TARGET} m. Water use doubles from minute 20 to 40.\n")
    summary("On/off", t1, l1, p1)
    summary("PID", t2, l2, p2)
    print("\nThe PID controller holds the level steadier and runs the pump smoothly")
    print("instead of slamming it on and off, which also makes the pump last longer.")

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    top.plot(t1, l1, label="On/off control")
    top.plot(t2, l2, label="PID control")
    top.axhline(TARGET, color="gray", linestyle="--", label="Target")
    top.axvspan(20, 40, color="orange", alpha=0.1, label="Morning rush")
    top.set_ylabel("Water level (m)")
    top.legend(loc="lower right", fontsize=8)
    top.grid(alpha=0.3)
    bottom.plot(t1, p1, label="On/off", alpha=0.7)
    bottom.plot(t2, p2, label="PID")
    bottom.set_ylabel("Pump power (%)")
    bottom.set_xlabel("Time (minutes)")
    bottom.grid(alpha=0.3)
    bottom.legend(loc="upper right", fontsize=8)
    fig.suptitle("Controlling a water tank's level")
    plt.tight_layout()
    plt.savefig("tank_control.png", dpi=150)
    print("Saved the chart as tank_control.png")
    plt.show()
