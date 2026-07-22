# UpdateCourse

Aktualisiert einen bestehenden Kurs. Über das `data`-Objekt können insbesondere Name, Summary und `descriptionRichText` geändert werden.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-005` |
| Objekt | Course |
| Typ | Mutation / UPDATE |
| Status | `verified` |
| Operation Name | `UpdateCourse` |
| Persisted Query Hash | `4149001c35a4454bc69fbc0231a22003d2692ca74d083567b69029fd5a4961e5` |
| Letzte Bestätigung | 2026-07-20 |

## Preflight

Vor dem Update sollte `CourseInfoQuery` ausgeführt werden. Dadurch werden die aktuelle Summary, die vorhandene Rich-Text-Struktur und die Course Node ID geladen.

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `data.id` | Node ID | Ja | Base64-ID des Kurses |
| `data.name` | String | Nein | Neuer Kursname |
| `data.summary` | String | Nein | Neue Kurzzusammenfassung |
| `data.descriptionRichText` | Array | Nein | Vollständige Rich-Text-Struktur |

Nur Felder senden, die tatsächlich geändert werden sollen.

## Vollständiger Request

```json
{
  "operationName": "UpdateCourse",
  "variables": {
    "data": {
      "id": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=",
      "summary": "Aktualisierte Kurzzusammenfassung",
      "descriptionRichText": [
        {
          "type": "paragraph",
          "children": [
            { "text": "Die neue, ausführliche Beschreibung." }
          ]
        }
      ]
    }
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "4149001c35a4454bc69fbc0231a22003d2692ca74d083567b69029fd5a4961e5"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "updateCourse": {
      "__typename": "Course",
      "id": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=",
      "name": "Test Kurs",
      "summary": "Aktualisierte Kurzzusammenfassung",
      "descriptionRichText": [
        {
          "type": "paragraph",
          "children": [
            { "text": "Die neue, ausführliche Beschreibung." }
          ]
        }
      ]
    }
  }
}
```

## Response-Pfade

- Kurs: `data.updateCourse`
- Course Node ID: `data.updateCourse.id`
- Kursname: `data.updateCourse.name`
- Summary: `data.updateCourse.summary`
- Beschreibung: `data.updateCourse.descriptionRichText`

## Wichtiger Hinweis

`descriptionRichText` wird vollständig ersetzt. Vorhandene Formatierungen, Links und weitere Rich-Text-Knoten müssen deshalb aus dem Ist-Zustand übernommen werden, sofern sie erhalten bleiben sollen.