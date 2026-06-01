from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

client = MongoClient(uri)
db = client[db_name]

print("Conexión exitosa")
print("Base de datos:", db.name)
print("Colecciones actuales:", db.list_collection_names())