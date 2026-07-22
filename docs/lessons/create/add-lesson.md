# AddLesson

Erstellt eine neue Lektion innerhalb einer bestehenden Sektion.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-LESSON-001` |
| Objekt | Lesson / Section |
| Typ | Mutation / CREATE |
| Status | `verified` |
| Operation Name | `AddLesson` |
| Persisted Query Hash | `644f5a8990fdb54d69e769c2921ce742119075e7d67e80bb5d141738296aa7e7` |
| Letzte Bestätigung | 2026-07-20 |

## Vorbedingung

1. Modulstruktur über `TopicQuery` laden.
2. Section Node ID der Zielsektion ermitteln.
3. Prüfen, ob bereits eine Lektion mit diesem Namen existiert.

## Parameter

| Name | Typ | Pflicht | ID-Typ | Beschreibung |
|---|---|---:|---|---|
| `sectionId` | String | Ja | Node ID | Base64-ID der Zielsektion |
| `name` | String | Ja | – | Name der neuen Lektion |

## Vollständiger Request

```json
{
  "operationName": "AddLesson",
  "variables": {
    "sectionId": "U2VjdGlvbjpjbW8xcjhlN3IwMG5rZzYwMWJ4MHZ1aTJn",
    "name": "Lektion Test"
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "644f5a8990fdb54d69e769c2921ce742119075e7d67e80bb5d141738296aa7e7"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "createLesson": {
      "__typename": "Lesson",
      "id": "TGVzc29uOmNtbzFyNWwybzFjMTE5NjAxN2Z6OGd6Mno=",
      "name": "Lektion Test",
      "description": ""
    }
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Erstellte Lektion | `data.createLesson` | Object |
| Lesson Node ID | `data.createLesson.id` | Node ID |
| Lektionsname | `data.createLesson.name` | String |
| Beschreibung | `data.createLesson.description` | String |

## Nachgelagerte Schritte

1. Lesson Node ID dauerhaft speichern.
2. `TopicQuery` erneut ausführen und die Zuordnung zur Sektion prüfen.
3. Inhalt, Veröffentlichung und weitere Lektionsfelder über separate Update-Operationen ergänzen.

## Hinweise

- `sectionId` ist eine Node ID, keine SID.
- Die Operation erstellt zunächst die Lektionshülle; Inhalt und Veröffentlichung können zusätzliche Mutationen erfordern.
- Auch bei HTTP 200 muss `errors` geprüft werden.
