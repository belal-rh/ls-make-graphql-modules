# Authentifizierung

Bevor GraphQL-Operationen ausgeführt werden können, muss ein Bearer-Token erzeugt werden.

## Token-Endpunkt

```http
POST https://auth.learningsuite.io/auth/token
```

## Header

```http
Content-Type: application/json
x-tenant-id: <TENANT_ID>
```

## Request Body

```json
{
  "email": "user@example.com",
  "password": "SECRET"
}
```

## Beispiel mit cURL

```bash
curl --request POST \
  --url "https://auth.learningsuite.io/auth/token" \
  --header "Content-Type: application/json" \
  --header "x-tenant-id: DEINE_TENANT_ID" \
  --data '{
    "email": "DEINE_EMAIL",
    "password": "DEIN_PASSWORT"
  }'
```

## Erwartete Antwort

```json
{
  "access_token": "eyJ..."
}
```

Der zurückgegebene Token wird anschließend für GraphQL-Requests verwendet:

```http
Authorization: Bearer <ACCESS_TOKEN>
```

## GraphQL-Endpunkt

```http
POST https://api-p.learningsuite.io/{tenant_id}/graphql
```

## Sicherheit

- E-Mail, Passwort und Token niemals im Repository speichern.
- Zugangsdaten ausschließlich über Umgebungsvariablen, Secret Stores oder Make-Connections verwalten.
- Authorization-Header und Token in Logs maskieren.
- Der bisher dokumentierte Authentifizierungsweg verwendet keinen separaten permanenten API-Key.
