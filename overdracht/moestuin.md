# Overdracht: project Moestuin aan project Tuin app

## Stand

24 november 2026. Vanaf deze datum wordt de Tuinapp alleen in het project Tuin app gebouwd en bijgehouden. Het project Moestuin beslist over de moestuin en legt dat vast in `moestuin/moestuinplan.md`. Het project Tuin app zet dat plan om naar de app-data.

## Besluiten

Details staan in `moestuin/moestuinplan.md`.

| # | Besluit | Status |
|---|---|---|
| 1 | Indeling: 8 grote bakken van 1,5 m breed (bak 1, 4, 5, 8 van 4,0 m; bak 2, 3, 6, 7 van 3,0 m), kruidenbak 3,0 × 1,0 m in het midden, bloemenbak (bak 9) ±3,0 × 0,8 m voor de schuur | besloten |
| 2 | Paden 0,65 m in de rij, 0,7 m onder de pergola, 0,85 m tussen de rijen; houtsnippers op worteldoek | besloten |
| 3 | Bakken van onbehandelde Douglas, één plank hoog, noppenfolie binnen, RVS-dwarsband, direct op opengeknipt worteldoek | besloten |
| 4 | Vulling: ±7 m³ schone tuinaarde los gestort (15 cm); kruidenbak met 30% grof zand | besloten (nog niet besteld) |
| 5 | Losse, verplaatsbare kasopzet van 1,5 × 2,0 m in plaats van een vaste kasbak | besloten |
| 6 | Pergola als korte tunnel over het pad tussen bak 2 en 3 | besloten (klimmer open) |
| 7 | Gewassen: suikermais + pompoen; courgette met Oost-Indische kers en goudsbloem; wortel + lente-ui + afrikaantjes; rode biet + snackkomkommer + ridderspoor + goudsbloem; aardbeien + knoflook; zoete aardappel + afrikaantjes; een vrije bak; bloemen, vooral dahlia's; kruidenbak met citroenmelisse, basilicum, rozemarijn, peterselie, lavendel, tijm en munt (munt in een pot) | besloten |
| 8 | Geen boerenkool, stokbonen of popcornmais | besloten |
| 9 | Uitgangspunt weinig werk geldt na de aanleg; de gewassen blijven zoals besloten, aandachtspunten worden alleen genoteerd | besloten |
| 10 | Lege bakken in de winter afdekken met zelf verzameld blad en stro; in het voorjaar compost erop | besloten |
| 11 | Koppeling gewas aan bak-nummer (bak 1 mais + pompoen, 2 wortel, 3 biet + komkommer, 4 courgette, 5 dahlia's, 6 zoete aardappel, 7 vrij, 8 aardbeien + knoflook) | voorgesteld |
| 12 | Wisselteelt: elk jaar ruilen binnen de paren bak 1 ↔ 4 en bak 2 ↔ 3; bak 5, 6 en 8 blijven | voorgesteld |
| 13 | Kasopzet in het voorjaar op bak 6 met voorteelt (radijs, pluksla, spinazie), in het najaar op een lege bak met veldsla | voorgesteld |
| 14 | Phacelia als groenbemester in bakken die vóór september leeg komen | voorgesteld |
| 15 | Druppelirrigatie op een zonnepomp met timer uit de regentonnen | voorgesteld (niets besteld) |
| 16 | Bijmesten van de hongerige gewassen in jun–jul | voorgesteld |
| 17 | De kruidenbak heeft geen bak-nummer. Heeft de app voor het filter (bak 1–10) een nummer nodig, gebruik dan bak 10 | voorgesteld |

## Open punten die taken opleveren

Zie `moestuinplan.md` §5 (eenmalige taken) en §6 (open punten). De belangrijkste:

- Aanleg deze winter: noppenfolie, RVS-band, worteldoek openknippen, tuinaarde en zand bestellen en vullen, houtsnippers, bloemenbak, kasopzet en pergola bouwen, pruim weg, reglement van het complex nalezen.
- Voorjaar 2027: kasopzet op bak 6 (e-feb), knoflook (feb–mrt) en aardbeien (mrt) in bak 8, kruidenbak planten (mrt–apr), irrigatie (na de keuze van het zonnepaneel).
- Keuzes die taken veranderen: invulling bak 7 en bak 9, plek van de dahlia's, type frambozen, soorten in de boomgaard, ridderspoor eenjarig of vast, voorteelt onder de kasopzet ja of nee.

## Hoort de tuinkas thuis bij de moestuin?

Nee. De glazen tuinkas staat thuis in de achtertuin en hoort bij het tuinplan (project Tuin); in de app valt hij onder de locatie achtertuin, zoals gekozen bij de filters (achtertuin: A, B, C, D en kas). De moestuin heeft geen vaste kas, alleen de losse kasopzet die over een bak wordt gezet. Die is in de app geen eigen plek, maar komt terug als taak bij de bak waarop hij staat.

## Wat het project Tuin app nog moet doen

- `data/moestuin/README.md` en de regels over `data/moestuin/` in `CLAUDE.md` en `docs/handoff-tuinapp.md` bijwerken: de bron is nu `moestuin/moestuinplan.md`.
- `moestuin/` en `overdracht/` opnemen in de tabel *Wat staat waar* in `CLAUDE.md`.
- Bij een wijziging in `moestuin/moestuinplan.md` staat er een regel in `overdracht/wijzigingen.md` met datum, wat er veranderd is en de sectie.

## Tekst in de projectinstructies van het project Moestuin

> De Tuinapp (repo SnarfNL/tuin, openbaar) wordt alleen in het project Tuin app gebouwd en bijgehouden. Dit project beslist over de moestuin en legt dat vast in moestuin/moestuinplan.md. Schrijf niet in data/, scripts/, CLAUDE.md, README.md of de app-bestanden. Raakt een wijziging gewassen, bakken, taken of planning, voeg dan in dezelfde commit een regel toe aan overdracht/wijzigingen.md: datum, wat er veranderd is, en de sectie in moestuinplan.md. Zet geen namen of andere persoonsgegevens in de repo.
