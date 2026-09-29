#!/usr/bin/env bash
#
# Развёртывание стенда Restful Booker Platform на чистой Ubuntu.
#
# Запуск (от root):
#   bash deploy.sh
#
# Переменные окружения:
#   TARGET      — каталог для исходников платформы (по умолчанию /opt/rbp)
#   REPO_URL    — репозиторий платформы
#   SWAP_SIZE   — размер swap-файла (по умолчанию 4G)
#   MAVEN_IMAGE — образ для сборки Java-модулей
#   MODULES     — модули Maven для сборки (без assets, см. README)

set -euo pipefail

TARGET="${TARGET:-/opt/rbp}"
REPO_URL="${REPO_URL:-https://github.com/mwinteringham/restful-booker-platform.git}"
SWAP_SIZE="${SWAP_SIZE:-4G}"
MAVEN_IMAGE="${MAVEN_IMAGE:-maven:3-eclipse-temurin-26}"
MODULES="${MODULES:-auth,booking,room,report,branding,message}"
COMPOSE_FILE="docker-compose.yml"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Пары «сервис:порт» для проверки готовности.
SERVICES="booking:3000 room:3001 branding:3002 auth:3004 report:3005 message:3006"

step() {
    printf '\n=== %s ===\n' "$1"
}

install_packages() {
    local missing=""
    local package

    for package in curl git; do
        command -v "$package" >/dev/null 2>&1 || missing="$missing $package"
    done

    if [ -n "$missing" ]; then
        step "Устанавливаю пакеты:$missing"
        apt-get update -qq
        # shellcheck disable=SC2086
        apt-get install -y -qq $missing
    fi
}

install_docker() {
    if command -v docker >/dev/null 2>&1; then
        step "Docker уже установлен: $(docker --version)"
        return
    fi

    step "Устанавливаю Docker"
    curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
    sh /tmp/get-docker.sh
}

ensure_swap() {
    if [ -n "$(swapon --show)" ]; then
        step "Swap уже включён"
        return
    fi

    step "Создаю swap $SWAP_SIZE"
    fallocate -l "$SWAP_SIZE" /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile

    if ! grep -q '^/swapfile' /etc/fstab; then
        echo '/swapfile none swap sw 0 0' >> /etc/fstab
    fi
}

fetch_sources() {
    step "Забираю исходники в $TARGET"

    if [ -d "$TARGET/.git" ]; then
        git -C "$TARGET" fetch --depth 1 origin
        git -C "$TARGET" reset --hard FETCH_HEAD
    else
        rm -rf "$TARGET"
        git clone --depth 1 "$REPO_URL" "$TARGET"
    fi
}

apply_frontend_dockerfile() {
    step "Подкладываю исправленный Dockerfile фронтенда"
    cp "$SCRIPT_DIR/assets.Dockerfile" "$TARGET/assets/Dockerfile"
}

stop_stand() {
    if [ -f "$TARGET/$COMPOSE_FILE" ]; then
        step "Останавливаю предыдущий стенд"
        docker compose -f "$TARGET/$COMPOSE_FILE" down --remove-orphans || true
    fi
}

build_jars() {
    step "Собираю Java-модули в контейнере $MAVEN_IMAGE"
    docker volume create rbp-m2 >/dev/null

    docker run --rm \
        -v "$TARGET":/src \
        -v rbp-m2:/root/.m2 \
        -w /src \
        "$MAVEN_IMAGE" \
        mvn -B -DskipTests package -pl "$MODULES"
}

start_stand() {
    step "Собираю образы и поднимаю стенд"
    docker compose -f "$TARGET/$COMPOSE_FILE" up -d --build
}

wait_for_stand() {
    step "Жду готовности сервисов"

    local attempt entry name port ready

    for attempt in $(seq 1 60); do
        ready=1

        for entry in $SERVICES; do
            name="${entry%%:*}"
            port="${entry##*:}"

            if ! curl -fsS "http://localhost:${port}/${name}/actuator/health" \
                    | grep -q '"status":"UP"'; then
                ready=0
                break
            fi
        done

        if [ "$ready" -eq 1 ] && curl -fsS -o /dev/null http://localhost/; then
            printf 'Стенд готов\n'
            return 0
        fi

        sleep 5
    done

    printf 'Сервисы не поднялись за отведённое время\n' >&2
    docker compose -f "$TARGET/$COMPOSE_FILE" ps >&2
    return 1
}

main() {
    if [ "$(id -u)" -ne 0 ]; then
        printf 'Скрипт нужно запускать от root\n' >&2
        exit 1
    fi

    install_packages
    install_docker
    ensure_swap
    fetch_sources
    apply_frontend_dockerfile
    stop_stand
    build_jars
    start_stand
    wait_for_stand

    printf '\nСтенд доступен: http://%s\n' "$(hostname -I | awk '{print $1}')"
}

main "$@"
