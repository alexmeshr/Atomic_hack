FROM python:3.12-bookworm

# ставим poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# ускоряем деплой
# (ставим либы, только если они поменялись)
COPY ./poetry.lock /app/
COPY ./pyproject.toml /app/
COPY ./.python-version /app/
WORKDIR /app

RUN \
    /root/.local/bin/poetry env use $(cat .python-version) && \
    /root/.local/bin/poetry install

COPY . /app

# резолвим зависимости локальной фигни
RUN /root/.local/bin/poetry install

ENTRYPOINT ["/root/.local/bin/poetry", "run"]
CMD ["ahack", "run-server"]
