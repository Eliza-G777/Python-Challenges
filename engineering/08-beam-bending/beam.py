"""
How much does a beam bend? Choosing a material for a small footbridge.

Question: A 4-metre footbridge beam carries people walking on it.
Which material bends least: wood, aluminium or steel? And why do real
beams have an "I" shape? We compare a solid square bar with an I-beam
made from exactly the same amount of material.

Engineering formula (simply supported beam, evenly spread load w):
  Deflection along the beam:  y(x) = w*x*(L^3 - 2*L*x^2 + x^3) / (24*E*I)
  Largest sag (middle):       y_max = 5*w*L^4 / (384*E*I)
  E = stiffness of the material (Young's modulus)
  I = how the cross-section's shape resists bending (second moment of area)
"""
import matplotlib.pyplot as plt

L = 4.0                 # beam length, m
W = 2_000.0             # load, N per metre of beam (about 2 people per metre)
LIMIT = L / 360         # common design rule: sag must stay under span / 360

MATERIALS = {           # Young's modulus E in pascals
    "Wood (pine)": 10e9,
    "Aluminium": 69e9,
    "Steel": 200e9,
}


def rectangle_I(width, height):
    """Second moment of area of a solid rectangle (m^4)."""
    return width * height**3 / 12


def i_beam_I(flange_w, flange_t, web_t, total_h):
    """Second moment of area of an I-beam: a big rectangle minus the two side gaps."""
    gap_w = (flange_w - web_t) / 2
    gap_h = total_h - 2 * flange_t
    return rectangle_I(flange_w, total_h) - 2 * rectangle_I(gap_w, gap_h)


def deflection(x, E, I):
    return W * x * (L**3 - 2 * L * x**2 + x**3) / (24 * E * I)


if __name__ == "__main__":
    solid = rectangle_I(0.10, 0.10)                       # 10 cm × 10 cm solid bar
    ibeam = i_beam_I(0.10, 0.02, 0.0375, 0.20)            # 20 cm tall I-beam
    area_solid = 0.10 * 0.10
    area_i = 2 * 0.10 * 0.02 + 0.0375 * (0.20 - 2 * 0.02)  # same area = same weight

    print(f"Span {L} m, load {W:,.0f} N/m. Allowed sag: {LIMIT * 1000:.1f} mm\n")
    print("Material      | Shape     | Max sag   | Passes?")
    results = []
    for name, E in MATERIALS.items():
        for shape, I in (("Solid", solid), ("I-beam", ibeam)):
            sag = 5 * W * L**4 / (384 * E * I)
            results.append((name, shape, E, I, sag))
            print(f"{name:<13} | {shape:<9} | {sag * 1000:>6.1f} mm | {'yes' if sag <= LIMIT else 'NO'}")

    print(f"\nBoth shapes use the same amount of material ({area_solid * 1e4:.0f} cm² cross-section),")
    print(f"but the I-beam is {ibeam / solid:.1f} times stiffer, because its material sits far from the middle,")
    print("where bending stretches and squeezes it most. That's why bridges and buildings use I-beams.")

    xs = [L * i / 200 for i in range(201)]
    plt.figure(figsize=(8, 4.5))
    for name, shape, E, I, sag in results:
        if shape == "I-beam":
            plt.plot(xs, [-deflection(x, E, I) * 1000 for x in xs], label=f"{name}, I-beam ({sag * 1000:.1f} mm)")
    plt.axhline(-LIMIT * 1000, color="red", linestyle="--", label=f"Design limit ({LIMIT * 1000:.1f} mm)")
    plt.xlabel("Position along the beam (m)")
    plt.ylabel("Sag (mm)")
    plt.title("How far each 4 m I-beam bends under people walking on it")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("beam.png", dpi=150)
    print("Saved the chart as beam.png")
    plt.show()
