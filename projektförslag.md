# Mathlock

Simon Fikse och Remu Mäenranta

## Vår idé

Mathlock: ett program som tvingar användaren att lösa matteuppgifter för att kunna fortsätta använda sin dator. Periodiskt visas det en popup med en ekvation som inte försvinner förrän användaren löst den. Användaren har hur många försök som helst på sig att klara dem.

## Systemets delar

* Genera ekvationer med lösning(ar)
  * Garantera att ekvationerna är lösbara med heltalsrötter
    * Börja med svaren, jobba baklänges
    * Alla operationer måste vara "snygga" (heltalskoefficienter)
* Anropa en funktion periodiskt
* Startmeny med inställningar
  * Olika typer av ekvationer
  * Svårighetsgrad
  * Hur ofta en uppgift ges
* Skapa ett ljud/popup för att få användarens uppmärksamhet

## Representation

En uppgift kan representeras av en tuple av en sträng (ekvationen) och en lista av heltal (dess lösningar).

Alternativt kan en uppgift beskrivas av ett binärträd där noder lagrar operationer eller konstanter.

Periodiciteten är ett heltal som avgör hur länge i sekunder programmet ska vänta mellan att det ger ut nästa uppgift.

Vilka typer av ekvationer användaren vill få kan lagras som strängar (namn) i en lista.

Svårighetsgraden beskrivs av en heltal som avgör antalet operationer som görs på ursprungsekvationen innan den ges till användaren.

## Komplexitet och förenkling

### Förenklingar

* Ekvationerna kan följa fördefinierade mallar

### Ökad komplexitet

* Flera sorters ekvationer
* Kunna verifiera svaret oberoende av ursprungslösningarna för ifall t.ex. kvadrering skapar fler rötter
* GUI om tids finns över

## Personliga utvecklingsmål

Projektet kommer lagras hos GitHub för att vi ska vänja oss vid det arbetssättet. Dessutom kan vi använda bibliotek för t.ex. grafik för att öva på det också.
