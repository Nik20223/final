# Jenkins для прогона тестов Restful Booker Platform.
#
# Кроме самого Jenkins в образе есть:
#   * Python (python3 + venv) — пайплайн создаёт venv и ставит зависимости тестов;
#   * Chrome — UI-тесты поднимают реальный браузер, chromedriver Selenium Manager
#     скачивает сам;
#   * плагины Pipeline, Git и Allure — без последнего стадия `allure` упадёт.
#
# Контейнер запускается с --network host: так он видит стенд на localhost:80 и
# портах 3000-3006, а сам Jenkins слушает 8080.

FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        python3 \
        python3-venv \
        python3-pip \
        fonts-liberation \
        libnss3 \
        libgbm1 \
    && curl -fsSL -o /tmp/chrome.deb \
        https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y --no-install-recommends /tmp/chrome.deb \
    && rm -f /tmp/chrome.deb \
    && rm -rf /var/lib/apt/lists/*

USER jenkins

RUN jenkins-plugin-cli --plugins \
        allure-jenkins-plugin \
        configuration-as-code \
        workflow-aggregator \
        git
