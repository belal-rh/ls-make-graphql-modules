# LearningSuite GraphQL SDK

Zentrale Sammlung aller dokumentierten LearningSuite-GraphQL-Operationen, Persisted Queries und Entwicklungswerkzeuge.

Das Repository dient als **Single Source of Truth** für die inoffizielle LearningSuite-API. Jede bestätigte Operation wird einmal dokumentiert und kann anschließend für Make Custom Apps, Python-Skripte, Tests und weitere Integrationen wiederverwendet werden.

## Aktueller Stand

Dokumentiert sind derzeit:

### FETCH

| Objekt | Operation | Zweck |
|---|---|---|
| Course | `AuthoredCourses` | Alle verfügbaren Kurse abrufen |
| Course | `CourseInfoQuery` | Details und Beschreibung eines Kurses abrufen |
| Course / Topic | `CoursePaths` | Module eines Kurses abrufen |
| Topic | `TopicQuery` | Sektionen und Lektionen eines Moduls abrufen |

### CREATE

| Objekt | Operation | Zweck |
|---|---|---|
| Course | `AddCourse` | Kurs erstellen |
| Topic | `CreateTopic` | Eigenständiges Modul in der Bibliothek erstellen |
| Topic / Course | `AddTopicToCourse` | Modul direkt in einem Kurs erstellen |
| Section | `AddSection` | Sektion innerhalb eines Moduls erstellen |
| Lesson | `AddLesson` | Lektion innerhalb einer Sektion erstellen |

Die vollständige Navigation befindet sich unter [`docs/README.md`](docs/README.md).

## Objektorientierte Struktur

```text
.
├── README.md
├── docs/
│   ├── README.md
│   ├── authentication.md
│   ├── conventions.md
│   ├── courses/
│   │   ├── fetch/
│   │   └── create/
│   ├── topics/
│   │   ├── fetch/
│   │   └── create/
│   ├── sections/
│   │   └── create/
│   └── lessons/
│       └── create/
├── operations/
│   ├── courses/
│   │   ├── fetch/
│   │   └── create/
│   ├── topics/
│   │   ├── fetch/
│   │   └── create/
│   ├── sections/
│   │   └── create/
│   └── lessons/
│       └── create/
├── deploy_learningsuite_make_app.py
└── requirements.txt
```

Die Markdown-Dateien sind für Menschen gedacht. Die YAML-Dateien unter `operations/` bilden die maschinenlesbare Grundlage für Generatoren, Make-Module und Tests.

## Grundprinzip: Fetch before Mutation

Bevor ein Objekt erstellt oder verändert wird, soll zuerst der aktuelle Zustand geladen werden. Dadurch lassen sich Duplikate, falsche IDs und unbeabsichtigte Änderungen vermeiden.

## Persisted Queries

LearningSuite sendet keinen vollständigen GraphQL-Query-String. Ein Request besteht im Kern aus:

- `operationName`
- `variables`
- `extensions.persistedQuery.version`
- `extensions.persistedQuery.sha256Hash`

Bei `PersistedQueryNotFound` muss der aktuelle RAW-Request im Browser erfasst und der Hash in Dokumentation, YAML und Code aktualisiert werden.

## Make Custom App deployen

Der Make-API-Token benötigt `sdk-apps:read` und `sdk-apps:write`.

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
- Tokens, Passwörter und lokale `.env`-Dateien dürfen nicht committed werden.
- Node IDs und SIDs müssen entsprechend ihrer dokumentierten Verwendung eingesetzt werden.

## Status

Die LearningSuite-GraphQL-Schnittstelle ist nicht offiziell dokumentiert. Alle Angaben basieren auf beobachteten und bestätigten Requests und müssen bei Änderungen der LearningSuite-Webanwendung erneut geprüft werden.
