#!/usr/bin/env python3
"""Controleert de gedeelde tuindata in data/ en vergelijkt de plantenlijst met tuinplan/tuinplan.md.

Gebruik: python3 scripts/check_data.py   (vanuit de hoofdmap van de repo)
Eindigt met code 1 als er fouten zijn.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MAANDEN = {"jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"}
ACTIES = {"snoeien", "planten_zaaien", "delen_verplanten", "uitgebloeid_verwijderen",
          "zaaien", "uitplanten", "oogsten", "bemesten", "afdekken",
          "mulchen", "meten", "water_geven", "niet_doen", "aanvullen"}
HERHALING = {"jaarlijks", "eenmalig_aanplant", "indien_nodig", "conditioneel"}
BRONNEN = {"tuinplan", "moestuin"}

fouten = []


def laad(naam):
    pad = DATA / naam
    try:
        return json.loads(pad.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        fouten.append(f"{naam}: kan niet gelezen worden ({e})")
        return []


def laad_moestuin(naam):
    pad = DATA / "moestuin" / naam
    if not pad.exists():
        return []
    return json.loads(pad.read_text(encoding="utf-8"))


bakken = laad("bakken.json") + laad_moestuin("bakken.json")
planten = laad("planten.json") + laad_moestuin("gewassen.json")
bollen = laad("bollen_per_bak.json")
regels = laad("onderhoudsregels.json") + laad_moestuin("onderhoudsregels.json")
algemeen = laad("algemene_regels.json")
taken = laad("eenmalige_taken.json")

bak_ids = [b["id"] for b in bakken]
plant_ids = [p["id"] for p in planten]
for naam, ids in (("bakken", bak_ids), ("planten", plant_ids),
                  ("onderhoudsregels", [r["id"] for r in regels]),
                  ("eenmalige_taken", [t["id"] for t in taken])):
    dubbel = {i for i in ids if ids.count(i) > 1}
    if dubbel:
        fouten.append(f"{naam}: dubbele id's {sorted(dubbel)}")

for rij in bakken + planten + bollen + regels + algemeen + taken:
    if rij.get("bron") not in BRONNEN:
        fouten.append(f"{rij.get('id', rij)}: bron moet 'tuinplan' of 'moestuin' zijn")

for p in planten:
    for b in p.get("bakken", []):
        if b not in bak_ids:
            fouten.append(f"plant {p['id']}: onbekende bak {b}")

for r in bollen:
    if r["bak"] not in bak_ids:
        fouten.append(f"bollen: onbekende bak {r['bak']}")
    if r["plant"] not in plant_ids:
        fouten.append(f"bollen: onbekende plant {r['plant']}")

for r in regels:
    if r["plant"] not in plant_ids:
        fouten.append(f"regel {r['id']}: onbekende plant {r['plant']}")
    if r["actie"] not in ACTIES:
        fouten.append(f"regel {r['id']}: onbekende actie {r['actie']}")
    if r["herhaling"] not in HERHALING:
        fouten.append(f"regel {r['id']}: onbekende herhaling {r['herhaling']}")
    if not set(r["maanden"]) <= MAANDEN:
        fouten.append(f"regel {r['id']}: onbekende maand in {r['maanden']}")

for r in algemeen:
    if not set(r["maanden"]) <= MAANDEN:
        fouten.append(f"algemene regel {r['id']}: onbekende maand in {r['maanden']}")
    for b in r["bakken"]:
        if b not in bak_ids:
            fouten.append(f"algemene regel {r['id']}: onbekende bak {b}")

zonder = [p["id"] for p in planten if p.get("status") != "vervallen"
          and not any(r["plant"] == p["id"] for r in regels)]
if zonder:
    fouten.append(f"planten zonder onderhoudsregel: {zonder}")

# Vergelijk met de tabel 'Alle planten' in tuinplan.md (alleen de siertuin).
md = (ROOT / "tuinplan" / "tuinplan.md").read_text(encoding="utf-8")
blok = md.split("## Alle planten", 1)[1].split("\n## ", 1)[0]
md_planten = {}
for regel in blok.splitlines():
    cellen = [c.strip() for c in regel.strip().strip("|").split("|")]
    if len(cellen) < 3 or cellen[0] in ("Nederlandse naam", "") or set(cellen[0]) <= {"-"}:
        continue
    md_planten[cellen[1]] = {z.strip() for z in cellen[2].split(",")}


def sleutel(latijn):
    return re.sub(r"[^a-z]", "", latijn.lower())


md_index = {sleutel(k): (k, v) for k, v in md_planten.items()}
json_sier = [p for p in planten if p.get("bron") == "tuinplan" and p.get("status") != "vervallen"]
for p in json_sier:
    k = sleutel(p["latijn"])
    kandidaten = [m for m in md_index if m.startswith(k) or k.startswith(m)]
    if not kandidaten:
        fouten.append(f"plant {p['id']} ({p['latijn']}) staat niet in de tabel 'Alle planten' van tuinplan.md")
        continue
    naam, zones = md_index[kandidaten[0]]
    if zones != set(p["bakken"]):
        fouten.append(f"plant {p['id']}: bakken {sorted(p['bakken'])} wijken af van tuinplan.md {sorted(zones)}")
if len(md_planten) != len(json_sier):
    fouten.append(f"aantal planten: tuinplan.md {len(md_planten)}, data/planten.json {len(json_sier)}")

if fouten:
    print("FOUTEN:")
    for f in fouten:
        print(" -", f)
    sys.exit(1)
print(f"OK: {len(bakken)} bakken, {len(planten)} planten, {len(regels)} onderhoudsregels, "
      f"{len(algemeen)} algemene regels, {len(taken)} eenmalige taken; plantenlijst klopt met tuinplan/tuinplan.md.")
