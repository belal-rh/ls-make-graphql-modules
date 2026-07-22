# SetLessonImage

Fordert eine signierte Upload-URL für das Bild einer Lektion an.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-LESSON-002` |
| Objekt | Lesson |
| Typ | Mutation / UPLOAD PREPARE |
| Status | `observed` |
| Operation Name | `SetLessonImage` |
| Persisted Query Hash | `6498cfd61f61564acf8dad163e9a9fb31b7e144e3040ef6959d9b5f2ed968a6e` |

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `lessonId` | Node ID | Ja | Base64-ID der Lektion |

## GraphQL-Request

```json
{
  "operationName": "SetLessonImage",
  "variables": {
    "lessonId": "TGVzc29uOmNtbzFyZ2k1ODE3dXBlajAxbzQ4eTZyMXg="
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "6498cfd61f61564acf8dad163e9a9fb31b7e144e3040ef6959d9b5f2ed968a6e"
    }
  }
}
```

## Beobachtete Antwortstruktur

Root-Pfad: `data.setLessonImage`

```json
{
  "data": {
    "setLessonImage": {
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

Bilddatei per `PUT` an `uploadUrl` senden. Alle Werte aus `requestHeaders` müssen übernommen werden. Siehe [`../../uploads.md`](../../uploads.md).

## Verifizierung

Die Lektion anschließend über `TopicQuery` oder in der LearningSuite-Oberfläche prüfen.