# Moestuin

Deze map wordt gevuld vanuit het project Tuinapp. Alle records hebben `"bron": "moestuin"`.

Verwachte bestanden (zie `docs/handoff-tuinapp.md`, §4):

- `bakken.json` — moestuinbakken: `id`, `naam`, `type` (`moestuin` of `kas`), `zon`, `m2`, `grond`
- `gewassen.json` — gewassen, kruiden en fruit: zelfde velden als `data/planten.json`, plus `familie` (voor wisselteelt), `plantafstand`
- `onderhoudsregels.json` — zaaien, uitplanten, oogsten, bemesten, afdekken per gewas
- `teeltplan.json` — welk gewas in welke bak, per seizoen en jaar

`scripts/check_data.py` leest deze bestanden mee zodra ze bestaan.
