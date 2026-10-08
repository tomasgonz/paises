"""Paises — comprehensive country & group data library."""

from paises.models import Country, Group, GroupMember
from paises.countries import Countries
from paises.groups import Groups

__version__ = "1.1.0"

__all__ = [
    "__version__",
    "Country",
    "Group",
    "GroupMember",
    "Countries",
    "Groups",
    "countries",
    "groups",
]

_countries_singleton = None
_groups_singleton = None


def countries() -> Countries:
    """Lazy singleton for the Countries collection."""
    global _countries_singleton
    if _countries_singleton is None:
        _countries_singleton = Countries()
    return _countries_singleton


def groups() -> Groups:
    """Lazy singleton for the Groups collection."""
    global _groups_singleton
    if _groups_singleton is None:
        _groups_singleton = Groups()
    return _groups_singleton
