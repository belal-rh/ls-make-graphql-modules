# Dokumentationskonventionen

## Zweck

Jede LearningSuite-Operation wird doppelt dokumentiert:

1. **Markdown** für Menschen
2. **YAML** als maschinenlesbare Quelle für Generatoren, Make-Module und Tests

## Persisted-Query-Struktur

```json
{
  "operationName": "NameDerOperation",
  "variables": {},
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "<HASH>"
    }
  }
}
```

## ID-Typen

### Node ID

Base64-codierte ID, beispielsweise:

```text
Q291cnNlOmNtbzFyNHRpazFiYnc5NjAxbmR6OTltYWI=
```

Node IDs werden insbesondere für Mutationen und Objektbeziehungen verwendet.

### SID

Kurze ID, beispielsweise:

```text
t1bDr7Bd
```

SIDs werden häufig für lesende Abfragen und Hierarchien verwendet.

## Statuswerte

- `verified`: Request wurde beobachtet und erfolgreich bestätigt.
- `observed`: Request wurde im Browser erfasst, aber noch nicht ausreichend getestet.
- `experimental`: Operation oder Feldstruktur ist noch unsicher.
- `deprecated`: Operation sollte nicht mehr verwendet werden.

## Namenskonventionen

- Markdown-Dateien: `kebab-case.md`
- YAML-Dateien: `kebab-case.yaml`
- GraphQL-Operationen: Originalname aus dem RAW-Request
- Interne Dokumentations-ID: `LS-<OBJEKT>-<NUMMER>`

Beispiele:

```text
LS-COURSE-001
LS-TOPIC-001
```

## Pflichtbestandteile je Operation

- Zweck
- Status
- Objekt
- Operationstyp
- `operationName`
- Persisted-Query-Hash
- Endpunkt
- Authentifizierung
- Parameter und ID-Typen
- vollständiger Request
- Beispielantwort
- relevante Response-Pfade
- Fehlerhinweise
- Datum der letzten Bestätigung

## Fehlerbehandlung

Ein GraphQL-Request kann HTTP-Status `200` liefern und dennoch fehlgeschlagen sein. Deshalb muss zusätzlich geprüft werden:

```text
body.errors ist leer
```

Bei folgendem Fehler muss der aktuelle RAW-Request erneut erfasst werden:

```text
PersistedQueryNotFound
```

## Fetch before Update

Vor Create- oder Update-Operationen soll der aktuelle Zustand geladen werden. Ziel:

- Duplikate vermeiden
- korrekte Node IDs und SIDs verwenden
- bestehende Inhalte nicht überschreiben
- Objektbeziehungen vor Mutationen validieren
