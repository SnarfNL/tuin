"""Eenmalig: zet data/ (schema 2) om naar tab-gescheiden tabellen voor de Google Sheet (één .tsv per tabblad)."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1]
MK = "jan feb mrt apr mei jun jul aug sep okt nov dec".split()
L = lambda m, f: json.load(open(os.path.join(ROOT, "data", m, f + ".json")))[f]
idx = json.load(open(os.path.join(ROOT, "data", "index.json")))
def mnd(vs): return ", ".join(MK[v[0]-1] if len(v) == 1 else MK[v[0]-1] + "-" + MK[v[-1]-1] for v in vs)
def c(x): return "" if x is None else str(x).replace("\t", " ").replace("\n", " ")
T = {}
T["Locaties"] = [["id", "naam", "plekwoord", "beslist_in"]] + [[l["id"], l["naam"], l["plekwoord"], l["beslist_in"]] for l in idx["locaties"]]
KL = {"snoeien": ("#e3eddb", "#34492a"), "mulchen": ("#efe4d2", "#634724"), "mest": ("#f3e0cf", "#7a3f16"), "planten": ("#e0eaf1", "#28465c"),
      "oogsten": ("#f5e5c2", "#5f470c"), "water": ("#dbe8f2", "#234b69"), "opruimen": ("#e9e5df", "#47413a"), "onderhoud": ("#e8e1ee", "#4a3a5c")}
T["Acties"] = [["id", "label", "kleur_achtergrond", "kleur_tekst"]] + [[a["id"], a["label"], *KL[a["id"]]] for a in idx["acties"]]
T["Plekken"] = [["locatie", "id", "naam", "type", "zon", "zonklasse", "thema", "m2", "maat", "grond", "grond_uitgevoerd", "mulch", "water_per_week", "plantplek_en_mest", "beschrijving", "foto", "status"]]
T["Planten"] = [["locatie", "id", "nl", "latijn", "soort", "levensduur", "bijen", "vogels", "score_eigen", "bron_scores", "beschrijving", "link_label", "link_url",
                 "sierwaarde", "bron_bloei", "onderhoud", "familie", "plantgoed", "plantafstand", "bloei", "vorm", "hoogte", "plantmoment", "grondwens", "tip",
                 "lente", "zomer", "herfst", "winter", "emoji", "kleur", "fotos"]]
T["Beplanting"] = [["locatie", "plant", "plek", "status", "aantal", "vanaf", "jaren"]]
T["Regels"] = [["locatie", "id", "plant", "plekken", "actie", "detail", "soort", "maanden", "keuze", "herhaling", "deel_start", "deel_eind", "uiterlijk",
                "voorwaarde", "meting", "toelichting", "waar", "bron"]]
T["Projecttaken"] = [["locatie", "id", "titel", "actie", "plekken", "wanneer", "van", "tot", "deel", "uiterlijk", "status", "afhankelijk_van", "bron"]]
T["Info"] = [["locatie", "soort", "id", "titel", "tekst", "extra"]]
for l in idx["locaties"]:
    m = l["id"]
    for p in L(m, "plekken"):
        g = p.get("grond"); g = g if isinstance(g, dict) else {"plan": g}
        w = p.get("water") or {}
        T["Plekken"].append([m, p["id"], p["naam"], p["type"], p.get("zon"), p.get("zonklasse"), p.get("thema"), str(p.get("m2") or "").replace(".", ","), p.get("maat"),
                             g.get("plan"), g.get("uitgevoerd"), p.get("mulch"), (w.get("per_week", "") + (". " + w["opmerking"] if w.get("opmerking") else "")) if w else "",
                             " • ".join(p.get("plantplek", [])), p.get("beschrijving"), p.get("foto"), p["status"]])
    for p in L(m, "planten"):
        st = p.get("seizoenstekst", {}); lk = p.get("link") or {}
        T["Planten"].append([m, p["id"], p["nl"], p.get("latijn"), p["soort"], p.get("levensduur"), p.get("bijen"), p.get("vogels"), ", ".join(p.get("score_eigen") or []),
                             p.get("bron_scores"), p.get("beschrijving"), lk.get("label"), lk.get("url"), p.get("sierwaarde"), p.get("bron_bloei"), p.get("onderhoud"),
                             p.get("familie"), p.get("plantgoed"), p.get("plantafstand"), p.get("bloei"), p.get("vorm"), p.get("hoogte"), p.get("plantmoment"),
                             p.get("grondwens"), p.get("tip"), st.get("lente"), st.get("zomer"), st.get("herfst"), st.get("winter"), p.get("emoji"),
                             ",".join(p.get("kleur") or []), ", ".join(p.get("fotos", []))])
    for b in L(m, "beplanting"):
        T["Beplanting"].append([m, b["plant"], b["plek"], b["status"], b.get("aantal"), b.get("vanaf"), b.get("jaren")])
    for r in L(m, "regels"):
        d = r.get("deel") or {}; u = r.get("uiterlijk"); me = r.get("meting")
        T["Regels"].append([m, r["id"], r.get("plant"), ", ".join(r.get("plekken", [])), r["actie"], r["detail"], r["soort"], mnd(r["vensters"]),
                            "ja" if r.get("keuze") else "", r["herhaling"], d.get("start"), d.get("eind"), "%s %s" % (u["deel"], MK[u["maand"]-1]) if u else "",
                            r.get("voorwaarde"), "%s, streef %s" % (me["eenheid"], me["streef"]) if me else "", r.get("toelichting"), r.get("waar"), r.get("bron")])
    for t in L(m, "projecttaken"):
        p = t.get("periode") or {}; u = p.get("uiterlijk")
        T["Projecttaken"].append([m, t["id"], t["titel"], t["actie"], ", ".join(t["plekken"]), t["wanneer"], p.get("van"), p.get("tot"), p.get("deel"),
                                  "%s %s" % (u["deel"], MK[u["maand"]-1]) if u else "", t["status"], t.get("afhankelijk_van"), t.get("bron")])
    i = L(m, "info")
    T["Info"].append([m, "titel", "", i.get("titel"), i.get("ondertitel"), ""])
    for x in i.get("themas", []): T["Info"].append([m, "thema", x["id"], x["naam"], x["beschrijving"], x["emoji"]])
    for x in i.get("tips", []):
        for n, pt in enumerate(x["punten"]): T["Info"].append([m, "tip", x["id"], x["titel"], pt, x["emoji"] if n == 0 else ""])
    for x in i.get("impressies", []): T["Info"].append([m, "impressie", x["seizoen"], x["seizoen"].capitalize(), "", x["foto"]])
    for x in i.get("open_punten", []): T["Info"].append([m, "open_punt", "", "", x, ""])
T["Stand"] = [["key", "locatie", "plant", "naam", "plek", "status", "aantal", "notitie", "nieuw", "via_regel", "datum"]]
T["Voortgang"] = [["jaar", "taak", "datum", "notitie", "meting"]]
T["Instellingen"] = [["sleutel", "waarde", "uitleg"],
    ["geen_achterstand_voor", idx["geen_achterstand_voor"], "Taken uit maanden vóór deze maand (jjjj-mm) tellen niet als nog open"],
    ["achterstand_maanden", "3", "Hoeveel maanden terug de app nog open taken toont"],
    ["sierwaarde_codes", "B bloei, L blad, E bes of vrucht, Z zaadhoofden, W wintersilhouet, - geen", "Codes in Planten.sierwaarde (12 tekens, jan-dec)"]]
for k, rows in T.items():
    with open(os.path.join(OUT, k + ".tsv"), "w") as f:
        f.write("\n".join("\t".join(c(x) for x in r) for r in rows))
print({k: len(v) - 1 for k, v in T.items()})
