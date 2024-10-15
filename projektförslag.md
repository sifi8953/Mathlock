# Mathlock

Simon Fikse och Remu Mäenranta

## Vår idé

Mathlock: ett program som tvingar användaren att lösa matteuppgifter för att kunna fortsätta använda sin dator. Periodiskt skapas det en popup med en ekvation och popup-en försvinner inte från skärmen förrän användaren löst ekvationen.

## Systemets delar

* Genera en ekvation med lösning(ar)
  * garantera att ekvationerna är lösbara med heltalsrötter
    * börja med svaren, jobba baklänges
    * alla operationer måste vara "snygga" (heltalskoefficienter)
* Kalla en funktion periodiskt
* Startmeny med inställningar
  * olika typer av ekvationer
  * svårighetsgrad
  * hur ofta
* Skapa en popup

## Representation

En uppgift kan representeras av en tuple av en sträng (ekvationen) och en lista av heltal (dess lösningar)

## Komplexitet och förenkling

### Förenklingar

* Kan vara i terminalen till en början och utöka med GUI om tids finns över
* Ekvationerna kan följa fördefinierade templates

### Ökad komplexitet

* Lägga till flera sorters ekvationer
* Kunna verifiera svaret oberoende av ursprungslösningarna för ifall t.ex. kvadrering skapar fler rötter

## Personliga utvecklingsmål

Projektet kommer lagras hos GitHub för att vi ska vänja oss vid det arbetssätten. Dessutom kan vi använda bibliotek för t.ex. grafik för att bli bättre på det också.
