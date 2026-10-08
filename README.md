# Paises

Comprehensive country and international-group data for Python — 250 countries, 48 groups, typed dataclasses, zero runtime dependencies.

Unlike [pycountry](https://github.com/pycountry/pycountry) (ISO codes only) or [country_converter](https://github.com/IndEcol/country_converter) (conversion-focused), paises bundles **rich metadata** — geography, economics, currencies, languages, flags, population, 180+ organization memberships — in a single, pip-installable package with O(1) lookups.

## Installation

```bash
pip install paises
```

Requires Python 3.10+.

## Quick Start

```python
import paises

# Look up a country by name, ISO-2, or ISO-3 code
brazil = paises.countries().get("Brazil")
print(brazil.name)                    # Brazil
print(brazil.codes.iso3)              # BRA
print(brazil.geography.continent)     # South America
print(brazil.currency.code)           # BRL
print(brazil.flags.emoji)             # (flag emoji)
print(brazil.population)              # 212559409
```

```python
# Filter countries by group, region, continent, or income level
un_members = paises.countries().filter_by_group("UN")
print(len(un_members))  # 193

european = paises.countries().filter_by_continent("Europe")
high_income = paises.countries().filter_by_income("High income")
```

```python
# Explore international groups
brics = paises.groups().get("BRICS")
print(brics.name)                     # BRICS
print(len(brics.countries))           # 5
for member in brics.countries:
    print(f"  {member.name} ({member.iso2})")

# Find all groups a country belongs to
brazil_groups = paises.groups().get_country_groups("BR")
```

## Features

- **250 countries** with 20+ fields each (names, codes, geography, currency, phone, flags, population, and more)
- **48 international groups** (UN, NATO, EU, G20, BRICS, OECD, ASEAN, AU, OIC, LDCs, LLDCs, SIDS, developing economies, and others)
- **180+ organization memberships** per country
- **Typed dataclasses** — full IDE autocompletion and type checking
- **O(1) lookups** by name, ISO-2, ISO-3, or alias
- **Zero runtime dependencies** — all data is bundled
- **Multilingual names** — common, official, native, and 30+ translations

## API Reference

### `Countries`

Instantiate with `Countries()` or use the lazy singleton `paises.countries()`.

| Method | Description |
|---|---|
| `get(id)` | Look up by name, ISO-2, ISO-3, or alias. Returns `Country` or `None`. |
| `search(query)` | Partial name match. Returns `list[Country]`. |
| `filter_by_group(group)` | Countries in a group (e.g. `"UN"`). Returns `list[Country]`. |
| `filter_by_region(region)` | Filter by region. Returns `list[Country]`. |
| `filter_by_continent(continent)` | Filter by continent. Returns `list[Country]`. |
| `filter_by_income(level)` | Filter by income level. Returns `list[Country]`. |
| `get_names()` | All country names. Returns `list[str]`. |
| `get_iso2_codes()` | All ISO-2 codes. Returns `list[str]`. |
| `get_iso3_codes()` | All ISO-3 codes. Returns `list[str]`. |
| `as_dict()` | All countries as list of dicts. |
| `as_json()` | All countries as JSON string. |

### `Groups`

Instantiate with `Groups()` or use the lazy singleton `paises.groups()`.

| Method | Description |
|---|---|
| `get(acronym)` | Get a group by acronym. Returns `Group` or `None`. |
| `get_members(acronym)` | Members of a group. Returns `list[GroupMember]`. |
| `get_country_groups(iso)` | Groups a country belongs to. Returns `list[Group]`. |
| `names` | All group acronyms (property). Returns `list[str]`. |

### `Country` fields

| Field | Type | Example |
|---|---|---|
| `name` | `str` | `"Brazil"` |
| `names` | `Names` | common, official, native, translations, aliases |
| `codes` | `Codes` | iso2, iso3, iso_numeric, fips, stanag |
| `geography` | `Geography` | capital, continent, region, subregion, area_km2, borders |
| `income_level` | `str` | `"Upper middle income"` |
| `currency` | `Currency` | code, name, symbol |
| `phone` | `Phone` | root, suffixes |
| `languages` | `dict` | `{"por": "Portuguese"}` |
| `flags` | `Flags` | emoji, png, svg |
| `population` | `int` | `212559409` |
| `groups` | `list[str]` | `["UN", "G20", "BRICS", ...]` |
| `organizations` | `dict` | 180+ org memberships |
| `timezones` | `list[str]` | `["UTC-05:00", ...]` |
| `profile` | `str` | Qualitative country description |

## Data Sources

Country data is merged from five sources (via `scripts/build_data.py`):

1. **Countrycodesfull.json** — ISO codes, currency, population, area, 180+ org memberships
2. **REST Countries API** — multilingual names, flags, phone, borders, timezones
3. **World Bank API** — income level, lending type, development status
4. **Group files** — 48 country groups with ISO-coded members (every member carries a valid ISO2/ISO3 that resolves to an entry in `countries.json`; enforced by `tests/test_data_integrity.py`)
5. **Country profiles** — qualitative descriptions

## Contributing

Contributions are welcome! To get started:

```bash
git clone https://github.com/tomasgonz/paises.git
cd paises
pip install -e ".[dev]"
pytest tests/
```

Please open an issue or pull request on [GitHub](https://github.com/tomasgonz/paises).

## License

[MIT](LICENSE) — Copyright 2024-2025 Tomas.
