"""Live weather from the Aviation Weather Center (aviationweather.gov) and optional web search.

aviationweather.gov is the official NOAA/NWS source, free and keyless. SerpAPI web search
(needs SERPAPI_KEY) is for general context only, never for weather or NOTAM decisions.
"""
from __future__ import annotations

import os

import requests

AWC = "https://aviationweather.gov/api/data"
HEADERS = {"User-Agent": "PilotGPT-portfolio/3.1 (educational project)"}
CEILING_COVERS = {"BKN", "OVC", "OVX", "VV"}


def _visibility_sm(value) -> float | None:
    if value is None or value == "":
        return None
    text = str(value).replace("+", "").replace("SM", "").strip()
    if " " in text:  # "1 1/2"
        whole, frac = text.split(" ", 1)
        return float(whole) + _visibility_sm(frac)
    if "/" in text:
        num, den = text.split("/")
        return float(num) / float(den)
    return float(text)


def _altimeter_inhg(value) -> float | None:
    if value is None:
        return None
    value = float(value)
    return round(value / 33.8639, 2) if value > 100 else value  # AWC JSON reports hPa


def parse_metar(obs: dict) -> dict:
    """Turn one AWC METAR JSON record into the fields PilotGPT uses."""
    clouds = obs.get("clouds") or []
    ceilings = [c.get("base") for c in clouds if c.get("cover") in CEILING_COVERS and c.get("base") is not None]
    if obs.get("vertVis") is not None:
        ceilings.append(obs["vertVis"])
    elev_m = obs.get("elev")
    return {
        "station": obs.get("icaoId"),
        "observed": obs.get("reportTime"),
        "raw": obs.get("rawOb"),
        "wind_from_deg": obs.get("wdir"),
        "wind_kt": obs.get("wspd"),
        "gust_kt": obs.get("wgst"),
        "visibility_sm": _visibility_sm(obs.get("visib")),
        "ceiling_ft_agl": min(ceilings) if ceilings else None,
        "clouds": [f"{c.get('cover')} {c.get('base')}" if c.get("base") is not None else c.get("cover") for c in clouds],
        "temp_c": obs.get("temp"),
        "dewpoint_c": obs.get("dewp"),
        "altimeter_inhg": _altimeter_inhg(obs.get("altim")),
        "field_elevation_ft": round(elev_m * 3.28084) if elev_m is not None else None,
        "weather": obs.get("wxString"),
    }


def get_metar(icao: str, timeout: float = 15) -> dict:
    """Latest METAR for an airport, decoded. Raises on network errors."""
    r = requests.get(f"{AWC}/metar", params={"ids": icao.upper(), "format": "json"}, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    data = r.json() if r.content else []
    if not data:
        return {"error": f"No current METAR for {icao.upper()}"}
    return parse_metar(data[0])


def get_taf(icao: str, timeout: float = 15) -> dict:
    """Latest TAF for an airport, as raw text."""
    r = requests.get(f"{AWC}/taf", params={"ids": icao.upper(), "format": "raw"}, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    text = r.text.strip()
    return {"station": icao.upper(), "raw": text} if text else {"error": f"No current TAF for {icao.upper()}"}


def web_search(query: str, num: int = 3, timeout: float = 15) -> dict:
    """Google results via SerpAPI. Uses one search from the SerpAPI plan per call."""
    key = os.getenv("SERPAPI_KEY")
    if not key:
        return {"error": "SERPAPI_KEY is not set in .env"}
    r = requests.get("https://serpapi.com/search",
                     params={"api_key": key, "engine": "google", "q": query, "num": num}, timeout=timeout)
    r.raise_for_status()
    results = r.json().get("organic_results", [])[:num]
    return {"query": query, "results": [{"title": x.get("title"), "snippet": x.get("snippet"), "link": x.get("link")}
                                        for x in results],
            "note": "Web results are unofficial: confirm anything operational with official FAA sources."}
