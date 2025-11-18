from flask import Flask, redirect, request, render_template, session, url_for, jsonify
import threading 
import time
import requests
import os
import sys
import datetime
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import random
import string
from urllib.parse import urlencode
import base64
from DataBase import data_conn
from api import client, auth

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

<<<<<<< HEAD
# Landing page   
@app.route('/')
def inicio():    
    return render_template('select.html', url=client.url_login(), url2=url_for('dashboard'))
=======
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

# Landing page   
@app.route('/')
def inicio():    
    return render_template('select.html', url=url_login(), url2=url_for('dashboard'))
>>>>>>> 477bba26e23c324336719a19064b5a5de14f510d

# Ruta para el login de spotify
@app.route('/login')
def login():
    return redirect(client.url_login())

# Ruta de reproductor
@app.route('/player')
def player():
    return render_template('player.html')

# Ruta del dashboard (admin)
@app.route('/dashboard')
def dashboard():
    return render_template('panel.html')

# Ruta de reproductor
@app.route('/player')
def player():
    return render_template('player.html')

# Ruta del dashboard (admin)
@app.route('/dashboard')
def dashboard():
    return render_template('panel.html')

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
    token_response = auth.UserToken(code)
    #Guardamos el access_token en una session para obtenerlo en consultas mas adelante .get()
    session['access_token'] = token_response['access_token']
    # Guardamos también en una variable global para el hilo en segundo plano del loop_player
    global access_token_global
    access_token_global = token_response['access_token']
    return redirect(url_for('player'))
<<<<<<< HEAD
=======

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
>>>>>>> 477bba26e23c324336719a19064b5a5de14f510d

def insertar_canciones(data_song):
    result = data_conn.collection.insert_one(data_song)

def insertar_reproduccion(data_reproduccion):
    result = data_conn.reproducciones_collection.insert_one(data_reproduccion)


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

                    # Cola de reproducciones
                    cancion = data_conn.collection.find_one({'spotify_id': id_cancion})
                    if cancion:
                        # Insertar reproduccion con metricas
                        dia_semana = datetime.datetime.now().strftime('%A')  # lunes, martes, etc.
                        hora = datetime.datetime.now().hour
                        
                        # Calcular metricas automáticas
                        puntuacion_base = random.uniform(6.0, 9.5)  # Ejemplos (POR IMPLEMENTAR AHHHHHHHHHH)
                        impacto_base = random.uniform(5.0, 25.0)    
                        aforo_base = random.randint(50, 95)         
                        
                        # Ajustar por dia y hora
                        if dia_semana in ['Friday', 'Saturday']:
                            puntuacion_base += 0.5
                            impacto_base += 5.0
                        
                        if 20 <= hora <= 23:  # Horario pico EJEMPLOOOOO POR AJUSTAR AAAAAAAAAAAA
                            aforo_base += 10
                        
                        reproduccion_data = {
                            'cancion_id': cancion['_id'],
                            'fecha': datetime.datetime.now(),
                            'puntuacion': round(puntuacion_base, 1),
                            'impacto_ventas': round(impacto_base, 1),
                            'aforo': min(aforo_base, 100),  
                            'dia_semana': dia_semana,
                            'hora': hora
                        }                        
                        insertar_reproduccion(reproduccion_data)
                        print(f"Reproducción registrada: {name_song} - Puntuación: {reproduccion_data['puntuacion']}")
                    
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
    
'''
@app.route('/api/canciones-metricas')
def canciones_metricas():
    try:
        # Canciones en el database (para dashboard)
        canciones = list(data_conn.collection.find().limit(20))
        
        canciones_formateadas = []
        for cancion in canciones:
            canciones_formateadas.append({
                'id': str(cancion['_id']),
                'nombre': cancion['cancion'],  
                'artista': cancion['artista'],
                'album': cancion['album'],
                'imagen_url': cancion['imagen_album'],
                'reproducciones': random.randint(1, 15),  # Valor por defecto temporal xd (No hay timpo!!!!)
                'puntuacion': round(random.uniform(7.0, 9.5), 1),    # Valor por defecto temporal xd 
                'impacto_ventas': round(random.uniform(10.0, 25.0), 1)  # Valor por defecto temporal xd 
            })
        
        return jsonify({'canciones': canciones_formateadas})
        
    except Exception as e:
        print(f"Error en canciones-metricas: {e}")
        return jsonify({'error': str(e)}), 500
'''
''
@app.route('/api/canciones-metricas')
def canciones_metricas():
    try:        
        # Agregación para métricas 
        pipeline = [
            {
                '$lookup': {
                    'from': 'Reproducciones',
                    'localField': '_id', 
                    'foreignField': 'cancion_id',
                    'as': 'reproducciones_data'
                }
            },
            {
                '$project': {
                    'nombre': '$cancion',
                    'artista': 1,
                    'album': 1,
                    'imagen_url': '$imagen_album',
                    'reproducciones': { '$size': '$reproducciones_data' },
                    'puntuacion_promedio': { '$avg': '$reproducciones_data.puntuacion' },
                    'impacto_ventas_promedio': { '$avg': '$reproducciones_data.impacto_ventas' }
                }
            },
            {
                '$sort': { 'puntuacion_promedio': -1 }
            },
            {
                '$limit': 50
            }
        ]
        
        canciones = list(data_conn.collection.find().limit(20))
        reproduccion = list(data_conn.reproducciones_collection.find())
        
        canciones_formateadas = []
        
        for cancion in canciones:
            # Filtrar reproducciones de esta canción específica
            reproducciones_cancion = [
                r for r in reproduccion 
                if str(r['cancion_id']) == str(cancion['_id'])
            ]
            
            # Calcular metricas basadas en las reproducciones
            total_reproducciones = len(reproducciones_cancion)
            
            if total_reproducciones > 0:
                # Calcular promedios
                puntuacion_promedio = sum(r['puntuacion'] for r in reproducciones_cancion) / total_reproducciones
                impacto_promedio = sum(r['impacto_ventas'] for r in reproducciones_cancion) / total_reproducciones
            else:
                # Si no hay reproducciones, usar valores por defecto
                puntuacion_promedio = 0
                impacto_promedio = 0
            
            canciones_formateadas.append({
                'id': str(cancion['_id']),
                'nombre': cancion['cancion'],  
                'artista': cancion['artista'],
                'album': cancion['album'],
                'imagen_url': cancion['imagen_album'],
                'reproducciones': total_reproducciones,
                'puntuacion': round(puntuacion_promedio, 1),
                'impacto_ventas': round(impacto_promedio, 1)
            })
        
        # Ordenar por puntuación (mayor a menor)
        canciones_formateadas.sort(key=lambda x: x['puntuacion'], reverse=True)
        
        return jsonify({'canciones': canciones_formateadas})
        
    except Exception as e:
        print(f"Error en canciones-metricas: {e}")
        return cargar_canciones_simple()
    
def cargar_canciones_simple():
    try:
        canciones = list(data_conn['Canciones'].find().limit(20))  
        reproduccion = list(data_conn.reproducciones_collection.find())  
        canciones_formateadas = []
        for cancion in canciones:
            # Filtrar reproducciones de esta canción específica
            reproducciones_cancion = [
                r for r in reproduccion 
                if str(r['cancion_id']) == str(cancion['_id'])
            ]
        if total_reproducciones > 0:
                # Calcular promedios
                puntuacion_promedio = sum(r['puntuacion'] for r in reproducciones_cancion) / total_reproducciones
                impacto_promedio = sum(r['impacto_ventas'] for r in reproducciones_cancion) / total_reproducciones
        else:
            # Si no hay reproducciones, usar valores por defecto
            puntuacion_promedio = 0
            impacto_promedio = 0            
            # Calcular metricas basadas en las reproducciones
        total_reproducciones = len(reproducciones_cancion)
        for cancion in canciones:
            canciones_formateadas.append({
                'id': str(cancion['_id']),
                'nombre': cancion['cancion'],
                'artista': cancion['artista'],
                'album': cancion['album'],
                'imagen_url': cancion['imagen_album'],
                'reproducciones': total_reproducciones,
                'puntuacion': round(puntuacion_promedio, 1),
                'impacto_ventas': round(impacto_promedio, 1)
            })
        
        return jsonify({'canciones': canciones_formateadas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'' 

@app.route('/api/grafica-ventas')
def grafica_ventas():
    try:
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        # Agrupar por día de la semana
        ventas_por_dia = {
            'Monday': [], 'Tuesday': [], 'Wednesday': [], 
            'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []
        }
        
        for repro in reproducciones:
            dia = repro['dia_semana']
            ventas_por_dia[dia].append(repro['impacto_ventas'])
        
        # Calcular promedios
        datos_grafica = {
            'dias': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
            'ventas_promedio': [
                round(sum(ventas_por_dia['Monday']) / len(ventas_por_dia['Monday']), 1) if ventas_por_dia['Monday'] else 0,
                round(sum(ventas_por_dia['Tuesday']) / len(ventas_por_dia['Tuesday']), 1) if ventas_por_dia['Tuesday'] else 0,
                round(sum(ventas_por_dia['Wednesday']) / len(ventas_por_dia['Wednesday']), 1) if ventas_por_dia['Wednesday'] else 0,
                round(sum(ventas_por_dia['Thursday']) / len(ventas_por_dia['Thursday']), 1) if ventas_por_dia['Thursday'] else 0,
                round(sum(ventas_por_dia['Friday']) / len(ventas_por_dia['Friday']), 1) if ventas_por_dia['Friday'] else 0,
                round(sum(ventas_por_dia['Saturday']) / len(ventas_por_dia['Saturday']), 1) if ventas_por_dia['Saturday'] else 0,
                round(sum(ventas_por_dia['Sunday']) / len(ventas_por_dia['Sunday']), 1) if ventas_por_dia['Sunday'] else 0
            ]
        }
        
        return jsonify(datos_grafica)
        
    except Exception as e:
        print(f"Error en grafica-ventas: {e}")
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    hilo = threading.Thread(target=loop_player, daemon=True)
    hilo.start()    
    app.run(debug=True, use_reloader=False)
