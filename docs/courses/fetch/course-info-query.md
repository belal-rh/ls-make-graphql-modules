# CourseInfoQuery

Lädt die Detailinformationen eines einzelnen Kurses. Die Operation ist besonders wichtig, um Summary und Rich-Text-Beschreibung vor einem Update zu prüfen.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-002` |
| Objekt | Course |
| Typ | Query / FETCH |
| Status | `verified` |
| Operation Name | `CourseInfoQuery` |
| Persisted Query Hash | `a7d1b550276e5621430a8a9fe646ed7d91178232bce12b72923265d89ace0240` |
| Letzte Bestätigung | 2026-07-20 |

## Parameter

| Name | Typ | Pflicht | ID-Typ | Beschreibung |
|---|---|---:|---|---|
| `courseSid` | String | Ja | SID | Kurze ID des Kurses |

## Vollständiger Request

```json
{
  "operationName": "CourseInfoQuery",
  "variables": {
    "courseSid": "t1bDr7Bd"
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "a7d1b550276e5621430a8a9fe646ed7d91178232bce12b72923265d89ace0240"
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
      "sid": "t1bDr7Bd",
      "name": "Mein Erster Kurs",
      "summary": "Das ist die Kurzzusammenfassung",
      "descriptionRichText": [
        {
          "type": "paragraph",
          "children": [{ "text": "Dies ist die ausführliche Beschreibung." }]
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
| Course SID | `data.course.sid` | SID |
| Kursname | `data.course.name` | String |
| Summary | `data.course.summary` | String |
| Beschreibung | `data.course.descriptionRichText` | Rich-Text-Array |

## Typischer Einsatz

- bestehende Kursbeschreibung vor `UpdateCourse` laden
- aktuelle Summary prüfen
- Node ID aus einer bekannten SID ermitteln
- Kursdaten für Synchronisationen vergleichen

## Wichtiger Hinweis

`descriptionRichText` ist kein einfacher String. Die bestehende Array-Struktur sollte vor einem Update vollständig berücksichtigt werden, damit Formatierungen nicht versehentlich verloren gehen.
