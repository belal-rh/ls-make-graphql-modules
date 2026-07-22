# Bilder und Datei-Uploads

LearningSuite-Bilduploads unterscheiden sich von normalen GraphQL-Mutationen. Der Ablauf besteht aus zwei Requests.

## Schritt 1: UploadSpec anfordern

Eine Persisted-Query-Mutation wird mit der Node ID des Zielobjekts ausgeführt. Die GraphQL-Antwort enthält ein `UploadSpec`.

Beobachtete Felder:

```json
{
  "__typename": "UploadSpec",
  "id": "<INTERNAL_ID>",
  "requestHeaders": {
    "x-goog-meta-flags": "convert"
  },
  "uploadUrl": "https://storage.googleapis.com/..."
}
```

Die signierte URL ist zeitlich begrenzt und darf nicht gespeichert oder wiederverwendet werden.

## Schritt 2: Binärdatei hochladen

Die Datei wird per `PUT` direkt an `uploadUrl` gesendet. Sämtliche Werte aus `requestHeaders` müssen unverändert übernommen werden.

```bash
curl --request PUT \
  --url "<UPLOAD_URL>" \
  --header "Content-Type: image/png" \
  --header "x-goog-meta-flags: convert" \
  --data-binary "@thumbnail.png"
```

## Verarbeitungshinweise

- Kein LearningSuite-Bearer-Token beim GCP-Upload mitsenden.
- Keine GraphQL-URL für Schritt 2 verwenden.
- Redirects nur zulassen, wenn der verwendete HTTP-Client die Upload-Methode und Header beibehält.
- `uploadUrl`, Authorization-Header und Zugangsdaten in Logs maskieren.
- Die Datei sollte vollständig in den Request-Body geschrieben werden; kein JSON und kein Base64-Wrapper.
- Erfolg des PUT-Requests anhand des HTTP-Status prüfen.
- Anschließend das Zielobjekt erneut abrufen oder in der LearningSuite-Oberfläche verifizieren.

## Status

Die GraphQL-Requests und UploadSpec-Struktur wurden im Browser beobachtet. Die Operationen sind daher zunächst als `observed` klassifiziert, bis automatisierte Ende-zu-Ende-Tests für alle Bildtypen vorhanden sind.