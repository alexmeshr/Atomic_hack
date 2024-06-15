from contextlib import contextmanager

import psycopg

from atomic_hack.settings import settings


@contextmanager
def get_pg_cursor() -> psycopg.connection.Connection:
    conn = psycopg.connect(
        host=settings.postgres_url,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        dbname=settings.postgres_db,
    )

    cur = conn.cursor()

    yield cur

    conn.commit()
    cur.close()
    conn.close()
