import pymysql
import pymysql.cursors
from config import Config

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=Config.TIDB_HOST,
            port=Config.TIDB_PORT,
            user=Config.TIDB_USER,
            password=Config.TIDB_PASSWORD,
            database=Config.TIDB_DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            ssl={'ssl_verify_cert': True, 'ssl_verify_identity': True}
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
