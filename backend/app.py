from flask import Flask, redirect, request, render_template, session, url_for, jsonify
import threading 
import time
import requests
import os
import sys
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import random
import string
from urllib.parse import urlencode
import base64
from DataBase import data_conn



app = Flask(__name__, 
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)

# secret_key obligatoria para el session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# Carga de datos relevantes DOTENV (.env)
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# función para generar el state (verificación de state)
def generate_random_strings(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# generación de URL para inicio de sesión y obtención de datos necesarios para el codigo (Documentación de spotify)
def url_login():
    state = generate_random_strings(16)
    session['oauth_state'] = state
    scope = 'user-read-private user-read-email user-read-playback-state user-read-currently-playing' # Información que estamos solicitando de la API, si no se especifica nada, solo se muestra información publica.  
    params = {
        'response_type' : 'code', # Indicado por el API de spotify
        'client_id' : CLIENT_ID, #Client ID proporcionado en el dashboard de spotify
        'scope' : scope, # Permisos que estamos solicitando (especificado anteriormente)
        'redirect_uri' : REDIRECT_URI, # URI de redirección especificado en el dashboard de spotify. 
        'state' : state # Es un token de seguridad que previene ataques (Opcional pero recomendado)
    }
    return f'https://accounts.spotify.com/authorize?{urlencode(params)}'
    
@app.route('/')
def inicio():    
    return render_template('index.html', url=url_login())

@app.route('/login')
def login():
    return redirect(url_login())

# Función para recibir los parametros enviados por la ruta login especificada anteriormente
# Luego del login se envian dos parametros (el code y el state)
# El parametro state sirve solo para verificar la coincidencia del request (para evitar falsificación)
@app.route('/callback')
def callback():
    code = request.args.get('code')    
    received_state = request.args.get('state') 
    stored_state = session.get('oauth_state')

    if stored_state is None:
        return 'Error: No se inicio correctamente'
    if received_state != stored_state:
        return 'Error: State no coincide'
    #Obtenemos el token a traves del codigo que teniamos inicialmente luego del login del usuario y la autorización de permisos (redirección a url generada en el url_login)
    token_response = UserToken(code)
    #Guardamos el access_token en una session para obtenerlo en consultas mas adelante .get()
    session['access_token'] = token_response['access_token']
    # Guardamos también en una variable global para el hilo en segundo plano del loop_player
    global access_token_global
    access_token_global = token_response['access_token']
    return redirect(url_for('hola'))

# Petición al API para obtención del codigo de inicio.
def UserToken(code):
    url = 'https://accounts.spotify.com/api/token'
    # Header indicado por Spotify
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded'        
    }
    # Cuerpo indicado por Spotify (Documentación)
    body = {    
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : REDIRECT_URI, 
        'client_id' : CLIENT_ID,        
        'client_secret': CLIENT_SECRET,      
    }
    response = requests.post(url, headers= headers, data=body)
    return response.json()

@app.route('/hola')
def hola():
    return render_template('hola.html')
'''
# Petición para traer información del usuario (Debug)
@app.route('/player')
def player():
    url = 'https://api.spotify.com/v1/me/player'
    token = session.get('access_token')
    
    if not token:
        return 'Error: No hay token, por favor inicie sesión'
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data_player = response.json()
        id_cancion = data_player['item']['id']
        id_actual = session.get('ultima_cacion_id')
        if id_cancion != id_actual:
            nombre_artista = data_player['item']['artists'][0]['name']
            img_album = data_player ['item']['album']['images'][0]['url']
            nombre_album = data_player["item"]["album"]["name"]
            duracion_ms = data_player['item']['duration_ms']
            minutos = duracion_ms // 60000
            segundos = (duracion_ms % 60000) // 1000
            duracion_formateada = f"{minutos}:{segundos:02d}"
            name_song = data_player['item']['name']        
            datos_cancion = {
            "artista": nombre_artista,
            "imagen_album": img_album,
            "album": nombre_album,
            "duracion": duracion_formateada,
            "cancion": name_song
            }
            insertar_canciones(datos_cancion)
            session['ultima_cancion_id'] = id_cancion
            guardada = True
        else: 
            guardada = False

        return jsonify({"guardada": guardada, "id": id_cancion})


       
    elif response.status_code == 204:
        # Usuario no está reproduciendo nada
        return {"status": "No hay música reproduciéndose"}
    else:
        return f"Error {response.status_code}: {response.text}"      
'''

def insertar_canciones(data_song):
    result = data_conn.collection.insert_one(data_song)


def loop_player():
    print("loop iniciando correctamente :D")
    global ultima_cancion_id
    ultima_cancion_id = None  # guardamos el último ID visto
    while True:
        try:
            token = globals().get('access_token_global')
            if not token:                
                time.sleep(10)
                continue            
            url = 'https://api.spotify.com/v1/me/player'
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url, headers=headers)            
            
            if response.status_code == 200:
                data_player = response.json()
                id_cancion = data_player['item']['id']                                      
                if id_cancion != ultima_cancion_id:
                    ultima_cancion_id = id_cancion
                    nombre_artista = data_player['item']['artists'][0]['name']
                    img_album = data_player['item']['album']['images'][0]['url']
                    nombre_album = data_player["item"]["album"]["name"]
                    duracion_ms = data_player['item']['duration_ms']
                    minutos = duracion_ms // 60000
                    segundos = (duracion_ms % 60000) // 1000
                    duracion_formateada = f"{minutos}:{segundos:02d}"
                    name_song = data_player['item']['name']
                    datos_cancion = {
                        "spotify_id": id_cancion,
                        "artista": nombre_artista,
                        "imagen_album": img_album,
                        "album": nombre_album,
                        "duracion": duracion_formateada,
                        "cancion": name_song
                    }
                    insertar_canciones(datos_cancion)
                    print(f" Nueva canción detectada y guardada: {name_song}")
            time.sleep(10)
        except Exception as e:
            print("Error en el loop", e)
            time.sleep(10)

# Endpoint para verificar que cancion se esta reproduciendo 
@app.route('/estado')
def estado():
    ultima = data_conn.collection.find_one(sort=[('_id', -1)])
    if ultima:
        ultima['_id'] = str(ultima['_id'])
        return jsonify(ultima)
    else:
        return jsonify({"status": "No hay canciones registradas"})


if __name__ == '__main__':
    hilo = threading.Thread(target=loop_player, daemon=True)
    hilo.start()    
    app.run(debug=True, use_reloader=False)

    

