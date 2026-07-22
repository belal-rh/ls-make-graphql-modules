# LearningSuite GraphQL SDK

Zentrale Sammlung aller dokumentierten LearningSuite-GraphQL-Operationen, Persisted Queries und Entwicklungswerkzeuge.

Das Repository dient als **Single Source of Truth** für die inoffizielle LearningSuite-API. Jede bestätigte Operation wird einmal technisch dokumentiert und kann anschließend für Make Custom Apps, Python-Skripte, Tests und weitere Integrationen wiederverwendet werden.

## Inhalt

- Dokumentation aller bestätigten GraphQL-Requests
- Persisted-Query-Hashes und Variablen
- Beispielhafte Request- und Response-Payloads
- Make-Custom-App-Deployer
- Python-Hilfstools
- Maschinenlesbare YAML-Definitionen
- Testfälle und spätere Validierungen

## Dokumentationsphasen

Die API-Dokumentation wird schrittweise aufgebaut:

1. **FETCH** – Daten abrufen und bestehende Strukturen prüfen
2. **CREATION** – Kurse, Module, Sektionen und Lektionen erstellen
3. **UPDATE** – bestehende Objekte und Thumbnails aktualisieren

Aktuell dokumentiert ist die FETCH-Phase.

## FETCH-Operationen

| Objekt | Operation | Zweck |
|---|---|---|
| Course | `AuthoredCourses` | Alle verfügbaren Kurse abrufen |
| Course | `CourseInfoQuery` | Details und Beschreibung eines Kurses abrufen |
| Course / Topic | `CoursePaths` | Alle Module eines Kurses abrufen |
| Topic | `TopicQuery` | Sektionen und Lektionen eines Moduls abrufen |

Siehe [`docs/fetch/README.md`](docs/fetch/README.md).

## Repository-Struktur

```text
.
├── README.md
├── docs/
│   ├── authentication.md
│   ├── conventions.md
│   └── fetch/
│       ├── README.md
│       ├── courses/
│       │   ├── authored-courses.md
│       │   ├── course-info-query.md
│       │   └── course-paths.md
│       └── topics/
│           └── topic-query.md
├── operations/
│   └── fetch/
│       ├── courses/
│       │   ├── authored-courses.yaml
│       │   ├── course-info-query.yaml
│       │   └── course-paths.yaml
│       └── topics/
│           └── topic-query.yaml
├── deploy_learningsuite_make_app.py
└── requirements.txt
```

## Grundprinzip: Fetch before Update

Bevor ein Objekt erstellt oder verändert wird, sollte zuerst der aktuelle Zustand geladen werden. Dadurch lassen sich Duplikate, falsche IDs und unbeabsichtigtes Überschreiben vermeiden.

## Persisted Queries

LearningSuite sendet keinen vollständigen GraphQL-Query-String. Stattdessen besteht ein Request aus:

- `operationName`
- `variables`
- `extensions.persistedQuery.version`
- `extensions.persistedQuery.sha256Hash`

Ändert LearningSuite eine Operation, kann der bisherige Hash ungültig werden. Typischer Fehler:

```text
PersistedQueryNotFound
```

Dann muss der aktuelle RAW-Request im Browser erfasst und der Hash in Dokumentation und Code aktualisiert werden.

## Make Custom App deployen

Der Make-API-Token benötigt:

- `sdk-apps:read`
- `sdk-apps:write`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export MAKE_API_TOKEN="DEIN_MAKE_TOKEN"
export MAKE_ZONE="eu1"

python deploy_learningsuite_make_app.py
```

Testlauf ohne Änderungen:

```bash
python deploy_learningsuite_make_app.py --dry-run
```

## Sicherheit

- Zugangsdaten gehören ausschließlich in Make-Connections oder Umgebungsvariablen.
- Tokens und Passwörter dürfen nicht committed werden.
- Node IDs und SIDs müssen entsprechend ihrer dokumentierten Verwendung eingesetzt werden.

## Status

Die LearningSuite-GraphQL-Schnittstelle ist nicht offiziell dokumentiert. Alle Angaben basieren auf beobachteten und bestätigten Requests und müssen bei Änderungen der LearningSuite-Webanwendung erneut geprüft werden.
