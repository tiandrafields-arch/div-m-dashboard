#!/usr/bin/env python3
"""
Merge precinct registration counts into precincts_section1.geojson.

Usage:
    python3 join_voter_data.py registration.csv

The CSV needs a precinct key column and any value columns you want to show.
The script tries to match on VOTING_PRECINCT_NAME first, then on WARD + PRECINCT.

Recognized key columns (case insensitive), any one of:
    VOTING_PRECINCT_NAME            e.g. 1-086
    WARD and PRECINCT               e.g. 1 and 86
Recognized value column for the popup total:
    reg_total  (or REGISTERED, TOTAL, REG)
Extra columns are copied onto each precinct as is.
"""
import sys, csv, json, os

GEO = os.path.join("data", "precincts_section1.geojson")

def norm(s): return str(s).strip().lstrip("﻿").lower()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 join_voter_data.py registration.csv"); sys.exit(1)
    csv_path = sys.argv[1]

    rows = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = {norm(h): h for h in reader.fieldnames}
        for r in reader:
            rows.append(r)

    name_col = headers.get("voting_precinct_name")
    ward_col = headers.get("ward")
    prec_col = headers.get("precinct")
    total_col = next((headers[k] for k in ("reg_total","registered","total","reg") if k in headers), None)

    by_name, by_wp = {}, {}
    for r in rows:
        if name_col and r.get(name_col):
            by_name[norm(r[name_col])] = r
        if ward_col and prec_col and r.get(ward_col) and r.get(prec_col):
            by_wp[(norm(r[ward_col]), norm(r[prec_col]))] = r

    geo = json.load(open(GEO, encoding="utf-8"))
    matched = 0
    for feat in geo["features"]:
        p = feat["properties"]
        rec = by_name.get(norm(p.get("name",""))) or by_wp.get((norm(p.get("ward","")), norm(p.get("precinct",""))))
        if not rec: continue
        matched += 1
        if total_col and rec.get(total_col) not in (None, ""):
            try: p["reg_total"] = int(float(str(rec[total_col]).replace(",", "")))
            except ValueError: p["reg_total"] = rec[total_col]
        # copy any extra value columns
        for nk, orig in headers.items():
            if orig in (name_col, ward_col, prec_col): continue
            val = rec.get(orig)
            if val not in (None, ""): p[orig] = val

    json.dump(geo, open(GEO, "w", encoding="utf-8"))
    print(f"Matched {matched} of {len(geo['features'])} precincts. Wrote {GEO}.")
    if matched < len(geo["features"]):
        print("Unmatched precincts kept reg_total = null. Check that your key column matches the precinct naming (e.g. 1-086).")

if __name__ == "__main__":
    main()
