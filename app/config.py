from dotenv import load_dotenv
import os

# Load .env into environment variables
load_dotenv()

# Database
DB_USER = os.getenv("SPRING_DATASOURCE_USERNAME")
DB_PASS = os.getenv("SPRING_DATASOURCE_PASSWORD")
DB_HOST = os.getenv("SPRING_DATASOURCE_HOST", "127.0.0.1")
DB_PORT = os.getenv("SPRING_DATASOURCE_PORT", "3306")
DB_NAME = os.getenv("SPRING_DATASOURCE_DB")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# RabbitMQ
RABBITMQ_USER = os.getenv("SPRING_RABBITMQ_USERNAME")
RABBITMQ_PASS = os.getenv("SPRING_RABBITMQ_PASSWORD")

# Invertexto
INVERTEXTO_TOKEN = os.getenv("INVERTEXTO_TOKEN")
INVERTEXTO_URL = os.getenv("INVERTEXTO_URL")