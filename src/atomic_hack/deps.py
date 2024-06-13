from contextlib import contextmanager

import psycopg2

from atomic_hack.settings import settings


@contextmanager
def get_pg_cursor() -> psycopg2._psycopg.cursor:
    conn = psycopg2.connect(
        host=settings.postgres_url,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        dbname=settings.postgres_db,
    )

    yield conn.cursor()
