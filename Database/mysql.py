from dotenv import load_dotenv
import os

load_dotenv(".env.pp")  # Загружает переменные из .env

# Взято из файла .env
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db_name = os.getenv("db_name")