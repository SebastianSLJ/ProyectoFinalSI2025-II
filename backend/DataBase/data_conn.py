from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os 
from dotenv import load_dotenv
load_dotenv()


uri = os.getenv('URI_DATABASE')
client = MongoClient(uri)
database = client['Project_SI']
collection = database['Canciones']
reproducciones_collection = database['Reproducciones']


'''
#Prueba de conexión.
try:
    client.admin.command('ping')
    print("Conexión exitosa")
except Exception as e: 
    print(e)
'''