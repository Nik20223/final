# Структура проекта `restful_booker_tests`

Комплексная автоматизация тестирования UI и API платформы Restful Booker:
`pytest` + Selenium (Page Object Model) + `requests` + Allure, непрерывная
интеграция через Jenkins.

Подробное описание проекта, разбор тестовых наборов, генерации данных и
конвейера — в `PROJECT_DESCRIPTION.md`. Развёртывание стенда и Jenkins — в
`deploy/README.md`.

```text
restful_booker_tests/
├── config/
│   └── config.py                     # адреса сервисов, таймауты, учётные данные
├── utils/
│   ├── driver_factory.py             # создание WebDriver (Chrome, Firefox)
│   └── data_generator.py             # генерация данных: uuid4 + Faker
├── api/                              # клиенты HTTP-сервисов
│   ├── api_client.py                 # обёртка над requests.Session
│   ├── auth_api.py                   # /login, /validate, /logout
│   ├── booking_api.py                # CRUD /booking + занятые номера и сводка
│   ├── room_api.py                   # CRUD /room
│   └── report_api.py                 # /report по комнате и по всем
├── pages/                            # Page Object Model
│   ├── base_page.py                  # общие операции и ожидания
│   ├── login_page.py                 # вход в админ-панель
│   ├── room_page.py                  # список комнат в админке
│   ├── booking_page.py               # публичная форма бронирования
│   └── room_details_page.py          # страница комнаты в админке
├── tests/
│   ├── api/                          # 5 файлов, 29 тестов
│   │   ├── test_health_api.py        # 6 тестов: 1 функция × 6 сервисов
│   │   ├── test_auth_api.py          # 5 тестов
│   │   ├── test_booking_api.py       # 8 тестов
│   │   ├── test_room_api.py          # 7 тестов
│   │   └── test_report_api.py        # 3 теста
│   └── ui/                           # 4 файла, 10 тестов
│       ├── test_login_ui.py          # 3 теста
│       ├── test_booking_ui.py        # 2 теста
│       ├── test_rooms_ui.py          # 3 теста
│       └── test_room_details_ui.py   # 2 теста
├── deploy/                           # развёртывание стенда и Jenkins
│   ├── deploy.sh                     # идемпотентный подъём стенда с нуля
│   ├── assets.Dockerfile             # сборка фронтенда с адресами сервисов
│   ├── jenkins.Dockerfile            # Jenkins + Python + Chrome + плагины
│   ├── jenkins-casc.yaml             # настройки Jenkins как код
│   ├── jenkins-job.xml               # описание джобы
│   ├── jenkins-create-job.sh         # создание джобы через REST
│   ├── .env.example                  # шаблон локальных секретов
│   └── README.md                     # документация развёртывания
├── conftest.py                       # фикстуры: драйвер, админ, API-клиенты
├── pytest.ini                        # маркеры и режим захвата вывода
├── requirements.txt                  # зависимости Python
├── Jenkinsfile                       # конвейер: health → API → UI → Allure
├── PROJECT_DESCRIPTION.md            # описание проекта
├── PROJECT_STRUCTURE.md              # этот файл
└── README.md
```

## Сколько тестов и почему

Всего **39 тестов в девяти файлах**. Число тестов не равно числу файлов по двум
причинам: pytest считает каждый метод `test_*` отдельным тестом, а
`@pytest.mark.parametrize` размножает один метод на несколько.

Отдельно стоит счётчик выполнений: за одну сборку тесты запускаются три раза с
разными маркерами — `-m smoke` (6), `-m api` (29), `-m ui` (10). Health-тесты
помечены сразу двумя маркерами, поэтому выполняются дважды, и суммарно за сборку
выходит 45 выполнений при 39 уникальных тестах.

## Генерируемые и игнорируемые файлы

В репозиторий не попадают:

- `allure-results/` — результаты прогона для отчёта Allure;
- `screenshots/` — снимки упавших UI-тестов;
- `restful-booker-platform/` — локальный клон тестируемой платформы;
- `deploy/.env` — локальные секреты (пароль администратора Jenkins).

## Конфигурация

Адреса, таймауты и учётные данные собраны в `config/config.py`. Практически каждое
значение переопределяется переменной окружения с префиксом `RBP_` — это позволяет
гонять один и тот же код против локального стенда и против публичного, не меняя
файлы.
