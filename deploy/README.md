# Развёртывание стенда

`deploy.sh` поднимает Restful Booker Platform на чистой Ubuntu с нуля: ставит
Docker, добавляет swap, забирает исходники платформы, собирает Java-модули и
запускает `docker compose`. Скрипт идемпотентен — повторный запуск обновляет
исходники и пересобирает стенд.

## Запуск

```bash
scp -r deploy root@<host>:/root/
ssh root@<host> 'bash /root/deploy/deploy.sh'
```

## Зачем нужен свой Dockerfile фронтенда

`next.config.js` запекает адреса сервисов в `rewrites` **на этапе сборки**, а в
апстримном `assets/Dockerfile` переменные `BOOKING_API`…`REPORT_API` объявлены
только в финальном слое `runner`. Из-за этого в образ попадают адреса
`http://localhost:300X`, и почти все прокси (`/api/room/{id}`,
`/api/report/room/{id}` и остальные) отдают 500 — страница резервации бесконечно
крутит спиннер.

`assets.Dockerfile` рядом с этим файлом — та же сборка, но `ENV` объявлены уже в
базовом слое `base`, поэтому адреса попадают и в сборку. Скрипт подкладывает этот
файл поверх клона, чтобы развёртывание не зависело от локальных правок
репозитория платформы.

## Зачем собирать jar в контейнере

Dockerfile'ы Java-сервисов делают `COPY target/*-exec.jar`, то есть jar должны
существовать **до** `docker build`. Проект требует Java 26 (`<release>26</release>`
в корневом `pom.xml`), которой нет в репозиториях Ubuntu, поэтому сборка идёт в
образе `maven:3-eclipse-temurin-26`, а скачанные зависимости кэшируются в томе
`rbp-m2` и переиспользуются между запусками.

Модуль `assets` из Maven-сборки исключён намеренно: его `pom.xml` вызывает
`npm install`, `npm test` и `npm run build` через `exec-maven-plugin`, что внутри
контейнера не нужно — фронтенд собирается собственным Dockerfile'ом.

Стенд перед сборкой останавливается, чтобы Maven не конкурировал за память с
шестью работающими JVM.

## Проверка

```bash
curl -fsS http://<host>:3001/room/actuator/health   # {"status":"UP"}
curl -fsS -o /dev/null -w '%{http_code}\n' http://<host>/   # 200
```

У сервисов задан servlet context-path, поэтому health доступен не в корне, а по
пути `/<service>/actuator/health`.

## Тесты против стенда

Адрес стенда задан в `config/config.py`. Для другого хоста он переопределяется
переменными окружения:

```bash
python -m pytest                     # против адреса из config
RBP_API_HOST=http://localhost RBP_UI_URL=http://localhost python -m pytest
```

## Jenkins

Jenkins живёт отдельным контейнером рядом со стендом и собирается из
`jenkins.Dockerfile`: в образе есть Python (пайплайн создаёт venv), Chrome для
UI-тестов и плагины Pipeline, Git и Allure.

```bash
docker build -t jenkins-rbp -f jenkins.Dockerfile .
printf 'JAVA_OPTS=%s\nCASC_JENKINS_CONFIG=%s\n' \
    '-Djenkins.install.runSetupWizard=false' \
    '/var/jenkins_home/casc_configs' > /root/jenkins.env
docker run -d --name jenkins --restart always --network host \
    -v jenkins_home:/var/jenkins_home \
    --env-file /root/jenkins.env jenkins-rbp
```

Почему флаги именно такие:

- `--network host` — контейнер видит стенд на `localhost:80` и портах 3000-3006,
  а сам Jenkins слушает 8080.
- `runSetupWizard=false` — без мастера настройки. Мастер заодно создаёт
  администратора, поэтому и аккаунт, и права задаются в `jenkins-casc.yaml`.
- `CASC_JENKINS_CONFIG` — без этой переменной configuration-as-code не
  подхватывает конфиг, и Jenkins остаётся открытым всем желающим
  (`SecurityRealm=None`, `AuthorizationStrategy=Unsecured`).
- Репозиторий `github.com/Nik20223/final` публичный, поэтому джоба клонирует
  его анонимно и учётные данные в Jenkins заводить не нужно.

`jenkins-casc.yaml` описывает администратора, запрет анонимного доступа, адрес
инстанса (без него не работает CLI) и установку Allure (без неё шаг `allure`
падает с «No Allure installation found»).

Джоба создаётся из `job-config.xml`: файл кладётся в `jobs/rbp-tests/config.xml`
внутри `JENKINS_HOME`, потому что POST в `createItem` требует crumb, а тот в
Jenkins 2.568 не проходит при Basic-аутентификации. Конфиг джобы — обычный
Pipeline from SCM, скрипт берётся из `Jenkinsfile` в корне репозитория.

Запуск сборки из CLI (сам REST-запуск упирается в ту же проверку crumb):

```bash
docker exec -w / jenkins sh -c 'curl -s -o /tmp/cli.jar -u admin:<pass> \
    http://localhost:8080/jnlpJars/jenkins-cli.jar; \
    java -jar /tmp/cli.jar -s http://<host>:8080 -auth admin:<pass> build rbp-tests'
```
