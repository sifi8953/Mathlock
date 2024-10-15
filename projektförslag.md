# Mathlock

Simon Fikse och Remu Mäenranta

## Vår idé

Mathlock: ett program som tvingar användaren att lösa matteuppgifter för att kunna fortsätta använda sin dator. Periodiskt skapas det en popup med en ekvation som inte försvinner förrän användaren löst den.

## Systemets delar

* Genera en ekvation med lösning(ar)
  * garantera att ekvationerna är lösbara med heltalsrötter
    * börja med svaren, jobba baklänges
    * alla operationer måste vara "snygga" (heltalskoefficienter)
* Kalla en funktion periodiskt
* Startmeny med inställningar
  * olika typer av ekvationer
  * svårighetsgrad
  * hur ofta en uppgift ges
* Skapa ett ljud/popup för att få användarens uppmärksamhet

## Representation

En uppgift kan representeras av en tuple av en sträng (ekvationen) och en lista av heltal (dess lösningar).

Periodiciteten kan representeras av ett heltal som avgör hur länge i sekunder programmet ska vänta innan den ger ut nästa uppgift.

Vilka typer av ekvationer användaren vill få kan lagras som strängar (namn) i en lista.

Svårighetsgraden beskrivs av en heltal som avgör antalet operationer som görs på ursprungsekvationen innan den ges till användaren.

## Komplexitet och förenkling

### Förenklingar

* Ekvationerna kan följa fördefinierade templates

### Ökad komplexitet

* Lägga till flera sorters ekvationer
* Kunna verifiera svaret oberoende av ursprungslösningarna för ifall t.ex. kvadrering skapar fler rötter
* GUI om tids finns över

## Personliga utvecklingsmål

Projektet kommer lagras hos GitHub för att vi ska vänja oss vid det arbetssättet. Dessutom kan vi använda bibliotek för t.ex. grafik för att bli bättre på det också.
