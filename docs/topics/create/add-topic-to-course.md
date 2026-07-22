# AddTopicToCourse

Erstellt ein neues Modul (`Topic`) direkt innerhalb eines bestehenden Kurses. LearningSuite legt dabei gleichzeitig eine erste Sektion an.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-TOPIC-003` |
| Objekt | Topic / Course |
| Typ | Mutation / CREATE |
| Status | `verified` |
| Operation Name | `AddTopicToCourse` |
| Persisted Query Hash | `4f527eaf6c524c2319bc1607a67ab52667028bd7f00d231e77dbd3ea4554b573` |
| Letzte Bestätigung | 2026-07-20 |

## Vorbedingung

1. Kurs über `AuthoredCourses` finden.
2. Course Node ID verwenden.
3. Über `CoursePaths` prüfen, ob ein Modul mit diesem Namen bereits existiert.

## Parameter

| Name | Typ | Pflicht | ID-Typ | Beschreibung |
|---|---|---:|---|---|
| `courseId` | String | Ja | Node ID | Base64-ID des Zielkurses |
| `name` | String | Ja | – | Modulname |
| `description` | String | Nein | – | Einfache Modulbeschreibung |
| `sectionName` | String | Ja | – | Name der automatisch angelegten ersten Sektion |

## Vollständiger Request

```json
{
  "operationName": "AddTopicToCourse",
  "variables": {
    "courseId": "Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=",
    "name": "Neues Modul",
    "description": "Kurze Beschreibung des Moduls",
    "sectionName": "Erste Sektion"
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "4f527eaf6c524c2319bc1607a67ab52667028bd7f00d231e77dbd3ea4554b573"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "addTopicToCourse": {
      "__typename": "Topic",
      "id": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
      "sid": "aB3x9QpL"
    }
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Erstelltes Modul | `data.addTopicToCourse` | Object |
| Topic Node ID | `data.addTopicToCourse.id` | Node ID |
| Topic SID | `data.addTopicToCourse.sid` | SID |

## Nachgelagerte Schritte

1. Topic Node ID und SID speichern.
2. `CoursePaths` erneut ausführen und die Kurszuordnung verifizieren.
3. `TopicQuery` ausführen, um die initiale Section Node ID zu ermitteln.
4. Danach weitere Sektionen oder Lektionen erstellen.

## Hinweise

- Modulbeschreibungen sind einfache Strings, kein Rich-Text-Array.
- Die erste Sektion wird zusammen mit dem Modul angelegt.
- Der Request erwartet die Course Node ID, nicht die Course SID.
