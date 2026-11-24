# Overdracht: project Moestuin aan project Tuin app

## Stand

24 november 2026. Vanaf deze datum wordt de Tuinapp alleen in het project Tuin app gebouwd en bijgehouden. Het project Moestuin beslist over de moestuin en legt dat vast in `moestuin/moestuinplan.md`. Het project Tuin app zet dat plan om naar de app-data.

## Besluiten

Details staan in `moestuin/moestuinplan.md`.

| # | Besluit | Status |
|---|---|---|
| 1 | Indeling: 8 grote bakken van 1,5 m breed (bak 1, 4, 5, 8 van 4,0 m; bak 2, 3, 6, 7 van 3,0 m), bak 9 = kruidenbak 3,0 × 1,0 m in het midden, bak 10 = bloemenbak ±3,0 × 0,8 m voor de schuur | besloten |
| 2 | Paden 0,65 m in de rij, 0,7 m onder de pergola, 0,85 m tussen de rijen; houtsnippers op worteldoek | besloten |
| 3 | Bakken van onbehandelde Douglas, één plank hoog, noppenfolie binnen, RVS-dwarsband (bak 10: 1 band), direct op opengeknipt worteldoek | besloten |
| 4 | Vulling: ±7 m³ schone tuinaarde los gestort (15 cm); kruidenbak met 30% grof zand | besloten (nog niet besteld) |
| 5 | Losse, verplaatsbare kasopzet van 1,5 × 2,0 m in plaats van een vaste kasbak | besloten |
| 6 | Pergola als korte tunnel over het pad tussen bak 2 en 3, begroeid met eenjarige snackkomkommer en klimmende Oost-Indische kers uit de aangrenzende bak | besloten |
| 7 | Gewassen per bak: 1 suikermais + pompoen; 2 wortel + lente-ui + afrikaantjes; 3 rode biet + snackkomkommer + eenjarige ridderspoor + goudsbloem + klimmende Oost-Indische kers; 4 courgette met Oost-Indische kers en goudsbloem; 5 dahlia's; 6 zoete aardappel + afrikaantjes; 7 vrij; 8 aardbeien + knoflook; 9 kruiden (citroenmelisse, basilicum, rozemarijn, peterselie, lavendel, tijm, munt in een pot); 10 eenjarige bloemen (goudsbloem, cosmos, zinnia) | besloten |
| 8 | Wisselteelt: elk jaar ruilen binnen de paren bak 1 ↔ 4 en bak 2 ↔ 3; bak 5, 6, 8, 9 en 10 blijven | besloten |
| 9 | Kasopzet in het voorjaar op bak 6 met voorteelt (radijs, pluksla, spinazie), in het najaar op een lege bak met veldsla | besloten |
| 10 | Phacelia als groenbemester in bakken die vóór september leeg komen | besloten |
| 11 | Eén keer bijmesten met organische korrels in jun–jul voor pompoen, courgette, komkommer, mais en dahlia | besloten |
| 12 | Lege bakken in de winter afdekken met zelf verzameld blad en stro; in het voorjaar compost erop | besloten |
| 13 | Water geven met de hand uit de regentonnen; het irrigatieplan is een concept | besloten |
| 14 | Knoflook het eerste jaar in feb–mrt 2027 planten, daarna elk jaar in okt–nov | besloten |
| 15 | Alle terugkerende onderhoudstaken in `moestuinplan.md` §4 | besloten (taken met [eigen inschatting] zijn niet uit een bron) |
| 16 | Geen boerenkool, stokbonen of popcornmais; uitgangspunt weinig werk na de aanleg | besloten |
| 17 | De bestaande houten verhoogde bak naast de frambozen is al weg | besloten |

## Open punten die taken opleveren

Zie `moestuinplan.md` §5 (eenmalige taken) en §6 (open punten).

- Aanleg deze winter: noppenfolie, RVS-band, worteldoek openknippen, tuinaarde en zand bestellen en vullen, houtsnippers, bloemenbak, kasopzet en pergola bouwen, pruim weg, reglement van het complex nalezen.
- Voorjaar 2027: kasopzet op bak 6 met voorteelt (e-feb), knoflook (feb–mrt) en aardbeien (mrt) in bak 8, bak 9 planten (mrt–apr), bak 10 inzaaien (m-apr–mei).
- Nog te beslissen: invulling bak 7, rassen (bij het bestellen in dec–jan), irrigatie (concept).
- Nog na te gaan: type frambozen (oogsttijd 2027) en de soorten in de boomgaard.
- Stand 24 november 2026: bak 2, 3, 6 en 7 zijn verschoven; bak 10 staat en moet nog een meter worden ingekort. Op het complex is geen kraan, wel een handpomp op het eigen perceel.

## Hoort de tuinkas thuis bij de moestuin?

Nee. De glazen tuinkas staat thuis in de achtertuin en hoort bij het tuinplan (project Tuin); in de app valt hij onder de locatie achtertuin, zoals gekozen bij de filters (achtertuin: A, B, C, D en kas). De moestuin heeft geen vaste kas, alleen de losse kasopzet die over een bak wordt gezet. Die is in de app geen eigen plek, maar komt terug als taak bij de bak waarop hij staat. Planten uit de tuinkas mogen wel naar de moestuin worden verplaatst (besloten 24 november 2026 in het project Tuin); vanaf dat moment vallen ze onder het moestuinplan.

## Wat het project Tuin app nog moet doen

- `data/moestuin/README.md` en de regels over `data/moestuin/` in `CLAUDE.md` en `docs/handoff-tuinapp.md` bijwerken: de bron is nu `moestuin/moestuinplan.md`.
- `moestuin/` en `overdracht/` opnemen in de tabel *Wat staat waar* in `CLAUDE.md`.
- Bij een wijziging in `moestuin/moestuinplan.md` staat er een regel in `overdracht/wijzigingen.md` met datum, wat er veranderd is en de sectie.

## Tekst in de projectinstructies van het project Moestuin

> De Tuinapp (repo SnarfNL/tuin, openbaar) wordt alleen in het project Tuin app gebouwd en bijgehouden. Dit project beslist over de moestuin en legt dat vast in moestuin/moestuinplan.md. Schrijf niet in data/, scripts/, CLAUDE.md, README.md of de app-bestanden. Raakt een wijziging gewassen, bakken, taken of planning, voeg dan in dezelfde commit een regel toe aan overdracht/wijzigingen.md: datum, wat er veranderd is, en de sectie in moestuinplan.md. Zet geen namen of andere persoonsgegevens in de repo.
