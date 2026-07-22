# LearningSuite GraphQL SDK

Zentrale Sammlung aller dokumentierten LearningSuite-GraphQL-Operationen, Persisted Queries und Entwicklungswerkzeuge.

Das Repository dient als **Single Source of Truth** für die inoffizielle LearningSuite-API. Jede bestätigte oder beobachtete Operation wird technisch dokumentiert und kann anschließend für Make Custom Apps, Python-Skripte, Tests und weitere Integrationen wiederverwendet werden.

## Aktueller Stand

Dokumentiert sind derzeit **19 GraphQL-Operationen**:

| Bereich | Anzahl | Operationen |
|---|---:|---|
| FETCH | 4 | `AuthoredCourses`, `CourseInfoQuery`, `CoursePaths`, `TopicQuery` |
| CREATE | 5 | `AddCourse`, `CreateTopic`, `AddTopicToCourse`, `AddSection`, `AddLesson` |
| UPDATE | 5 | `UpdateCourse`, `EditTopic`, `EditSection`, `SetCourseThumbnail`, `SetModuleThumbnail` |
| UPLOAD | 5 | `SetCourseImage`, `SetCourseThumbnailBG`, `TopicEditSetImage`, `SetModuleThumbnailBG`, `SetLessonImage` |

Die vollständige Navigation befindet sich unter [`docs/README.md`](docs/README.md).

## Objektorientierte Struktur

```text
.
├── README.md
├── docs/
│   ├── README.md
│   ├── authentication.md
│   ├── conventions.md
│   ├── uploads.md
│   ├── courses/
│   │   ├── fetch/
│   │   ├── create/
│   │   ├── update/
│   │   └── upload/
│   ├── topics/
│   │   ├── fetch/
│   │   ├── create/
│   │   ├── update/
│   │   └── upload/
│   ├── sections/
│   │   ├── create/
│   │   └── update/
│   └── lessons/
│       ├── create/
│       └── upload/
├── operations/
│   └── <object>/<action>/*.yaml
├── scripts/
│   └── upload_learningsuite_image.py
├── deploy_learningsuite_make_app.py
├── deploy_learningsuite_make_app_compatible.py
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

python deploy_learningsuite_make_app_compatible.py
```

Testlauf ohne Änderungen:

```bash
python deploy_learningsuite_make_app_compatible.py --dry-run
```

Der kompatible Deployer unterstützt beide aktuell beobachteten Request-Formate für `POST /sdk/apps`: App-Felder direkt auf oberster Ebene sowie den von Make dokumentierten `app`-Wrapper. Der bisherige Deployer bleibt als Kernmodul bestehen.

Der aktuelle Deployer enthält die bestätigten FETCH-, CREATE-, UPDATE- und Preset-Thumbnail-Module. Die UploadSpec-Operationen sind in YAML dokumentiert und können über den Python-Helper ausgeführt werden.

## Bilder hochladen

Für echte Bilddateien wird zunächst per GraphQL eine signierte Upload-URL angefordert. Anschließend wird die Datei direkt per `PUT` zu Google Cloud Storage übertragen.

```bash
cp .env.example .env
export LS_TENANT_ID="DEIN_TENANT"
export LS_EMAIL="DEINE_EMAIL"
export LS_PASSWORD="DEIN_PASSWORT"

python scripts/upload_learningsuite_image.py course-image \
  --node-id "<COURSE_NODE_ID>" \
  --file "./kursbild.png"
```

Verfügbare Ziele:

- `course-image`
- `course-thumbnail-bg`
- `topic-image`
- `module-thumbnail-bg`
- `lesson-image`

Weitere Details: [`docs/uploads.md`](docs/uploads.md).

## Sicherheit

- Zugangsdaten gehören ausschließlich in Make-Connections oder Umgebungsvariablen.
- Tokens, Passwörter, signierte Upload-URLs und lokale `.env`-Dateien dürfen nicht committed werden.
- Node IDs und SIDs müssen entsprechend ihrer dokumentierten Verwendung eingesetzt werden.
- Beim GCP-Upload darf kein LearningSuite-Bearer-Token mitgesendet werden.

## Status

Die LearningSuite-GraphQL-Schnittstelle ist nicht offiziell dokumentiert. `verified`-Operationen wurden grundlegend bestätigt; als `observed` markierte Upload-Operationen benötigen noch automatisierte Ende-zu-Ende-Tests.
