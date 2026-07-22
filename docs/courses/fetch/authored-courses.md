# AuthoredCourses

Lädt alle verfügbaren bzw. selbst erstellten Kurse des aktuellen LearningSuite-Tenants. Die Operation eignet sich für das initiale Mapping von Course Node IDs und SIDs.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-001` |
| Objekt | Course |
| Typ | Query / FETCH |
| Status | `verified` |
| Operation Name | `AuthoredCourses` |
| Persisted Query Hash | `a70e28d2b8370d93ce039c75abe29c0ed646259d799d1522bf31e0c22b813c0b` |
| Letzte Bestätigung | 2026-07-20 |

## Parameter

Keine Variablen erforderlich.

```json
{}
```

## Vollständiger Request

```json
{
  "operationName": "AuthoredCourses",
  "variables": {},
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "a70e28d2b8370d93ce039c75abe29c0ed646259d799d1522bf31e0c22b813c0b"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "authoredCourses": [
      {
        "id": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=",
        "sid": "t1bDr7Bd",
        "name": "Mein Erster Kurs",
        "isPublished": true
      }
    ]
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Kurse | `data.authoredCourses` | Array |
| Course Node ID | `data.authoredCourses[].id` | Node ID |
| Course SID | `data.authoredCourses[].sid` | SID |
| Kursname | `data.authoredCourses[].name` | String |
| Veröffentlicht | `data.authoredCourses[].isPublished` | Boolean |

## Typischer Einsatz

- Kursmapping initialisieren
- vorhandenen Kurs anhand Name oder SID suchen
- Node ID für spätere Mutationen ermitteln
- Duplikate vor `AddCourse` vermeiden

## Fehlerbehandlung

Neben dem HTTP-Status muss geprüft werden, ob `errors` in der GraphQL-Antwort enthalten ist. Bei `PersistedQueryNotFound` ist der Hash erneut über einen aktuellen RAW-Request zu ermitteln.
