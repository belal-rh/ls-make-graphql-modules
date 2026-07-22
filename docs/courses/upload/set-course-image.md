# SetCourseImage

Fordert eine signierte Upload-URL für das Hauptbild eines Kurses an. Der eigentliche Datei-Upload erfolgt anschließend per HTTP `PUT`.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-COURSE-007` |
| Objekt | Course |
| Typ | Mutation / UPLOAD PREPARE |
| Status | `observed` |
| Operation Name | `SetCourseImage` |
| Persisted Query Hash | `f2cf01baef20d81055fba0c2a6164b9d74973b42fd0eb26f7161fa4bff3e36de` |

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `courseId` | Node ID | Ja | Base64-ID des Kurses |

## GraphQL-Request

```json
{
  "operationName": "SetCourseImage",
  "variables": {
    "courseId": "Q291cnNlOmNtbzcwOG5rcDAwbzNveDAxc25oZGVnMHQ="
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "f2cf01baef20d81055fba0c2a6164b9d74973b42fd0eb26f7161fa4bff3e36de"
    }
  }
}
```

## UploadSpec

Erwarteter Root-Pfad: `data.setCourseImage`

Relevante Felder:

- `data.setCourseImage.id`
- `data.setCourseImage.requestHeaders`
- `data.setCourseImage.uploadUrl`

## Zweiter Schritt

Die Bilddatei mit `PUT` an `uploadUrl` senden und alle gelieferten `requestHeaders` übernehmen. Siehe [`../../uploads.md`](../../uploads.md).

## Verifizierung

Kurs nach dem Upload erneut über `CourseInfoQuery` bzw. die LearningSuite-Oberfläche prüfen.