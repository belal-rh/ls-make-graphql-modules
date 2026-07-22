# TopicQuery

Lädt die vollständige Struktur eines Moduls einschließlich Sektionen und der darin enthaltenen Lektionen.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-TOPIC-001` |
| Objekt | Topic / Section / Lesson |
| Typ | Query / FETCH |
| Status | `verified` |
| Operation Name | `TopicQuery` |
| Persisted Query Hash | `b44496383040234ea01b5031834480ab3aa50435f4aa2f5ef8fa6f63ee7d285c` |
| Letzte Bestätigung | 2026-07-20 |

## Parameter

| Name | Typ | Pflicht | ID-Typ | Beschreibung |
|---|---|---:|---|---|
| `topicId` | String | Ja | Node ID | Base64-ID des Moduls |
| `courseSid` | String | Ja | SID | Kurze ID des zugehörigen Kurses |

```json
{
  "topicId": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
  "courseSid": "t1bDr7Bd"
}
```

## Vollständiger Request

```json
{
  "operationName": "TopicQuery",
  "variables": {
    "topicId": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
    "courseSid": "t1bDr7Bd"
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "b44496383040234ea01b5031834480ab3aa50435f4aa2f5ef8fa6f63ee7d285c"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "topic": {
      "id": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
      "sections": [
        {
          "id": "U2VjdGlvbjpjbW8xcjVmemIxYzB5OTYwMWJwcDNhcGNt",
          "name": "Sektion 1",
          "description": "Beschreibung der Sektion",
          "lessons": [
            {
              "id": "TGVzc29uOmNtbzFyNWwybzFjMTE5NjAxN2Z6OGd6Mno=",
              "name": "Lektion 1.1: Willkommen",
              "isPublished": true
            }
          ]
        }
      ]
    }
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Topic | `data.topic` | Object |
| Topic Node ID | `data.topic.id` | Node ID |
| Sektionen | `data.topic.sections` | Array |
| Section Node ID | `data.topic.sections[].id` | Node ID |
| Sektionsname | `data.topic.sections[].name` | String |
| Sektionsbeschreibung | `data.topic.sections[].description` | String |
| Lektionen | `data.topic.sections[].lessons` | Array |
| Lesson Node ID | `data.topic.sections[].lessons[].id` | Node ID |
| Lektionsname | `data.topic.sections[].lessons[].name` | String |
| Veröffentlicht | `data.topic.sections[].lessons[].isPublished` | Boolean |

## Typischer Einsatz

- vollständige Modulstruktur inventarisieren
- Section Node IDs für `AddLesson` oder `EditSection` ermitteln
- bestehende Lektionen vor einer Erstellung prüfen
- Reihenfolge und Vollständigkeit eines Moduls kontrollieren

## Wichtiger Hinweis

Die Query benötigt gleichzeitig die Topic Node ID und die Course SID. Beide Werte sollten zuvor über `CoursePaths` ermittelt bzw. validiert werden.
