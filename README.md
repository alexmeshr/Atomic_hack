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

# Разработка

- коммиты в `main` - это норма (времени мало делать нормально)
- за `git push --force ...` сломаю колено в двух местах
  - `git push --force-with-lease ...` - окей

### А как запустить

Точкой входа всегда является файлик `cli.py`. Функции, помеченные декоратором `@cli.command` можно
запустить. Например web-server стартует в функции `run_server`.
```python
@cli.command
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=8888)
def run_server(host: str, port: int):
  uvicorn.run(app, host=host, port=port)
```

В `docker-compose.yaml` запуск этого сервиса
выглядит так:
```yaml
services:
  ahack-web:
    build: .
    command: ahack run-server          <--- вот тут вот команда
    ports:
      - "8888:8888"
    env_file:
      - 'pg_config.env'
    depends_on:
      - postgre
```

Для простоты экспериментов есть функция `do` (она пустая и выводит hello). Вот её кусок в `docker-compose.yaml`:
```yaml
ahack-experiments:
  build: .
  command: ahack do          <--- вот тут вот её вызов
  depends_on:
    - postgres
```

Роль функций `cli.py` - вызвать что-то и передать параметры. Бизнес-логика / бесконечные циклы / всякая всячина
сдесь быть не должна. Если очень нужно - правильнее создать новую функцию в `src/atomic_hack/services/???.py`.


Для простототы логи отключены (идея не такая плоха, как кажется) для всех сервисов кроме `ahack-experiments`.
Поэтому после запуска `docker-compose up` логов будет немного и вывод будет хорошо видно

### А как хранить константы

Настройки лежат в `settings.py` в единственном классе `Settings`.
Скорее всего настройка будет константой - можно сделать так же, как заданы `postgres_url`.
(дальше можно не читать) Если настройку надо прокинуть в другой контейнер (например `POSTGRES_PASSWORD`), то её нужно
прокинуть в `.env` файлик (например в `pg_config.env`). И дальше в нижнем регистре написать её в `Settings`.

```python
class Settings(BaseSettings):
  postgres_url: str = Field(default='postgres')
  postgres_password: str = Field(...)
```

### А как с бд поработать

Всё взаимодействие с внешними сервисами находится в `src/atomic_hack/repositories/`.
Соединение с бд держать вечно не очень хорошо (как и соединение с чем угодно).
Поэтому 'подключение' берём только на момент взаимодействия. Ну и для 'подключения' нужны параметры, поэтому это всё
заворачиваем в фабрику. Вот оно и лежит в `deps.py`.

Например вот так воспользоваться pg для чего-нибудь
```python
# src/atomic_hack/repositories/pg_smth.py
from atomic_hack.deps import get_pg_cursor  # вот эта фабрика

def run_my_super_pg_script():
    with get_pg_cursor() as cursor:
        cursor.execte('select 123 as a')
        data = cursor.fetchall()
        ...
```
