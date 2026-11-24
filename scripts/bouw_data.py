"""Bouwt data/ (schema 2) uit de leesbare plannen.

Bronnen (niet aanpassen vanuit het project Tuin app):
  tuinplan/tuinplan.md        achtertuin (project Tuin)
  tuinplan/index.html         foto-sleutels, emoji en kleur per plant (project Tuin)
  moestuin/moestuinplan.md    moestuin (project Moestuin)
  overdracht/tuin.md          open taken van de achtertuin met datum (overdracht van 24 november 2026)

Wat niet in een tabel staat (algemene regels en waarschuwingen) staat hieronder in ALG_ACHTERTUIN,
met de sectie in tuinplan.md waar het vandaan komt.

Gebruik (vanuit de hoofdmap van de repo):  python3 -I scripts/bouw_data.py
"""
import ast, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
MK = "jan feb mrt apr mei jun jul aug sep okt nov dec".split()
MND = {m: i + 1 for i, m in enumerate(MK)}
MND.update({"maart": 3, "sept": 9, "januari": 1, "februari": 2, "maart": 3, "april": 4, "juni": 6, "juli": 7, "augustus": 8,
            "september": 9, "oktober": 10, "november": 11, "december": 12})
DEELW = {"b": "begin", "m": "midden", "e": "eind"}
AANVULLEN = []


def lees(*a):
    return open(P(*a), encoding="utf-8").read()


def sectie(t, kop, niveau="## "):
    i = t.index(kop)
    j = t.find("\n" + niveau, i + len(kop))
    return t[i: j if j > 0 else len(t)]


def tabel(s):
    """Alle rijen van de eerste tabel in s, als lijsten van cellen (zonder kopregel)."""
    rijen, bezig = [], False
    for l in s.splitlines():
        if l.startswith("|"):
            if re.match(r"\|\s*-", l):
                bezig = True
                continue
            if bezig:
                rijen.append([c.strip() for c in l.strip().strip("|").split("|")])
        elif bezig:
            break
    return rijen


def kaal(x):
    return re.sub(r"\*+|↑", "", x).strip()


def norm_lat(x):
    x = kaal(x).lower()
    x = re.sub(r"\(.*?\)", " ", x)
    return re.sub(r"\s+", " ", re.sub(r"[^a-z' ]", " ", x)).strip()


def gs(x):
    w = re.sub(r"'.*?'", "", norm_lat(x)).split()
    return (w + ["", ""])[:2]


def slug(s):
    s = s.lower().replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def zones(z):
    return re.findall(r"\b([ABCDS])\b", z)


def vensters(ms):
    ms = sorted(set(ms))
    runs = []
    for m in ms:
        if runs and runs[-1][-1] == m - 1:
            runs[-1].append(m)
        else:
            runs.append([m])
    if len(runs) > 1 and runs[0][0] == 1 and runs[-1][-1] == 12:
        runs[0] = runs.pop() + runs[0]
    return runs


MAAND_RE = r"(?:(b|m|e)-)?(jan|feb|mrt|maart|apr|mei|jun|jul|aug|sep|okt|nov|dec)[a-z]*\b"
SEIZOEN = {"voorjaar": "mrt–mei", "lente": "mrt–mei", "zomer": "jun–aug", "herfst": "sep–nov", "najaar": "sep–nov", "winter": "dec–feb"}


def periode(txt):
    """Eerste maandreeks uit een tekst als 'm-apr–b-mei (in pot)' → (maanden, deel) of (None, None)."""
    t = txt.lower()
    if not re.search(MAAND_RE, t):
        for k, v in SEIZOEN.items():
            t = re.sub(r"\b%s\b" % k, v, t)
    t = t.replace("ijsheiligen", "m-mei").replace("half ", "m-").replace("begin ", "b-").replace("eind ", "e-")
    t0 = t
    t = re.split(r"\(|;|\. ", t)[0]
    hits = list(re.finditer(MAAND_RE, t))
    if not hits:
        t = re.split(r";|\. ", t0.replace("(", "").replace(")", ""))[0]
        hits = list(re.finditer(MAAND_RE, t))
    if not hits:
        return None, None
    a = hits[0]
    b = a
    if len(hits) > 1 and re.match(r"\s*[–-]\s*", t[a.end(): hits[1].start()]) and t[a.end(): hits[1].start()].strip() in ("–", "-"):
        b = hits[1]
    m1, m2 = MND[a.group(2)], MND[b.group(2)]
    ms = list(range(m1, m2 + 1)) if m1 <= m2 else list(range(m1, 13)) + list(range(1, m2 + 1))
    deel = {}
    if a.group(1):
        deel["start"] = DEELW[a.group(1)]
    if b.group(1) and (b is not a or not a.group(1)):
        deel["eind"] = DEELW[b.group(1)]
    elif a.group(1) and b is a:
        deel["eind"] = DEELW[a.group(1)]
    return ms, deel or None


def score(c):
    m = re.match(r"(\d)", c.strip())
    return (int(m.group(1)), "(e)" in c) if m else (None, False)


def link(c):
    m = re.search(r"\[(.*?)\]\((.*?)\)", c)
    return {"label": m.group(1), "url": m.group(2)} if m else None


# ============================================================ ACHTERTUIN
T = lees("tuinplan", "tuinplan.md")
oud = {}
for pad in (("data", "achtertuin", "planten.json"), ("data", "planten.json")):
    if os.path.exists(P(*pad)):
        d = json.load(open(P(*pad)))
        for p in (d["planten"] if isinstance(d, dict) else d):
            oud.setdefault(norm_lat(p["latijn"]), p)

# foto's, emoji en kleur uit de interactieve weergave
G = {}
h = lees("tuinplan", "index.html")
gi = h.index("const G=[")
for l in h[gi: h.index("];", gi)].split("\n"):
    l = l.strip()
    if not l.startswith("["):
        continue
    l = re.sub(r"W\('([^']*)'\)", r"'https://en.wikipedia.org/wiki/\1'", l.rstrip(",")).replace("null", "None")
    try:
        r = ast.literal_eval(l)
    except Exception:
        continue
    G[norm_lat(r[1])] = r
IMG = sorted(f[:-4] for f in os.listdir(P("tuinplan", "images")) if f.endswith(".jpg"))


def fotos_voor(key):
    if not key:
        return []
    ids = [key] if key in IMG else [i for i in IMG if i.endswith("-" + key)]
    return ["tuinplan/images/%s.jpg" % i for i in ids]


# --- plekken
opp = dict(re.findall(r"\b([ABCDS]) (\d+(?:,\d+)?) m²", sectie(T, "**Oppervlaktes per zone")))
mulch = {}
for r in tabel(sectie(T, "**Wat per zone**", "## ")):
    for z in zones(r[0]):
        mulch[z] = kaal(r[1]) + (". " + kaal(r[2]) if len(r) > 2 else "")
water = {}
for r in tabel(sectie(T, "**Per zone (per week")):
    if r[0] in "ABCDS":
        water[r[0]] = {"behoefte": kaal(r[2]), "per_week": kaal(r[3]), "opmerking": kaal(r[4])}
THEMA = {"Natuurlijk": "natuurlijk", "Landelijk": "landelijk", "Jardin Sauvage": "sauvage", "Sauvage": "sauvage"}
ZON = {"Volle zon": ("volle zon (>6 u)", "vol"), "Half-zon": ("half-zon (3–6 u)", "half"), "Schaduw": ("schaduw (<3 u)", "schaduw")}
plekken = []
for m in re.finditer(r"^### Zone ([ABCDS]) — (.+)$", T, re.M):
    z, kop = m.group(1), m.group(2)
    s = sectie(T, m.group(0), "### ")
    zon = next(v for k, v in ZON.items() if kop.startswith(k))
    thema = next(v for k, v in THEMA.items() if k in kop.split("·")[-1])
    gp = re.search(r"\*\*Grondsoort \(plan\):\*\* (.+)", s)
    gu = re.search(r"\*\*Grondverbetering, uitgevoerd[^*]*\*\* (.+)", s)
    pp = sectie(s, "**📍 Plantplek en mest", "### ") if "**📍 Plantplek en mest" in s else ""
    plekken.append({
        "id": z, "naam": "Zone " + z, "type": "zone", "zon": zon[0], "zonklasse": zon[1], "thema": thema,
        "m2": float(opp[z].replace(",", ".")) if z in opp else None,
        "grond": {"plan": gp.group(1).strip() if gp else None, "uitgevoerd": gu.group(1).strip() if gu else None},
        "plantplek": [kaal(re.sub(r"^\s*-\s*", "", l)) for l in pp.splitlines() if l.strip().startswith("- ")],
        "mulch": mulch.get(z), "water": water.get(z),
        "foto": "tuinplan/images/zone-%s-seizoenen.jpg" % z, "status": "actief"})
plekken.append({"id": "kas", "naam": "Tuinkas", "type": "kas", "zon": "volle zon (>6 u, aanname)", "zonklasse": "vol",
                "beschrijving": "Glazen achthoek met fundering. Nog geen teeltplanning; planten uit de kas mogen naar de moestuin.",
                "status": "actief"})
plekken.append({"id": "algemeen", "naam": "Algemeen", "type": "algemeen",
                "beschrijving": "Schorspad, rond terras en de ringen van schors om de bomen; regenton.", "status": "actief"})

# --- planten
BOMEN = {}
for m in re.finditer(r"^### (.+?) — \*(.+?)\*(.*)$", sectie(T, "## Bomen"), re.M):
    s = sectie(T, m.group(0), "### ")
    f = dict((k.strip(), kaal(v)) for k, v in re.findall(r"^- \*\*(.+?):\*\* (.+)$", s, re.M))
    BOMEN[gs(m.group(2))[0]] = {
        "vorm": "halfstam" if "alf" in m.group(3) else "struikvorm",
        "hoogte": f.get("Hoogte"),
        "seizoenstekst": {k.lower(): re.sub(r"^[^\w]+", "", f[k]).strip() for k in ("Lente", "Zomer", "Herfst", "Winter") if k in f},
        "grondwens": f.get("Grond"), "tip": f.get("Tip"), "plantmoment": f.get("Plantmoment")}
    BOMEN[gs(m.group(2))[0]]["_geplant"] = "**Geplant" in s
LEV = {"⏳": "zaaien", "⏱": "kort"}
planten, beplanting, idx = [], [], {}
CODE = {"Bloei": "B", "Blad": "L", "Bes": "E", "Zaad": "Z", "Win": "W", "–": "-", "-": "-"}
kal = {}
for r in tabel(sectie(T, "## Jaarkalender")):
    m = re.search(r"\(\*(.+?)\*\)", r[0])
    if m and len(r) >= 15:
        kal[norm_lat(m.group(1))] = ("".join(CODE.get(c.strip(), "-") for c in r[2:14]), kaal(r[14]))
for r in tabel(sectie(T, "## Alle planten")):
    nl, lat, zs = kaal(r[0]), kaal(r[1]), zones(r[2])
    k = norm_lat(lat)
    o = oud.get(k) or next((v for kk, v in oud.items() if gs(kk) == gs(lat)), None)
    pid = o["id"] if o else slug(lat).replace("-", "_")
    g = G.get(k) or next((v for kk, v in G.items() if gs(kk) == gs(lat) and len(set(v[2]) & set(zs))), None)
    bij, bij_e = score(r[4])
    vog, vog_e = score(r[5])
    p = {"id": pid, "nl": nl, "latijn": lat, "soort": o["soort"] if o else "vaste plant",
         "levensduur": next((v for s2, v in LEV.items() if s2 in r[7]), None),
         "klimplant": (o or {}).get("soort") == "klimplant", "beschrijving": kaal(r[3]),
         "bijen": bij, "vogels": vog, "score_eigen": [n for n, e in (("bijen", bij_e), ("vogels", vog_e)) if e] or None,
         "bron_scores": kaal(r[6]), "link": link(r[8]),
         "emoji": g[3] if g else None, "kleur": g[4].split(",") if g else None, "fotos": fotos_voor(g[9]) if g else []}
    if not p["fotos"] or not os.path.exists(P(p["fotos"][0])):
        p["fotos"] = ["tuinplan/images/%s.jpg" % i for i in IMG if i.split("-")[-1] == gs(lat)[0] and i.split("-")[0] in zs]
    if k in kal:
        p["sierwaarde"], p["bron_bloei"] = kal[k]
    else:
        AANVULLEN.append("tuinplan: geen jaarkalender-regel voor %s" % nl)
    p.update({k2: v2 for k2, v2 in BOMEN.get(gs(lat)[0], {}).items() if not k2.startswith("_")} if p["soort"] == "boom" else {})
    if not p["fotos"]:
        AANVULLEN.append("tuinplan: geen foto voor %s" % nl)
    planten.append({kk: v for kk, v in p.items() if v not in (None, [], {})})
    idx[pid] = p
    geplant = p["soort"] == "boom" and BOMEN.get(gs(lat)[0], {}).get("_geplant", False)
    for z in zs:
        beplanting.append({"plant": pid, "plek": z, "status": "geplant" if geplant else "gepland"})

bol = {}
for r in tabel(sectie(T, "### Bollen per zone")):
    if "staat er al" in r[1]:
        AANVULLEN.append("tuinplan: *Bollen per zone* zegt voor zone %s \"%s\", maar de onderhoudskalender en stap 7 noemen ze nog als te poten; in de data staan ze als gepland" % (r[0], kaal(r[1])))
    for naam, aantal in re.findall(r"([A-Za-z' ]+?) (±[\d–]+)", r[1]):
        bol[(r[0], naam.strip().lower())] = aantal
for b in beplanting:
    p = idx[b["plant"]]
    for (z, naam), a in bol.items():
        if p["soort"] == "bol" and z == b["plek"] and (naam == p["nl"].lower() or naam.startswith(p["nl"].lower().split(" ")[0]) and p["nl"].lower().startswith(naam.split(" ")[0])):
            b["aantal"] = a

# --- regels uit de onderhoudskalender (per soort; gelden in alle plekken waar de soort staat)
EMO = {"✂️": "snoeien", "🌱": "planten", "🪴": "delen", "🥀": "uitgebloeid"}


def zoek_plant(cel, zs):
    m = re.search(r"\(\*(.+?)\*", cel)
    lat = m.group(1) if m else cel
    k = norm_lat(lat)
    for p in planten:
        if norm_lat(p["latijn"]) == k:
            return p
    kand = [p for p in planten if gs(p["latijn"]) == gs(lat)]
    if len(kand) == 1:
        return kand[0]
    kand = [p for p in planten if gs(p["latijn"])[0] == gs(lat)[0] and any(b["plant"] == p["id"] and b["plek"] in zs for b in beplanting)]
    return kand[0] if len(kand) == 1 else None


per_plant = {}
for r in tabel(sectie(T, "## Onderhoudskalender")):
    zs = zones(r[0])
    p = zoek_plant(r[1], zs)
    if not p:
        AANVULLEN.append("onderhoudskalender: plant niet gevonden: " + r[1])
        continue
    e = per_plant.setdefault(p["id"], {"maanden": {}, "toel": []})
    for i, c in enumerate(r[2:14]):
        for emo, act in EMO.items():
            if emo in c:
                e["maanden"].setdefault(act, set()).add(i + 1)
    if kaal(r[14]) and kaal(r[14]) not in e["toel"]:
        e["toel"].append(kaal(r[14]))
regels = []
for pid, e in per_plant.items():
    p = idx[pid]
    if e["toel"]:
        p["onderhoud"] = " ".join(e["toel"])
    for act, ms in e["maanden"].items():
        v = vensters(ms)
        if act == "snoeien":
            r = {"id": pid + ".snoeien", "actie": "snoeien", "detail": "Snoeien / terugknippen", "soort": "taak", "herhaling": "jaarlijks"}
        elif act == "uitgebloeid":
            r = {"id": pid + ".uitgebloeid_verwijderen", "actie": "snoeien", "detail": "Uitgebloeide bloemen weghalen", "soort": "taak", "herhaling": "jaarlijks"}
        elif act == "delen":
            r = {"id": pid + ".delen_verplanten", "actie": "planten", "detail": "Delen / verplanten", "soort": "suggestie", "herhaling": "jaarlijks"}
        else:
            zaai = p.get("levensduur") == "zaaien"
            r = {"id": pid + ".planten_zaaien", "actie": "planten", "soort": "taak",
                 "detail": "Bollen poten" if p["soort"] == "bol" else "Zaaien" if zaai else "Planten",
                 "herhaling": "jaarlijks" if zaai else "tot_geplant"}
            if len(v) > 1:
                r["keuze"] = True
            if re.search(r"tot half december", p.get("onderhoud", "")):
                r["uiterlijk"] = {"maand": 12, "deel": "midden"}
        r["plant"] = pid
        r["vensters"] = v
        regels.append(r)
for p in planten:
    if p["id"] not in per_plant:
        AANVULLEN.append("onderhoudskalender: geen regel voor %s" % p["nl"])

# --- algemene regels en waarschuwingen (geen tabel in tuinplan.md; bron per regel)
WATER_V = "Alleen als er die week minder dan ±10 mm regen viel en de grond op 5 cm droog aanvoelt"
ALG_ACHTERTUIN = [
    {"id": "alg.mulch_winter", "plekken": ["A", "B", "C", "S"], "actie": "mulchen", "detail": "Kale grond afdekken", "vensters": [[12]],
     "toelichting": "±5 cm op vochtige grond, vrij van stengels en stammen. Niet in D.", "bron": "Mulchen, Hoe 8"},
    {"id": "alg.mulch_voorjaar", "plekken": ["A", "B", "C", "S"], "actie": "mulchen", "detail": "Mulchlaag aanvullen na het terugknippen", "vensters": [[2, 3]],
     "toelichting": "±5 cm. Niet in D; in C niet rond Aster, Salvia en Liatris.", "bron": "Mulchen, Hoe 8; Jaarlijks onderhoud"},
    {"id": "alg.ph_kornoelje", "plekken": ["A"], "plant": "cornus", "actie": "onderhoud", "detail": "pH meten en noteren", "vensters": [[3, 4], [10]],
     "meting": {"eenheid": "pH", "streef": "5,5–6,5"},
     "toelichting": "Op dezelfde plekken in de zure plantplek. In 2027 en 2028 in voor- en najaar, daarna jaarlijks. Regenwater geven.",
     "bron": "pH-beheer kornoelje 5; overdracht/tuin.md"},
    {"id": "alg.schorspad", "plekken": ["algemeen"], "actie": "mulchen", "detail": "Schorspad en schorsringen controleren en aanvullen", "vensters": [[3]],
     "toelichting": "Aanvullen als de laag dunner is dan 5 cm; Franse boomschors, liever te weinig bestellen en later aanvullen.",
     "bron": "Schorspad, Aanvullen"},
    {"id": "alg.zaadhoofden", "plekken": ["A", "B", "C", "D", "S"], "actie": "snoeien", "detail": "Zaadhoofden laten staan tot maart", "soort": "waarschuwing",
     "vensters": [[10, 11, 12, 1, 2]], "toelichting": "Voedsel en beschutting voor vogels en insecten.", "bron": "Bijen-tips"},
    {"id": "alg.blad_sauvage", "plekken": ["D", "S"], "actie": "opruimen", "detail": "Blad laten liggen", "soort": "waarschuwing",
     "vensters": [[10, 11, 12]], "toelichting": "In de sauvage-zones blijft het blad liggen.", "bron": "Jaarlijks onderhoud"},
    {"id": "alg.bollen_blad", "plekken": ["A", "B", "C", "D"], "actie": "snoeien", "detail": "Blad van uitgebloeide bollen laten afsterven", "soort": "waarschuwing",
     "vensters": [[4, 5]], "toelichting": "Niet afknippen; de bol haalt er de kracht voor volgend jaar uit.", "bron": "Jaarlijks onderhoud"},
    {"id": "alg.klimop_broedseizoen", "plekken": ["S"], "plant": "hedera", "actie": "snoeien", "detail": "Klimop niet snoeien (broedseizoen)", "soort": "waarschuwing",
     "vensters": [[3, 4, 5, 6, 7, 8]], "toelichting": "Snoeien buiten het broedseizoen.", "bron": "Onderhoudskalender, klimop"},
    {"id": "alg.druif_maart", "plekken": ["D"], "plant": "vitis", "actie": "snoeien", "detail": "Druif niet snoeien in maart (bloedt)", "soort": "waarschuwing",
     "vensters": [[3]], "toelichting": "Wintersnoei in dec–jan.", "bron": "Nieuwe klimmers; Onderhoudskalender, druif"},
]
for z in "ABCDS":
    w = water.get(z)
    if w and not w["per_week"].lower().startswith("geen"):
        ALG_ACHTERTUIN.append({"id": "alg.water." + z, "plekken": [z], "actie": "water", "detail": "Water geven",
                               "vensters": [[4, 5, 6, 7, 8, 9]], "voorwaarde": WATER_V,
                               "toelichting": "Per week: %s. %s" % (w["per_week"], w["opmerking"]), "bron": "Water geven (indicatie per zone)"})
ALG_ACHTERTUIN.append({"id": "alg.water.bomen", "plekken": ["A", "C"], "actie": "water", "detail": "Bomen water geven",
                       "vensters": [[4, 5, 6, 7, 8, 9]], "voorwaarde": WATER_V,
                       "toelichting": "40–60 l per boom per week in droge perioden, jaar 1–2; de kornoelje met regenwater.",
                       "bron": "Water geven, Bomen"})
for r in ALG_ACHTERTUIN:
    r.setdefault("soort", "taak")
    r.setdefault("herhaling", "jaarlijks")
    regels.append(r)

# --- projecttaken: open taken met datum uit de overdracht (zonder de terugkerende)
JAAR0 = 2026
VANDAAG = "2026-11-24"


def pt_periode(w):
    t = w.lower().replace("**", "")
    for k, v in SEIZOEN.items():
        t = re.sub(r"\b%s\b" % k, v, t)
    snel = "zo snel mogelijk" in t
    jaren = [int(j) for j in re.findall(r"20\d\d", t)]
    jr = jaren[0] if jaren else None
    if "zo snel mogelijk" in t and "uiterlijk" in t:
        t = t[t.index("uiterlijk"):]
    m = re.search(r"uiterlijk (\d+) (\w+)", t)
    if m and m.group(2) in MND:
        mm = MND[m.group(2)]
        return {"van": "%d-%02d" % (jr, mm), "tot": "%d-%02d" % (jr, mm), "uiterlijk": {"maand": mm, "deel": "begin" if int(m.group(1)) <= 10 else "midden" if int(m.group(1)) <= 20 else "eind"}}
    kern = re.sub(r"\(.*?\)", "", t)
    t2 = t.replace("vóór ", "").replace("voor ", "")
    t2 = t2.replace("half ", "m-").replace("begin ", "b-").replace("eind ", "e-")
    hits = list(re.finditer(MAAND_RE, t2))
    if not hits:
        return None
    def mnd(h):
        return MND[h.group(2)]
    a, b = hits[0], hits[0]
    if len(hits) > 1 and t2[a.end(): hits[1].start()].strip() in ("–", "-"):
        b = hits[1]
    m1, m2 = mnd(a), mnd(b)
    j1 = jr or (JAAR0 if m1 >= 11 else JAAR0 + 1)
    j2 = j1 if m2 >= m1 else j1 + 1
    per = {"van": "%d-%02d" % (j1, m1), "tot": "%d-%02d" % (j2, m2)}
    if snel:
        per["van"] = VANDAAG[:7]
    if "vóór" in kern or "uiterlijk" in kern:
        per["uiterlijk"] = {"maand": m2, "deel": DEELW.get(b.group(1), "eind")}
        if "vóór eind" in t:
            per["uiterlijk"]["deel"] = "eind"
    elif a.group(1):
        per["deel"] = DEELW[a.group(1)]
    return per


ACTIE_PT = [("planten", "plant"), ("planten", "bollen"), ("planten", "zaai"), ("planten", "bestellen"), ("mulchen", "afdekken"),
            ("mulchen", "mulch"), ("onderhoud", "")]
OV = lees("overdracht", "tuin.md")
projecttaken = []
for r in tabel(sectie(OV, "## Open punten die taken opleveren")):
    taak, wanneer, zone = kaal(r[0]), kaal(r[1]), kaal(r[2])
    if re.search(r"jaarlijks|daarna jaarlijks|en 2028|herzaaien", wanneer + " " + taak, re.I) or taak.lower().startswith("met de hand water"):
        continue  # terugkerend: staat al als regel
    pk = zones(zone) if zones(zone) else ["algemeen"]
    if "alle" in zone:
        pk = list("ABCDS")
    actie = next(a for a, w in ACTIE_PT if w in taak.lower())
    e = {"id": "tuin." + slug(taak)[:40], "titel": taak, "actie": actie, "plekken": pk, "wanneer": wanneer,
         "status": "geparkeerd" if "geparkeerd" in wanneer.lower() else "open", "bron": "overdracht/tuin.md"}
    if kaal(r[3]) not in ("—", "-", ""):
        e["afhankelijk_van"] = kaal(r[3])
    per = pt_periode(wanneer)
    if per:
        e["periode"] = per
    projecttaken.append(e)

# --- info
info = {"titel": kaal(T.splitlines()[0].lstrip("# ")), "ondertitel": kaal(T.splitlines()[2]), "themas": [], "tips": [],
        "impressies": [{"seizoen": s, "foto": "tuinplan/images/tuin-impressie-%s.jpg" % s} for s in ("lente", "zomer", "herfst", "winter")
                       if os.path.exists(P("tuinplan", "images", "tuin-impressie-%s.jpg" % s))]}
for m in re.finditer(r"^- (\S+) \*\*(.+?)\*\* — (.+)$", sectie(T, "## De drie thema's"), re.M):
    info["themas"].append({"id": THEMA[m.group(2)], "naam": m.group(2), "emoji": m.group(1), "beschrijving": m.group(3).strip()})
for kop, tid in (("### 🐝 Bijen-tips", "bijen"), ("### 🐦 Vogel-tips", "vogels"), ("### 🌸 Nieuwe klimmers", "klimmers"), ("### 🪱 Klei — advies", "klei")):
    s = sectie(T, kop, "### ")
    info["tips"].append({"id": tid, "emoji": kop.split()[1], "titel": kop.split(None, 2)[2],
                         "punten": [kaal(l[2:]) for l in s.splitlines() if l.startswith("- ")]})

# ============================================================ MOESTUIN
M = lees("moestuin", "moestuinplan.md")
mplek = []
for r in tabel(sectie(M, "### Bakken", "### ")):
    m = re.match(r"Bak (\d+)\s*\((.*)\)", kaal(r[0]))
    nr, oms = m.group(1), m.group(2)
    naam = "Bak %s" % nr + (" · kruidenbak" if "kruidenbak" in oms else " · bloemenbak" if "bloemenbak" in oms else "")
    mplek.append({"id": "bak-" + nr, "naam": naam, "type": "bak", "beschrijving": oms[0].upper() + oms[1:], "maat": kaal(r[1]),
                  "m2": float(kaal(r[2]).replace("±", "").replace(",", ".")), "zon": kaal(r[3]), "grond": kaal(r[4]), "status": "actief"})
mplek += [
    {"id": "boomgaard", "naam": "Boomgaard", "type": "boomgaard", "beschrijving": "Appelboom, vijg, een jonge fruitboom en een bessenstruik, met grasstrook", "status": "actief"},
    {"id": "fruit", "naam": "Frambozen en rabarber", "type": "fruit", "beschrijving": "Frambozen op een houten rek, rabarber", "status": "actief"},
    {"id": "compost", "naam": "Compost", "type": "algemeen", "beschrijving": "Houten compostbakken achter de vijg, bij het hek", "status": "actief"},
    {"id": "algemeen", "naam": "Algemeen", "type": "algemeen", "beschrijving": "Paden, pergola, kasopzet, regentonnen, handpomp, schuur", "status": "actief"}]
MPK = {p["id"] for p in mplek}

# gewassen
GEWAS_SOORT = {"Groenten": "groente", "Bloemen": "eenjarig", "Kruiden": "kruid", "Fruit": "fruit", "Groenbemester": "groenbemester"}
mplanten, mregels, mbeplanting = [], [], []
VAST = {"citroenmelisse", "rozemarijn", "lavendel", "tijm", "munt", "aardbei", "appelboom", "vijg", "jonge-fruitboom",
        "bessenstruik", "framboos", "rabarber"}


def mregel(pid, actie, detail, txt, soort="taak"):
    ms, deel = periode(txt)
    if not ms:
        return
    r = {"id": "%s.%s" % (pid, slug(detail)), "plant": pid, "actie": actie, "detail": detail, "soort": soort,
         "vensters": vensters(ms), "herhaling": "jaarlijks", "toelichting": kaal(txt)}
    if deel:
        r["deel"] = deel
    mregels.append(r)


for kop in ("### Groenten", "### Bloemen", "### Kruiden", "### Fruit", "### Groenbemester"):
    s = sectie(M, kop, "### ")
    kopregel = [c.strip() for c in s.splitlines()[[i for i, l in enumerate(s.splitlines()) if l.startswith("|")][0]].strip("|").split("|")]
    for r in tabel(s):
        c = dict(zip(kopregel, r))
        naam = kaal(r[0]).split(" (")[0]
        pid = slug(naam)
        soort = GEWAS_SOORT[kop.split()[1]]
        if naam == "Dahlia":
            soort = "knol"
        p = {"id": pid, "nl": naam, "latijn": kaal(c.get("Latijn", "")), "soort": soort,
             "levensduur": None if pid in VAST else "seizoen", "familie": c.get("Familie"),
             "plantgoed": kaal(c.get("Zaad of plantgoed", "")) or None, "plantafstand": kaal(c.get("Plantafstand", "")) or None,
             "beschrijving": kaal(c.get("Bijzonderheden") or c.get("Verder", "")) or None}
        if "Bloei" in c:
            p["bloei"] = kaal(c["Bloei"])
        mplanten.append({k: v for k, v in p.items() if v not in (None, "", [])})
        if "Binnen zaaien" in c and kaal(c["Binnen zaaien"]) not in ("—", ""):
            mregel(pid, "planten", "Binnen zaaien", c["Binnen zaaien"])
        if "Buiten zaaien of planten" in c:
            mregel(pid, "planten", "Buiten zaaien of planten", c["Buiten zaaien of planten"])
        if "Uitplanten" in c and kaal(c["Uitplanten"]) not in ("—", ""):
            mregel(pid, "planten", "Uitplanten", c["Uitplanten"])
        if "Zaaien" in c:
            mregel(pid, "planten", "Zaaien", c["Zaaien"])
        if "Planten of zaaien" in c:
            mregel(pid, "planten", "Planten of zaaien", c["Planten of zaaien"])
        if "Oogst" in c and kop != "### Kruiden":
            mregel(pid, "oogsten", "Oogsten", c["Oogst"])
        # snoei van fruit en kruiden staat in §4 (terugkerende taken); niet dubbel opnemen

MP = {p["id"]: p for p in mplanten}
# planten/zaaien van vaste planten alleen bij aanplant
for r in mregels:
    if r["actie"] == "planten" and r["plant"] in VAST:
        r["herhaling"] = "tot_geplant"

# teeltplan 2027 (en wisselteelt: bak 1↔4 en 2↔3 ruilen elk jaar)
ALIAS = {"suikermais": ["suikermais", "mais"], "pompoen": ["pompoen"], "courgette": ["courgette"], "snackkomkommer": ["snackkomkommer"],
         "wortel": ["wortel"], "lente-ui": ["lente-ui"], "rode-biet": ["rode biet", "biet"], "zoete-aardappel": ["zoete aardappel"],
         "knoflook": ["knoflook"], "radijs-voorteelt": ["radijs"], "pluksla-voorteelt": ["pluksla"], "spinazie-voorteelt": ["spinazie"],
         "dahlia": ["dahlia"], "goudsbloem": ["goudsbloem"], "oost-indische-kers": ["oost-indische kers"], "afrikaantje": ["afrikaantje"],
         "ridderspoor-eenjarig": ["ridderspoor"], "cosmos": ["cosmos"], "zinnia": ["zinnia"], "aardbei": ["aardbei"]}
for pid in list(ALIAS):
    if pid not in MP:
        alt = [k for k in MP if k.startswith(pid.split("-")[0])]
        if alt:
            ALIAS[alt[0]] = ALIAS.pop(pid)
s2027 = sectie(M, "### 2027", "### ")
PAAR = {"bak-1": "bak-4", "bak-4": "bak-1", "bak-2": "bak-3", "bak-3": "bak-2"}
for r in tabel(s2027):
    nr = re.match(r"(\d+)", r[0]).group(1)
    tekst = " ".join(r[1:4]).lower()
    for pid, namen in ALIAS.items():
        if pid in MP and any(n in tekst for n in namen) and not (pid == "suikermais" and "zoete" in tekst and "mais" not in tekst):
            if pid in ("knoflook", "aardbei") and nr != "8":
                continue
            b = {"plant": pid, "plek": "bak-" + nr, "status": "gepland", "vanaf": 2027}
            if "bak-" + nr in PAAR:
                b["jaren"] = "oneven"
                mbeplanting.append(b)
                mbeplanting.append(dict(b, plek=PAAR["bak-" + nr], jaren="even"))
            else:
                mbeplanting.append(b)
for p in mplanten:
    if p["soort"] == "kruid":
        mbeplanting.append({"plant": p["id"], "plek": "bak-9", "status": "gepland", "vanaf": 2027})
for pid, plek, st in (("appelboom", "boomgaard", "geplant"), ("vijg", "boomgaard", "geplant"), ("jonge-fruitboom", "boomgaard", "geplant"),
                      ("bessenstruik", "boomgaard", "geplant"), ("framboos", "fruit", "geplant"), ("rabarber", "fruit", "geplant")):
    if pid in MP:
        mbeplanting.append({"plant": pid, "plek": plek, "status": st})
for p in mplanten:
    if not any(b["plant"] == p["id"] for b in mbeplanting) and p["soort"] != "groenbemester" and not p["id"].startswith("veldsla"):
        AANVULLEN.append("moestuin: %s staat in geen enkele bak" % p["nl"])

# terugkerende taken §4
SOORT_ACTIE = {"voorbereiden": "onderhoud", "snoeien": "snoeien", "verplaatsen": "onderhoud", "bemesten": "mest", "aanvullen": "mulchen",
               "compost": "mest", "afdekken (gaas)": "onderhoud", "afdekken (net)": "onderhoud", "afdekken": "mulchen", "maaien": "onderhoud",
               "mulchen": "mulchen", "uitgebloeid_verwijderen": "snoeien", "opbinden": "onderhoud", "water_geven": "water",
               "snoeien, bemesten": "snoeien", "zaaien": "planten", "rooien": "oogsten", "planten": "planten", "winterklaar": "onderhoud",
               "controleren": "onderhoud"}


def waar_naar(w, taak):
    w2 = w.lower()
    if w2.startswith("alle") or w2 in ("vrijgekomen bakken", "wisselend"):
        return {"plekken": ["algemeen"]}  # één taak voor alle bakken, niet tien
    if w2.startswith("bak "):
        m = re.findall(r"\d+", w2)
        if "–" in w2 and len(m) == 2:
            return {"plekken": ["bak-%d" % i for i in range(int(m[0]), int(m[1]) + 1)]}
        return {"plekken": ["bak-" + n for n in m]}
    for k, v in (("boomgaard", "boomgaard"), ("frambozenrek", "fruit"), ("rabarber", "fruit"), ("compost", "compost")):
        if w2 == k:
            return {"plekken": [v]}
    for k, pid in (("wortelbak", "wortel"), ("aardbeibak", "aardbei"), ("dahliabak", "dahlia"), ("dahlia's", "dahlia"), ("knoflookbak", "knoflook"),
                   ("biet en komkommer", "rode-biet")):
        if k in w2:
            return {"plant": pid}
    if "pompoen" in w2:
        return {"planten": ["pompoen", "courgette", "snackkomkommer", "suikermais", "dahlia"]}
    if "kasopzet" in w2 and "bak met" in w2:
        return {"plekken": ["bak-6"]}
    return {"plekken": ["algemeen"]}


for i, r in enumerate(tabel(sectie(M, "## 4. Terugkerende taken"))):
    maand, taak, waar, soort, herh, status = [kaal(c) for c in r[:6]]
    ms, deel = periode(maand.replace(" en ", "–") if " en " not in maand else maand.split(" en ")[0])
    vs = vensters(ms) if ms else []
    if " en " in maand:
        vs = [vensters(periode(x)[0])[0] for x in maand.split(" en ")]
    actie = SOORT_ACTIE.get(soort, "onderhoud")
    doel = waar_naar(waar, taak)
    basis = {"actie": actie, "detail": taak, "soort": "taak", "vensters": vs, "herhaling": "jaarlijks", "waar": waar}
    if herh == "conditioneel":
        basis["voorwaarde"] = taak
    if deel:
        basis["deel"] = deel
    if "eigen inschatting" in status:
        basis["eigen_inschatting"] = True
    if "planten" in doel:
        for pid in doel["planten"]:
            if pid in MP:
                mregels.append(dict(basis, id="mt.%d.%s" % (i + 1, pid), plant=pid))
    elif "plant" in doel:
        mregels.append(dict(basis, id="mt.%d" % (i + 1), plant=doel["plant"]))
    else:
        mregels.append(dict(basis, id="mt.%d" % (i + 1), plekken=doel["plekken"]))

# eenmalige taken §5
mprojecten = []
for r in tabel(sectie(M, "## 5. Eenmalige taken")):
    per_t, taak, status = kaal(r[0]), kaal(r[1]), kaal(r[2])
    t = per_t.lower().replace("winter 2026–27", "dec 2026–feb 2027").replace("voorjaar 2027", "mrt–mei 2027") \
        .replace("groeiseizoen 2027", "apr–sep 2027").replace(", rond 12.00 uur", "")
    jaren = re.findall(r"20\d\d", t)
    ms = list(re.finditer(MAAND_RE, t))
    e = {"id": "moes." + slug(taak)[:40], "titel": taak, "actie": "planten" if re.search(r"planten|zaaien|overzetten", taak.lower()) else "onderhoud",
         "plekken": ["bak-" + n for n in re.findall(r"bak (\d+)", taak.lower())] or ["algemeen"], "wanneer": per_t,
         "status": {"open": "open", "besloten": "open", "concept": "geparkeerd"}.get(status.split(" ")[0], "open"), "bron": "moestuin/moestuinplan.md §5"}
    if ms and jaren:
        j1 = int(jaren[0]); j2 = int(jaren[-1])
        a, b = ms[0], ms[-1]
        e["periode"] = {"van": "%d-%02d" % (j1, MND[a.group(2)]), "tot": "%d-%02d" % (j2, MND[b.group(2)])}
        if a.group(1):
            e["periode"]["deel"] = DEELW[a.group(1)]
    mprojecten.append(e)

minfo = {"titel": "Moestuin", "ondertitel": kaal(sectie(M, "## 1. Plekken").splitlines()[2])[:160],
         "open_punten": [kaal(l.split(". ", 1)[1]) for l in sectie(M, "## 6. Open punten").splitlines() if re.match(r"\d+\. ", l)]}

# ============================================================ schrijven
STAND = re.search(r"Stand: (\d+ \w+ \d{4})", M)
meta = {"schema_versie": 2, "gebouwd_uit": ["tuinplan/tuinplan.md", "tuinplan/index.html", "moestuin/moestuinplan.md", "overdracht/tuin.md"],
        "script": "scripts/bouw_data.py"}
index = {
    "schema_versie": 2,
    "locaties": [
        {"id": "achtertuin", "naam": "Achtertuin", "map": "achtertuin", "plekwoord": "Zone", "bron": "tuinplan/tuinplan.md", "beslist_in": "project Tuin"},
        {"id": "moestuin", "naam": "Moestuin", "map": "moestuin", "plekwoord": "Bak", "bron": "moestuin/moestuinplan.md", "beslist_in": "project Moestuin"}],
    "acties": [{"id": "snoeien", "label": "Snoeien"}, {"id": "mulchen", "label": "Mulchen"}, {"id": "mest", "label": "Mest geven"},
               {"id": "planten", "label": "Planten & zaaien"}, {"id": "oogsten", "label": "Oogsten & rooien"}, {"id": "water", "label": "Water"},
               {"id": "opruimen", "label": "Opruimen"}, {"id": "onderhoud", "label": "Onderhoud"}],
    "geen_achterstand_voor": VANDAAG[:7],
    "sierwaarde_codes": {"B": "bloei", "L": "blad", "E": "bes of vrucht", "Z": "zaadhoofden", "W": "wintersilhouet", "-": "geen"},
}


def dump(rel, obj):
    pad = P("data", rel)
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    with open(pad, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


dump("index.json", dict(index, meta=meta))
for loc, d in (("achtertuin", {"plekken": plekken, "planten": planten, "beplanting": beplanting, "regels": regels,
                               "projecttaken": projecttaken, "info": info}),
               ("moestuin", {"plekken": mplek, "planten": mplanten, "beplanting": mbeplanting, "regels": mregels,
                             "projecttaken": mprojecten, "info": minfo})):
    for k, v in d.items():
        dump("%s/%s.json" % (loc, k), {k: v})
    if not os.path.exists(P("data", loc, "stand.json")):
        dump("%s/stand.json" % loc, {"items": []})
with open(P("data", "AANVULLEN.md"), "w", encoding="utf-8") as f:
    f.write("# Opgevallen bij het bouwen van data/\n\nGemaakt door `scripts/bouw_data.py`. Lees dit na elke run; meld wat de plannen moeten aanvullen.\n\n")
    f.write("\n".join("- " + a for a in AANVULLEN) + ("\n" if AANVULLEN else "- Niets.\n"))
print("achtertuin: %d plekken, %d planten, %d beplanting, %d regels, %d projecttaken" % (len(plekken), len(planten), len(beplanting), len(regels), len(projecttaken)))
print("moestuin:   %d plekken, %d planten, %d beplanting, %d regels, %d projecttaken" % (len(mplek), len(mplanten), len(mbeplanting), len(mregels), len(mprojecten)))
print("aanvullen:  %d punten" % len(AANVULLEN))
