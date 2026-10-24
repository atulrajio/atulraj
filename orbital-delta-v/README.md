# Orbital Delta-v Calculator

A small, educational Python project for estimating the idealized delta-v required for a Hohmann transfer between two circular, coplanar orbits around the same central body.

## Scope

The first version will focus on a clearly defined calculation, unit-safe inputs, readable output, and automated tests. It is not intended for operational mission planning.

## Planned features

- Compute transfer-orbit periapsis and apoapsis speeds.
- Estimate the two impulsive burns for a Hohmann transfer.
- Validate radii and gravitational parameter inputs.
- Provide examples using SI units (metres, seconds, and metres per second).
- Include tests for edge cases and known relationships.

## Model assumptions

The idealized model assumes two circular, coplanar orbits; instantaneous impulses; a two-body gravitational model; and no atmospheric drag, finite-burn effects, perturbations, plane changes, or launch/landing losses.

## Status

Initial project brief. Implementation and tests will be added in follow-up commits.

## Disclaimer

This is an educational calculator, not a validated flight-dynamics tool. Verify the model and all outputs independently before using them for engineering decisions.
