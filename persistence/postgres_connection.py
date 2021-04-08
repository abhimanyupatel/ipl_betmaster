import os
import psycopg2


def setup_connection():
    # TODO check if the DB already exists, create if not
    if os.getenv('PROD') is not None and os.environ['PROD'] == 'TRUE':
        db_url = os.environ['DATABASE_URL']
        conn = psycopg2.connect(db_url, sslmode='require')
    else:
        conn = psycopg2.connect(host=os.environ['HOST'],
                                port=os.environ['PORT'],
                                database=os.environ['DATABASE'],
                                user=os.environ['DB_USER'],
                                password=os.environ['DB_PASSWORD'])
    cur = conn.cursor()
    return cur, conn


def close_connection(cur, conn):
    cur.close()
    conn.close()

