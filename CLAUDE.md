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

## Bron van waarheid

**Alle gegevens van de app staan in de Google Sheet "Tuinapp"** (id `1gkO__1D6oWzxG2rEm-hj0PXKLjp2ZVHNyVd9Rf0jJIg`). Uitleg en afspraken staan in het tabblad *Leesmij*.

- Wie kijkt: iedereen met de link mag alleen lezen. Bewerken mogen alleen de eigenaars.
- Wijzigen: de app leest de Sheet rechtstreeks. Een nieuwe plant, plek, taak of andere naam is dus een wijziging in de Sheet, niet in de app.
- Bewerken door Claude: via de Google Sheets-koppeling. Lees alleen het tabblad en bereik dat nodig is. Controleer daarna het tabblad *Controle* (totaal 0).
- De plannen `tuinplan/tuinplan.md` en `moestuin/moestuinplan.md` blijven de uitleg en het ontwerp. Een besluit dat planten, plekken of taken raakt, gaat in dezelfde werksessie in de Sheet.
- `data/` is de stand van 24 november 2026 (schema 2) en wordt niet meer bijgewerkt. `scripts/bouw_data.py` is niet meer nodig.
- `overdracht/wijzigingen.md` is niet meer nodig.

## Wat staat waar

| Pad | Inhoud | Wie schrijft |
|---|---|---|
| `tuinplan/tuinplan.md` | Plan van de achtertuin (bron van waarheid) | project Tuin |
| `tuinplan/index.html`, `tuinplan/images/` | Interactieve weergave van het tuinplan, foto's | project Tuin |
| `moestuin/moestuinplan.md` | Plan van de moestuin (bron van waarheid) | project Moestuin |
| `overdracht/tuin.md`, `overdracht/moestuin.md` | Overdracht van 24 november 2026 | Tuin en Moestuin |
| `docs/projectcontext.md` | Context en besluiten van het tuinontwerp | project Tuin |
| Google Sheet "Tuinapp" | Alle gegevens van de app | zie Regels 2 |
| `data/` | Bevroren stand van 24 november 2026 (schema 2) | niemand meer |
| `index.html` (hoofdmap), `scripts/`, `docs/datamodel.md`, `CLAUDE.md`, `README.md` | App, scripts en afspraken | project Tuin app |

## Regels

1. **Plannen:** alleen het project Tuin wijzigt `tuinplan/`; alleen het project Moestuin wijzigt `moestuin/`.
2. **Sheet, per locatie:**
   - het project Tuin wijzigt de rijen met locatie `achtertuin`;
   - het project Moestuin wijzigt de rijen met locatie `moestuin`;
   - het project Tuin app wijzigt de tabbladen *Locaties*, *Acties*, *Instellingen*, *Controle* en *Leesmij*.
   - *Stand* en *Voortgang* schrijft de app. Kas en zijn vrouw mogen alles wijzigen.
3. **Werkelijke stand:** lees het tabblad *Stand* vóór een beslissing over de beplanting. Bij twijfel wint voor waar een plant nu staat de stand, en voor wat de bedoeling is het plan.
4. **Niet verwijderen en id's niet wijzigen:** zet `status` op `vervallen`. Zo blijven de voortgang en de stand kloppen.
5. **Controle:** na elke wijziging in de Sheet moet het tabblad *Controle* op 0 staan.
6. **Commits** gaan direct op `main`, klein en met een duidelijke Nederlandse omschrijving (bijvoorbeeld `Zone S: bosaster-cultivar gekozen`).
