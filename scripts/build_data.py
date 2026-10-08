#!/usr/bin/env python3
"""
Build script: merges multiple data sources into paises/data/countries.json.

Sources:
1. booklet/cache/Countrycodesfull.json  — codes, currency, population, area, orgs
2. booklet/cache/country_facts.json     — REST Countries API (names, flags, phone, etc.)
3. paises/cache/countries.json          — World Bank (income level, lending type)
4. booklet/cache/groups/                — 46 group JSON files
5. booklet/cache/countries.json         — qualitative profiles
6. paises/ccs.py data (capital coords)  — fallback for capital coordinates
7. paises/data.py aliases               — country alias mappings
"""

import json
import os
import sys
import copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKLET = os.path.join(os.path.dirname(ROOT), "booklet")
PAISES_PKG = os.path.join(ROOT, "paises")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  wrote {path} ({len(json.dumps(data, ensure_ascii=False))//1024}KB)")


# ── 1. Load Countrycodesfull.json (primary: codes, currency, pop, area, orgs) ──
def load_countrycodes():
    path = os.path.join(BOOKLET, "cache", "Countrycodesfull.json")
    raw = load_json(path)
    by_iso2 = {}
    by_iso3 = {}
    for entry in raw:
        iso2 = entry.get("ISO_3166_2", "")
        iso3 = entry.get("ISO_3166_3", "")
        if iso2:
            by_iso2[iso2] = entry
        if iso3:
            by_iso3[iso3] = entry
    print(f"  Countrycodesfull: {len(raw)} entries")
    return raw, by_iso2, by_iso3


# ── 2. Load country_facts.json (REST Countries API) ──
def load_country_facts():
    path = os.path.join(BOOKLET, "cache", "country_facts.json")
    raw = load_json(path)
    by_iso2 = {}
    by_iso3 = {}
    for entry in raw:
        iso2 = entry.get("cca2", "")
        iso3 = entry.get("cca3", "")
        if iso2:
            by_iso2[iso2] = entry
        if iso3:
            by_iso3[iso3] = entry
    print(f"  country_facts: {len(raw)} entries")
    return by_iso2, by_iso3


# ── 3. Load World Bank countries.json ──
def load_world_bank():
    path = os.path.join(PAISES_PKG, "cache", "countries.json")
    raw = load_json(path)
    entries = raw[1] if isinstance(raw, list) and len(raw) == 2 else raw
    by_iso2 = {}
    by_iso3 = {}
    for entry in entries:
        iso2 = entry.get("iso2Code", "")
        iso3 = entry.get("id", "")
        if iso2:
            by_iso2[iso2] = entry
        if iso3:
            by_iso3[iso3] = entry
    print(f"  World Bank: {len(entries)} entries")
    return by_iso2, by_iso3


# ── 4. Load profiles ──
def load_profiles():
    path = os.path.join(BOOKLET, "cache", "countries.json")
    raw = load_json(path)
    by_iso3 = {}
    for entry in raw:
        iso3 = entry.get("iso3", "")
        if iso3:
            by_iso3[iso3] = entry.get("profile", "")
    print(f"  profiles: {len(raw)} entries")
    return by_iso3


# ── 5. Load capital coordinates from ccs.py data ──
def load_ccs():
    path = os.path.join(PAISES_PKG, "ccs.py")
    # Parse the Python file to extract country_data
    with open(path, encoding="utf-8") as f:
        content = f.read()
    # Find the JSON array in the file
    start = content.index("[")
    data = json.loads(content[start:])
    by_code = {}
    for entry in data:
        code = entry.get("CountryCode", "")
        if code and code != "NULL":
            by_code[code] = entry
    print(f"  ccs capital coords: {len(by_code)} entries")
    return by_code


# ── 6. Load aliases from data.py ──
def load_aliases():
    aliases = {
        'Bahamas, The': ['Bahamas'],
        'Bolivia': ['Bolivia (Plurinational State of)'],
        'Central African Republic': ['CAR'],
        'Congo, Dem. Rep.': ['Democratic Republic of the Congo', 'DR Congo', 'DRC', 'D.R. of the Congo'],
        'Congo': ['Republic of Congo'],
        'Gambia, The': ['Gambia', 'The Gambia', 'Gambia (Republic of The)'],
        'Guinea-Bissau': ['Guinea Bissau'],
        'Iran, Islamic Rep.': ['Iran', 'Iran (Islamic Republic of)', 'Islamic Republic of Iran'],
        'Lao PDR': ["Lao People's Democratic Republic", 'Laos', 'Lao P.D.R.', "Lao People's DR"],
        'Micronesia': ['Micronesia, Fed. Sts.', 'Micronesia (Federated States of)', 'Federated States of Micronesia'],
        'St. Vincent and the Grenadines': ['Saint Vincent and the Grenadines'],
        'St. Kitts and Nevis': ['Saint Kitts and Nevis'],
        'St. Lucia': ['Saint Lucia'],
        'Sao Tome and Principe': ['São Tomé and Príncipe', 'São Tomé and Principe'],
        'Syria': ['Syrian Arab Republic'],
        'Tanzania': ['United Republic of Tanzania', 'U.R. of Tanzania: Mainland'],
        'United Kingdom': ['United Kingdom of Great Britain and Northern Ireland'],
        'United States': ['United States of America'],
        'Venezuela': ['Venezuela, RB', 'Venezuela, Bolivarian Republic of',
                       'Venezuela (Bolivarian Republic of)'],
        'Vietnam': ['Viet Nam'],
        'Yemen, Rep.': ['Yemen'],
        'Egypt': ['Egypt, Arab Rep.'],
        "Korea, Dem. People's Rep.": ["Democratic People's Republic of Korea", 'North Korea'],
    }
    # Build reverse map: alias -> canonical name
    reverse = {}
    for canonical, alias_list in aliases.items():
        for a in alias_list:
            reverse[a.strip().lower()] = canonical
        reverse[canonical.strip().lower()] = canonical
    return aliases, reverse


# ── 7. Load group files from booklet ──
def load_groups():
    groups_dir = os.path.join(BOOKLET, "cache", "groups")
    groups = {}
    for fname in sorted(os.listdir(groups_dir)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(groups_dir, fname)
        data = load_json(path)
        acronym = data.get("acronym", fname.replace(".json", "").upper())
        groups[acronym] = data
    print(f"  groups: {len(groups)} files")
    return groups


def build_organizations(cc_entry):
    """Build organizations dict from Countrycodesfull org_id/org_member arrays."""
    org_ids = cc_entry.get("org_id", [])
    org_members = cc_entry.get("org_member", [])
    orgs = {}
    for i, org_id in enumerate(org_ids):
        status = org_members[i] if i < len(org_members) else None
        if status:
            orgs[org_id] = status
    return orgs


def merge_country(cc_entry, facts_entry, wb_entry, profile, ccs_entry, aliases_dict, groups_for_country):
    """Merge data from all sources into a single country dict."""
    c = {}

    iso2 = cc_entry.get("ISO_3166_2", "")
    iso3 = cc_entry.get("ISO_3166_3", "")

    # ── Name ──
    name_en = cc_entry.get("NAME.EN", "")
    c["name"] = name_en

    # ── Names ──
    names = {
        "common": name_en,
        "official": name_en,
        "native": {},
        "translations": {},
        "spanish": cc_entry.get("NAME.ES", ""),
        "aliases": [],
        "alt_spellings": [],
    }

    if facts_entry:
        name_obj = facts_entry.get("name", {})
        names["common"] = name_obj.get("common", name_en)
        names["official"] = name_obj.get("official", name_en)
        names["native"] = name_obj.get("nativeName", {})
        names["translations"] = facts_entry.get("translations", {})
        names["alt_spellings"] = facts_entry.get("altSpellings", [])

    # Add aliases from data.py
    for canonical, alias_list in aliases_dict.items():
        if canonical == name_en or canonical == names["common"]:
            names["aliases"] = alias_list
            break
    # Also check if any alias maps to this country
    if not names["aliases"]:
        for canonical, alias_list in aliases_dict.items():
            if any(a.lower() == name_en.lower() for a in alias_list):
                names["aliases"] = [canonical] + [a for a in alias_list if a.lower() != name_en.lower()]
                break

    c["names"] = names

    # ── Codes ──
    c["codes"] = {
        "iso2": iso2,
        "iso3": iso3,
        "iso_numeric": cc_entry.get("ISO_3166_1", cc_entry.get("M49", 0)),
        "fips": cc_entry.get("FIPS_GEC", ""),
        "stanag": cc_entry.get("STANAG", ""),
        "geonames_id": cc_entry.get("geonameId", 0),
        "fao": "",
        "sdg": "",
    }

    # ── Geography ──
    capital_name = cc_entry.get("CAPITAL.EN", "")
    capital_lat = 0.0
    capital_lng = 0.0

    # Try REST Countries first for capital coordinates
    if facts_entry:
        cap_info = facts_entry.get("capitalInfo", {})
        cap_latlng = cap_info.get("latlng", [])
        if cap_latlng and len(cap_latlng) == 2:
            capital_lat = cap_latlng[0]
            capital_lng = cap_latlng[1]
        # Override capital name from REST Countries if available
        cap_list = facts_entry.get("capital", [])
        if cap_list:
            capital_name = cap_list[0]

    # Fallback to ccs.py data
    if capital_lat == 0.0 and capital_lng == 0.0 and ccs_entry:
        try:
            capital_lat = float(ccs_entry.get("CapitalLatitude", 0))
            capital_lng = float(ccs_entry.get("CapitalLongitude", 0))
        except (ValueError, TypeError):
            pass

    # Fallback to World Bank data
    if capital_lat == 0.0 and capital_lng == 0.0 and wb_entry:
        try:
            capital_lat = float(wb_entry.get("latitude", 0))
            capital_lng = float(wb_entry.get("longitude", 0))
        except (ValueError, TypeError):
            pass

    continent = cc_entry.get("CONTINENT.EN", "")
    region = cc_entry.get("REGION.EN", "")
    subregion = cc_entry.get("SUBREGION.EN", "")

    # Prefer REST Countries for region/subregion if richer
    if facts_entry:
        if facts_entry.get("region"):
            region = facts_entry["region"]
        if facts_entry.get("subregion"):
            subregion = facts_entry["subregion"]
        # continent from REST Countries
        continents = facts_entry.get("continents", [])
        if continents:
            continent = continents[0]

    borders = []
    landlocked = False
    latlng = []
    area_km2 = cc_entry.get("area_km2", 0) or 0

    if facts_entry:
        borders = facts_entry.get("borders", []) or []
        landlocked = facts_entry.get("landlocked", False) or False
        latlng = facts_entry.get("latlng", []) or []
        if facts_entry.get("area") and not area_km2:
            area_km2 = facts_entry["area"]

    c["geography"] = {
        "capital": capital_name,
        "capital_lat": capital_lat,
        "capital_lng": capital_lng,
        "continent": continent,
        "region": region,
        "subregion": subregion,
        "area_km2": area_km2,
        "borders": borders,
        "landlocked": landlocked,
        "latlng": latlng,
    }

    # ── Income level & lending type (World Bank) ──
    if wb_entry:
        il = wb_entry.get("incomeLevel", {})
        lt = wb_entry.get("lendingType", {})
        c["income_level"] = il.get("value", "").strip() if il else ""
        c["lending_type"] = lt.get("value", "").strip() if lt else ""
    else:
        c["income_level"] = ""
        c["lending_type"] = ""

    # ── Development status ──
    c["development_status"] = cc_entry.get("Developed", "")

    # ── Currency ──
    currency_code = cc_entry.get("currency", "")
    currency_name = ""
    currency_symbol = ""
    if facts_entry and facts_entry.get("currencies"):
        currencies = facts_entry["currencies"]
        # Use the first currency, preferring the one matching Countrycodesfull
        if currency_code and currency_code in currencies:
            cur = currencies[currency_code]
            currency_name = cur.get("name", "")
            currency_symbol = cur.get("symbol", "")
        else:
            # Take first available
            for code, cur in currencies.items():
                if not currency_code:
                    currency_code = code
                currency_name = cur.get("name", "")
                currency_symbol = cur.get("symbol", "")
                break

    c["currency"] = {
        "code": currency_code,
        "name": currency_name,
        "symbol": currency_symbol,
    }

    # ── Phone ──
    phone = {"root": "", "suffixes": []}
    if facts_entry and facts_entry.get("idd"):
        idd = facts_entry["idd"]
        phone["root"] = idd.get("root", "")
        phone["suffixes"] = idd.get("suffixes", [])
    c["phone"] = phone

    # ── TLD ──
    c["tld"] = facts_entry.get("tld", []) if facts_entry else []

    # ── Languages ──
    c["languages"] = facts_entry.get("languages", {}) if facts_entry else {}

    # ── Independent & UN member ──
    c["independent"] = cc_entry.get("independent", False)
    c["un_member"] = facts_entry.get("unMember", False) if facts_entry else False

    # ── Flags ──
    flags = {"emoji": "", "png": "", "svg": ""}
    if facts_entry:
        flags["emoji"] = facts_entry.get("flag", "")
        flags_obj = facts_entry.get("flags", {})
        if flags_obj:
            flags["png"] = flags_obj.get("png", "")
            flags["svg"] = flags_obj.get("svg", "")
    c["flags"] = flags

    # ── Population ──
    pop = cc_entry.get("pop", 0) or 0
    if facts_entry and facts_entry.get("population"):
        pop = facts_entry["population"]  # REST Countries is more up to date
    c["population"] = pop

    # ── Demonyms ──
    demonyms = {"eng": {}, "fra": {}}
    if facts_entry and facts_entry.get("demonyms"):
        d = facts_entry["demonyms"]
        demonyms["eng"] = d.get("eng", {})
        demonyms["fra"] = d.get("fra", {})
    c["demonyms"] = demonyms

    # ── Timezones ──
    c["timezones"] = facts_entry.get("timezones", []) if facts_entry else []

    # ── Driving side ──
    c["driving_side"] = ""
    if facts_entry and facts_entry.get("car"):
        c["driving_side"] = facts_entry["car"].get("side", "")

    # ── Groups ──
    c["groups"] = sorted(groups_for_country)

    # ── Organizations ──
    c["organizations"] = build_organizations(cc_entry)

    # ── Profile ──
    c["profile"] = profile or ""

    return c


def _normalize(s):
    """Normalize Unicode quotes and whitespace for name matching."""
    return s.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').strip().lower()


def build_country_groups(groups_data, by_iso2, by_iso3, name_to_iso2):
    """Map each country (by ISO2) to a list of group acronyms it belongs to."""
    country_groups = {}  # iso2 -> set of acronyms

    for acronym, gdata in groups_data.items():
        members = gdata.get("names", [])
        if isinstance(members, list):
            for m in members:
                if isinstance(m, dict):
                    iso2 = m.get("ISO", "")
                    iso3 = m.get("ISO3", "")
                    mname = m.get("name", "")
                    if iso2:
                        country_groups.setdefault(iso2, set()).add(acronym)
                    elif iso3:
                        cc = by_iso3.get(iso3)
                        if cc:
                            i2 = cc.get("ISO_3166_2", "")
                            if i2:
                                country_groups.setdefault(i2, set()).add(acronym)
                    elif mname:
                        # Fallback: resolve by name (with Unicode normalization)
                        normalized = _normalize(mname)
                        i2 = name_to_iso2.get(normalized)
                        if i2:
                            country_groups.setdefault(i2, set()).add(acronym)
    return country_groups


def main():
    print("Loading data sources...")
    cc_raw, cc_by_iso2, cc_by_iso3 = load_countrycodes()
    facts_by_iso2, facts_by_iso3 = load_country_facts()
    wb_by_iso2, wb_by_iso3 = load_world_bank()
    profiles_by_iso3 = load_profiles()
    ccs_by_code = load_ccs()
    aliases_dict, aliases_reverse = load_aliases()
    groups_data = load_groups()

    # Build name->iso2 mapping for group member resolution
    print("\nBuilding name-to-ISO2 index...")
    name_to_iso2 = {}
    for cc_entry in cc_raw:
        iso2 = cc_entry.get("ISO_3166_2", "")
        if not iso2:
            continue
        name_en = cc_entry.get("NAME.EN", "")
        if name_en:
            name_to_iso2[_normalize(name_en)] = iso2
        # Also add aliases
        for canonical, alias_list in aliases_dict.items():
            if canonical == name_en:
                for a in alias_list:
                    name_to_iso2[_normalize(a)] = iso2
            for a in alias_list:
                if _normalize(a) == _normalize(name_en):
                    name_to_iso2[_normalize(canonical)] = iso2
    # Add REST Countries names
    for iso2_key, facts_entry in facts_by_iso2.items():
        name_obj = facts_entry.get("name", {})
        if name_obj.get("common"):
            name_to_iso2[_normalize(name_obj["common"])] = iso2_key
        if name_obj.get("official"):
            name_to_iso2[_normalize(name_obj["official"])] = iso2_key
    # Add World Bank names
    for iso2_key, wb_entry in wb_by_iso2.items():
        wb_name = wb_entry.get("name", "")
        if wb_name:
            name_to_iso2[_normalize(wb_name)] = iso2_key

    print("\nBuilding country-group mappings...")
    country_groups = build_country_groups(groups_data, cc_by_iso2, cc_by_iso3, name_to_iso2)

    print("\nMerging countries...")
    countries = []
    seen_iso2 = set()

    # Primary: iterate over Countrycodesfull (most comprehensive)
    for cc_entry in cc_raw:
        iso2 = cc_entry.get("ISO_3166_2", "")
        iso3 = cc_entry.get("ISO_3166_3", "")
        if not iso2:
            continue
        seen_iso2.add(iso2)

        facts_entry = facts_by_iso2.get(iso2) or facts_by_iso3.get(iso3)
        wb_entry = wb_by_iso2.get(iso2) or wb_by_iso3.get(iso3)
        profile = profiles_by_iso3.get(iso3, "")
        ccs_entry = ccs_by_code.get(iso2)
        groups_for = country_groups.get(iso2, set())

        country = merge_country(
            cc_entry, facts_entry, wb_entry, profile, ccs_entry,
            aliases_dict, groups_for
        )
        countries.append(country)

    # Secondary: add any countries from REST Countries not in Countrycodesfull
    for iso2, facts_entry in facts_by_iso2.items():
        if iso2 in seen_iso2:
            continue
        iso3 = facts_entry.get("cca3", "")
        # Build a minimal cc_entry-like dict
        name_obj = facts_entry.get("name", {})
        cc_like = {
            "ISO_3166_2": iso2,
            "ISO_3166_3": iso3,
            "ISO_3166_1": int(facts_entry.get("ccn3", 0) or 0),
            "M49": int(facts_entry.get("ccn3", 0) or 0),
            "NAME.EN": name_obj.get("common", ""),
            "NAME.ES": "",
            "CONTINENT.EN": "",
            "REGION.EN": facts_entry.get("region", ""),
            "SUBREGION.EN": facts_entry.get("subregion", ""),
            "CAPITAL.EN": (facts_entry.get("capital") or [""])[0],
            "currency": "",
            "independent": facts_entry.get("independent", False),
            "pop": facts_entry.get("population", 0),
            "area_km2": facts_entry.get("area", 0),
            "Developed": "",
            "org_id": [],
            "org_member": [],
        }
        # Set currency from facts
        if facts_entry.get("currencies"):
            first_code = next(iter(facts_entry["currencies"]))
            cc_like["currency"] = first_code

        wb_entry = wb_by_iso2.get(iso2) or wb_by_iso3.get(iso3)
        profile = profiles_by_iso3.get(iso3, "")
        ccs_entry = ccs_by_code.get(iso2)
        groups_for = country_groups.get(iso2, set())

        country = merge_country(
            cc_like, facts_entry, wb_entry, profile, ccs_entry,
            aliases_dict, groups_for
        )
        countries.append(country)
        seen_iso2.add(iso2)

    # Sort by name
    countries.sort(key=lambda c: c["name"])
    print(f"  Total merged countries: {len(countries)}")

    # ── Write countries.json ──
    out_path = os.path.join(PAISES_PKG, "data", "countries.json")
    save_json(countries, out_path)

    # ── Write profiles.json ──
    profiles_out = os.path.join(PAISES_PKG, "data", "profiles.json")
    save_json(profiles_by_iso3, profiles_out)

    # ── Copy and fix group files ──
    print("\nCopying group files...")
    groups_out_dir = os.path.join(PAISES_PKG, "data", "groups")
    os.makedirs(groups_out_dir, exist_ok=True)

    # Build a name->iso lookup from our merged data
    name_to_iso = {}
    for c in countries:
        pair = (c["codes"]["iso2"], c["codes"]["iso3"])
        name_to_iso[_normalize(c["name"])] = pair
        if c["names"]["common"]:
            name_to_iso[_normalize(c["names"]["common"])] = pair
        if c["names"]["official"]:
            name_to_iso[_normalize(c["names"]["official"])] = pair
        for alias in c["names"]["aliases"]:
            name_to_iso[_normalize(alias)] = pair
        for alt in c["names"]["alt_spellings"]:
            name_to_iso[_normalize(alt)] = pair

    for acronym, gdata in groups_data.items():
        out_data = {
            "gid": gdata.get("gid", acronym.lower()),
            "acronym": acronym,
            "name": gdata.get("name", acronym),
            "description": gdata.get("description", ""),
            "classifier": gdata.get("classifier", ""),
            "domains": gdata.get("domains", []),
            "countries": [],
        }

        members = gdata.get("names", [])
        if isinstance(members, list):
            for m in members:
                if isinstance(m, dict):
                    mname = m.get("name", "")
                    miso2 = m.get("ISO", "") or ""
                    miso3 = m.get("ISO3", "") or ""

                    # Fix missing ISO codes by name lookup
                    if (not miso2 or not miso3) and mname:
                        lookup = name_to_iso.get(_normalize(mname))
                        if lookup:
                            if not miso2:
                                miso2 = lookup[0]
                            if not miso3:
                                miso3 = lookup[1]

                    # Fix known typos
                    if mname == "Brazi":
                        mname = "Brazil"
                        miso2 = "BR"
                        miso3 = "BRA"

                    out_data["countries"].append({
                        "name": mname,
                        "iso2": miso2,
                        "iso3": miso3,
                    })
                elif isinstance(m, str):
                    mname = m
                    lookup = name_to_iso.get(mname.strip().lower(), ("", ""))
                    out_data["countries"].append({
                        "name": mname,
                        "iso2": lookup[0],
                        "iso3": lookup[1],
                    })

        fname = gdata.get("gid", acronym.lower()) + ".json"
        save_json(out_data, os.path.join(groups_out_dir, fname))

    print(f"  Wrote {len(groups_data)} group files")
    print("\nDone!")


if __name__ == "__main__":
    main()
