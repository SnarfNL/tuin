"""Controleert data/ (schema 2). Draai vóór elke commit:  python3 -I scripts/check_data.py

- verwijzingen: beplanting, regels, projecttaken en stand verwijzen naar bestaande plekken en planten
- maanden 1–12, acties uit data/index.json, geldige soort, herhaling, status en deel
- plantenlijst van de achtertuin = tabel *Alle planten* in tuinplan/tuinplan.md
- foto's bestaan
- geen namen in voortgang en stand (de repo is openbaar)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
fout = []


def laad(*a):
    return json.load(open(P(*a), encoding="utf-8"))


idx = laad("data", "index.json")
acties = {a["id"] for a in idx["acties"]}
tellingen = []
for loc in idx["locaties"]:
    m = loc["map"]
    D = {k: laad("data", m, k + ".json")[k] for k in ("plekken", "planten", "beplanting", "regels", "projecttaken")}
    plekken = {p["id"] for p in D["plekken"]}
    planten = {p["id"] for p in D["planten"]}
    for naam, lijst in (("plekken", D["plekken"]), ("planten", D["planten"]), ("regels", D["regels"]), ("projecttaken", D["projecttaken"])):
        ids = [x["id"] for x in lijst]
        dubbel = {i for i in ids if ids.count(i) > 1}
        if dubbel:
            fout.append("%s/%s: dubbele id's %s" % (m, naam, sorted(dubbel)))
    for p in D["planten"]:
        for f in p.get("fotos", []):
            if not os.path.exists(P(f)):
                fout.append("%s/planten %s: foto ontbreekt %s" % (m, p["id"], f))
    for p in D["plekken"]:
        if p.get("foto") and not os.path.exists(P(p["foto"])):
            fout.append("%s/plekken %s: foto ontbreekt %s" % (m, p["id"], p["foto"]))
    for b in D["beplanting"]:
        if b["plant"] not in planten:
            fout.append("%s/beplanting: onbekende plant %s" % (m, b["plant"]))
        if b["plek"] not in plekken:
            fout.append("%s/beplanting: onbekende plek %s" % (m, b["plek"]))
        if b["status"] not in ("gepland", "geplant", "vervallen"):
            fout.append("%s/beplanting: status %s" % (m, b["status"]))
        if b.get("jaren") not in (None, "even", "oneven"):
            fout.append("%s/beplanting: jaren %s" % (m, b.get("jaren")))
    for r in D["regels"]:
        w = "%s/regels %s" % (m, r["id"])
        if r["actie"] not in acties:
            fout.append(w + ": onbekende actie " + r["actie"])
        if r.get("soort") not in ("taak", "suggestie", "waarschuwing"):
            fout.append(w + ": soort " + str(r.get("soort")))
        if r.get("herhaling") not in ("jaarlijks", "tot_geplant"):
            fout.append(w + ": herhaling " + str(r.get("herhaling")))
        if "plant" not in r and "plekken" not in r:
            fout.append(w + ": geen plant en geen plekken")
        if r.get("plant") and r["plant"] not in planten:
            fout.append(w + ": onbekende plant " + r["plant"])
        for p in r.get("plekken", []):
            if p not in plekken:
                fout.append(w + ": onbekende plek " + p)
        if not r["vensters"] or not all(v and all(1 <= x <= 12 for x in v) for v in r["vensters"]):
            fout.append(w + ": vensters " + str(r["vensters"]))
        for k, v in (r.get("deel") or {}).items():
            if k not in ("start", "eind") or v not in ("begin", "midden", "eind"):
                fout.append(w + ": deel " + str(r.get("deel")))
    for t in D["projecttaken"]:
        w = "%s/projecttaken %s" % (m, t["id"])
        if t["actie"] not in acties:
            fout.append(w + ": onbekende actie " + t["actie"])
        for p in t["plekken"]:
            if p not in plekken:
                fout.append(w + ": onbekende plek " + p)
        per = t.get("periode")
        if per and not (re.match(r"^\d{4}-\d\d$", per["van"]) and re.match(r"^\d{4}-\d\d$", per["tot"]) and per["van"] <= per["tot"]):
            fout.append(w + ": periode " + str(per))
        if t["status"] not in ("open", "geparkeerd", "vervallen"):
            fout.append(w + ": status " + t["status"])
    stand = laad("data", m, "stand.json")["items"] if os.path.exists(P("data", m, "stand.json")) else []
    for s in stand:
        w = "%s/stand %s" % (m, s.get("key"))
        if "wie" in s:
            fout.append(w + ": bevat een naam (wie)")
        if s.get("plek") not in plekken:
            fout.append(w + ": onbekende plek " + str(s.get("plek")))
        if s.get("status") not in ("gepland", "geplant", "weg"):
            fout.append(w + ": status " + str(s.get("status")))
        if not s.get("nieuw") and s.get("plant") not in planten:
            fout.append(w + ": onbekende plant " + str(s.get("plant")))
    tellingen.append("%s: %d plekken, %d planten, %d beplanting, %d regels, %d projecttaken, %d in de stand" % (
        m, len(D["plekken"]), len(D["planten"]), len(D["beplanting"]), len(D["regels"]), len(D["projecttaken"]), len(stand)))

# plantenlijst achtertuin tegen tuinplan.md
t = open(P("tuinplan", "tuinplan.md"), encoding="utf-8").read()
i = t.index("## Alle planten")
j = t.index("\n## ", i + 5)
plan_lat = set()
for l in t[i:j].splitlines():
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if l.startswith("|") and len(c) > 2 and not c[0].startswith("-") and c[0] != "Nederlandse naam":
        plan_lat.add(c[1])
data_lat = {p["latijn"] for p in laad("data", "achtertuin", "planten.json")["planten"]}
for x in sorted(plan_lat - data_lat):
    fout.append("achtertuin: %s staat in tuinplan.md maar niet in data" % x)
for x in sorted(data_lat - plan_lat):
    fout.append("achtertuin: %s staat in data maar niet in tuinplan.md" % x)

# voortgang
vd = P("data", "voortgang")
if os.path.isdir(vd):
    for f in os.listdir(vd):
        if f.endswith(".json"):
            for it in laad("data", "voortgang", f).get("items", []):
                if "wie" in it:
                    fout.append("voortgang/%s: bevat een naam (wie)" % f)

if fout:
    print("FOUT:\n- " + "\n- ".join(fout))
    sys.exit(1)
print("OK\n" + "\n".join(tellingen) + "\nplantenlijst achtertuin klopt met tuinplan/tuinplan.md (%d soorten)" % len(plan_lat))
