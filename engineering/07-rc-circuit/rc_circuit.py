"""
Charging and discharging a capacitor (an RC circuit).

Question: When you connect a capacitor to a battery through a resistor,
how long does it take to charge? Engineers use this in camera flashes,
timers and the "debounce" circuits behind every keyboard key.

Physics used:
  Current through the resistor: I = (V_battery - V_capacitor) / R   (Ohm's law)
  The capacitor's voltage rises as charge flows in: dV/dt = I / C
  Exact answer: V(t) = V_battery * (1 - e^(-t / RC)).  RC is the "time constant".
"""
import math
import matplotlib.pyplot as plt

V_BATTERY = 9.0      # volts
R = 10_000           # ohms (10 kΩ)
C = 100e-6           # farads (100 µF)
TAU = R * C          # time constant in seconds
DT = TAU / 1000      # simulation time step


def simulate(t_end):
    """Charge for half the time, then discharge (battery removed)."""
    t, v = 0.0, 0.0
    times, volts = [t], [v]
    while t < t_end:
        source = V_BATTERY if t < t_end / 2 else 0.0   # switch flips halfway
        current = (source - v) / R                       # Ohm's law
        v += current / C * DT                            # capacitor fills up
        t += DT
        times.append(t)
        volts.append(v)
    return times, volts


if __name__ == "__main__":
    print(f"R = {R:,} Ω, C = {C * 1e6:.0f} µF, time constant RC = {TAU:.2f} s\n")
    print("After... | Formula voltage | % of full charge")
    for n in range(1, 6):
        v = V_BATTERY * (1 - math.exp(-n))
        print(f"{n} × RC   | {v:>12.2f} V  | {v / V_BATTERY * 100:>6.1f} %")
    print("Rule of thumb engineers use: a capacitor is 'full' after about 5 time constants.")

    t_end = 10 * TAU
    times, volts = simulate(t_end)
    exact = [V_BATTERY * (1 - math.exp(-t / TAU)) if t < t_end / 2 else None for t in times]

    plt.figure(figsize=(8, 4.5))
    plt.plot(times, volts, label="Simulation (Ohm's law, step by step)")
    plt.plot(times, exact, "--", label="Exact formula while charging")
    for n in range(1, 6):
        plt.axvline(n * TAU, color="gray", alpha=0.2)
    plt.axvline(t_end / 2, color="red", alpha=0.5, label="Battery disconnected")
    plt.xlabel("Time (s)")
    plt.ylabel("Capacitor voltage (V)")
    plt.title(f"RC circuit: charging and discharging (RC = {TAU:.1f} s)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("rc_circuit.png", dpi=150)
    print("\nSaved the chart as rc_circuit.png")
    plt.show()
