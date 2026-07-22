# CreateTopic

Erstellt ein eigenständiges Modul (`Topic`) in der LearningSuite-Modulbibliothek. Das Modul wird dabei noch nicht zwingend einem Kurs zugeordnet.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-TOPIC-002` |
| Objekt | Topic |
| Typ | Mutation / CREATE |
| Status | `observed` |
| Operation Name | `CreateTopic` |
| Persisted Query Hash | `cc092ff870aa21654e2a2cb7c790c0d9e8fdc9ac64ab1aaaedfa0cc19ab33cdf` |
| Quelle | Im Browser erfasster RAW-Request |

## Abgrenzung

- `CreateTopic` erstellt ein eigenständiges Bibliotheksmodul.
- `AddTopicToCourse` erstellt ein Modul direkt im Kontext eines Kurses.

Diese Abgrenzung basiert auf den beobachteten Requests und sollte bei Änderungen der LearningSuite-Oberfläche erneut validiert werden.

## Parameter

| Name | Typ | Pflicht | ID-Typ | Beschreibung |
|---|---|---:|---|---|
| `name` | String | Ja | – | Modulname |
| `description` | String | Nein | – | Einfache Modulbeschreibung |
| `folderId` | String / Null | Unklar | Node ID | Zielordner der Modulbibliothek; Null-Verhalten noch nicht abschließend getestet |
| `sectionName` | String | Ja | – | Name der initialen Sektion |

## Vollständiger Request

```json
{
  "operationName": "CreateTopic",
  "variables": {
    "name": "Neues Bibliotheksmodul",
    "description": "Kurze Beschreibung",
    "folderId": "<FOLDER_NODE_ID>",
    "sectionName": "Erste Sektion"
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "cc092ff870aa21654e2a2cb7c790c0d9e8fdc9ac64ab1aaaedfa0cc19ab33cdf"
    }
  }
}
```

## Beobachtete Antwort

```json
{
  "data": {
    "createTopic": {
      "id": "VG9waWM6Y21yc3preTFuMDhpalzAxZ3duNWRnd2g=",
      "name": "Neues Bibliotheksmodul"
    }
  }
}
```

## Response-Pfade

| Feld | Pfad | Typ |
|---|---|---|
| Erstelltes Modul | `data.createTopic` | Object |
| Topic Node ID | `data.createTopic.id` | Node ID |
| Modulname | `data.createTopic.name` | String |

## Nachgelagerte Schritte

1. Topic Node ID speichern.
2. Bibliothekszuordnung und initiale Sektion im UI oder über einen passenden FETCH-Call verifizieren.
3. Falls das Modul einem Kurs zugeordnet werden soll, den dafür beobachteten Zuordnungsprozess separat dokumentieren.

## Offene Validierung

- Ist `folderId` optional oder muss explizit `null` gesendet werden?
- Welche weiteren Felder liefert `createTopic` im vollständigen Response?
- Wird die initiale Sektion immer erzeugt?
