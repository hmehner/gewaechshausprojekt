# Gewächshausprojekt

Dieser Code dient der Überwachung und Steuerung eines Gewächshauses.

## Vorbereitung

In der **.env** Datei können Änderungen an der Konfiguration des Programms vorgenommen werden.
Wenn sie noch nicht existiert, wird bei Start des Programms aus dem Template eine Standardkonfiguration erzeugt.

Da das Programm über das **start.sh** Skript gestartet wird, muss sichergestellt werden, dass die Datei ausführbar ist. Dafür:

``` bash
chmod +x ./start.sh
```

## Starten

Um das Programm zu starten muss das **start.sh** Skript aus dem Root Verzeichnis des Projekts ausgeführt werden. Dafür:

``` bash
./start.sh
```