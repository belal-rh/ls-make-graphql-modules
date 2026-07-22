# SetModuleThumbnail

Setzt ein automatisch generiertes Modul-Thumbnail anhand eines LearningSuite-Presets.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-TOPIC-005` |
| Objekt | Topic |
| Typ | Mutation / UPDATE |
| Status | `verified` |
| Operation Name | `SetModuleThumbnail` |
| Persisted Query Hash | `fa2764b86629193cd84f19da0a4777f22011e2db9bdeb3e0263643fd738575a1` |
| Letzte Bestätigung | 2026-07-20 |

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `moduleId` | Node ID | Ja | Base64-ID des Moduls |
| `thumbnailId` | Node ID | Ja | ID des Thumbnail-Presets |
| `content.overline` | String | Ja | Kleine Textzeile oberhalb des Haupttexts |
| `content.text` | Array | Ja | Textsegmente mit `text` und `highlight` |

## Vollständiger Request

```json
{
  "operationName": "SetModuleThumbnail",
  "variables": {
    "moduleId": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
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
      "sha256Hash": "fa2764b86629193cd84f19da0a4777f22011e2db9bdeb3e0263643fd738575a1"
    }
  }
}
```

## Beobachtete Antwortstruktur

```json
{
  "data": {
    "setModuleThumbnail": {
      "__typename": "Topic",
      "id": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw=="
    }
  }
}
```

## Response-Pfade

- Modul: `data.setModuleThumbnail`
- Topic Node ID: `data.setModuleThumbnail.id`

## Voraussetzungen

Die Preset-ID muss vorab bekannt sein. Im Unterschied zu `SetModuleThumbnailBG` wird das Thumbnail serverseitig aus Preset und Text erzeugt; es ist kein Datei-Upload erforderlich.