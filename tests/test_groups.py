"""Tests for the Groups class."""

import paises
from paises import Groups


def test_groups_init():
    g = Groups()
    assert len(g) == 48


def test_get_group():
    g = Groups()
    un = g.get("UN")
    assert un is not None
    assert un.acronym == "UN"
    assert un.name == "United Nations"
    assert len(un.countries) == 193


def test_get_group_case_insensitive():
    g = Groups()
    assert g.get("un") is not None
    assert g.get("Un") is not None


def test_get_members():
    g = Groups()
    members = g.get_members("BRICS")
    assert len(members) == 10          # five founders + Egypt, Ethiopia, Iran, UAE (2024), Indonesia (2025)
    names = {m.name for m in members}
    assert "Brazil" in names
    assert "China" in names
    assert "Indonesia" in names


def test_get_country_groups():
    g = Groups()
    br_groups = g.get_country_groups("BR")
    assert "UN" in br_groups
    assert "G20" in br_groups


def test_get_country_groups_by_iso3():
    g = Groups()
    br_groups = g.get_country_groups("BRA")
    assert "UN" in br_groups


def test_names_property():
    g = Groups()
    names = g.names
    assert "UN" in names
    assert "EU" in names
    assert len(names) == 48


def test_contains():
    g = Groups()
    assert "UN" in g
    assert "FAKE" not in g


def test_iteration():
    g = Groups()
    count = sum(1 for _ in g)
    assert count == 48


def test_groups_singleton():
    g1 = paises.groups()
    g2 = paises.groups()
    assert g1 is g2
