# PharmaBus

## Dependencies

```
python3
pip
virtualenv
sqlite
working internet ;)
```

## Install

Install via:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

Das folgende Skript erstellt die sqlite Datenbank und startet das Programm.
ACHTUNG: Dies überschreibt alle Daten in der Datenbank!

```
bash run.sh
```

## Develop

Add new packages to requirements.txt pls :)


## Goal

> Wie können wir sicher stellen dass jede:r Bürger:in in max 4 Stunden die benötige Rezepte und Medikamente nach Hause bekommt?

## Approach

Pharmacies and drivers are able to register with our Website.

Drivers can state where they live and their range of distribution as well as the size of their trunk.

Users can sign up and upload a order of medication. The backend will then schedule based on pharmacy inventory and driver availability drivers who pick up medication and distribute it appropriately.

### Out of Scope
- Data protection foo
- How prescriptions are handled
- legality of having citizens deliver prescription drugs
- legality of ordering prescription drugs online
- payment processing
