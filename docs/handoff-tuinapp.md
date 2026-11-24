# Handoff: Tuinapp (taken voor siertuin en moestuin)

*Opgesteld 24 november 2026 vanuit het project Tuin; bijgewerkt dezelfde dag na de keuze voor deze repo als gedeelde plek. Bron: `tuinplan/tuinplan.md` en `docs/projectcontext.md`, stand 24 november 2026.*

## 1. Doel

Eén app met alle tuintaken: de taken uit het tuinplan (siertuin, zones A, B, C, D en S) en de taken in de moestuin. De app groepeert de taken per maand en per soort actie, zodat bijvoorbeeld alle snoeiwerk in één ronde per maand kan. Voorbeeld uit het huidige plan: in maart staan 23 snoei- en terugknipacties, in juli 8 en in augustus 5.

## 2. Beslissingen

**Besloten (24 november 2026):**

- De gedeelde plek is de GitHub-repo **SnarfNL/tuin** (openbaar, gepubliceerd via GitHub Pages). Het tuinplan staat in `tuinplan/`, de startpagina van de app in `index.html` in de hoofdmap.
- **De repo is leidend.** Het project Tuin en het project Tuinapp lezen en schrijven hier; projectdocumenten zijn hoogstens een kopie.
- De plantenlijst per bak en de taken staan als **JSON** in `data/`.
- Wijzigingen gaan **direct op `main`**.
- Siertuin (`bron: "tuinplan"`) wordt beheerd vanuit het project Tuin; moestuin (`bron: "moestuin"`) vanuit het project Tuinapp. Zie `CLAUDE.md`.

**Nog te beslissen in het project Tuinapp** (voorstellen):

| # | Beslissing | Voorstel | Alternatief |
|---|---|---|---|
| 1 | Waar draait de app? | Op GitHub Pages, vanaf `index.html` in de hoofdmap; de app leest `data/*.json` met een relatief pad (er staat al een testpagina) | Zelf gehost, of een Claude-artifact die de JSON inleest |
| 2 | Waar komt het afvinken en het logboek? | Niet in de openbare repo, maar in de opslag van de app zelf (lokaal of eigen database) | Een aparte, privé repo of map |
| 3 | Hoe fijn is de planning? | Per maand, met een optionele aanduiding begin, midden of eind (nodig voor "vóór half december") | Per week |
| 4 | Wie gebruikt de app? | Eén huishouden, meerdere gebruikers mogen afvinken | Alleen de eigenaar |

## 3. Hoe de gedeelde data werkt

- De bestanden in `data/` zijn de machineleesbare versie van het tuinplan; `tuinplan/tuinplan.md` is de leesbare versie met toelichting en besluiten.
- Raakt een wijziging planten, bakken of onderhoud, dan worden `tuinplan/tuinplan.md` en `data/` **in dezelfde commit** bijgewerkt, met `data/meta.json` (`stand`) erbij.
- `scripts/check_data.py` controleert de data (verwijzingen, maanden, acties) en vergelijkt de plantenlijst in `data/planten.json` met de tabel *Alle planten* in `tuinplan/tuinplan.md`. Draai het vóór elke commit.
- Records worden niet verwijderd maar krijgen `"status": "vervallen"`, zodat het logboek van de app blijft kloppen.
- Een Claude-sessie kan in deze repo werken als de repo aan de sessie is gekoppeld. De Claude-projecten kunnen de repo ook als (alleen-lezen) kennis inlezen via hun GitHub-koppeling.

## 4. Datamodel

| Bestand | Velden |
|---|---|
| `data/bakken.json` | `id`, `naam`, `type` (sier, moestuin, kas), `zon`, `thema`, `m2`, `mest`, `mulch`, `bron` |
| `data/planten.json` | `id`, `nl`, `latijn`, `bakken[]`, `soort` (boom, klimplant, vaste plant, bol, gras, varen, struik, eenjarig, tweejarig; moestuin ook groente, kruid), `levensduur` (⏳, ⏱ of leeg), `status` (gepland, geplant, vervallen), `bron` |
| `data/bollen_per_bak.json` | `bak`, `plant`, `aantal`, `bron` |
| `data/onderhoudsregels.json` | `id`, `plant`, `actie`, `maanden[]`, `herhaling`, `toelichting`, `bron` |
| `data/algemene_regels.json` | Regels per bak in plaats van per plant (mulchen, pH meten, water geven, schorspad aanvullen) en **niet-doen-regels** (klimop niet snoeien in het broedseizoen, zaadhoofden laten staan tot maart): `id`, `actie`, `maanden[]`, `bakken[]`, `herhaling`, `toelichting`, `bron` |
| `data/eenmalige_taken.json` | `id`, `titel`, `wanneer`, `status`, `herkomst`, `bron` (open stappen uit de planning en actiepunten) |
| `data/meta.json` | `schema_versie`, `stand`, bestandslijst, eigenaar per bron |
| `data/moestuin/` | `bakken.json`, `gewassen.json` (plus `familie` voor wisselteelt en `plantafstand`), `onderhoudsregels.json`, `teeltplan.json` (gewas per bak per seizoen en jaar) |

Acties: `snoeien`, `planten_zaaien`, `delen_verplanten`, `uitgebloeid_verwijderen`, `mulchen`, `meten`, `water_geven`, `niet_doen`, `aanvullen`; voor de moestuin ook `zaaien`, `uitplanten`, `oogsten`, `bemesten`, `afdekken`.

Herhaling: `jaarlijks`, `eenmalig_aanplant`, `indien_nodig`, `conditioneel`.

## 5. Taaklogica

- **Maandoverzicht:** alle taken van de maand, gegroepeerd per actie en daarbinnen per bak. Zo is "snoeironde maart" één lijst.
- **Aanplant vervalt na het planten:** `🌱` in de onderhoudskalender is voor de meeste soorten het plantvenster, geen jaarlijkse taak. Regels met `eenmalig_aanplant` verdwijnen zodra de plant `status: "geplant"` heeft. Bij ⏳-soorten (eenjarig of tweejarig) is zaaien wel jaarlijks.
- **Delen** (`indien_nodig`): tonen als suggestie, niet als verplichte taak; de ⏱-check staat apart in herfst 2029.
- **Conditioneel** (water geven): alleen tonen met de voorwaarde (minder dan ±10 mm regen die week en droge grond op 5 cm). Later eventueel koppelen aan regendata.
- **Niet-doen-regels** tonen als waarschuwing bij de taken van die bak en maand.
- **Afvinken per jaar:** een jaarlijkse taak is per jaar af, niet voor altijd.

## 6. Wat het app-project nodig heeft

### 6a. Projectinstructies voor het project Tuinapp (voorstel)

> Antwoord altijd in het Nederlands. Dit project bouwt de Tuinapp: één takenoverzicht per maand voor de siertuin (zones A, B, C, D en S) en de moestuin. De gedeelde bron is de GitHub-repo SnarfNL/tuin; die is leidend. Lees bij de start `CLAUDE.md` en `docs/handoff-tuinapp.md` in de repo. Records met `bron: "tuinplan"` worden alleen vanuit het project Tuin gewijzigd; dit project beheert `data/moestuin/` en de app. Draai `scripts/check_data.py` vóór elke commit. De repo is openbaar: geen persoonsgegevens. Benoem beslissingen eerst en leg ze pas daarna vast. Gebruik Nederlandse (of Vlaamse) websites als bron voor plantinformatie.

### 6b. Feiten over de tuin

- Kleibodem; de grond meet pH 7 met vrije kalk.
- Siertuin: vijf zones als licht verhoogde plantvakken met rand: A 4,5 m², B 8 m², C 8 m², D 4 m², S ±2,5 m² (samen ±27 m²); drie thema's; focus op bijen en vogels, het hele jaar iets in bloei.
- Zon: alleen D en de tuinkas hebben meer dan 6 uur zon; A, B en C 3–6 uur; S minder dan 3 uur. Nog te meten in het groeiseizoen.
- Bomen (geplant november 2026): krentenboom (halfstam, C) en Amerikaanse kornoelje (struikvorm, A, op een zure plantplek; pH voor- en najaar meten, regenwater geven).
- Er staat een tuinkas (glazen achthoek); er is een regenton van 120 l en een schorspad.
- Geen irrigatie: met de hand water geven.
- Werkwijze: eerst informatie verzamelen en beslissingen benoemen, dan pas vastleggen.

## 7. Nog nodig voor de moestuin

In het tuinplan staat nog niets over de moestuin. Eerst uitzoeken:

1. Hoeveel moestuinbakken zijn er, hoe groot, waar (zon) en met welke grond? Hoort de tuinkas erbij?
2. Welke gewassen, kruiden en eventuele fruitstruiken? Zaaien of plantgoed?
3. Wordt er wisselteelt gedaan (gewasfamilie per bak per jaar)?
4. Welke terugkerende moestuintaken zijn er (bemesten, groenbemester, afdekken, netten)?

## 8. Bekende onzekerheden in de data

- `🌱` is vertaald naar `eenmalig_aanplant`, behalve bij ⏳-soorten (`jaarlijks`). Controleer dit per soort; bij de bollen in najaar 2026 is het de huidige aanplant.
- De maand voor het aanvullen van het schorspad (maart) is een voorstel; het plan zegt alleen "elk jaar".
- Ooievaarsbek 'Rozanne' staat in A en B, maar de onderhoudskalender had alleen een regel voor A; in de data geldt de regel voor beide bakken. Hetzelfde voor kerstroos (oosterse), bermzegge, kattenkruid en rudbeckia.
- Alle planten behalve de twee bomen hebben `status: "gepland"`; zet de bollen op `geplant` zodra ze in de grond zitten.
