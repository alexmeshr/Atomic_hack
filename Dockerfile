FROM python:3.12-bookworm

COPY . /atomic_hack
WORKDIR /atomic_hack


ENV POETRY_VIRTUALENVS_CREATE false
RUN pip install poetry

RUN poetry install --no-dev

ENTRYPOINT ["sh", "-c"]
CMD ["ahack", "run-server"]
