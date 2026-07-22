# LearningSuite GraphQL → Make Custom App

Das Skript erstellt bzw. aktualisiert eine private Make Custom App mit 15 Modulen für die dokumentierten LearningSuite-Persisted-Queries.

## Vorbereitung

Der Make-API-Token benötigt:

- `sdk-apps:read`
- `sdk-apps:write`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MAKE_API_TOKEN="DEIN_MAKE_TOKEN"
export MAKE_ZONE="eu1"
```

## Deployment

```bash
python deploy_learningsuite_make_app.py
```

Für `eu2.make.com`:

```bash
python deploy_learningsuite_make_app.py --zone eu2
```

Testlauf ohne Änderungen:

```bash
python deploy_learningsuite_make_app.py --dry-run
```

## Danach in Make

Öffne eines der neuen LearningSuite-Module und erstelle eine Connection mit:

- Tenant-ID
- LearningSuite-E-Mail
- LearningSuite-Passwort

Die App ruft vor jedem GraphQL-Command einen frischen Bearer-Token ab.

## Enthalten

- Kurs- und Modulabfragen
- Kurs erstellen/aktualisieren
- Modul in der Bibliothek erstellen
- Modul direkt zu einem Kurs hinzufügen
- Modulbeschreibung aktualisieren
- Sektion erstellen/bearbeiten
- Lektion erstellen
- Kurs-/Modul-Thumbnail setzen
- universelles Persisted-GraphQL-Modul

## Hinweis

Die LearningSuite-GraphQL-Schnittstelle ist inoffiziell. Bei `PersistedQueryNotFound` muss der betreffende Hash aus einem neuen RAW-Request aktualisiert werden.
