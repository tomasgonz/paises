#!/usr/bin/env python3
"""Re-sync the `groups` field in paises/data/countries.json with the group files.

For every country, `groups` must list exactly the acronyms of the groups in
paises/data/groups/*.json that contain the country's ISO3 (this is what
tests/test_data_integrity.py::test_country_groups_field_matches_group_files
checks). Existing order is kept; dropped groups are removed and new ones
appended. Run after editing any group file:

    python3 scripts/sync_country_groups.py          # rewrite countries.json
    python3 scripts/sync_country_groups.py --check  # report only, exit 1 if stale
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "paises", "data")
COUNTRIES = os.path.join(DATA, "countries.json")
GROUPS_DIR = os.path.join(DATA, "groups")


def expected_groups():
    """iso3 -> set of group acronyms, from the group files."""
    out = {}
    for fname in sorted(os.listdir(GROUPS_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(GROUPS_DIR, fname), encoding="utf-8") as f:
            group = json.load(f)
        for member in group["countries"]:
            out.setdefault(member["iso3"], set()).add(group["acronym"])
    return out


def main(check_only=False):
    with open(COUNTRIES, encoding="utf-8") as f:
        countries = json.load(f)
    want_by_iso3 = expected_groups()
    changed = []
    for country in countries:
        iso3 = country["codes"]["iso3"]
        have = country.get("groups", [])
        want = want_by_iso3.get(iso3, set())
        if set(have) == want:
            continue
        kept = [g for g in have if g in want]
        added = sorted(want - set(have))
        changed.append((country["name"], sorted(set(have) - want), added))
        country["groups"] = kept + added
    for name, removed, added in changed:
        print(f"  {name}: -{removed or ''} +{added or ''}")
    if not changed:
        print("countries.json groups already in sync")
        return 0
    if check_only:
        print(f"{len(changed)} countries out of sync")
        return 1
    with open(COUNTRIES, "w", encoding="utf-8") as f:
        json.dump(countries, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"updated {len(changed)} countries in {COUNTRIES}")
    return 0


if __name__ == "__main__":
    sys.exit(main(check_only="--check" in sys.argv[1:]))
