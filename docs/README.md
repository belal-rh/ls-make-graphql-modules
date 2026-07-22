# LearningSuite GraphQL – Dokumentationsindex

Die Dokumentation ist nach LearningSuite-Objekten organisiert. Innerhalb jedes Objekts werden die Operationen nach Aktion (`fetch`, `create`, später `update`) getrennt.

## Globale Grundlagen

- [Authentifizierung](authentication.md)
- [Dokumentationskonventionen](conventions.md)

## Courses

### FETCH

- [`AuthoredCourses`](courses/fetch/authored-courses.md) – alle Kurse abrufen
- [`CourseInfoQuery`](courses/fetch/course-info-query.md) – Kursdetails abrufen
- [`CoursePaths`](courses/fetch/course-paths.md) – Module eines Kurses abrufen

### CREATE

- [`AddCourse`](courses/create/add-course.md) – Kurs erstellen

## Topics / Module

### FETCH

- [`TopicQuery`](topics/fetch/topic-query.md) – Sektionen und Lektionen eines Moduls abrufen

### CREATE

- [`CreateTopic`](topics/create/create-topic.md) – eigenständiges Modul in der Bibliothek erstellen
- [`AddTopicToCourse`](topics/create/add-topic-to-course.md) – Modul direkt in einem Kurs erstellen

## Sections

### CREATE

- [`AddSection`](sections/create/add-section.md) – Sektion in einem Modul erstellen

## Lessons

### CREATE

- [`AddLesson`](lessons/create/add-lesson.md) – Lektion in einer Sektion erstellen

## Maschinenlesbare Definitionen

Zu jeder Markdown-Dokumentation existiert unter [`../operations/`](../operations/) eine YAML-Datei mit Hash, Variablen, Response-Pfaden und Make-Modul-Metadaten.

## Grundsatz

Vor jeder Mutation sollen die relevanten FETCH-Operationen ausgeführt werden. Damit werden korrekte Node IDs und SIDs verwendet und unnötige Duplikate vermieden.
