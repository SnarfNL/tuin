# Tuin

Plannen en takenapp voor twee tuinen op klei: een natuurvriendelijke achtertuin met vijf zones (A, B, C, D, S) en een tuinkas, en een moestuin op een volkstuin met tien bakken, een boomgaard en fruit.

- `index.html`: de app (GitHub Pages); leest en schrijft de Google Sheet "Tuinapp" via `appsscript/Code.gs`
- `tuinplan/`: het plan van de achtertuin (`tuinplan.md`), de interactieve weergave en de foto's
- `moestuin/`: het plan van de moestuin (`moestuinplan.md`)
- `data/`: de gegevens van de app, gebouwd uit de plannen; zie `docs/datamodel.md`
- `overdracht/`: wijzigingen in de plannen die de app raken
- `scripts/bouw_data.py` bouwt `data/`; `scripts/check_data.py` controleert de data

Afspraken over wie wat wijzigt staan in `CLAUDE.md`.

## Apps Script installeren (eenmalig)

1. Open de Sheet "Tuinapp" > *Uitbreidingen* > *Apps Script*. Vervang de inhoud van `Code.gs` door `appsscript/Code.gs` uit deze repo en sla op.
2. *Projectinstellingen* (tandwiel) > *Scriptproperty's* > property `SLEUTEL` met een zelfgekozen wachtwoord.
3. *Implementeren* > *Nieuwe implementatie* > type *Web-app*. Uitvoeren als: *Ik*; Wie heeft toegang: *Iedereen*. Geef toestemming.
4. Kopieer de URL (eindigt op `/exec`). Zet hem in `index.html` bij `API_STANDAARD`, of vul hem in de app in bij *Meer* > *Instellingen*, samen met de sleutel.

Lezen kan zonder sleutel (de Sheet is toch openbaar leesbaar). Afvinken en de stand bijwerken vragen de sleutel; die staat alleen op je toestel. Na een wijziging in `Code.gs`: *Implementeren* > *Implementaties beheren* > bewerken > *Nieuwe versie*, zodat de URL gelijk blijft.
