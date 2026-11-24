# Afspraken voor Claude in deze repo

Deze repo bevat de Tuinapp en de plannen van twee tuinen: de achtertuin (`tuinplan/`) en de moestuin (`moestuin/`). Er werken drie Claude-projecten mee:

- **Tuin app** bouwt en onderhoudt de app en de afgeleide data.
- **Tuin** beslist over de achtertuin.
- **Moestuin** beslist over de moestuin.

## Taal en werkwijze

- Schrijf en antwoord in het Nederlands.
- Benoem beslissingen eerst. Leg ze pas vast als de gebruiker ze bevestigt. Een besluit uit een gesprek is "voorgesteld" tot het is bevestigd.
- Gebruik Nederlandse of Vlaamse websites als bron voor plantinformatie. Vermeld het als alleen een anderstalige bron beschikbaar is.
- De repo is **openbaar** en wordt gepubliceerd via GitHub Pages. Zet er geen namen, adressen, contactgegevens of details van de thuisinfrastructuur in.

## Wat staat waar

| Pad | Inhoud | Wie schrijft |
|---|---|---|
| `tuinplan/tuinplan.md` | Plan van de achtertuin (bron van waarheid) | project Tuin |
| `tuinplan/index.html`, `tuinplan/images/` | Interactieve weergave van het tuinplan, foto's | project Tuin |
| `moestuin/moestuinplan.md` | Plan van de moestuin (bron van waarheid) | project Moestuin |
| `overdracht/wijzigingen.md` | Eén regel per wijziging in een plan die de app raakt | Tuin en Moestuin (toevoegen); Tuin app (afvinken als verwerkt) |
| `overdracht/tuin.md`, `overdracht/moestuin.md` | Overdracht van 24 november 2026 | Tuin en Moestuin |
| `docs/projectcontext.md` | Context en besluiten van het tuinontwerp | project Tuin |
| `data/` | App-data, gebouwd uit de plannen (schema 2, zie `docs/datamodel.md`) | project Tuin app |
| `data/<locatie>/stand.json`, `data/voortgang/` | Werkelijke stand en afvinken | de app zelf |
| `index.html` (hoofdmap), `scripts/`, `docs/datamodel.md`, `CLAUDE.md`, `README.md` | App, scripts en afspraken | project Tuin app |

## Regels

1. **Plannen:** alleen het project Tuin wijzigt `tuinplan/`; alleen het project Moestuin wijzigt `moestuin/`. Een wijziging die planten, zones, bakken, onderhoud, taken of planning raakt, krijgt in dezelfde commit een regel in `overdracht/wijzigingen.md`: datum, wat er veranderd is en de sectie.
2. **Data:** alleen het project Tuin app schrijft in `data/`, en altijd via `python3 -I scripts/bouw_data.py`. Pas de JSON niet met de hand aan, behalve `stand.json` en `voortgang/` (die schrijft de app).
3. **Verwerken:** het project Tuin app draait na een nieuwe regel in `overdracht/wijzigingen.md` het bouwscript. Daarna leest het `data/AANVULLEN.md`, controleert de data en zet achter de regel ` (verwerkt <datum>)`.
4. **Werkelijke stand:** lees `data/<locatie>/stand.json` vóór een beslissing over de beplanting. Bij twijfel wint voor waar een plant nu staat de stand, en voor wat de bedoeling is het plan.
5. **Niet verwijderen:** een plant, plek of regel die vervalt, krijgt `"status": "vervallen"` in het plan of in de data. Zo blijven de voortgang en de stand kloppen.
6. **Controle:** draai `python3 -I scripts/check_data.py` vóór elke commit die `data/` raakt.
7. **Commits** gaan direct op `main`, klein en met een duidelijke Nederlandse omschrijving (bijvoorbeeld `Zone S: bosaster-cultivar gekozen`).
