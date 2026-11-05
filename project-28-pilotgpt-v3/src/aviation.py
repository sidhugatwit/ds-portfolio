"""Flight-planning math and rules for PilotGPT v3.

Educational only. Not for navigation or flight planning.

Sources:
- 14 CFR 91.155 (basic VFR weather minimums) and FAA Aeronautical Information Manual (AIM) 5-3-8 (holding entries)
- FAA Pilot's Handbook of Aeronautical Knowledge: wind triangle, magnetic variation, density altitude
- Magnetic variation from NOAA's World Magnetic Model (WMM2025) via pygeomag
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date

EARTH_RADIUS_NM = 3440.065


def haversine_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in nautical miles."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return EARTH_RADIUS_NM * 2 * math.asin(math.sqrt(a))


def true_course(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Initial great-circle true course in degrees (0-360)."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    x = math.sin(lon2 - lon1) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


# --- Magnetic variation -------------------------------------------------------------

_GEOMAG = None


def magnetic_variation(lat: float, lon: float, when: date | None = None) -> float:
    """Magnetic variation (declination) in degrees from WMM2025. East is positive, West negative."""
    global _GEOMAG
    from pygeomag import GeoMag

    if _GEOMAG is None:
        _GEOMAG = GeoMag(coefficients_file="wmm/WMM_2025.COF")
    when = when or date.today()
    decimal_year = when.year + (when.timetuple().tm_yday - 1) / 365.25
    return _GEOMAG.calculate(glat=lat, glon=lon, alt=0, time=decimal_year).d


def format_variation(var_deg: float) -> str:
    return f"{abs(var_deg):.1f}°{'E' if var_deg >= 0 else 'W'}"


# --- Wind triangle ------------------------------------------------------------------

@dataclass
class WindSolution:
    wind_correction_angle: float  # degrees; positive means turn right (into a wind from the right)
    true_heading: float
    magnetic_heading: float
    ground_speed: float
    headwind: float  # knots; negative means tailwind
    crosswind: float  # knots; positive means from the right


def wind_triangle(tas_kt: float, true_course_deg: float, wind_from_deg: float, wind_kt: float,
                  variation_deg: float = 0.0) -> WindSolution:
    """Solve the E6B wind triangle.

    variation_deg follows the chart convention: East positive, West negative.
    Magnetic heading = true heading - East variation + West variation ("East is least, West is best").
    """
    if tas_kt <= 0:
        raise ValueError("True airspeed must be positive.")
    angle = math.radians(wind_from_deg - true_course_deg)
    headwind = wind_kt * math.cos(angle)
    crosswind = wind_kt * math.sin(angle)
    if abs(crosswind) >= tas_kt:
        raise ValueError("Crosswind component is at least the true airspeed: the course can't be held.")
    wca = math.degrees(math.asin(crosswind / tas_kt))
    ground_speed = tas_kt * math.cos(math.radians(wca)) - headwind
    true_heading = (true_course_deg + wca) % 360
    magnetic_heading = (true_heading - variation_deg) % 360
    return WindSolution(round(wca, 1), round(true_heading, 1), round(magnetic_heading, 1),
                        round(ground_speed, 1), round(headwind, 1), round(crosswind, 1))


# --- Density altitude ---------------------------------------------------------------

def pressure_altitude(field_elevation_ft: float, altimeter_inhg: float) -> float:
    return field_elevation_ft + (29.92 - altimeter_inhg) * 1000


def density_altitude(field_elevation_ft: float, oat_c: float, altimeter_inhg: float = 29.92) -> dict:
    """Density altitude by the FAA rule of thumb: DA = PA + 118.8 x (OAT - ISA temperature at PA)."""
    pa = pressure_altitude(field_elevation_ft, altimeter_inhg)
    isa_c = 15 - 1.98 * pa / 1000
    return {
        "pressure_altitude_ft": round(pa),
        "isa_temp_c": round(isa_c, 1),
        "density_altitude_ft": round(pa + 118.8 * (oat_c - isa_c)),
    }


# --- Holding entries (AIM 5-3-8) -----------------------------------------------------

_COMPASS = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]


def compass_word(bearing: float) -> str:
    return _COMPASS[round((bearing % 360) / 45) % 8]

def holding_entry(inbound_course: float, heading: float, right_turns: bool = True) -> dict:
    """Recommended holding entry from the aircraft's heading on arrival at the fix.

    Uses the AIM sectors: a 70-degree line through the fix splits arrivals into direct (180 degrees),
    teardrop (70 degrees, holding side) and parallel (110 degrees, non-holding side).
    Within about 5 degrees of a boundary either entry is acceptable.
    """
    inbound = inbound_course % 360
    outbound = (inbound + 180) % 360
    rel = (heading - inbound) % 360 if right_turns else (inbound - heading) % 360
    turn, opposite = ("right", "left") if right_turns else ("left", "right")
    holding_side = compass_word(inbound + (90 if right_turns else -90))
    non_holding_side = compass_word(inbound - (90 if right_turns else -90))
    if rel <= 70 or rel >= 250:
        entry = "Direct"
        steps = f"Cross the fix and turn {turn} to the outbound heading {outbound:03.0f}°, then fly the pattern."
    elif rel <= 180:
        entry = "Parallel"
        steps = (f"Cross the fix and turn to the outbound heading {outbound:03.0f}° on the non-holding ({non_holding_side}) side for 1 minute. "
                 f"Then turn {opposite} toward the holding ({holding_side}) side through more than 180° and intercept the inbound course "
                 f"{inbound:03.0f}° or return to the fix.")
    else:
        entry = "Teardrop"
        teardrop = (outbound - 30) % 360 if right_turns else (outbound + 30) % 360
        steps = (f"Cross the fix and fly heading {teardrop:03.0f}° (30° into the holding side, {holding_side} of the course) for 1 minute. "
                 f"Then turn {turn} to intercept the inbound course {inbound:03.0f}°.")
    lo, hi = {"Direct": (250, 70), "Parallel": (70, 180), "Teardrop": (180, 250)}[entry]
    first, last = ((inbound + lo) % 360, (inbound + hi) % 360) if right_turns else ((inbound - hi) % 360, (inbound - lo) % 360)
    why = (f"Heading {heading % 360:03.0f}° is in the {entry.lower()} sector, which covers arrival headings "
           f"{first:03.0f}° clockwise to {last:03.0f}° for this hold (AIM 5-3-8).")
    near_boundary = min(abs(rel - b) for b in (70, 180, 250)) <= 5
    return {"entry": entry, "steps": steps, "why": why, "turns": turn,
            "holding_side": f"{holding_side} of the inbound course", "non_holding_side": f"{non_holding_side} of the inbound course",
            "note": "Within 5° of a sector boundary: either entry is acceptable." if near_boundary else ""}


# --- VFR weather minimums (14 CFR 91.155, day) ----------------------------------------

@dataclass(frozen=True)
class VfrMinimums:
    visibility_sm: float
    below_ft: int | None  # None means clear of clouds
    above_ft: int | None
    horizontal: str | None


def vfr_minimums(airspace_class: str, altitude_msl_ft: float, altitude_agl_ft: float) -> VfrMinimums | None:
    """Basic VFR weather minimums for daytime flight. Returns None where VFR is not allowed (Class A)."""
    c = airspace_class.upper()
    if c == "A":
        return None
    if c == "B":
        return VfrMinimums(3, None, None, None)
    if c in ("C", "D"):
        return VfrMinimums(3, 500, 1000, "2,000 ft")
    if c == "E":
        if altitude_msl_ft >= 10_000:
            return VfrMinimums(5, 1000, 1000, "1 SM")
        return VfrMinimums(3, 500, 1000, "2,000 ft")
    if c == "G":
        if altitude_agl_ft <= 1200:
            return VfrMinimums(1, None, None, None)
        if altitude_msl_ft >= 10_000:
            return VfrMinimums(5, 1000, 1000, "1 SM")
        return VfrMinimums(1, 500, 1000, "2,000 ft")
    raise ValueError(f"Unknown airspace class: {airspace_class}")


def flight_category(visibility_sm: float, ceiling_ft: float | None) -> str:
    """Aviation Weather Center flight category: VFR, MVFR, IFR or LIFR."""
    ceiling = math.inf if ceiling_ft is None else ceiling_ft
    if ceiling < 500 or visibility_sm < 1:
        return "LIFR"
    if ceiling < 1000 or visibility_sm < 3:
        return "IFR"
    if ceiling <= 3000 or visibility_sm <= 5:
        return "MVFR"
    return "VFR"


def vfr_check(visibility_sm: float, ceiling_agl_ft: float | None, cruise_agl_ft: float,
              airspace_class: str, field_elevation_ft: float = 0, surface_area: bool = True) -> dict:
    """Day VFR go/no-go against 14 CFR 91.155 for one airspace class and cruise altitude.

    ceiling_agl_ft: lowest broken or overcast layer above ground level (None if there's no ceiling).
    surface_area: True when operating in the Class B, C, D or E surface area of an airport,
    where 91.155(c) and (d) require a 1,000 ft ceiling and 3 SM ground visibility.
    """
    c = airspace_class.upper()
    mins = vfr_minimums(c, field_elevation_ft + cruise_agl_ft, cruise_agl_ft)
    problems, ok, options = [], [], []
    if mins is None:
        problems.append("Class A: VFR flight is not allowed; IFR clearance required.")
    else:
        if visibility_sm < mins.visibility_sm:
            problems.append(f"Visibility {visibility_sm:g} SM is below the {mins.visibility_sm:g} SM minimum for Class {c}.")
        else:
            ok.append(f"Visibility {visibility_sm:g} SM meets the {mins.visibility_sm:g} SM minimum for Class {c}.")
        if ceiling_agl_ft is not None:
            if mins.below_ft is None:
                if cruise_agl_ft >= ceiling_agl_ft:
                    problems.append(f"Cruise at {cruise_agl_ft:,.0f} ft AGL is at or above the {ceiling_agl_ft:,.0f} ft ceiling: you must stay clear of clouds.")
                else:
                    ok.append(f"Cruise below the {ceiling_agl_ft:,.0f} ft ceiling, clear of clouds.")
            else:
                highest = ceiling_agl_ft - mins.below_ft
                if cruise_agl_ft > highest:
                    problems.append(
                        f"Class {c} needs {mins.below_ft} ft below clouds: with a {ceiling_agl_ft:,.0f} ft ceiling, "
                        f"cruise no higher than {highest:,.0f} ft AGL (planned {cruise_agl_ft:,.0f}).")
                    options.append(f"Cruise at or below {highest:,.0f} ft AGL, or wait for a higher ceiling.")
                else:
                    ok.append(f"Cruise {cruise_agl_ft:,.0f} ft AGL keeps {mins.below_ft} ft below the {ceiling_agl_ft:,.0f} ft ceiling.")
        if surface_area and c in ("B", "C", "D", "E"):
            if ceiling_agl_ft is not None and ceiling_agl_ft < 1000:
                problems.append("Ceiling below 1,000 ft in a surface area: VFR needs a Special VFR clearance (91.155(c)).")
            if visibility_sm < 3:
                problems.append("Ground visibility below 3 SM in a surface area: no VFR takeoff or landing without Special VFR (91.155(d)).")
    if ceiling_agl_ft is not None and cruise_agl_ft >= ceiling_agl_ft:
        options.append("Flying above the ceiling is not a VFR option: a broken or overcast layer can't be climbed "
                       "through in VFR, and you would need a legal way back down.")
    category = flight_category(visibility_sm, ceiling_agl_ft)
    legal = not problems
    if not legal:
        verdict = "NO-GO: below VFR minimums for this plan"
    elif category == "VFR":
        verdict = "GO: VFR minimums met"
    else:
        verdict = f"LEGAL but {category}: minimums met with little margin; consider a higher personal minimum"
    return {"verdict": verdict, "legal": legal, "flight_category": category,
            "problems": problems, "checks_passed": ok, "options": options,
            "assumptions": "Daytime, basic VFR minimums only; check airspace altitude limits, NOTAMs and TFRs separately."}
