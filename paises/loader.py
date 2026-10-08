"""Load bundled JSON data into model objects."""

from __future__ import annotations

import json
import os
from pathlib import Path

from paises.models import (
    Country, Names, Codes, Geography, Currency, Phone, Flags, Demonyms,
    Group, GroupMember,
)

_DATA_DIR = Path(__file__).parent / "data"


def _load_json(path: str | Path) -> list | dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_countries() -> list[Country]:
    """Load all countries from bundled data/countries.json."""
    raw = _load_json(_DATA_DIR / "countries.json")
    countries = []
    for entry in raw:
        c = _dict_to_country(entry)
        countries.append(c)
    return countries


def load_groups() -> list[Group]:
    """Load all groups from bundled data/groups/*.json."""
    groups_dir = _DATA_DIR / "groups"
    groups = []
    for path in sorted(groups_dir.glob("*.json")):
        data = _load_json(path)
        g = _dict_to_group(data)
        groups.append(g)
    return groups


def _dict_to_country(d: dict) -> Country:
    """Convert a raw dict into a Country dataclass."""
    names_d = d.get("names", {})
    names = Names(
        common=names_d.get("common", ""),
        official=names_d.get("official", ""),
        native=names_d.get("native", {}),
        translations=names_d.get("translations", {}),
        spanish=names_d.get("spanish", ""),
        aliases=names_d.get("aliases", []),
        alt_spellings=names_d.get("alt_spellings", []),
    )

    codes_d = d.get("codes", {})
    codes = Codes(
        iso2=codes_d.get("iso2", ""),
        iso3=codes_d.get("iso3", ""),
        iso_numeric=codes_d.get("iso_numeric", 0),
        fips=codes_d.get("fips", ""),
        stanag=codes_d.get("stanag", ""),
        geonames_id=codes_d.get("geonames_id", 0),
        fao=codes_d.get("fao", ""),
        sdg=codes_d.get("sdg", ""),
    )

    geo_d = d.get("geography", {})
    geography = Geography(
        capital=geo_d.get("capital", ""),
        capital_lat=geo_d.get("capital_lat", 0.0),
        capital_lng=geo_d.get("capital_lng", 0.0),
        continent=geo_d.get("continent", ""),
        region=geo_d.get("region", ""),
        subregion=geo_d.get("subregion", ""),
        area_km2=geo_d.get("area_km2", 0.0),
        borders=geo_d.get("borders", []),
        landlocked=geo_d.get("landlocked", False),
        latlng=geo_d.get("latlng", []),
    )

    cur_d = d.get("currency", {})
    currency = Currency(
        code=cur_d.get("code", ""),
        name=cur_d.get("name", ""),
        symbol=cur_d.get("symbol", ""),
    )

    phone_d = d.get("phone", {})
    phone = Phone(
        root=phone_d.get("root", ""),
        suffixes=phone_d.get("suffixes", []),
    )

    flags_d = d.get("flags", {})
    flags = Flags(
        emoji=flags_d.get("emoji", ""),
        png=flags_d.get("png", ""),
        svg=flags_d.get("svg", ""),
    )

    dem_d = d.get("demonyms", {})
    demonyms = Demonyms(
        eng=dem_d.get("eng", {}),
        fra=dem_d.get("fra", {}),
    )

    return Country(
        name=d.get("name", ""),
        names=names,
        codes=codes,
        geography=geography,
        income_level=d.get("income_level", ""),
        lending_type=d.get("lending_type", ""),
        development_status=d.get("development_status", ""),
        currency=currency,
        phone=phone,
        tld=d.get("tld", []),
        languages=d.get("languages", {}),
        independent=d.get("independent", False),
        un_member=d.get("un_member", False),
        flags=flags,
        population=d.get("population", 0),
        demonyms=demonyms,
        timezones=d.get("timezones", []),
        driving_side=d.get("driving_side", ""),
        groups=d.get("groups", []),
        organizations=d.get("organizations", {}),
        profile=d.get("profile", ""),
    )


def _dict_to_group(d: dict) -> Group:
    """Convert a raw dict into a Group dataclass."""
    members = []
    for m in d.get("countries", []):
        members.append(GroupMember(
            name=m.get("name", ""),
            iso2=m.get("iso2", ""),
            iso3=m.get("iso3", ""),
        ))

    return Group(
        gid=d.get("gid", ""),
        acronym=d.get("acronym", ""),
        name=d.get("name", ""),
        description=d.get("description", ""),
        classifier=d.get("classifier", ""),
        domains=d.get("domains", []),
        countries=members,
    )
