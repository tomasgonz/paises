"""Tests for data integrity across the bundled dataset."""

from paises import Countries, Groups


def test_all_countries_have_iso2():
    c = Countries()
    for country in c:
        assert country.codes.iso2, f"{country.name} missing ISO2"


def test_all_countries_have_iso3():
    c = Countries()
    for country in c:
        assert country.codes.iso3, f"{country.name} missing ISO3"


def test_no_duplicate_iso2():
    c = Countries()
    seen = set()
    for country in c:
        assert country.codes.iso2 not in seen, f"Duplicate ISO2: {country.codes.iso2}"
        seen.add(country.codes.iso2)


def test_no_duplicate_iso3():
    c = Countries()
    seen = set()
    for country in c:
        assert country.codes.iso3 not in seen, f"Duplicate ISO3: {country.codes.iso3}"
        seen.add(country.codes.iso3)


def test_group_members_have_iso_codes():
    """Every group member carries a non-empty ISO2 and ISO3.

    Entities without an ISO code (the EU as a G20 member, Channel Islands,
    the dissolved Netherlands Antilles) are deliberately not listed as members.
    """
    g = Groups()
    missing = [f"{group.acronym}: {m.name!r}"
               for group in g for m in group.countries if not m.iso2 or not m.iso3]
    assert missing == [], f"Group members without ISO codes: {missing}"


def test_group_member_iso_codes_resolve_to_countries():
    """Every member ISO3 exists in countries.json and its ISO2 agrees."""
    c = Countries()
    by_iso3 = {country.codes.iso3: country for country in c}
    unknown, mismatched = [], []
    for group in Groups():
        for m in group.countries:
            country = by_iso3.get(m.iso3)
            if country is None:
                unknown.append(f"{group.acronym}: {m.name!r} iso3={m.iso3!r}")
            elif country.codes.iso2 != m.iso2:
                mismatched.append(f"{group.acronym}: {m.name!r} iso2={m.iso2!r} "
                                  f"(countries.json: {country.codes.iso2!r})")
    assert unknown == [], f"Member ISO3 not in countries.json: {unknown}"
    assert mismatched == [], f"Member ISO2 disagrees with countries.json: {mismatched}"


def test_no_duplicate_group_members():
    for group in Groups():
        seen = set()
        for m in group.countries:
            assert m.iso3 not in seen, f"{group.acronym}: duplicate member {m.iso3}"
            seen.add(m.iso3)


def test_group_member_names_are_clean():
    for group in Groups():
        for m in group.countries:
            assert m.name == m.name.strip(), f"{group.acronym}: untrimmed name {m.name!r}"
            assert "\u200b" not in m.name, f"{group.acronym}: zero-width space in {m.name!r}"
            assert "  " not in m.name, f"{group.acronym}: double space in {m.name!r}"


def test_country_groups_field_matches_group_files():
    """countries.json `groups` lists exactly the groups whose files contain the country."""
    c = Countries()
    expected = {}
    for group in Groups():
        for m in group.countries:
            expected.setdefault(m.iso3, set()).add(group.acronym)
    for country in c:
        want = expected.get(country.codes.iso3, set())
        have = set(country.groups)
        assert have == want, (f"{country.name}: groups field {sorted(have)} != "
                              f"group files {sorted(want)}")


def test_developing_groups():
    g = Groups()
    un = {m.iso3 for m in g.get_members("UN")}
    lldcs = {m.iso3 for m in g.get_members("LLDCs")}
    dev = {m.iso3 for m in g.get_members("Developing")}
    dev_ex = {m.iso3 for m in g.get_members("Developing-ex-LLDCs")}
    assert len(dev) == 144
    assert dev <= un
    assert dev_ex == dev - lldcs
    assert len(dev_ex) == 112
    assert "AFG" in dev and "AFG" not in dev_ex  # Afghanistan is an LLDC
    assert "BRA" in dev and "BRA" in dev_ex


def test_known_countries_exist():
    c = Countries()
    for name in ["Brazil", "United States", "China", "India", "France",
                  "Japan", "Germany", "Australia", "South Africa", "Mexico"]:
        country = c.get(name)
        assert country is not None, f"{name} not found"
        assert country.codes.iso2, f"{name} missing ISO2"


def test_un_members_count():
    c = Countries()
    un = c.filter_by_group("UN")
    assert len(un) == 193


def test_eu_members_count():
    c = Countries()
    eu = c.filter_by_group("EU")
    assert len(eu) == 27


def test_brazil_comprehensive():
    c = Countries()
    br = c.get("Brazil")
    assert br.codes.iso2 == "BR"
    assert br.codes.iso3 == "BRA"
    assert br.geography.continent == "South America"
    assert br.currency.code == "BRL"
    assert br.income_level == "Upper middle income"
    assert br.independent is True
    assert br.un_member is True
    assert br.flags.emoji != ""
    assert br.population > 100_000_000
    assert "UN" in br.groups
    assert len(br.organizations) > 0
