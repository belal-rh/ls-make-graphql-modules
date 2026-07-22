# AddSection

Erstellt eine weitere Sektion innerhalb eines bestehenden Moduls (`Topic`).

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-SECTION-001` |
| Objekt | Section / Topic |
| Typ | Mutation / CREATE |
| Status | `verified` |
| Operation Name | `AddSection` |
| Persisted Query Hash | `729bbd9af3894f4950dd0823350975645c2834fe4303c92c25350f0316a7f2ac` |
| Letzte Bestätigung | 2026-07-20 |

## Vorbedingung

1. Modul über `CoursePaths` ermitteln.
2. Aktuelle Sektionen über `TopicQuery` laden.
3. Prüfen, ob die gewünschte Sektion bereits existiert.

## Parameter

| Name | Typ | Pflicht | ID-Typ | Beschreibung |
|---|---|---:|---|---|
| `topicId` | String | Ja | Node ID | Base64-ID des Moduls |
| `data.name` | String | Ja | – | Name der neuen Sektion |
| `data.description` | String | Nein | – | Optionale Beschreibung |
| `data.lessonsDoneOneByOne` | Boolean | Ja | – | Legt fest, ob Lektionen nacheinander abgeschlossen werden müssen |

## Vollständiger Request

```json
{
  "operationName": "AddSection",
  "variables": {
    "topicId": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
    "data": {
      "name": "Weitere Sektion",
      "description": "Optionale Beschreibung",
      "lessonsDoneOneByOne": false
    }
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "729bbd9af3894f4950dd0823350975645c2834fe4303c92c25350f0316a7f2ac"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "createSection": {
      "__typename": "Topic",
      "id": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
      "sections": [
        {
          "id": "U2VjdGlvbjpjbW8xcjVmemIxYzB5OTYwMWJwcDNhcGNt",
          "name": "Erste Sektion"
        },
        {
          "id": "U2VjdGlvbjpabW8xcjVmemIxYzB5OTYwMWJwcDNhcGNt",
          "name": "Weitere Sektion"
        }
      ]
    }
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Aktualisiertes Modul | `data.createSection` | Topic Object |
| Topic Node ID | `data.createSection.id` | Node ID |
| Alle Sektionen | `data.createSection.sections` | Array |
| Section Node IDs | `data.createSection.sections[].id` | Node ID |

## Wichtiger Hinweis

Die API gibt das vollständige Sektions-Array zurück und nicht ausschließlich die neu erstellte Sektion. Die neue Section Node ID muss daher anhand eines eindeutigen Namens oder durch Vergleich mit dem Zustand vor der Mutation ermittelt werden.

## Nachgelagerte Schritte

- `TopicQuery` erneut ausführen.
- Neue Section Node ID dauerhaft speichern.
- Erst danach Lektionen mit `AddLesson` erstellen.
