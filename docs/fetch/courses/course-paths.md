# CoursePaths

Lädt alle Module eines Kurses. LearningSuite bezeichnet Module intern als `Topics`.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-003` |
| Objekt | Course / Topic |
| Typ | Query / FETCH |
| Status | `verified` |
| Operation Name | `CoursePaths` |
| Persisted Query Hash | `dcb1132ae4701875b7ce74fc38afd5ae97ea08df83c06959bff99f3ebe28227b` |
| Letzte Bestätigung | 2026-07-20 |

## Parameter

| Name | Typ | Pflicht | ID-Typ | Beschreibung |
|---|---|---:|---|---|
| `courseSid` | String | Ja | SID | Kurze ID des Kurses |

```json
{
  "courseSid": "t1bDr7Bd"
}
```

## Vollständiger Request

```json
{
  "operationName": "CoursePaths",
  "variables": {
    "courseSid": "t1bDr7Bd"
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "dcb1132ae4701875b7ce74fc38afd5ae97ea08df83c06959bff99f3ebe28227b"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "course": {
      "id": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=",
      "modules": [
        {
          "module": {
            "id": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
            "sid": "aB3x9QpL",
            "name": "Modul 1: Grundlagen",
            "description": "Kurzbeschreibung des Moduls"
          }
        }
      ]
    }
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Kurs | `data.course` | Object |
| Course Node ID | `data.course.id` | Node ID |
| Module | `data.course.modules` | Array |
| Topic Node ID | `data.course.modules[].module.id` | Node ID |
| Topic SID | `data.course.modules[].module.sid` | SID |
| Modulname | `data.course.modules[].module.name` | String |
| Modulbeschreibung | `data.course.modules[].module.description` | String |

## Typischer Einsatz

- Module eines Kurses inventarisieren
- vorhandenes Modul anhand Name oder SID finden
- Topic Node ID für `TopicQuery`, `EditTopic` oder Sektions-Mutationen ermitteln
- doppelte Module vor `AddTopicToCourse` vermeiden

## Wichtiger Hinweis

Die Module liegen innerhalb eines Wrapper-Objekts:

```text
data.course.modules[].module
```

Generatoren und Make-Module müssen diesen zusätzlichen Pfad berücksichtigen.
