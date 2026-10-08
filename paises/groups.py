"""Groups collection for international organization memberships."""

from __future__ import annotations

from typing import Optional

from paises.models import Group, GroupMember
from paises.loader import load_groups


class Groups:
    """Queryable collection of Group objects.

    Auto-loads from bundled data/groups/*.json on init.
    """

    def __init__(self):
        self._groups: list[Group] = load_groups()
        self._by_acronym: dict[str, Group] = {}
        for g in self._groups:
            self._by_acronym[g.acronym.upper()] = g

    def get(self, acronym: str) -> Optional[Group]:
        """Get a group by its acronym (case-insensitive)."""
        return self._by_acronym.get(acronym.strip().upper())

    def get_members(self, acronym: str) -> list[GroupMember]:
        """Get members of a group by acronym."""
        g = self.get(acronym)
        return g.countries if g else []

    def get_country_groups(self, iso_code: str) -> list[str]:
        """Get all group acronyms a country belongs to (by ISO2 or ISO3)."""
        code = iso_code.strip().upper()
        result = []
        for g in self._groups:
            for m in g.countries:
                if m.iso2.upper() == code or m.iso3.upper() == code:
                    result.append(g.acronym)
                    break
        return sorted(result)

    @property
    def names(self) -> list[str]:
        """Return all group acronyms."""
        return [g.acronym for g in self._groups]

    def __len__(self) -> int:
        return len(self._groups)

    def __iter__(self):
        return iter(self._groups)

    def __getitem__(self, index):
        return self._groups[index]

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            return self.get(item) is not None
        return item in self._groups
