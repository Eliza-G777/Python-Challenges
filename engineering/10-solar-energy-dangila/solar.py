"""
How much electricity could a solar panel make in Dangila, Ethiopia?

Question: If a family in Dangila puts one solar panel on the roof,
how much energy does it make in a day, and does it change through the year?

Science and engineering used:
  The Sun's height in the sky depends on latitude, the date and the time of day
  (solar declination and hour angle, from spherical geometry).
  A flat panel collects sunlight in proportion to sin(sun height).
  Air absorbs more light when the Sun is low (air mass), so we reduce it a bit.

This is a clear-sky estimate: real output is lower on cloudy days, especially in the rainy season.
"""
import math
import matplotlib.pyplot as plt

LATITUDE = 11.26        # Dangila, degrees north
PANEL_WATTS = 300       # panel rating at full sun (1000 W/m^2)
EFFICIENCY_LOSS = 0.8   # wiring, heat and dust losses


def declination(day):
    """The Sun's angle north/south of the equator on day 1–365 (degrees)."""
    return 23.44 * math.sin(math.radians(360 / 365 * (day - 81)))


def sun_height(day, hour):
    """Height of the Sun above the horizon (degrees) at solar time 'hour'."""
    lat, dec = math.radians(LATITUDE), math.radians(declination(day))
    hour_angle = math.radians(15 * (hour - 12))           # Earth turns 15° per hour
    s = math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(hour_angle)
    return math.degrees(math.asin(s))


def sunlight(height_deg):
    """Clear-sky sunlight reaching a flat panel (W/m^2)."""
    if height_deg <= 0:
        return 0.0
    air_mass = 1 / math.sin(math.radians(height_deg))
    direct = 1361 * 0.7 ** (air_mass ** 0.678)           # light that survives the atmosphere
    return direct * math.sin(math.radians(height_deg))


def panel_power(day, hour):
    return PANEL_WATTS * sunlight(sun_height(day, hour)) / 1000 * EFFICIENCY_LOSS


def daily_energy(day):
    """Energy in watt-hours: add up power over the day in 6-minute steps."""
    step = 0.1
    return sum(panel_power(day, h * step) * step for h in range(int(24 / step)))


if __name__ == "__main__":
    days = {"21 March": 80, "21 June": 172, "21 September": 264, "21 December": 355}
    print(f"One {PANEL_WATTS} W panel in Dangila ({LATITUDE}° N), clear sky:\n")
    print("Date          | Noon sun height | Energy per day")
    for name, d in days.items():
        print(f"{name:<13} | {sun_height(d, 12):>12.1f}°   | {daily_energy(d) / 1000:>6.2f} kWh")

    yearly = [daily_energy(d) for d in range(1, 366)]
    total = sum(yearly) / 1000
    print(f"\nWhole year: about {total:,.0f} kWh on clear days.")
    print(f"That could light six 10 W LED bulbs for 5 hours every day ({6 * 10 * 5 * 365 / 1000:.0f} kWh a year)")
    print("and still leave energy for phones and a radio.")

    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.5))
    hours = [h / 10 for h in range(50, 191)]
    for name, d in days.items():
        left.plot(hours, [panel_power(d, h) for h in hours], label=name)
    left.set_xlabel("Solar time (hour of day)")
    left.set_ylabel("Panel power (W)")
    left.set_title("Power through the day")
    left.legend(fontsize=8)
    left.grid(alpha=0.3)

    right.plot(range(1, 366), [e / 1000 for e in yearly])
    right.set_xlabel("Day of the year")
    right.set_ylabel("Energy per day (kWh)")
    right.set_title("Energy through the year (clear sky)")
    right.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("solar.png", dpi=150)
    print("Saved the chart as solar.png")
    plt.show()
