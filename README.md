# Атомик Хак 2.0

Мы много времени потратились на воспроизводимость.

# Установка

### 0. Требования
- Требуется машинка с видеокартой и поддержкой cuda12. На этой машинке будут запускаться LLM-ки. Модельки маленькие, но без них оно не запустится. Мы тестили на Nvidia 3060. Если поддерживается cuda меньших версий - придётся повозиться с пакетами (напишите нам - мы поможем воспроизвести)

- На машине должен быть установлен `docker` и `docker-compose`
  + [как поставить docker](https://docs.docker.com/engine/install/)
  + [как поставить docker-compose](https://docs.docker.com/compose/install/)

### 1. Скачать репозиторий
```bash
git clone git@github.com:alexmeshr/Atomic_hack.git
```

Дальше вся работа будет в папке репозитория - _Atomic_hack_

### 2. Скачать архив с инструкциями

Для теста можно взять архив из [задания](https://pgenesis.notion.site/914cc4e0aca041d997aa3928fa73239b). Сам архив - [вот ссылочка](https://disk.yandex.ru/d/oiLAkiqiwNap5Q)

(можно взять любые другие)

Инструкции (в формате pdf!) необходимо поместить в папку `instructions`.

### 3. Запуск

Запуск производится одной командой (если выполнены два требования выше)

```bash
docker-compose up --build
```

Эта команда соберет и запустит все сервисы, а именно
- установит необходимые python-пакеты
- скачает postgres и установит pgvector
- выгрузит инструкции из папки `instructions` в хранилище

