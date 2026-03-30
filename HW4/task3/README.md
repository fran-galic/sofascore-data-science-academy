# Task 3 - Grafana visualizations

U ovom zadatku izrađen je Grafana dashboard koji vizualizira podatke iz tablice `fgalic.l4_dataset`. Svi paneli temelje se na upitima iz datoteke `queries.sql`, a svaki od njih prikazuje različit aspekt podataka.

## Obavezni paneli

1. **Daily row count**  
   Za prikaz broja zapisa po danima korišten je **bar chart**.  
   Podaci su grupirani po datumu (`eventDate`), čime se dobiva jasan pregled dnevnog volumena podataka kroz promatrani period.

2. **Table size**  
   Ukupna veličina tablice prikazana je kroz **table** vizualizaciju.  
   Panel prikazuje komprimiranu i nekomprimiranu veličinu podataka, ukupan broj redaka te broj aktivnih dijelova (parts), koristeći podatke iz `system.parts`.

3. **Column size share**  
   Udio veličine pojedinih stupaca prikazan je pomoću **pie charta**.  
   Svaki segment grafa predstavlja jedan stupac, a veličina segmenta odgovara količini memorije koju taj stupac zauzima.

## Bonus paneli

Dodatno su implementirani i sljedeći paneli:

4. **Top event names**  
   Prikaz najčešćih vrijednosti u stupcu `eventName` korištenjem **bar charta**, gdje su jasno vidljivi najzastupljeniji događaji.

5. **Top countries**  
   Distribucija podataka po državama (`geoCountry`) prikazana je pomoću **pie charta**, što omogućuje brz uvid u geografski raspored korisnika.

6. **Platform and status breakdown**  
   Kombinirani prikaz po platformi i statusu izrađen je kao **horizontalni bar chart**, čime se jasno vidi raspodjela događaja po različitim platformama (ANDROID, IOS, WEB) i njihovim statusima.

## Kako testirati

Za provjeru ispravnosti rješenja potrebno je:

1. Pokrenuti ClickHouse i Grafanu (Task 1)  
2. Importati podatke (Task 2)  
3. U Grafani otvoriti datasource `ClickHouse`  
4. Kreirati dashboard i zalijepiti upite iz `queries.sql`  
5. Postaviti odgovarajuće tipove vizualizacija za svaki panel  
6. Provjeriti da se svi paneli ispravno prikazuju  

## Napomena

U ovom folderu nalaze se `queries.sql` i README.  

Za predaju su dodani screenshot-ovi izrađenog dashboarda pod imenom:

```text
dashboard-1.png i dashboard-2.png
```