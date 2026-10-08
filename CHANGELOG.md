# Changelog

## v1.2.0 — 2026-10-08

Membership audit of every group against the organisations' own lists (October 2026).

- LDCs: São Tomé and Príncipe removed (graduated 13 December 2024); 44 members.
- SIDS: aligned with the UN-OHRLLS list, 39 SIDS + 18 associate members (57); Bahrain removed, seven Caribbean territories added.
- BRICS: Egypt, Ethiopia, Iran, UAE (2024) and Indonesia (2025) added; 10 members. Saudi Arabia not counted.
- OECD: Costa Rica added (2021); 38 members.
- World Bank income groups (LICs, LMCs, UMCs, HICs) replaced with the FY2027 classification (July 2026).
- Mercosur: Bolivia added (2024); Venezuela (suspended since 2016) not counted.

Membership refresh of 32 group files against the organisations' own sites
(Wikipedia / UN DGACM as fallback), current as of October 2026. Suspended
members are kept; only states that left, were never members, or joined are
changed. `countries.json` `groups` re-synced with the new
`scripts/sync_country_groups.py` helper.

- `nato`: 28 → 32 — added Montenegro (2017), North Macedonia (2020),
  Finland (2023), Sweden (2024); description updated.
- `asean`: 10 → 11 — added Timor-Leste (admitted 26 October 2025).
- `eac`: 5 → 8 — added South Sudan (2016), DR Congo (2022), Somalia (2024).
- `ecowas`: 14 → 12 — removed Mali and Niger (withdrew with Burkina Faso on
  29 January 2025; Burkina Faso was already absent). Guinea-Bissau kept
  (suspended, still a member).
- `mercosur`: 4 → 6 — added Bolivia (full member since 8 July 2024) and
  Venezuela (State Party, suspended since 2016); associate list in the
  description refreshed (Panama 2024).
- `oic`: 56 → 57 — added Syria (suspension lifted March 2025).
- `oas`: 35 → 34 — removed Nicaragua (withdrawal effective 19 November 2023).
  Cuba and Venezuela kept, as the OAS still lists both.
- `cw` (Commonwealth): 54 → 56 — added Gabon and Togo (June 2022).
- `nam`: 125 → 120 — removed Chile (withdrew August 2026) and the observers
  Bosnia and Herzegovina, Brazil, Costa Rica and Paraguay, which were never
  members; South Sudan (2024) was already listed.
- `g24`: 29 → 28 — removed China (a "Special Invitee", not a member).
- `ida`: 58 → 78 — now the World Bank FY2027 IDA-eligible list (IDA-only +
  blend countries): added Belize, Cabo Verde, Cameroon, Congo Rep.,
  Dominica, Eswatini, Fiji, Grenada, Kenya, Nigeria, Pakistan, Papua New
  Guinea, Saint Lucia, Saint Vincent and the Grenadines, Somalia, Sri Lanka,
  Suriname, Timor-Leste, Uzbekistan, Zimbabwe.
- `acp` (OACPS): 56 → 80 — added the 24 members that were missing (Bahamas,
  Cabo Verde, Comoros, Cook Islands, Equatorial Guinea, Eritrea, Ethiopia,
  Kiribati, Liberia, Marshall Islands, Micronesia, Nauru, Niue, Palau,
  Samoa, Sao Tome and Principe, Seychelles, Somalia, South Sudan, Sudan,
  Timor-Leste, Tonga, Tuvalu, Vanuatu). The OACPS describes itself as
  79 members; South Sudan (acceded 2012) is the 80th entry.
- `acd`: 34 → 35 — added Palestine (2019).
- Descriptions only: `pif` (18 members, not 16), `weog` (29 members, not
  28), `sica` (text was a copy of the CPLP description).
- Verified unchanged: `gcc`, `au` (55 incl. Sahrawi Republic; six suspended
  members kept), `caricom` (15 incl. Montserrat), `sadc`, `cplp`, `las`,
  `zangger`, `osce`, `grulac`, `ag`, `ap`, `ioc` (France for Réunion),
  `nordic`, `can`, `canz`, `cegpl`, `pif`.

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
