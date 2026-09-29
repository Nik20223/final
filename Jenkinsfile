pipeline {
    agent any

    parameters {
        string(name: 'BASE_URL', defaultValue: 'http://localhost',
               description: 'Адрес тестируемого стенда')
        booleanParam(name: 'HEADLESS', defaultValue: true,
                     description: 'Запускать UI-тесты без окна браузера')
    }

    options {
        timeout(time: 45, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
    }

    // Автоматический запуск без внешнего триггера: ночной прогон.
    // Для запуска на каждый коммит замените на pollSCM('H/15 * * * *')
    // после переключения джобы на репозиторий GitHub.
    triggers {
        cron('H 3 * * *')
    }

    environment {
        RBP_UI_URL = "${params.BASE_URL}"
        RBP_API_HOST = "${params.BASE_URL}"
        RBP_HEADLESS = "${params.HEADLESS}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                script {
                    runStep(
                        'python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt',
                        'python -m venv .venv && .venv\\Scripts\\python.exe -m pip install -r requirements.txt'
                    )
                }
            }
        }

        stage('Health check') {
            steps {
                script {
                    runStep(
                        '.venv/bin/python -m pytest -m smoke --alluredir=allure-results --clean-alluredir',
                        '.venv\\Scripts\\python.exe -m pytest -m smoke --alluredir=allure-results --clean-alluredir'
                    )
                }
            }
        }

        stage('API tests') {
            steps {
                script {
                    runStep(
                        '.venv/bin/python -m pytest -m api --alluredir=allure-results',
                        '.venv\\Scripts\\python.exe -m pytest -m api --alluredir=allure-results'
                    )
                }
            }
        }

        stage('UI tests') {
            steps {
                script {
                    runStep(
                        '.venv/bin/python -m pytest -m ui --alluredir=allure-results',
                        '.venv\\Scripts\\python.exe -m pytest -m ui --alluredir=allure-results'
                    )
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'screenshots/**', allowEmptyArchive: true
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}

def runStep(String unixCommand, String windowsCommand) {
    if (isUnix()) {
        sh unixCommand
    } else {
        bat windowsCommand
    }
}
