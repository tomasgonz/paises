"""Typed data models for paises."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict


@dataclass
class Names:
    common: str = ""
    official: str = ""
    native: dict[str, dict[str, str]] = field(default_factory=dict)
    translations: dict[str, dict[str, str]] = field(default_factory=dict)
    spanish: str = ""
    aliases: list[str] = field(default_factory=list)
    alt_spellings: list[str] = field(default_factory=list)


@dataclass
class Codes:
    iso2: str = ""
    iso3: str = ""
    iso_numeric: int = 0
    fips: str = ""
    stanag: str = ""
    geonames_id: int = 0
    fao: str = ""
    sdg: str = ""


@dataclass
class Geography:
    capital: str = ""
    capital_lat: float = 0.0
    capital_lng: float = 0.0
    continent: str = ""
    region: str = ""
    subregion: str = ""
    area_km2: float = 0.0
    borders: list[str] = field(default_factory=list)
    landlocked: bool = False
    latlng: list[float] = field(default_factory=list)


@dataclass
class Currency:
    code: str = ""
    name: str = ""
    symbol: str = ""


@dataclass
class Phone:
    root: str = ""
    suffixes: list[str] = field(default_factory=list)


@dataclass
class Flags:
    emoji: str = ""
    png: str = ""
    svg: str = ""


@dataclass
class Demonyms:
    eng: dict[str, str] = field(default_factory=dict)
    fra: dict[str, str] = field(default_factory=dict)


@dataclass
class Country:
    name: str = ""
    names: Names = field(default_factory=Names)
    codes: Codes = field(default_factory=Codes)
    geography: Geography = field(default_factory=Geography)
    income_level: str = ""
    lending_type: str = ""
    development_status: str = ""
    currency: Currency = field(default_factory=Currency)
    phone: Phone = field(default_factory=Phone)
    tld: list[str] = field(default_factory=list)
    languages: dict[str, str] = field(default_factory=dict)
    independent: bool = False
    un_member: bool = False
    flags: Flags = field(default_factory=Flags)
    population: int = 0
    demonyms: Demonyms = field(default_factory=Demonyms)
    timezones: list[str] = field(default_factory=list)
    driving_side: str = ""
    groups: list[str] = field(default_factory=list)
    organizations: dict[str, str | None] = field(default_factory=dict)
    profile: str = ""

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __repr__(self) -> str:
        return f"Country(name={self.name!r}, iso2={self.codes.iso2!r}, iso3={self.codes.iso3!r})"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Country):
            return NotImplemented
        return self.codes.iso2 == other.codes.iso2

    def __hash__(self) -> int:
        return hash(self.codes.iso2)

    def as_dict(self) -> dict:
        return asdict(self)

    def as_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


@dataclass
class GroupMember:
    name: str = ""
    iso2: str = ""
    iso3: str = ""

    def __repr__(self) -> str:
        return f"GroupMember({self.name!r}, iso2={self.iso2!r})"


@dataclass
class Group:
    gid: str = ""
    acronym: str = ""
    name: str = ""
    description: str = ""
    classifier: str = ""
    domains: list[str] = field(default_factory=list)
    countries: list[GroupMember] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Group(acronym={self.acronym!r}, members={len(self.countries)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Group):
            return NotImplemented
        return self.acronym == other.acronym

    def __hash__(self) -> int:
        return hash(self.acronym)

    def as_dict(self) -> dict:
        return asdict(self)
