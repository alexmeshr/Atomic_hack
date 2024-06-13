FROM python:3.12-bookworm

# ставим poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

COPY . /app
WORKDIR /app

RUN \
    /root/.local/bin/poetry env use $(cat .python-version) && \
    /root/.local/bin/poetry install

ENTRYPOINT ["/root/.local/bin/poetry", "run"]
CMD ["ahack", "run-server"]
