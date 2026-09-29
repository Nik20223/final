# Структура проекта `restful_booker_tests`

Комплексная автоматизация тестирования UI и API платформы Restful Booker:
`pytest` + Selenium (Page Object Model) + `requests` + Allure, CI/CD через Jenkins.

```text
restful_booker_tests/
├── config/
│   └── config.py              # URL, таймауты, креды
├── pages/                     # Page Object Model для UI
│   ├── base_page.py           # Базовые методы (клик, ввод, ожидания)
│   ├── login_page.py
│   ├── booking_page.py
│   └── room_page.py
├── api/                       # Хелперы для API
│   ├── api_client.py          # Обёртка над requests
│   ├── auth_api.py            # POST /auth
│   └── booking_api.py         # CRUD /booking
├── tests/
│   ├── ui/
│   │   ├── test_login_ui.py
│   │   ├── test_booking_ui.py
│   │   └── test_rooms_ui.py
│   └── api/
│       ├── test_auth_api.py
│       ├── test_booking_api.py
│       └── test_health_api.py
├── utils/
│   ├── driver_factory.py      # Создание WebDriver
│   └── data_generator.py      # Генерация тестовых данных (Faker)
├── conftest.py                # Фикстуры: драйвер, API-клиент, скриншоты при падении
├── pytest.ini                 # Маркеры (ui, api, smoke, regression)
├── requirements.txt
├── Jenkinsfile                # Pipeline для Jenkins
└── allure-results/            # Результаты прогона (в .gitignore)
```

## Примечания

- Все `.py`-файлы, `pytest.ini`, `requirements.txt` и `Jenkinsfile` созданы пустыми заглушками (0 байт) и наполняются по мере реализации.
- Каталог `allure-results/` добавлен в `.gitignore`; в репозитории он удерживается файлом `.gitkeep`.
