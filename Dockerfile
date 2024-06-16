FROM python:3.12-bookworm

COPY . /atomic_hack
WORKDIR /atomic_hack

# ставим poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN \
    /root/.local/bin/poetry env use $(cat .python-version) && \
    /root/.local/bin/poetry install

ENTRYPOINT ["/root/.local/bin/poetry", "run"]
CMD ["ahack", "run-server"]
