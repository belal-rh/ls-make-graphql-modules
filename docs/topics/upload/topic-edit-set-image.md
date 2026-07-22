# TopicEditSetImage

Fordert eine signierte Upload-URL für das Hauptbild eines Moduls (`Topic`) an.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-TOPIC-006` |
| Objekt | Topic |
| Typ | Mutation / UPLOAD PREPARE |
| Status | `observed` |
| Operation Name | `TopicEditSetImage` |
| Persisted Query Hash | `06538877b15a180f42502d24f7ced1a2c0b0fcd86d887683d13c2292b1852451` |

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `topicId` | Node ID | Ja | Base64-ID des Moduls |

## GraphQL-Request

```json
{
  "operationName": "TopicEditSetImage",
  "variables": {
    "topicId": "VG9waWM6Y21vMXI4ZTdxMDBuamc2MDFkamtzcnhsYQ=="
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "06538877b15a180f42502d24f7ced1a2c0b0fcd86d887683d13c2292b1852451"
    }
  }
}
```

## Beobachtete Antwortstruktur

Root-Pfad: `data.setTopicImage`

```json
{
  "data": {
    "setTopicImage": {
      "__typename": "UploadSpec",
      "id": "<INTERNAL_ID>",
      "requestHeaders": {
        "x-goog-meta-flags": "convert"
      },
      "uploadUrl": "https://storage.googleapis.com/..."
    }
  }
}
```

## Zweiter Schritt

Datei per `PUT` an `uploadUrl` senden und alle gelieferten Header übernehmen. Siehe [`../../uploads.md`](../../uploads.md).

## Verifizierung

Modul nach dem Upload über `TopicQuery` oder die LearningSuite-Oberfläche prüfen.