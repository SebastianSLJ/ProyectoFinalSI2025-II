import requests
import base64
import os
from dotenv import load_dotenv
import random 

load_dotenv()

URL = 'https://accounts.spotify.com/api/token'

# Documentación de spotify Quickstart
# client id y client secret proporcionados por spotify 
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# codificación de credenciales a base64
credenciales = f"{client_id}:{client_secret}"
credenciales_bytes = credenciales.encode('ascii')
credenciales_base64 = base64.b64encode(credenciales_bytes).decode('ascii')

# Datos del cuerpo de la petición
data = {
    'grant_type': 'client_credentials'    
}


# Header de la petición para obtener token
header_token = {
    'Authorization' : f'Basic {credenciales_base64}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Petición a la api para obtener el token de acceso.
response = requests.post(
    URL, headers=header_token, data=data
)

# Verificación de estatus de respuesta
if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']       
else:
    print("Error:", response.status_code)
    print(response.text)

















