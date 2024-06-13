# Атомик Хак 2.0

# Разработка

- коммиты в `main` - это норма (времени мало делать нормально)
- за `git push --force ...` сломаю колено в двух местах
  - `git push --force-with-lease ...` - окей

# Установка

Ставим `docker` и `docker-compose`. Инструкции есть на официальном сайте [тут](https://docs.docker.com/get-docker/) и [тут](https://docs.docker.com/compose/install/).

Проверить, что есть рабочий `docker` можно командой
```bash
docker run hello-world
```

1. Скачиваем репозиторий
```bash
git clone git@github.com:alexmeshr/Atomic_hack.git
```

2. Используем dev-ops магию

В `Dockerfile` описан базовый образ. На его основе запускаются все воркеры.
По умолчанию он запускает web-сервер. Но в `docker-compose.yaml` он используется для всего
(там кастомизируется `cmd`).

Запускаем `docker-compose` и он всё сделает (первый раз может запускаться +-минуту)
```bash
docker-compose up
```
Для остановки нужно нажать `Ctrl-C`

При изменении кода, нужно пересобрать docker-образ. Для этого можно запустить с флагом `--build`
```bash
docker-compose up --build
```

Если стартануло плохо, можно попробовать удалить `volumes`
```bash
docker-compose down -v
```
А потом снова `docker-compose up`

3. Проверяем
Заходим на страницу [127.0.0.1:8888/ping](127.0.0.1:8888/ping) и проверяем, что пришёл ответ
```json
{"message":"pong"}
```
