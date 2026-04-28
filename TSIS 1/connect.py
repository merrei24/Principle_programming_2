# connect.py
import psycopg2
import config

def get_connection():
    try:
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,      # Осы жерде config.user болуы керек
            password=config.password
        )
        return conn
    except Exception as error:
        print(f"Error connecting to DB: {error}")
        return None