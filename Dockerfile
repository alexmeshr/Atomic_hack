FROM python:3.12-bookworm

# ставим poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# ускоряем деплой
# (ставим либы, только если они поменялись)
COPY ./poetry.lock /atomic_hack/
COPY ./pyproject.toml /atomic_hack/
COPY ./.python-version /atomic_hack/
COPY ./src/atomic_hack/cli.py /atomic_hack/src/atomic_hack/
WORKDIR /atomic_hack

RUN \
    /root/.local/bin/poetry env use $(cat .python-version) && \
    /root/.local/bin/poetry install

COPY . /atomic_hack

# резолвим зависимости локальной фигни
RUN /root/.local/bin/poetry install

ENTRYPOINT ["/root/.local/bin/poetry", "run"]
CMD ["ahack", "run-server"]
