# FETCH-Operationen

Die FETCH-Phase dokumentiert alle bestätigten lesenden LearningSuite-Operationen.

## Ziel

Vor jeder Erstellung oder Änderung soll zunächst der aktuelle Zustand geladen werden. Dieses Prinzip verhindert Duplikate, falsche Objektzuordnungen und unbeabsichtigtes Überschreiben.

## Dokumentierte Calls

| Objekt | Operation | Dokumentation | YAML |
|---|---|---|---|
| Course | `AuthoredCourses` | [`courses/authored-courses.md`](courses/authored-courses.md) | [`../../operations/fetch/courses/authored-courses.yaml`](../../operations/fetch/courses/authored-courses.yaml) |
| Course | `CourseInfoQuery` | [`courses/course-info-query.md`](courses/course-info-query.md) | [`../../operations/fetch/courses/course-info-query.yaml`](../../operations/fetch/courses/course-info-query.yaml) |
| Course / Topic | `CoursePaths` | [`courses/course-paths.md`](courses/course-paths.md) | [`../../operations/fetch/courses/course-paths.yaml`](../../operations/fetch/courses/course-paths.yaml) |
| Topic | `TopicQuery` | [`topics/topic-query.md`](topics/topic-query.md) | [`../../operations/fetch/topics/topic-query.yaml`](../../operations/fetch/topics/topic-query.yaml) |

## Gemeinsamer Ablauf

1. Bearer-Token erzeugen
2. GraphQL-Endpunkt mit Tenant-ID aufrufen
3. `operationName`, `variables` und Persisted-Query-Hash senden
4. HTTP-Status prüfen
5. Zusätzlich `body.errors` prüfen
6. benötigte Node IDs und SIDs aus der Antwort übernehmen

## Noch nicht bestätigt

Folgende FETCH-Bereiche sollen später ergänzt werden, sobald belastbare RAW-Requests vorliegen:

- Modulbibliothek und Ordner
- Thumbnail-Presets
- einzelne Lektionsdetails
- Nutzer, Gruppen und Berechtigungen
