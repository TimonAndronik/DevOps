# Task Tracker

Простий навчальний web-додаток для лабораторних робіт з Docker та Docker Compose.

## Що тут є

- **Frontend**: статичний HTML/CSS/JS інтерфейс
- **Backend**: FastAPI REST API
- **Database**: PostgreSQL
- **Тести**: pytest + FastAPI TestClient
- **Контейнеризація**: Dockerfile для frontend та backend, `docker-compose.yml` для всього стеку

## Чому цей проєкт підходить під вимоги лабораторної

1. Реалізований на зручному стеку: **Python + FastAPI + PostgreSQL + JavaScript**
2. Це **web-додаток**, що працює з **базою даних PostgreSQL**
3. Є **інтеграційні тести** для API
4. Складається з **кількох частин**:
   - frontend
   - backend
   - database

## Структура

```text
task-tracker/
├── backend/
│   ├── app/
│   │   ├── crud.py
│   │   ├── db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── tests/
│   │   └── test_api.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.js
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

Після запуску:

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Запуск тестів локально

Перейдіть у папку backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # Linux / macOS
pip install -r requirements.txt
pytest
```

## Основні API endpoints

- `GET /health` — перевірка сервісу
- `GET /tasks` — список задач
- `POST /tasks` — створити задачу
- `PUT /tasks/{id}` — оновити задачу
- `DELETE /tasks/{id}` — видалити задачу

## Як залити на GitHub

```bash
git init
git add .
git commit -m "Initial commit: task tracker with Docker"
git branch -M main
git remote add origin https://github.com/<your-username>/task-tracker.git
git push -u origin main
```

## Ідеї для наступних лабораторних

- Додати авторизацію
- Винести повідомлення/черги в Redis
- Розбити backend на декілька мікросервісів
- Додати CI/CD через GitHub Actions
