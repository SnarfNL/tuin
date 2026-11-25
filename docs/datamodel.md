# Datamodel Tuinapp (schema 2)

De app is dynamisch: er staan geen planten, plekken of taken in de code. Alles komt uit `data/`. Die map wordt **gebouwd** uit de leesbare plannen met `python3 -I scripts/bouw_data.py`, en gecontroleerd met `python3 -I scripts/check_data.py`.

## Bronnen en eigenaars

| Pad | Wat | Wie beslist / schrijft |
|---|---|---|
| `tuinplan/tuinplan.md` | Achtertuin: zones, planten, kalenders, onderhoud, planning | project Tuin |
| `tuinplan/index.html`, `tuinplan/images/` | Interactieve weergave; de app haalt hier emoji, kleur en foto-sleutels uit | project Tuin |
| `moestuin/moestuinplan.md` | Moestuin: bakken, teeltplan, gewassen, taken | project Moestuin |
| `overdracht/wijzigingen.md` | Eén regel per wijziging die de app raakt | Tuin en Moestuin |
| `overdracht/tuin.md`, `overdracht/moestuin.md` | Overdracht van 24 november 2026 (open taken met datum) | Tuin en Moestuin |
| `data/` (behalve `stand.json` en `voortgang/`), `scripts/`, `docs/`, `index.html`, `CLAUDE.md`, `README.md` | App en afgeleide data | project Tuin app |
| `data/<locatie>/stand.json`, `data/voortgang/<jaar>.json` | Werkelijke stand en afvinken | de app zelf (GitHub-API) |

- **Bij twijfel:** voor wat de bedoeling is, wint het plan. Voor waar een plant nu staat, wint `stand.json`.
- **Verwijderen doe je niet.** Wat vervalt, krijgt `status: "vervallen"`.
- **Geen namen:** de repo is openbaar. Afvinken en de werkelijke stand bewaren alleen de datum.

## data/index.json

- `locaties[]`: `id`, `naam`, `map`, `plekwoord` ("Zone" of "Bak"), `bron`, `beslist_in`
- `acties[]`: de 8 filters: `snoeien`, `mulchen`, `mest`, `planten` (Planten & zaaien), `oogsten` (Oogsten & rooien), `water`, `opruimen`, `onderhoud`
- `sierwaarde_codes`: B bloei, L blad, E bes of vrucht, Z zaadhoofden, W wintersilhouet, - geen
- `geen_achterstand_voor` ("2026-11"): taken uit maanden vóór de start van de app tellen niet als "nog open"

## Per locatie: data/<locatie>/

**plekken.json**
- Altijd: `id`, `naam`, `type` (`zone`, `bak`, `kas`, `boomgaard`, `fruit`, `algemeen`) en `status`.
- Optioneel: `zon`, `zonklasse` (`vol`/`half`/`schaduw`), `thema`, `m2`, `maat`, `beschrijving` en `foto`.
- Grond: `grond` is tekst, of een object met `plan` en `uitgevoerd`.
- Alleen bij de achtertuin: `plantplek[]` (de punten uit *Plantplek en mest*), `mulch`, `water` {`behoefte`, `per_week`, `opmerking`}.

**planten.json**
- Altijd: `id` (blijft gelijk, want de voortgang verwijst ernaar), `nl`, `latijn` en `soort`.
- `levensduur`:
  - `zaaien`: eenjarig of tweejarig, elk jaar zaaien
  - `kort`: kortlevend
  - `seizoen`: moestuingewas; alle regels gelden elk jaar, ook als het gewas nog "gepland" staat
- Achtertuin:
  - scores: `bijen` en `vogels` (0–5), `score_eigen[]` (welke score een eigen inschatting is), `bron_scores`
  - verder: `beschrijving`, `link` {`label`, `url`}, `emoji`, `kleur[2]`, `fotos[]`, `onderhoud` (de toelichting uit de onderhoudskalender)
  - sierwaarde: `sierwaarde` (12 tekens, jan–dec) en `bron_bloei`
  - alleen bomen: `vorm`, `hoogte`, `plantmoment`, `seizoenstekst`, `grondwens`, `tip`
- Moestuin: `familie`, `plantgoed`, `plantafstand`, `bloei`, `beschrijving`.

**beplanting.json**
- `plant`, `plek`, `status` (`gepland`, `geplant` of `vervallen`), optioneel `aantal`.
- Moestuin: `vanaf` (jaar) en `jaren` (`oneven` of `even`) voor de wisselteelt. Bak 1↔4 en 2↔3 ruilen elk jaar; 2027 is oneven.

**regels.json**
- `id`, `actie` en `detail`.
- `plant`: de regel geldt in alle plekken waar die plant dat jaar staat. Of `plekken[]`: dan geldt hij op die plekken.
- `soort`: `taak`, `suggestie` (alleen tonen) of `waarschuwing` (niet doen).
- `vensters`: een lijst van maandreeksen. `[[3],[7]]` is twee momenten; `[[12,1]]` is één venster over de jaarwisseling.
- `keuze: true`: één van de vensters is genoeg.
- `herhaling`: `jaarlijks`, of `tot_geplant` (alleen zolang de plant gepland staat).
- Optioneel:
  - timing: `deel` {`start`, `eind`: `begin`/`midden`/`eind`} en `uiterlijk` {`maand`, `deel`}
  - voorwaarde en meting: `voorwaarde`, `meting` {`eenheid`, `streef`}
  - beschrijving: `toelichting`, `waar` (tekst uit het plan, bijvoorbeeld "Alle lege bakken")
  - herkomst: `bron` (de sectie in het plan, bij regels die niet uit een tabel komen) en `eigen_inschatting`
- Onderhoud van een vaste plant verschijnt pas als die plant `geplant` is; aanplanttaken alleen zolang hij gepland is.

**projecttaken.json**
- `id`, `titel`, `actie`, `plekken[]`, `wanneer` (tekst), `status` (`open`, `geparkeerd` of `vervallen`), `bron`.
- `periode` {`van`, `tot` als "2026-11", optioneel `deel` en `uiterlijk`}. Zonder periode valt de taak onder "Zonder datum".
- Optioneel `afhankelijk_van`.

**info.json**
- Achtertuin: `titel`, `ondertitel`, `themas[]`, `tips[]` en `impressies[]` (de vier seizoensfoto's van de hele tuin).
- Moestuin: `titel`, `ondertitel` en `open_punten[]`.

**stand.json** (de app schrijft dit)

```json
{ "items": [
  { "key": "achtertuin|geranium|A", "plant": "geranium", "plek": "B", "status": "geplant", "aantal": "", "notitie": "", "datum": "2026-11-24" },
  { "key": "achtertuin|vrij-zaailing|+1764000000", "plant": "vrij-zaailing", "naam": "Zaailing", "plek": "B", "status": "geplant", "nieuw": true, "datum": "2026-11-24" }
]}
```

- `key`: `<locatie>|<plant>|<plek uit het plan>`, of `…|+<id>` voor een plant die er extra staat.
- `status`: `gepland`, `geplant` of `weg`.
- `viaRegel`: het record is ontstaan door een aanplanttaak af te vinken. Wordt die taak weer uitgevinkt, dan verdwijnt het record.
- **Terug naar het plan** verwijdert het record.
- **Effectieve beplanting** = het plan met de stand eroverheen. Taken, plekken en de kalender gebruiken die; wat `weg` is telt niet mee.

## data/voortgang/<jaar>.json (de app schrijft dit)

`{ "jaar": 2026, "items": [ { "taak": "r:astrantia.snoeien:A:3", "datum": "2026-03-14", "notitie": "", "meting": null } ] }`

- **Taaksleutel:** `r:<regel>:<plek>:<startmaand van het venster>`, of `p:<projecttaak>`.
- **Venster over de jaarwisseling:** dec–jan telt in het jaar waarin het venster begint.
- **Afvinken** is een commit via de contents-API, met de `sha` van het bestand. Bij een conflict leest de app het bestand opnieuw en probeert het nog een keer.
- **Token:** fine-grained, per persoon, met alleen schrijfrechten op deze repo.

## Bouwen

`scripts/bouw_data.py` leest de tabellen uit de plannen:
- **Achtertuin** (`tuinplan.md`): *Alle planten*, *Jaarkalender*, *Onderhoudskalender*, *Bollen per zone*, de zones, *Bomen*, *Water geven* en *Mulchen*.
- **Moestuin** (`moestuinplan.md`): §1 tot en met §6.

De regels van de achtertuin die niet in een tabel staan, staan in het script (`ALG_ACHTERTUIN`), met de sectie als `bron`. Wat het script mist of niet kan plaatsen, schrijft het in `data/AANVULLEN.md`.

## Aanvullingen in de Sheet (25 november 2026)

- *Regels*: kolom `status`. Leeg is actief; `vervallen` verbergt de regel in de app.
- *Projecttaken*: kolommen `plant` (optioneel, id uit *Planten*) en `toelichting`.
- De app voegt taken toe en bewerkt ze via het Apps Script (`taak_zet`): eenmalig in *Projecttaken*, elk jaar in *Regels*. Nieuwe id's beginnen met `app.`. Bewerken van een regel geldt voor alle jaren; verwijderen zet `status` op `vervallen`.
