import os
from dotenv import load_dotenv

load_dotenv()

db_connection = os.getenv('DB_CONNECTION')
cors_origins = os.getenv("ALLOWED_ORIGINS", "*")