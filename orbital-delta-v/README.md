# Orbital Delta-v Calculator

A small, educational Python project for estimating an idealized Hohmann transfer between two circular, coplanar orbits around the same central body.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m pip install -e ".[test]"
python -m pytest
```

Example: estimate a transfer between circular orbits with radii of 7,000 km and 14,000 km around Earth. Radii are measured from Earth's centre, not its surface.

```bash
python -m orbital_delta_v \
  --initial-radius-m 7000000 \
  --final-radius-m 14000000 \
  --mu-m3-s2 3.986004418e14
```

The command reports the two burn magnitudes, total delta-v, and idealized half-ellipse transfer time.

## Python API

```python
from orbital_delta_v import hohmann_transfer

result = hohmann_transfer(
    initial_radius_m=7_000_000,
    final_radius_m=14_000_000,
    gravitational_parameter_m3_s2=3.986004418e14,
)

print(result.total_delta_v_m_s)
print(result.transfer_time_s)
```

All inputs and outputs use SI units: metres, seconds, metres per second, and m³/s².

## What the model assumes

- Initial and target orbits are circular and coplanar.
- The spacecraft follows an ideal two-body transfer ellipse.
- Both burns are instantaneous impulses.
- The central body's gravitational parameter is supplied by the caller.

The model does **not** include perturbations, atmospheric drag, finite-burn effects, plane changes, launch/landing losses, spacecraft mass, or propulsion performance. It is not a complete mission design tool.

## Project structure

- `orbital_delta_v/hohmann.py`: calculation and validated result type.
- `orbital_delta_v/__main__.py`: command-line entry point.
- `tests/test_hohmann.py`: calculation and input-validation tests.
- `.github/workflows/tests.yml`: automated test matrix for Python 3.10–3.13.

## Disclaimer

This is an educational calculator, not a validated flight-dynamics tool. Independently verify the model, assumptions, units, and outputs before using them for engineering decisions.
