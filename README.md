# Tuin

Plannen en takenapp voor twee tuinen op klei: een natuurvriendelijke achtertuin met vijf zones (A, B, C, D, S) en een tuinkas, en een moestuin op een volkstuin met tien bakken, een boomgaard en fruit.

- `index.html`: startpagina; hier komt de app (GitHub Pages)
- `tuinplan/`: het plan van de achtertuin (`tuinplan.md`), de interactieve weergave en de foto's
- `moestuin/`: het plan van de moestuin (`moestuinplan.md`)
- `data/`: de gegevens van de app, gebouwd uit de plannen; zie `docs/datamodel.md`
- `overdracht/`: wijzigingen in de plannen die de app raken
- `scripts/bouw_data.py` bouwt `data/`; `scripts/check_data.py` controleert de data

Afspraken over wie wat wijzigt staan in `CLAUDE.md`.
