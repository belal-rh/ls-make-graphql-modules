# SetModuleThumbnailBG

Fordert eine signierte Upload-URL für das Hintergrundbild eines Modul-Thumbnails an.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-TOPIC-007` |
| Objekt | Topic |
| Typ | Mutation / UPLOAD PREPARE |
| Status | `observed` |
| Operation Name | `SetModuleThumbnailBG` |
| Persisted Query Hash | `9ece459af9b322066a99dbc1f392bc8d89763b98788304fefce6455e4d0baba6` |

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `moduleId` | Node ID | Ja | Base64-ID des Moduls |

## GraphQL-Request

```json
{
  "operationName": "SetModuleThumbnailBG",
  "variables": {
    "moduleId": "VG9waWM6Y21vMXI4ZTdxMDBuamc2MDFkamtzcnhsYQ=="
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "9ece459af9b322066a99dbc1f392bc8d89763b98788304fefce6455e4d0baba6"
    }
  }
}
```

## Beobachtete Antwortstruktur

Root-Pfad: `data.setModuleThumbnailBGImage`

```json
{
  "data": {
    "setModuleThumbnailBGImage": {
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

Bilddatei per `PUT` an `uploadUrl` senden und die gelieferten Header unverändert übernehmen. Siehe [`../../uploads.md`](../../uploads.md).

## Abgrenzung

`SetModuleThumbnail` erzeugt ein Preset-Thumbnail. `SetModuleThumbnailBG` lädt eine echte Hintergrundbilddatei hoch.