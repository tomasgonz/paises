"""Tests for the data models."""

import json

from paises.models import (
    Country, Names, Codes, Geography, Currency, Phone, Flags, Demonyms,
    Group, GroupMember,
)


def test_country_defaults():
    c = Country()
    assert c.name == ""
    assert c.codes.iso2 == ""
    assert c.geography.capital == ""
    assert c.groups == []
    assert c.organizations == {}


def test_country_no_shared_mutable_state():
    c1 = Country()
    c2 = Country()
    c1.groups.append("UN")
    assert "UN" not in c2.groups


def test_country_as_dict():
    c = Country(name="Test", codes=Codes(iso2="XX", iso3="XXX"))
    d = c.as_dict()
    assert d["name"] == "Test"
    assert d["codes"]["iso2"] == "XX"


def test_country_as_json():
    c = Country(name="Test")
    j = c.as_json()
    parsed = json.loads(j)
    assert parsed["name"] == "Test"


def test_country_getitem():
    c = Country(name="Test")
    assert c["name"] == "Test"


def test_group_defaults():
    g = Group()
    assert g.gid == ""
    assert g.countries == []


def test_group_member():
    m = GroupMember(name="Brazil", iso2="BR", iso3="BRA")
    assert m.name == "Brazil"
    assert m.iso2 == "BR"


def test_group_as_dict():
    g = Group(gid="test", acronym="TEST", name="Test Group",
              countries=[GroupMember(name="X", iso2="XX", iso3="XXX")])
    d = g.as_dict()
    assert d["acronym"] == "TEST"
    assert len(d["countries"]) == 1
