import math

import pytest

from orbital_delta_v import hohmann_transfer


EARTH_MU_M3_S2 = 3.986004418e14


def test_transfer_returns_positive_burns_and_expected_time():
    result = hohmann_transfer(7_000_000, 14_000_000, EARTH_MU_M3_S2)

    assert result.first_burn_m_s == pytest.approx(1_167, abs=3)
    assert result.second_burn_m_s == pytest.approx(979, abs=3)
    assert result.total_delta_v_m_s == pytest.approx(
        result.first_burn_m_s + result.second_burn_m_s
    )
    assert result.transfer_time_s == pytest.approx(5_354, abs=20)
    assert result.transfer_semimajor_axis_m == pytest.approx(10_500_000)


def test_transfer_is_symmetric_in_total_delta_v_for_reversed_radii():
    outward = hohmann_transfer(7_000_000, 14_000_000, EARTH_MU_M3_S2)
    inward = hohmann_transfer(14_000_000, 7_000_000, EARTH_MU_M3_S2)

    assert inward.total_delta_v_m_s == pytest.approx(outward.total_delta_v_m_s)
    assert inward.transfer_time_s == pytest.approx(outward.transfer_time_s)


def test_same_radius_has_zero_delta_v():
    result = hohmann_transfer(7_000_000, 7_000_000, EARTH_MU_M3_S2)

    assert result.first_burn_m_s == pytest.approx(0)
    assert result.second_burn_m_s == pytest.approx(0)
    assert result.total_delta_v_m_s == pytest.approx(0)
    assert result.transfer_time_s > 0


@pytest.mark.parametrize(
    "r1, r2, mu",
    [
        (0, 1, 1),
        (-1, 1, 1),
        (1, 0, 1),
        (1, -1, 1),
        (1, 1, 0),
        (1, 1, -1),
        (math.inf, 1, 1),
        (1, math.nan, 1),
        (1, 1, math.inf),
    ],
)
def test_non_positive_or_non_finite_inputs_are_rejected(r1, r2, mu):
    with pytest.raises(ValueError):
        hohmann_transfer(r1, r2, mu)


def test_non_numeric_inputs_are_rejected():
    with pytest.raises(TypeError):
        hohmann_transfer("7000000", 14_000_000, EARTH_MU_M3_S2)
