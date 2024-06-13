FROM postgres:16.3-bookworm

# https://github.com/pgvector/pgvector/blob/master/Dockerfile
RUN \
    apt-get update && \
    apt-mark hold locales && \
    apt-get install -y --no-install-recommends build-essential postgresql-server-dev-16 git && \
    \
    cd /tmp && \
    export GIT_SSL_NO_VERIFY=1 && \
    git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git && \
    cd /tmp/pgvector && \
    \
    make OPTFLAGS="" && \
    make install && \
    mkdir /usr/share/doc/pgvector && \
    cp LICENSE README.md /usr/share/doc/pgvector && \
    rm -r /tmp/pgvector && \
    apt-get remove -y build-essential postgresql-server-dev-16 git && \
    apt-get autoremove -y && \
    apt-mark unhold locales && \
    rm -rf /var/lib/apt/lists/*
