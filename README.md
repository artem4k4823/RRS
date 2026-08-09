<div align="center">

  <img src="https://raw.githubusercontent.com/artem4k4823/RRS/main/assets/logo.png" alt="RRS Logo" width="120" height="120" />

  <h1>🚀 RRS (RSS Reader & Service)</h1>

  <p>
    <b>Современная микросервисная платформа для агрегации RSS-лент, управления подписками и генерации RSS из обычных веб-ссылок.</b>
  </p>

  <p>
    <a href="https://github.com/artem4k4823/RRS/stargazers"><img src="https://img.shields.io/github/stars/artem4k4823/RRS?style=for-the-badge&logo=github&color=gold" alt="Stars"></a>
    <a href="https://github.com/artem4k4823/RRS/issues"><img src="https://img.shields.io/github/issues/artem4k4823/RRS?style=for-the-badge&color=red" alt="Issues"></a>
    <a href="https://github.com/artem4k4823/RRS/blob/main/LICENSE"><img src="https://img.shields.io/github/license/artem4k4823/RRS?style=for-the-badge&color=blue" alt="License"></a>
    <a href="https://github.com/artem4k4823/RRS/releases"><img src="https://img.shields.io/github/v/release/artem4k4823/RRS?style=for-the-badge&color=green" alt="Release"></a>
  </p>

  <h4>
    <a href="#-о-проекте">О проекте</a> •
    <a href="#-архитектура">Архитектура</a> •
    <a href="#-стек-технологий">Стек</a> •
    <a href="#-возможности">Возможности</a> •
    <a href="#-быстрый-старт">Быстрый старт</a> •
    <a href="#-дорожная-карта">Roadmap</a>
  </h4>

</div>

---

## 📌 О проекте

**RRS (RSS Reader & Service)** — это асинхронная микросервисная система, созданная для удобной работы с информационными потоками. Она сочетает в себе функции классического агрегатора RSS-новостей и интеллектуального генератора RSS-лент из обычных страниц сайтов (например, Habr и других ресурсов, где стандартная RSS-лента отсутствует или ограничена).

> 💡 **Идея:** Предоставить единый инструмент с современным веб-интерфейсом, который позволяет подписываться на любые RSS-источники, генерировать свои RSS-потоки из веб-ссылок, кешировать их в Redis и отслеживать работу всей системы через полноценный мониторинг Prometheus & Grafana.


### Компоненты системы:
- 🌐 **Frontend (Vue 3 + Vite):** Веб-клиент с дашбордом статей, генератором RSS-ссылок, управлением подписками и встроенным админ-разделом.
- ⚙️ **Backend Service (FastAPI):** Основной микросервис обработки API, управления подписками, агрегации RSS-постов, миграций Alembic, административной панели (SQLAdmin) и экспорта метрик Prometheus.
- 🔑 **Auth Service (FastAPI + RabbitMQ):** Выделенный сервисный микросервис для регистрации, аутентификации пользователей и выписки JWT-токенов.
- 🔄 **Link-to-RRS Generator:** Микросервис парсинга страниц сайтов (с использованием `BeautifulSoup4` и `aiohttp`) и генерации стандартных XML RSS-лент.
- 🐰 **RabbitMQ:** Брокер сообщений для асинхронного RPC-взаимодействия между микросервисами.
- ⚡ **Redis:** Быстрое кеширование сгенерированных RSS XML лент.
- 📊 **Observability Stack (Prometheus + Grafana + Loki + Alloy):** Сбор метрик сервисов, агрегация логов контейнеров и готовые аналитические дашборды.

---

## 🛠 Стек технологий

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi,vue,vite,js,postgres,redis,rabbitmq,docker,prometheus,grafana" alt="Tech Stack" />
  </a>
</p>

- **Backend:** Python 3.12+, FastAPI, AsyncIO, SQLAlchemy (Async), Alembic, SQLAdmin, fastfeedparser, BeautifulSoup4, httpx.
- **Frontend:** Vue 3, Vite, Vue Router, Axios.
- **Инфраструктура:** Docker, Docker Compose, PostgreSQL 17, Redis, RabbitMQ.
- **Мониторинг и логи:** Prometheus, Grafana, Loki, Grafana Alloy, `prometheus-fastapi-instrumentator`.

---

## ✨ Возможности

- 📡 **Агрегация RSS:** Сбор новостей и статей из любых классических RSS XML каналов.
- 🔗 **Генерация RSS из ссылок:** Преобразование обычных веб-страниц (например, статей с Habr) в полноценный RSS XML поток с поддержкой пагинации.
- ⚡ **Высокая производительность:** Полностью асинхронный стек на базе Python AsyncIO, FastAPI и Redis-кеширования.
- 🔐 **Безопасность:** Изолированный микросервис аутентификации, хеширование паролей, JWT авторизация.
- 🛠️ **Панель администратора:** Встроенная SQLAdmin панель для удобного управления пользователями, подписками и постом в БД.
- 📈 **Полная наблюдаемость:** Встроенная конечная точка `/metrics` для Prometheus, визуализация в Grafana и считывание логов через Loki + Alloy.

---

## 🚀 Быстрый старт

### Системные требования

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/)

### Запуск в Docker Compose (Рекомендуемый способ)

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/artem4k4823/RRS.git
cd RRS

# 2. Запустите все сервисы в Docker
docker-compose up --build -d
```

После запуска будут доступны следующие сервисы:

| Сервис | Назначение | URL / Порт |
| :--- | :--- | :--- |
| **Frontend** | Vue 3 SPA веб-интерфейс | [http://localhost:8080](http://localhost:8080) |
| **Backend API** | FastAPI Документация (Swagger) | [http://localhost:8082/docs](http://localhost:8082/docs) |
| **Link-to-RRS** | Микросервис генерации RSS | [http://localhost:8083/docs](http://localhost:8083/docs) |
| **Auth Service** | Микросервис авторизации | [http://localhost:8084/docs](http://localhost:8084/docs) |
| **Grafana** | Мониторинг и Дашборды | [http://localhost:3000](http://localhost:3000) *(admin / admin)* |
| **Prometheus** | Метрики системы | [http://localhost:9090](http://localhost:9090) |
| **PgAdmin** | Управление PostgreSQL БД | [http://localhost:5050](http://localhost:5050) |
| **RabbitMQ** | Панель управления брокером | [http://localhost:15672](http://localhost:15672) *(guest / guest)* |

---

## 🧪 Тестирование

Для запуска тестов Backend-сервиса локально:

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
pytest -v
```

---

## 🗺 Дорожная карта (Roadmap)

- [x] Архитектура FastAPI Backend и модели SQLAlchemy
- [x] Разработка Vue 3 Frontend дашборда и генератора
- [x] Выделение Auth-сервиса и асинхронного взаимодействия через RabbitMQ
- [x] Реализация микросервиса `link-to-rss` (парсер Habr и XML генератор)
- [x] Интеграция стека мониторинга и логов (Prometheus, Grafana, Loki, Alloy)
- [x] Поддержка SQLAdmin панелей администратора
- [ ] Расширение поддерживаемых сайтов для генератора (Medium, Reddit, Dev.to)


---

## 🤝 Вклад в проект (Contributing)

Мы всегда рады новым идеям и пулл-реквестам! Если вы хотите внести вклад:

1. Сделайте **Fork** проекта.
2. Создайте свою ветку фичи (`git checkout -b feature/AmazingFeature`).
3. Сделайте коммит изменений (`git commit -m 'Add some AmazingFeature'`).
4. Запушьте изменения (`git push origin feature/AmazingFeature`).
5. Откройте **Pull Request**.

---

<div align="center">

Разработано с ❤️ от [artem4k4823](https://github.com/artem4k4823)

⭐ *Не забудьте поставить звездочку репозиторию, если проект был вам полезен!*

</div>

