"""Offline checks for METAR decoding (no network)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import weather as wx  # noqa: E402

SAMPLE = {
    "icaoId": "KBOS", "reportTime": "2026-11-05T18:54:00Z",
    "rawOb": "KBOS 051854Z 27012G20KT 10SM FEW035 BKN050 OVC250 12/02 A2996",
    "wdir": 270, "wspd": 12, "wgst": 20, "visib": "10+",
    "clouds": [{"cover": "FEW", "base": 3500}, {"cover": "BKN", "base": 5000}, {"cover": "OVC", "base": 25000}],
    "temp": 12, "dewp": 2, "altim": 1014.6, "elev": 6, "wxString": None,
}


def test_parse_metar_ceiling_is_lowest_broken_layer():
    m = wx.parse_metar(SAMPLE)
    assert m["ceiling_ft_agl"] == 5000
    assert m["visibility_sm"] == 10
    assert m["altimeter_inhg"] == pytest.approx(29.96, abs=0.01)
    assert m["field_elevation_ft"] == 20


def test_no_ceiling_when_only_few_or_scattered():
    m = wx.parse_metar({**SAMPLE, "clouds": [{"cover": "SCT", "base": 4000}]})
    assert m["ceiling_ft_agl"] is None


def test_fractional_visibility_and_inhg_altimeter():
    assert wx._visibility_sm("1 1/2") == pytest.approx(1.5)
    assert wx._visibility_sm("3/4") == pytest.approx(0.75)
    assert wx._altimeter_inhg(29.92) == 29.92
