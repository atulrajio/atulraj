"""Educational two-body Hohmann transfer calculations."""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real


@dataclass(frozen=True)
class HohmannTransfer:
    """Results for an idealized transfer, expressed in SI units."""

    initial_radius_m: float
    final_radius_m: float
    gravitational_parameter_m3_s2: float
    transfer_semimajor_axis_m: float
    first_burn_m_s: float
    second_burn_m_s: float
    total_delta_v_m_s: float
    transfer_time_s: float


def _positive_finite(value: float, name: str) -> float:
    """Return a numeric finite positive value, or raise a useful error."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be finite and greater than zero")
    return number


def hohmann_transfer(
    initial_radius_m: float,
    final_radius_m: float,
    gravitational_parameter_m3_s2: float,
) -> HohmannTransfer:
    """Estimate a Hohmann transfer between two circular, coplanar orbits.

    Args:
        initial_radius_m: Initial orbital radius from the central body's
            centre, in metres (not altitude above its surface).
        final_radius_m: Target orbital radius from the central body's centre,
            in metres (not altitude above its surface).
        gravitational_parameter_m3_s2: Standard gravitational parameter mu
            of the central body, in m^3/s^2.

    Returns:
        A frozen result object containing the idealized burn magnitudes and
        half-ellipse transfer time in SI units.

    Assumptions:
        Two-body gravity, circular coplanar endpoint orbits, and instantaneous
        impulses. Perturbations, atmospheric drag, finite-burn effects,
        plane changes, and launch/landing losses are excluded.
    """
    r1 = _positive_finite(initial_radius_m, "initial_radius_m")
    r2 = _positive_finite(final_radius_m, "final_radius_m")
    mu = _positive_finite(
        gravitational_parameter_m3_s2, "gravitational_parameter_m3_s2"
    )

    transfer_a = (r1 + r2) / 2.0
    circular_speed_1 = math.sqrt(mu / r1)
    circular_speed_2 = math.sqrt(mu / r2)
    transfer_speed_1 = math.sqrt(mu * (2.0 / r1 - 1.0 / transfer_a))
    transfer_speed_2 = math.sqrt(mu * (2.0 / r2 - 1.0 / transfer_a))

    first_burn = abs(transfer_speed_1 - circular_speed_1)
    second_burn = abs(circular_speed_2 - transfer_speed_2)
    total_delta_v = first_burn + second_burn
    transfer_time = math.pi * math.sqrt(transfer_a**3 / mu)

    return HohmannTransfer(
        initial_radius_m=r1,
        final_radius_m=r2,
        gravitational_parameter_m3_s2=mu,
        transfer_semimajor_axis_m=transfer_a,
        first_burn_m_s=first_burn,
        second_burn_m_s=second_burn,
        total_delta_v_m_s=total_delta_v,
        transfer_time_s=transfer_time,
    )
