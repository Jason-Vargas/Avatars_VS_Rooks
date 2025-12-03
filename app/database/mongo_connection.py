from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del .env

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB_NAME = os.getenv("MONGO_DB", "AVR")

URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?appName=AVR"

client = MongoClient(URI, server_api=ServerApi("1"))
db = client[MONGO_DB_NAME]

def test_connection():
    try:
        client.admin.command("ping")
        print("✅ Conectado a MongoDB correctamente")
        return True  # ← Asegúrate de que esto esté aquí
    except Exception as e:
        print("❌ Error conectando a MongoDB:", e)
        return False

if __name__ == "__main__":
    test_connection()