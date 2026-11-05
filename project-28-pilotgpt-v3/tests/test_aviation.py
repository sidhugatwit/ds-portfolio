"""Hand-worked checks for PilotGPT's flight math. Run: uv run pytest -q"""
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import aviation as av  # noqa: E402


def test_crosswind_from_right_and_west_variation():
    # TAS 100, course 360, wind 090/20: WCA = asin(20/100) = 11.5° right; GS = 100 cos 11.5° = 98.0
    s = av.wind_triangle(100, 360, 90, 20, variation_deg=-14)  # 14°W
    assert s.wind_correction_angle == pytest.approx(11.5, abs=0.1)
    assert s.ground_speed == pytest.approx(98.0, abs=0.1)
    assert s.true_heading == pytest.approx(11.5, abs=0.1)
    assert s.magnetic_heading == pytest.approx(25.5, abs=0.1)  # West is best: add 14


def test_east_variation_is_subtracted():
    s = av.wind_triangle(100, 90, 90, 0, variation_deg=15)  # 15°E, no wind
    assert s.magnetic_heading == pytest.approx(75, abs=0.1)


def test_headwind_and_tailwind():
    assert av.wind_triangle(120, 270, 270, 30).ground_speed == pytest.approx(90)
    assert av.wind_triangle(120, 90, 270, 20).ground_speed == pytest.approx(140)


def test_impossible_crosswind_raises():
    with pytest.raises(ValueError):
        av.wind_triangle(30, 360, 90, 40)


def test_density_altitude_hot_high_field():
    # PA 5,000 ft; ISA at 5,000 = 15 - 9.9 = 5.1 °C; DA = 5,000 + 118.8 x 24.9 = 7,958 ft
    r = av.density_altitude(5000, 30, 29.92)
    assert r["pressure_altitude_ft"] == 5000
    assert r["density_altitude_ft"] == pytest.approx(7958, abs=2)


def test_pressure_altitude_low_altimeter():
    assert av.pressure_altitude(19, 29.85) == pytest.approx(89)


@pytest.mark.parametrize("inbound, heading, expected", [
    (360, 360, "Direct"),    # arriving along the inbound course
    (360, 300, "Direct"),
    (360, 100, "Parallel"),  # arriving from the non-holding side
    (360, 200, "Teardrop"),  # arriving from the holding side, beyond the fix
    (90, 200, "Parallel"),   # the notebook's demo question
])
def test_holding_entries_right_turns(inbound, heading, expected):
    assert av.holding_entry(inbound, heading)["entry"] == expected


def test_holding_entries_left_turns_mirror_right():
    assert av.holding_entry(360, 160, right_turns=False)["entry"] == "Teardrop"
    assert av.holding_entry(360, 260, right_turns=False)["entry"] == "Parallel"


def test_parallel_entry_turns_toward_holding_side():
    h = av.holding_entry(90, 200)
    assert "turn left toward the holding (south) side" in h["steps"]
    assert "non-holding (north) side" in h["steps"]


@pytest.mark.parametrize("inbound, right, holding, non_holding", [
    (90, True, "south", "north"),
    (90, False, "north", "south"),
    (360, True, "east", "west"),
    (180, True, "west", "east"),
])
def test_holding_side_in_compass_terms(inbound, right, holding, non_holding):
    h = av.holding_entry(inbound, inbound, right_turns=right)
    assert h["holding_side"].startswith(holding)
    assert h["non_holding_side"].startswith(non_holding)


def test_vfr_above_the_ceiling_is_no_go():
    r = av.vfr_check(4, 2500, 3000, "C")
    assert not r["legal"]
    assert "no higher than 2,000 ft" in r["problems"][0]


def test_vfr_legal_but_marginal():
    r = av.vfr_check(4, 2500, 2000, "C")
    assert r["legal"] and r["flight_category"] == "MVFR"


def test_class_d_low_visibility_needs_special_vfr():
    r = av.vfr_check(2, 3000, 1500, "D")
    assert not r["legal"]
    assert any("Special VFR" in p for p in r["problems"])


def test_class_g_low_level_day():
    r = av.vfr_check(1.5, None, 1000, "G", surface_area=False)
    assert r["legal"]


def test_class_b_clear_of_clouds():
    assert av.vfr_check(3, 2000, 1900, "B")["legal"]
    assert not av.vfr_check(3, 2000, 2000, "B")["legal"]


def test_class_a_never_vfr():
    assert not av.vfr_check(10, None, 20000, "A")["legal"]


def test_flight_categories():
    assert av.flight_category(10, None) == "VFR"
    assert av.flight_category(5, 4000) == "MVFR"
    assert av.flight_category(2, 4000) == "IFR"
    assert av.flight_category(10, 400) == "LIFR"


def test_boston_variation_is_about_14_west():
    v = av.magnetic_variation(42.3656, -71.0096, date(2026, 11, 5))
    assert -15 < v < -13
    assert av.format_variation(v).endswith("W")


def test_boston_to_jfk_distance():
    d = av.haversine_nm(42.3656, -71.0096, 40.6413, -73.7781)
    assert 155 < d < 170
