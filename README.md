- **Frontend**: статичний HTML/CSS/JS інтерфейс
- **Backend**: FastAPI REST API
- **Database**: PostgreSQL
- **Тести**: pytest + FastAPI TestClient
- **Контейнеризація**: Dockerfile для frontend та backend, `docker-compose.yml` для всього стеку


## Запуск через Docker Compose
docker compose up --build

Після запуску:
- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Запуск тестів локально

Перейдіть у папку backend:
cd backend
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pytest

## Основні API endpoints
- `GET /health` — перевірка сервісу
- `GET /tasks` — список задач
- `POST /tasks` — створити задачу
- `PUT /tasks/{id}` — оновити задачу
- `DELETE /tasks/{id}` — видалити задачу
