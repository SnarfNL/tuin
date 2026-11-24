# Tuin

Tuinplan voor een tuin op kleibodem met vijf zones (A, B, C, D, S), drie thema's (Landelijk, Natuurlijk, Jardin Sauvage) en het hele jaar sierwaarde voor bijen en vogels. De repo is ook de gedeelde gegevensbron voor de tuinapp, die de taken uit het tuinplan en de moestuin per maand bundelt.

- `index.html` — startpagina (GitHub Pages); hier komt de app
- `tuinplan/` — het tuinplan: `tuinplan.md` (leesbare bron), `index.html` (interactieve weergave) en `images/`
- `data/` — plantenlijst per bak, onderhoudsregels en taken als JSON (`data/moestuin/` voor de moestuin)
- `docs/` — projectcontext en de overdracht voor de app
- `scripts/check_data.py` — controleert de data en vergelijkt de plantenlijst met `tuinplan/tuinplan.md`

Afspraken over wie wat wijzigt staan in `CLAUDE.md`.
