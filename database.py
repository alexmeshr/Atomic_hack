import psycopg2

DBNAME = 'AtomicDB'
TABLENAME = 'atomictable'
USER = 'postgres'
PASSWORD = 'password'
HOST = 'localhost'
PORT = '5432'


def create_table():
    try:
        conn = psycopg2.connect(
            database=DBNAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()
        query = f'''
                CREATE TABLE IF NOT EXISTS {TABLENAME}
                (task_id uuid PRIMARY KEY, chat_session_id uuid, task_stage text, task_status text, meta jsonb );
                '''
        cursor.execute(query)
        conn.commit()
        print("Table created successfully")
    except psycopg2.Error as e:
        print("Fail to execute due to the error:", e)


def get_info():
    try:
        conn = psycopg2.connect(
            database=DBNAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()
        print("PostgreSQL info:")
        print(conn.get_dsn_parameters(), "\n")
        print(f"{TABLENAME}:")
        cursor.execute(f"""
                        SELECT
                            column_name,
                            data_type
                        FROM
                            information_schema.columns
                        WHERE
                            table_name = '{TABLENAME}'
                        """)
        for name, dtype in cursor.fetchall():
            print(f"   {name}: {dtype}")

    except (Exception, psycopg2.Error) as e:
        print("Fail to execute due to the error:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()
