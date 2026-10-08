"""Tests for the Countries class."""

import paises
from paises import Countries, Country


def test_countries_init():
    c = Countries()
    assert len(c) > 200


def test_get_by_name():
    c = Countries()
    br = c.get("Brazil")
    assert br is not None
    assert br.name == "Brazil"
    assert br.codes.iso3 == "BRA"


def test_get_by_iso2():
    c = Countries()
    br = c.get("BR")
    assert br is not None
    assert br.name == "Brazil"


def test_get_by_iso3():
    c = Countries()
    br = c.get("BRA")
    assert br is not None
    assert br.name == "Brazil"


def test_get_by_alias():
    c = Countries()
    us = c.get("United States of America")
    assert us is not None
    assert us.codes.iso2 == "US"


def test_get_not_found():
    c = Countries()
    assert c.get("Atlantis") is None
    assert c.get("") is None


def test_search():
    c = Countries()
    results = c.search("Braz")
    assert len(results) >= 1
    assert any(r.name == "Brazil" for r in results)


def test_filter_by_group():
    c = Countries()
    un = c.filter_by_group("UN")
    assert len(un) == 193


def test_filter_by_region():
    c = Countries()
    europe = c.filter_by_region("Europe")
    assert len(europe) > 30


def test_filter_by_continent():
    c = Countries()
    africa = c.filter_by_continent("Africa")
    assert len(africa) > 40


def test_filter_by_income():
    c = Countries()
    high = c.filter_by_income("High income")
    assert len(high) > 30


def test_get_names():
    c = Countries()
    names = c.get_names()
    assert "Brazil" in names
    assert len(names) == len(c)


def test_get_iso2_codes():
    c = Countries()
    codes = c.get_iso2_codes()
    assert "BR" in codes
    assert "US" in codes


def test_get_iso3_codes():
    c = Countries()
    codes = c.get_iso3_codes()
    assert "BRA" in codes
    assert "USA" in codes


def test_contains():
    c = Countries()
    assert "Brazil" in c
    assert "BR" in c
    assert "Atlantis" not in c


def test_iteration():
    c = Countries()
    count = sum(1 for _ in c)
    assert count == len(c)


def test_country_data_fields():
    c = Countries()
    br = c.get("Brazil")
    assert br.geography.continent == "South America"
    assert br.currency.code == "BRL"
    assert br.flags.emoji != ""
    assert br.independent is True
    assert br.un_member is True
    assert br.population > 0


def test_singleton():
    c1 = paises.countries()
    c2 = paises.countries()
    assert c1 is c2
