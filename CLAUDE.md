# Afspraken voor Claude in deze repo

Deze repo is het **gedeelde geheugen** van de tuin: het tuinplan en de plantenlijst per bak. Twee Claude-projecten werken ermee: **Tuin** (tuinontwerp en siertuin) en **Tuinapp** (de takenapp, inclusief de moestuin). **De repo is leidend**: wat hier staat geldt, ook als een projectdocument iets anders zegt.

## Taal en werkwijze

- Schrijf en antwoord in het Nederlands.
- Benoem beslissingen eerst en leg ze pas vast als de gebruiker daarom vraagt. Een besluit uit een gesprek is "voorgesteld" tot het is bevestigd.
- Gebruik Nederlandse (of Vlaamse) websites als bron voor plantinformatie; vermeld het als alleen een anderstalige bron beschikbaar is.
- De repo is **openbaar** en wordt via GitHub Pages gepubliceerd: zet er geen persoonsgegevens, adressen, contactgegevens of details van de thuisinfrastructuur in.

## Wat staat waar

| Pad | Inhoud | Eigenaar |
|---|---|---|
| `tuinplan/tuinplan.md` | Het tuinplan: zones, planten, grond, kalenders, onderhoud, planning, besluiten | project Tuin |
| `tuinplan/index.html` + `tuinplan/images/` | Interactieve weergave van het tuinplan (GitHub Pages: `/tuinplan/`) | project Tuin |
| `index.html` (hoofdmap) | Startpagina en straks de app (GitHub Pages) | project Tuinapp |
| `docs/projectcontext.md` | Context, besluiten en open punten van het tuinontwerp | project Tuin |
| `data/*.json` | Gestructureerde siertuindata (`bron: "tuinplan"`): bakken, planten, bollen, onderhoudsregels, algemene regels, eenmalige taken | project Tuin |
| `data/moestuin/` | Moestuindata (`bron: "moestuin"`): bakken, gewassen, teeltplan, onderhoudsregels | project Tuinapp |
| `docs/handoff-tuinapp.md` | Overdracht en datamodel voor de app | project Tuinapp |

## Regels voor wijzigingen

1. **Siertuin:** wijzig `tuinplan/tuinplan.md`, de HTML en records met `bron: "tuinplan"` alleen op expliciet verzoek, en alleen vanuit het project Tuin (of als de gebruiker daar zelf om vraagt).
2. **Samen bijwerken:** raakt een wijziging planten, bakken of onderhoud, werk dan `tuinplan/tuinplan.md` én `data/` bij **in dezelfde commit**. Werk `meta.json` (`stand`) bij.
3. **De HTML** wordt alleen bijgewerkt als de gebruiker daar expliciet om vraagt. Houd hem dan consistent met `tuinplan/tuinplan.md`, maar zet er alleen plant- en plantonderhoudsinformatie in.
4. **Niet verwijderen:** een plant of regel die vervalt krijgt `"status": "vervallen"`, zodat verwijzingen en het logboek van de app blijven kloppen. Afgevallen soorten staan in `tuinplan/tuinplan.md` op de reservelijst.
5. **Moestuin en app:** het project Tuinapp schrijft in `data/moestuin/`, `docs/handoff-tuinapp.md` en de app-bestanden (zoals `index.html` in de hoofdmap).
6. **Controle:** draai `python3 scripts/check_data.py` vóór elke commit. Het script controleert verwijzingen, maanden en acties, en of de plantenlijst in `data/planten.json` overeenkomt met de tabel *Alle planten* in `tuinplan/tuinplan.md`.
7. **Commits** gaan direct op `main`, klein en met een duidelijke Nederlandse omschrijving (bijvoorbeeld `Zone S: bosaster-cultivar gekozen`).

## Datamodel (kort)

- Maanden: `jan feb mrt apr mei jun jul aug sep okt nov dec`.
- Acties: `snoeien`, `planten_zaaien`, `delen_verplanten`, `uitgebloeid_verwijderen`, `mulchen`, `meten`, `water_geven`, `niet_doen`, `aanvullen`; voor de moestuin ook `zaaien`, `uitplanten`, `oogsten`, `bemesten`, `afdekken`.
- Herhaling: `jaarlijks`, `eenmalig_aanplant` (vervalt zodra de plant `status: "geplant"` heeft), `indien_nodig`, `conditioneel`.
- Plantstatus: `gepland`, `geplant`, `vervallen`.
- Volledige beschrijving: `docs/handoff-tuinapp.md`.
