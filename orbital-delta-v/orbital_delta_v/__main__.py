"""Command-line entry point: python -m orbital_delta_v."""

import argparse

from .hohmann import hohmann_transfer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate idealized Hohmann-transfer delta-v (SI units)."
    )
    parser.add_argument(
        "--initial-radius-m",
        type=float,
        required=True,
        help="Initial orbital radius from the central body's centre, in metres.",
    )
    parser.add_argument(
        "--final-radius-m",
        type=float,
        required=True,
        help="Target orbital radius from the central body's centre, in metres.",
    )
    parser.add_argument(
        "--mu-m3-s2",
        type=float,
        required=True,
        help="Central body's gravitational parameter in m^3/s^2.",
    )
    args = parser.parse_args()

    result = hohmann_transfer(
        args.initial_radius_m, args.final_radius_m, args.mu_m3_s2
    )
    print(f"First burn:       {result.first_burn_m_s:,.3f} m/s")
    print(f"Second burn:      {result.second_burn_m_s:,.3f} m/s")
    print(f"Total delta-v:    {result.total_delta_v_m_s:,.3f} m/s")
    print(f"Transfer time:    {result.transfer_time_s:,.1f} s")
    print(f"Transfer time:    {result.transfer_time_s / 3600:,.3f} h")


if __name__ == "__main__":
    main()
