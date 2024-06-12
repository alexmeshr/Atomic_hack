# Атомик Хак 2.0

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

2. Собираем docker-образ

В `Dockerfile` описан базовый образ. На его основе запускаются все воркеры.
По умолчанию он запускает web-сервер.

Собираем образ (зададим тэг для `ahack-web` для удобства)
```bash
docker build . --tag ahack-web
```

3. Запускаем
```bash
docker run -p 8888:8888 ahack-web
```

4. Проверяем
Заходим на страницу [127.0.0.1:8888/ping](127.0.0.1:8888/ping) и проверяем, что пришёл ответ
```json
{"message":"pong"}
```
