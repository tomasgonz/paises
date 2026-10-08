"""Countries collection with indexed lookups."""

from __future__ import annotations

import json
from typing import Optional

from paises.models import Country
from paises.loader import load_countries


class Countries:
    """Queryable collection of Country objects.

    Auto-loads from bundled data on init. Supports O(1) lookups
    by name, ISO2, ISO3, and alias.
    """

    def __init__(self):
        self._countries: list[Country] = load_countries()
        self._by_iso2: dict[str, Country] = {}
        self._by_iso3: dict[str, Country] = {}
        self._by_name: dict[str, Country] = {}
        self._build_indexes()

    def _build_indexes(self):
        for c in self._countries:
            if c.codes.iso2:
                self._by_iso2[c.codes.iso2.upper()] = c
            if c.codes.iso3:
                self._by_iso3[c.codes.iso3.upper()] = c
            # Index by all name variants (lowercase)
            for key in self._name_keys(c):
                self._by_name[key] = c

    @staticmethod
    def _name_keys(c: Country) -> list[str]:
        keys = []
        if c.name:
            keys.append(c.name.lower())
        if c.names.common and c.names.common.lower() not in keys:
            keys.append(c.names.common.lower())
        if c.names.official and c.names.official.lower() not in keys:
            keys.append(c.names.official.lower())
        if c.names.spanish and c.names.spanish.lower() not in keys:
            keys.append(c.names.spanish.lower())
        for alias in c.names.aliases:
            a = alias.strip().lower()
            if a and a not in keys:
                keys.append(a)
        for alt in c.names.alt_spellings:
            a = alt.strip().lower()
            if a and a not in keys:
                keys.append(a)
        return keys

    def get(self, identifier: str) -> Optional[Country]:
        """Look up a country by name, ISO2, ISO3, or alias.

        Returns None if not found.
        """
        if not identifier:
            return None
        s = identifier.strip()
        upper = s.upper()
        # Try ISO2
        if len(s) == 2 and upper in self._by_iso2:
            return self._by_iso2[upper]
        # Try ISO3
        if len(s) == 3 and upper in self._by_iso3:
            return self._by_iso3[upper]
        # Try name
        return self._by_name.get(s.lower())

    def search(self, query: str) -> list[Country]:
        """Search countries by partial name match."""
        if not query:
            return []
        q = query.strip().lower()
        results = []
        for c in self._countries:
            if q in c.name.lower():
                results.append(c)
            elif c.names.common and q in c.names.common.lower():
                results.append(c)
            elif c.names.official and q in c.names.official.lower():
                results.append(c)
            elif any(q in a.lower() for a in c.names.aliases):
                results.append(c)
        return results

    def filter_by_group(self, group: str) -> list[Country]:
        """Return countries belonging to a group (by acronym)."""
        g = group.strip().upper()
        return [c for c in self._countries if g in (x.upper() for x in c.groups)]

    def filter_by_region(self, region: str) -> list[Country]:
        """Return countries in a given region."""
        r = region.strip().lower()
        return [c for c in self._countries if c.geography.region.lower() == r]

    def filter_by_continent(self, continent: str) -> list[Country]:
        """Return countries on a given continent."""
        ct = continent.strip().lower()
        return [c for c in self._countries if c.geography.continent.lower() == ct]

    def filter_by_income(self, level: str) -> list[Country]:
        """Return countries with a given income level."""
        lv = level.strip().lower()
        return [c for c in self._countries if c.income_level.lower() == lv]

    def get_names(self) -> list[str]:
        """Return all country names."""
        return [c.name for c in self._countries]

    def get_iso2_codes(self) -> list[str]:
        """Return all ISO2 codes."""
        return [c.codes.iso2 for c in self._countries if c.codes.iso2]

    def get_iso3_codes(self) -> list[str]:
        """Return all ISO3 codes."""
        return [c.codes.iso3 for c in self._countries if c.codes.iso3]

    def as_dict(self) -> dict[str, dict]:
        """Return all countries as a dict keyed by name."""
        return {c.name: c.as_dict() for c in self._countries}

    def as_json(self) -> str:
        """Return all countries as a JSON string."""
        return json.dumps(self.as_dict(), ensure_ascii=False)

    def __len__(self) -> int:
        return len(self._countries)

    def __iter__(self):
        return iter(self._countries)

    def __getitem__(self, index):
        return self._countries[index]

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            return self.get(item) is not None
        return item in self._countries
