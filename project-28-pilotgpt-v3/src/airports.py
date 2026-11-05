"""Small airport table for the demo. Coordinates and elevations from FAA airport data; classes are
the airspace around each airport's surface area."""
AIRPORTS = {
    "KBOS": {"name": "Boston Logan", "lat": 42.3656, "lon": -71.0096, "elev_ft": 19, "class": "B"},
    "KJFK": {"name": "New York JFK", "lat": 40.6413, "lon": -73.7781, "elev_ft": 13, "class": "B"},
    "KLGA": {"name": "New York LaGuardia", "lat": 40.7772, "lon": -73.8726, "elev_ft": 21, "class": "B"},
    "KORH": {"name": "Worcester Regional", "lat": 42.2673, "lon": -71.8757, "elev_ft": 1009, "class": "D"},
    "KBDL": {"name": "Hartford Bradley", "lat": 41.9389, "lon": -72.6832, "elev_ft": 173, "class": "C"},
    "KMHT": {"name": "Manchester-Boston", "lat": 42.9326, "lon": -71.4357, "elev_ft": 266, "class": "C"},
    "KPVD": {"name": "Providence T.F. Green", "lat": 41.7240, "lon": -71.4282, "elev_ft": 55, "class": "C"},
    "KBED": {"name": "Bedford Hanscom Field", "lat": 42.4700, "lon": -71.2890, "elev_ft": 133, "class": "D"},
    "KORD": {"name": "Chicago O'Hare", "lat": 41.9742, "lon": -87.9073, "elev_ft": 672, "class": "B"},
    "KATL": {"name": "Atlanta Hartsfield-Jackson", "lat": 33.6407, "lon": -84.4277, "elev_ft": 1026, "class": "B"},
    "KSEA": {"name": "Seattle-Tacoma", "lat": 47.4502, "lon": -122.3088, "elev_ft": 433, "class": "B"},
    "KBFI": {"name": "Seattle Boeing Field", "lat": 47.5300, "lon": -122.3019, "elev_ft": 21, "class": "D"},
}

AIRSPACE = {
    "A": {"entry": "IFR clearance only; no VFR", "altitudes": "18,000 ft MSL up to FL600", "transponder": "Mode C / ADS-B Out"},
    "B": {"entry": "ATC clearance required (\"cleared into the Class Bravo\")", "altitudes": "Surface to about 10,000 ft MSL",
          "transponder": "Mode C / ADS-B Out, and within the 30 NM veil"},
    "C": {"entry": "Two-way radio contact established before entry", "altitudes": "Surface to about 4,000 ft AGL (5 NM core, 10 NM shelf)",
          "transponder": "Mode C / ADS-B Out"},
    "D": {"entry": "Two-way radio contact established before entry", "altitudes": "Surface to about 2,500 ft AGL",
          "transponder": "Not required by the class itself"},
    "E": {"entry": "No ATC contact required for VFR", "altitudes": "Controlled airspace not A-D; floor varies (often 700 or 1,200 ft AGL)",
          "transponder": "Required at and above 10,000 ft MSL (excluding at or below 2,500 ft AGL)"},
    "G": {"entry": "No ATC contact required", "altitudes": "Uncontrolled, from the surface up to the overlying Class E floor",
          "transponder": "Not required by the class itself"},
}
