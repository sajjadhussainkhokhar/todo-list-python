# Copilot instructions for this repository

This document gives targeted, actionable context for AI coding assistants working on this Django project.

Key overview
- This is a small Django project (Django 5.x) with two main apps: `books` and `tasks`.
- REST framework (DRF) + Simple JWT are used for APIs (`rest_framework`, `rest_framework_simplejwt`).
- `books` exposes function-based DRF views and also hosts the JWT token endpoints.
- `tasks` uses DRF generic class-based views and enforces per-user filtering in `get_queryset` and `perform_create`.

Important files to read first
- `myproject/settings.py` — app list (`books`, `tasks`), middleware, REST_FRAMEWORK auth class, and DB config (currently set to MySQL). Check DEBUG/SECRET_KEY before making environment assumptions.
- `myproject/urls.py` — root URL routing. Note `books` is included at `books/`, while `tasks` is included under `api/tasks/`.
- `books/` (models.py, views.py, serializers.py, urls.py, templates/) — small function-based API (example: `book_list`, `book_detail`) and token endpoints (`api/token/`).
- `tasks/` (models.py, serializers.py, views.py, urls.py) — class-based views: `TaskListView`, `TaskCreateView`, `TaskDetailView` with per-user filtering; `TaskSerializer` marks `user` read-only.

Authentication & API patterns
- JWT auth is required for API endpoints: `DEFAULT_AUTHENTICATION_CLASSES` uses `rest_framework_simplejwt.authentication.JWTAuthentication`.
- To obtain a token (login) POST to `/books/api/token/` (this repo places token endpoints under the `books` app).
- Example token request (JSON): `{ "username": "...", "password": "..." }`. Use the returned `access` token in `Authorization: Bearer <token>`.
- `books` endpoints are function-based with explicit `@permission_classes([IsAuthenticated])` decorators. `tasks` endpoints rely on `permission_classes` attribute.

Routing inconsistencies to be aware of
- Token endpoints live at `/books/api/token/` while task APIs are under `/api/tasks/` — watch for this when composing URLs in tests or docs.

Data model & serializer conventions
- `books.models.Book` fields: `title`, `author`, `published_year`. Serializer: `BookSerializer` uses `ModelSerializer` with `fields='__all__'`.
- `tasks.models.Task` contains `user` FK (to `auth.User`) and several choice fields; `TaskSerializer` sets `user` as read-only and `perform_create` in the view assigns `self.request.user`.

Developer workflows & commands
- Run checks locally (no DB migration required for a quick static check):
  - `python3 manage.py check`
- Run tests (note: settings point to MySQL by default). If you don't have MySQL available, run tests by overriding DB in the environment or settings (e.g., create a temporary `settings_test.py` that uses SQLite or set `DJANGO_DB_ENGINE=...` before running). Basic command:
  - `python3 manage.py test`
- Run dev server (ensure DB is configured or use a lightweight sqlite override):
  - `python3 manage.py runserver`

Examples from the codebase
- Token (login) endpoint: `books/urls.py` registers `path('api/token/', TokenObtainPairView.as_view(), ...)`.
- `books.views.book_list` shows the function-based DRF pattern with `@api_view(['GET','POST'])` and serializer validation.
- `tasks.views.TaskCreateView.perform_create` demonstrates assigning `user` from `self.request.user` instead of expecting client to provide it.

Project-specific conventions
- Prefer DRF serializers + ModelSerializer with `fields='__all__'` for simple models (both apps follow this).
- Do not assume `api/` prefix uniformly; check `myproject/urls.py` and app `urls.py` when constructing endpoints.
- Authentication state: treat all API endpoints as requiring JWT unless explicitly decorated otherwise.

Notes and gotchas
- `myproject/settings.py` currently contains a checked-in SECRET_KEY and MySQL credentials — treat these as non-authoritative and avoid publishing them; when running CI or tests, override DB/keys via env vars.
- Templates exist under `books/templates/books/` (e.g., `add_book.html`) for any server-rendered pages; API endpoints are used elsewhere.

If you need clarification
- Ask: which environment should be considered canonical (MySQL vs a local SQLite override) for running tests/CI? Also confirm preferred URL prefixes for newly-added APIs.

End of file
