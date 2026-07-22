# EditSection

Aktualisiert eine bestehende Sektion innerhalb eines Moduls.

## Metadaten

| Feld | Wert |
|---|---|
| Dokumentations-ID | `LS-SECTION-002` |
| Objekt | Section |
| Typ | Mutation / UPDATE |
| Status | `verified` |
| Operation Name | `EditSection` |
| Persisted Query Hash | `b875f283e6678a486f47aec32cda3eada719c2f8cfd12614fc2af6fe06f0d6f0` |
| Letzte Bestätigung | 2026-07-20 |

## Preflight

`TopicQuery` ausführen, um die Section Node ID sowie Name, Beschreibung und vorhandene Lektionen zu laden.

## Parameter

| Name | Typ | Pflicht | Beschreibung |
|---|---|---:|---|
| `editSection.id` | Node ID | Ja | Base64-ID der Sektion |
| `editSection.name` | String | Ja | Sektionsname |
| `editSection.description` | String | Nein | Beschreibung |
| `editSection.lessonsDoneOneByOne` | Boolean | Ja | Lektionen müssen nacheinander abgeschlossen werden |

## Vollständiger Request

```json
{
  "operationName": "EditSection",
  "variables": {
    "editSection": {
      "id": "U2VjdGlvbjpabW8xcjVmemIxYzB5OTYwMWJwcDNhcGNt",
      "name": "Neuer Sektionsname",
      "description": "Neue Beschreibung",
      "lessonsDoneOneByOne": false
    }
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "b875f283e6678a486f47aec32cda3eada719c2f8cfd12614fc2af6fe06f0d6f0"
    }
  }
}
```

## Beispielantwort

```json
{
  "data": {
    "editSection": {
      "__typename": "Section",
      "id": "U2VjdGlvbjpabW8xcjVmemIxYzB5OTYwMWJwcDNhcGNt",
      "name": "Neuer Sektionsname",
      "description": "Neue Beschreibung"
    }
  }
}
```

## Response-Pfade

- Sektion: `data.editSection`
- Section Node ID: `data.editSection.id`
- Name: `data.editSection.name`
- Beschreibung: `data.editSection.description`

## Verifizierung

Nach dem Update `TopicQuery` erneut ausführen und die Sektion anhand ihrer Node ID prüfen.