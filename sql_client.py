import psycopg2
import os

class SQLClient(object):
    def __init__(self, port = 5432):
        self.conn = psycopg2.connect(
            host="localhost",
            database="dota",
            user="postgres",
            password=os.getenv("POSTGRES_PASS"),
            port=port)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()