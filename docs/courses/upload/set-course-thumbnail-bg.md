# SetCourseThumbnailBG

Fordert eine signierte Upload-URL für das Hintergrundbild eines Kurs-Thumbnails an. Der Binär-Upload erfolgt anschließend direkt zu Google Cloud Storage.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-008` |
| Objekt | Course |
| Typ | Mutation / UPLOAD PREPARE |
| Status | `observed` |
| Operation Name | `SetCourseThumbnailBG` |
| Persisted Query Hash | `8696c20b2d6f76cf22e9b1cdc5633b662a5e6fdffaccf405c93846474da076e2` |

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `courseId` | Node ID | Ja | Base64-ID des Kurses |

## GraphQL-Request

```json
{
  "operationName": "SetCourseThumbnailBG",
  "variables": {
    "courseId": "Q291cnNlOmNtbzcwOG5rcDAwbzNveDAxc25oZGVnMHQ="
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "8696c20b2d6f76cf22e9b1cdc5633b662a5e6fdffaccf405c93846474da076e2"
    }
  }
}
```

## UploadSpec

Beobachteter bzw. zu bestätigender Root-Pfad: `data.setCourseThumbnailBGImage`.

Relevante Felder:

- `id`
- `requestHeaders`
- `uploadUrl`

## Zweiter Schritt

Bilddatei per `PUT` an `uploadUrl` senden. Die gelieferten Header, insbesondere mögliche `x-goog-meta-flags`, unverändert übernehmen. Siehe [`../../uploads.md`](../../uploads.md).

## Abgrenzung

`SetCourseThumbnail` generiert ein Thumbnail aus Preset und Text. `SetCourseThumbnailBG` bereitet dagegen den Upload einer echten Hintergrundbilddatei vor.