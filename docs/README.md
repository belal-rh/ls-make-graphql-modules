# LearningSuite GraphQL – Dokumentationsindex

Die Dokumentation ist nach LearningSuite-Objekten organisiert. Innerhalb jedes Objekts werden die Operationen nach Aktion (`fetch`, `create`, `update`, `upload`) getrennt.

## Globale Grundlagen

- [Authentifizierung](authentication.md)
- [Dokumentationskonventionen](conventions.md)
- [Bilder und Datei-Uploads](uploads.md)

## Courses

### FETCH

- [`AuthoredCourses`](courses/fetch/authored-courses.md) – alle Kurse abrufen
- [`CourseInfoQuery`](courses/fetch/course-info-query.md) – Kursdetails abrufen
- [`CoursePaths`](courses/fetch/course-paths.md) – Module eines Kurses abrufen

### CREATE

- [`AddCourse`](courses/create/add-course.md) – Kurs erstellen

### UPDATE

- [`UpdateCourse`](courses/update/update-course.md) – Kursname, Summary und Rich Text aktualisieren
- [`SetCourseThumbnail`](courses/update/set-course-thumbnail.md) – generiertes Preset-Thumbnail setzen

### UPLOAD

- [`SetCourseImage`](courses/upload/set-course-image.md) – Kursbild hochladen
- [`SetCourseThumbnailBG`](courses/upload/set-course-thumbnail-bg.md) – Thumbnail-Hintergrund hochladen

## Topics / Module

### FETCH

- [`TopicQuery`](topics/fetch/topic-query.md) – Sektionen und Lektionen eines Moduls abrufen

### CREATE

- [`CreateTopic`](topics/create/create-topic.md) – eigenständiges Modul in der Bibliothek erstellen
- [`AddTopicToCourse`](topics/create/add-topic-to-course.md) – Modul direkt in einem Kurs erstellen

### UPDATE

- [`EditTopic`](topics/update/edit-topic.md) – Modulname oder Beschreibung aktualisieren
- [`SetModuleThumbnail`](topics/update/set-module-thumbnail.md) – generiertes Preset-Thumbnail setzen

### UPLOAD

- [`TopicEditSetImage`](topics/upload/topic-edit-set-image.md) – Modulbild hochladen
- [`SetModuleThumbnailBG`](topics/upload/set-module-thumbnail-bg.md) – Thumbnail-Hintergrund hochladen

## Sections

### CREATE

- [`AddSection`](sections/create/add-section.md) – Sektion in einem Modul erstellen

### UPDATE

- [`EditSection`](sections/update/edit-section.md) – Sektion aktualisieren

## Lessons

### CREATE

- [`AddLesson`](lessons/create/add-lesson.md) – Lektion in einer Sektion erstellen

### UPLOAD

- [`SetLessonImage`](lessons/upload/set-lesson-image.md) – Lektionsbild hochladen

## Maschinenlesbare Definitionen

Zu jeder Markdown-Dokumentation existiert unter [`../operations/`](../operations/) eine YAML-Datei mit Hash, Variablen, Response-Pfaden, Preflight-Logik und Make-Modul-Metadaten.

## Status

- `verified`: Request und grundlegende Response-Struktur wurden bestätigt.
- `observed`: RAW-Request wurde erfasst, benötigt aber noch weitere Ende-zu-Ende-Tests.

Die Datei-Uploads sind als `observed` markiert. Sie bestehen aus einer GraphQL-Anfrage für das `UploadSpec` und einem anschließenden binären `PUT` an eine signierte Google-Cloud-URL.

## Grundsatz

Vor jeder Mutation sollen die relevanten FETCH-Operationen ausgeführt werden. Damit werden korrekte Node IDs und SIDs verwendet, bestehende Inhalte geschützt und unnötige Duplikate vermieden.