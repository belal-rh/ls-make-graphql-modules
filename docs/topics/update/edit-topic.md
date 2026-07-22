# EditTopic

Aktualisiert ein bestehendes Modul (`Topic`). Beobachtet wurden Änderungen an Name und einfacher Textbeschreibung.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-TOPIC-004` |
| Objekt | Topic |
| Typ | Mutation / UPDATE |
| Status | `verified` |
| Operation Name | `EditTopic` |
| Persisted Query Hash | `5a49c91efbc2c8581ba26dda9f4768acbf47f0e83bc6d7a58c465dd3403c4dfd` |
| Letzte Bestätigung | 2026-07-20 |

## Preflight

`CoursePaths` und anschließend `TopicQuery` ausführen, um das Zielmodul, seine Node ID und die bestehende Struktur zu validieren.

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `editTopic.id` | Node ID | Ja | Base64-ID des Moduls |
| `editTopic.name` | String | Nein | Neuer Modulname |
| `editTopic.description` | String | Nein | Neue einfache Textbeschreibung |

Nur die zu ändernden Felder senden.

## Vollständiger Request

```json
{
  "operationName": "EditTopic",
  "variables": {
    "editTopic": {
      "id": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
      "description": "Aktualisierte Modul-Beschreibung"
    }
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "5a49c91efbc2c8581ba26dda9f4768acbf47f0e83bc6d7a58c465dd3403c4dfd"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "editTopic": {
      "__typename": "Topic",
      "id": "VG9waWM6Y21vMXI0eXo5MWMydDk2MDFucGk4eHpzaw==",
      "name": "Neues Modul",
      "description": "Aktualisierte Modul-Beschreibung"
    }
  }
}
```

## Response-Pfade

- Modul: `data.editTopic`
- Topic Node ID: `data.editTopic.id`
- Modulname: `data.editTopic.name`
- Beschreibung: `data.editTopic.description`

## Hinweis

Die Modulbeschreibung ist ein einfacher String und kein Rich-Text-Array.