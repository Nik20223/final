#!/usr/bin/env bash
#
# Создаёт Pipeline-джобу в Jenkins через REST API.
# Вынесено в скрипт, чтобы не тащить кавычки и crumb через ssh.
#
# Cookies сохраняются в jar: DefaultCrumbIssuer привязывает crumb к сессии,
# поэтому запрос без той же сессии получает 403 "No valid crumb".

set -euo pipefail

JENKINS_URL="http://localhost:8080"
JENKINS_USER="admin"
JENKINS_PASSWORD="rbp-jenkins-2026"
JOB_NAME="rbp-tests"
CONFIG_FILE="/root/job-config.xml"
COOKIES="/tmp/jenkins-cookies.txt"

CRUMB=$(curl -s -c "$COOKIES" -u "$JENKINS_USER:$JENKINS_PASSWORD" \
    "$JENKINS_URL/crumbIssuer/api/json" \
    | sed -E 's/.*"crumb":"([^"]+)".*/\1/')

if [ -z "$CRUMB" ] || [ "$CRUMB" = "null" ]; then
    printf 'Не удалось получить crumb\n' >&2
    exit 1
fi

printf 'crumb получен\n'

CODE=$(curl -s -b "$COOKIES" -c "$COOKIES" \
    -o /tmp/create-item.out -w '%{http_code}' \
    -H "Jenkins-Crumb: $CRUMB" \
    -X POST \
    -u "$JENKINS_USER:$JENKINS_PASSWORD" \
    --data-binary "@$CONFIG_FILE" \
    -H 'Content-Type: application/xml' \
    "$JENKINS_URL/createItem?name=$JOB_NAME")

printf 'createItem: HTTP %s\n' "$CODE"

CODE=$(curl -s -b "$COOKIES" \
    -o /dev/null -w '%{http_code}' \
    -u "$JENKINS_USER:$JENKINS_PASSWORD" \
    "$JENKINS_URL/job/$JOB_NAME/api/json")

printf 'проверка джобы: HTTP %s\n' "$CODE"
