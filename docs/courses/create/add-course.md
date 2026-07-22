# AddCourse

Erstellt einen neuen Kurs im aktuellen LearningSuite-Tenant.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-004` |
| Objekt | Course |
| Typ | Mutation / CREATE |
| Status | `verified` |
| Operation Name | `AddCourse` |
| Persisted Query Hash | `cc30311057ac58b722e109432dd275e82c7d26b2d217c6231d5825876525a990` |
| Letzte Bestätigung | 2026-07-20 |

## Vorbedingung

Vor der Erstellung sollte `AuthoredCourses` ausgeführt und anhand eines stabilen externen Schlüssels oder mindestens des Kursnamens geprüft werden, ob der Kurs bereits existiert.

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `courseCreationInput.name` | String | Ja | Name des neuen Kurses |
| `courseCreationInput.summary` | String | Nein | Kurze Kursbeschreibung |
| `courseCreationInput.descriptionRichText` | Array | Ja | LearningSuite-Rich-Text-Struktur |

## Vollständiger Request

```json
{
  "operationName": "AddCourse",
  "variables": {
    "courseCreationInput": {
      "name": "Test Kurs",
      "descriptionRichText": [
        {
          "type": "paragraph",
          "children": [{ "text": "" }]
        }
      ],
      "summary": ""
    }
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "cc30311057ac58b722e109432dd275e82c7d26b2d217c6231d5825876525a990"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "createCourse": {
      "__typename": "Course",
      "id": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=",
      "sid": "t1bDr7Bd"
    }
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Erstellter Kurs | `data.createCourse` | Object |
| Course Node ID | `data.createCourse.id` | Node ID |
| Course SID | `data.createCourse.sid` | SID |

## Nachgelagerte Schritte

1. Node ID und SID dauerhaft speichern.
2. Kurs über `CourseInfoQuery` verifizieren.
3. Erst danach Module mit `AddTopicToCourse` verknüpfen.

## Hinweise

- `descriptionRichText` muss als Array übertragen werden, nicht als einfacher String.
- Ein leerer Beschreibungstext sollte trotzdem als gültiger Absatz gesendet werden.
- Auch bei HTTP 200 muss `errors` geprüft werden.
