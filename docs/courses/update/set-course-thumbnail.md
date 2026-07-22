# SetCourseThumbnail

Setzt ein automatisch generiertes Kurs-Thumbnail anhand eines LearningSuite-Presets und strukturierter Textinhalte.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-006` |
| Objekt | Course |
| Typ | Mutation / UPDATE |
| Status | `verified` |
| Operation Name | `SetCourseThumbnail` |
| Persisted Query Hash | `9547b4268d57319d17a265dbc15e994b2efe11e6a6e08e07ad7669874b04576e` |
| Letzte Bestätigung | 2026-07-20 |

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `courseId` | Node ID | Ja | Base64-ID des Kurses |
| `thumbnailId` | Node ID | Ja | ID des Thumbnail-Presets |
| `content.overline` | String | Ja | Kleine Textzeile oberhalb des Haupttexts |
| `content.text` | Array | Ja | Textsegmente mit `text` und `highlight` |

## Vollständiger Request

```json
{
  "operationName": "SetCourseThumbnail",
  "variables": {
    "courseId": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=",
    "thumbnailId": "<THUMBNAIL_PRESET_NODE_ID>",
    "content": {
      "text": [
        { "text": "Grundlagen für ", "highlight": false },
        { "text": "Unternehmer", "highlight": true }
      ],
      "overline": "Modul 1"
    }
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "9547b4268d57319d17a265dbc15e994b2efe11e6a6e08e07ad7669874b04576e"
    }
  }
}
```

## Beobachtete Antwortstruktur

```json
{
  "data": {
    "setCourseThumbnail": {
      "__typename": "Course",
      "id": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI="
    }
  }
}
```

## Response-Pfade

- Kurs: `data.setCourseThumbnail`
- Course Node ID: `data.setCourseThumbnail.id`

## Voraussetzungen

Die Preset-ID muss vorab aus der LearningSuite-Oberfläche oder einem künftig dokumentierten Preset-FETCH-Call ermittelt werden. Die operation erzeugt das Bild serverseitig; es ist kein Binär-Upload erforderlich.