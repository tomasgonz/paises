# Changelog

## v1.1.0 — 2026-10-08

Data-integrity release: every group member now carries a valid ISO2/ISO3.

- Fixed 19 group member entries that shipped with empty ISO codes:
  - Congo, Dem. Rep. → CD/COD in ACP, Africa, AU, CEGPL, G24, G77, IDA, LICs, NAM, SADC, UN (11 groups)
  - Turkey → TR/TUR in G20 (name also stripped of zero-width spaces)
  - Venezuela (Bolivarian Republic of) → VE/VEN in GRULAC (double space in name fixed)
  - Macao SAR, China → MO/MAC and Virgin Islands (U.S.) → VI/VIR in HICs
  - West Bank and Gaza → PS/PSE in LMCs
  - Holy See → VA/VAT in OSCE
  - Commonwealth of Northern Marianas → MP/MNP and US Virgin Islands → VI/VIR in SIDS
- Removed 3 member entries that are not ISO countries: European Union (G20),
  Channel Islands (HICs), Netherlands Antilles (SIDS, dissolved 2010).
- New groups: `developing` (144 UN member states, UN M49 developing regions; DR Congo restored after the empty-ISO fix) and
  `developing-ex-lldcs` (112, = developing minus LLDCs). 48 groups in total.
- `countries.json` `groups` field re-synced with the group files (adds the new
  groups; also restores BRICS for Brazil, G20 for Turkey, GRULAC for Venezuela,
  OSCE for the Holy See, SIDS for Northern Mariana Islands and U.S. Virgin Islands).
- Tests: strict integrity test — no empty member ISO codes, every member ISO3
  resolves to `countries.json` with a matching ISO2, no duplicate members, and
  `countries.json` `groups` agrees with the group files.

## v1.0.0 — 2025-01-01

First stable release.

- 250 countries with 20+ fields each (names, codes, geography, currency, flags, population, etc.)
- 46 international groups (UN, NATO, EU, G20, BRICS, OECD, and more)
- 180+ organization memberships per country
- Typed dataclasses with full IDE support
- O(1) lookups by name, ISO-2, ISO-3, or alias
- Search and filter by group, region, continent, income level
- Lazy singleton accessors: `paises.countries()`, `paises.groups()`
- Zero runtime dependencies — all data bundled
- Comprehensive test suite (45+ tests)
