#!/usr/bin/env bash
#
# Инициирует опрос репозитория для джобы, не дожидаясь расписания pollSCM.
# Если в main появился новый коммит, Jenkins сам поставит сборку в очередь.
#
# Аутентификация через сессию, а не через -u на каждом запросе: повторная
# Basic-аутентификация меняет сессию, и crumb, полученный в старой, становится
# недействительным (Jenkins защищается от фиксации сессии). Поэтому cookie
# сохраняется и переиспользуется, а POST идёт уже без -u.

set -euo pipefail

JENKINS_URL="http://localhost:8080"
JENKINS_USER="admin"
# Пароль берётся из окружения и в репозитории не хранится (deploy/.env.example).
JENKINS_PASSWORD="${JENKINS_ADMIN_PASSWORD:?Задайте JENKINS_ADMIN_PASSWORD — см. deploy/.env.example}"
JOB_NAME="rbp-tests"
COOKIES="/tmp/jenkins-cookies.txt"

CRUMB=$(curl -s -c "$COOKIES" -u "$JENKINS_USER:$JENKINS_PASSWORD" \
    "$JENKINS_URL/crumbIssuer/api/json" \
    | sed -E 's/.*"crumb":"([^"]+)".*/\1/')

if [ -z "$CRUMB" ] || [ "$CRUMB" = "null" ]; then
    printf 'Не удалось получить crumb\n' >&2
    exit 1
fi

printf 'crumb получен\n'

CODE=$(curl -s -b "$COOKIES" -o /tmp/poll.out -w '%{http_code}' \
    -H "Jenkins-Crumb: $CRUMB" \
    -X POST \
    "$JENKINS_URL/job/$JOB_NAME/poll")

printf 'poll: HTTP %s\n' "$CODE"
