# Datamodel Tuinapp

Bron van waarheid: de Google Sheet "Tuinapp". De app (`index.html`) leest en schrijft de Sheet via het Apps Script in `appsscript/Code.gs`. Er staan geen planten, plekken of taken in de code. Werkwijze en afspraken: tabblad *Leesmij* en `CLAUDE.md`.

`data/` is de bevroren stand van 24 november 2026 (schema 2, JSON). De app gebruikt die map niet meer.

## Algemeen

- **Eén rij per record.** De meeste tabbladen beginnen met `locatie` (`achtertuin` of `moestuin`) en `id`.
- **Lijsten** in een cel scheid je met komma's (`A, B, S`). Uitzonderingen: `Fotos.urls` (spaties) en `Plekken.plantplek_en_mest` (` • `).
- **Maanden** schrijf je als tekst: `feb`, `mrt-apr`, `mrt, sep`, `dec-jan`. Elk deel is één venster.
- **Ja/nee**-velden: `ja` of leeg.
- **Verwijderen doe je niet**, en id's veranderen niet. Wat vervalt, krijgt `status` = `vervallen`. Leeg is actief.
- **Een plant uit een andere locatie** gebruik je als `locatie:id` (bijvoorbeeld `moestuin:tomaat` in de tuinkas).
- **Geen namen:** afvinken en stand bewaren alleen een datum.
- **Controle:** het tabblad *Controle* staat na elke wijziging op 0.

## Vaste tabbladen (project Tuin app)

- **Locaties:** `id`, `naam`, `plekwoord` ("Zone" of "Bak"), `beslist_in`
- **Acties:** de filters, met `id`, `label`, `kleur_achtergrond` en `kleur_tekst`. Ids: `snoeien`, `mulchen`, `mest`, `planten`, `oogsten`, `water`, `opruimen`, `onderhoud`.
- **Instellingen:** `sleutel`, `waarde`, `uitleg`
  - `geen_achterstand_voor` (jjjj-mm): taken van vóór deze maand tellen niet als nog open
  - `achterstand_maanden`: hoeveel maanden terug de app open taken toont
  - `sierwaarde_codes`: B bloei, L blad, E bes of vrucht, Z zaadhoofden, W wintersilhouet, - geen

## Plan (projecten Tuin en Moestuin, per locatie)

**Plekken**
- `id`, `naam`, `type` (`zone`, `bak`, `kas`, `boomgaard`, `fruit`, `algemeen`)
- Licht: `zon` (tekst) en `zonklasse` (`vol`, `half` of `schaduw`)
- Overig: `thema`, `m2`, `maat`, `grond`, `grond_uitgevoerd`, `mulch`, `water_per_week`, `plantplek_en_mest`, `beschrijving`, `foto` en `status`

**Planten**
- Altijd: `id`, `nl`, `latijn`, `soort`
- `soort`: een waarde uit `Instellingen.soorten_sier` of `soorten_eetbaar` (bijv. `vaste plant`, `kruid`, `kool`); de app filtert en groepeert hierop (Sier, Eetbaar)
- `levensduur`:
  - `zaaien`: eenjarig of tweejarig, elk jaar zaaien
  - `kort`: kortlevend
  - `seizoen`: moestuingewas; alle regels gelden elk jaar, ook als het op Plan staat
- Achtertuin:
  - `bijen` en `vogels` (0–5), `score_eigen`, `bron_scores`
  - tekst en link: `beschrijving`, `link_label`, `link_url`
  - bloei: `sierwaarde` (12 tekens, jan–dec) en `bron_bloei`
  - `onderhoud`
- Alle planten: `hoogte` (bijv. `60–90 cm`) en `plantafstand` (bijv. `40 cm · 7 per m²`), voor het uitzetten bij het planten
- Moestuin: `familie`, `plantgoed`, `bloei`
- Bomen: `vorm`, `plantmoment`, `grondwens`, `tip`, en per seizoen `lente`, `zomer`, `herfst` en `winter`
- Weergave: `emoji`, `kleur` (twee hex-waarden), `fotos`, `status`

**Beplanting**
- `plant`, `plek`, `status` en `aantal`. Een plant in twee plekken staat er twee keer in.
- `status`:

  | Waarde | Label in de app |
  |---|---|
  | `gepland` | Plan |
  | `geplant` | In de grond |
  | `vervallen` | – |

- Moestuin: `vanaf` (jaar) en `jaren` (`oneven` of `even`) voor de wisselteelt. Bak 1↔4 en 2↔3 ruilen elk jaar; 2027 is oneven.

**Regels** (terugkerende taken)
- `id`, `actie`, `detail`
- Waar: `plant` (de regel geldt op alle plekken waar die plant staat) en/of `plekken`
- `soort`: `taak`, `suggestie` (alleen tonen) of `waarschuwing` (niet doen)
- `maanden`: de vensters. `keuze` = `ja`: één van de vensters is genoeg.
- `herhaling`:
  - `jaarlijks`: de regel geldt pas als de plant In de grond staat
  - `tot_geplant`: de regel geldt alleen zolang de plant op Plan staat
- Timing: `deel_start` en `deel_eind` (`begin`, `midden` of `eind`), `uiterlijk`
- Overig: `voorwaarde`, `meting`, `toelichting`, `waar`, `bron` en `status`

**Projecttaken** (eenmalige taken)
- `id`, `titel`, `actie`, `plekken`, `plant`, `toelichting`
- Planning: `wanneer` (tekst uit het plan), `van` en `tot` (jjjj-mm), `deel` en `uiterlijk`. Zonder `van` staat de taak onder "Zonder datum".
- `status`: `open`, `geparkeerd` of `vervallen`
- `afhankelijk_van` en `bron`

**Info**
- `soort`, `id`, `titel`, `tekst`, `extra`: titel, thema's, tips en impressies (achtertuin) of open punten (moestuin).

## Wat de app schrijft

**Stand** (de werkelijke stand, los van het plan)
- `key`: `<locatie>|<plant>|<plek uit het plan>`, of `<locatie>|<plant>|+<id>` voor een plant die er extra staat (`nieuw` = `ja`). Een plant die niet in het plan staat, krijgt een id `vrij-…` en een `naam`.
- `plek`, `status`, `aantal`, `notitie`, `datum`
- `status`:

  | Waarde | Label in de app |
  |---|---|
  | `gepland` | Plan |
  | `geplant` | In de grond |
  | `weg` | Weg |

- `via_regel`: het record is ontstaan door een aanplanttaak (`tot_geplant`) af te vinken. Vink je die taak uit, dan verdwijnt het record.
- **Geen dubbelen:** voeg je een plant toe (of verplaats je hem) naar een plek waar het plan die plant dat jaar al heeft, dan werkt de app de planregel bij; een eigen regel gaat naar `weg`. Bestaande dubbelen toont de app als één regel. Een eigen regel met `weg` verbergt niets uit het plan. Controle: *Stand: nieuw dubbel met Beplanting*.
- **Effectieve beplanting** is het plan met de stand eroverheen. Taken, plekken en de kalender gebruiken die. Wat `weg` is, telt niet mee.
- **Afwijking** is een andere plek dan in het plan, `weg`, een ander aantal of een plant die niet in het plan staat.
- **Terug naar het plan** verwijdert het record.
- **Bij twijfel:** voor waar een plant nu staat, wint de stand. Voor wat de bedoeling is, wint het plan.

**Voortgang**
- `jaar`, `taak`, `datum`, `notitie`, `meting`
- Taaksleutel: `r:<regel>:<plek>:<startmaand van het venster>` of `p:<projecttaak>`
- Een venster over de jaarwisseling (dec–jan) telt in het jaar waarin het begint.

**Fotos**
- `key`, `soort` (plant of plek), `locatie`, `id`, `urls`, `datum`
- Een rij hier gaat voor de `fotos` of `foto` uit het plan.

## Taaklogica in de app

- **Maandoverzicht:**
  - alle `taak`-regels waarvan de maand in een venster valt, per plek
  - plus de projecttaken waarvan de periode die maand raakt
  - een taak uit een eerder venster die nog niet is afgevinkt, staat onder "Nog open" (zie Instellingen)
- **Suggesties** staan in een aparte, ingeklapte groep.
- **Waarschuwingen** staan bij de plek en de maand.
- **Afvinken van een aanplanttaak** (`tot_geplant`) zet de plant in de stand op In de grond, met `via_regel`. Daarna verschijnt het onderhoud.

## Apps Script

- `doGet` levert de leesbare tabbladen (optioneel alleen `?tabs=A,B`).
- `doPost` vraagt de sleutel uit de scripteigenschap `SLEUTEL` en werkt met een lock. Operaties:
  - `voortgang_aan`, `voortgang_uit`
  - `stand_zet`, `stand_weg`, `stand_weg_via`
  - `foto_zet`
  - `taak_zet` en `rij_zet`: alleen op Regels, Projecttaken, Plekken en Planten. Locatie en id veranderen niet.
- Nieuw door de app:
  - taken: id begint met `app.`
  - plekken en planten: id is de naam in kleine letters met streepjes
  - bewerken stuurt alleen de gewijzigde velden
