from flask import Flask, redirect, request, render_template, session, url_for, jsonify
import threading 
import time
import requests
import os
import sys
from bson import ObjectId
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

# Crear índices para optimizar búsquedas
def crear_indices():
    try:
        # Índice único en spotify_id para búsquedas rápidas
        data_conn.collection.create_index([('spotify_id', pymongo.ASCENDING)], unique=True)
        # Índice en cancion_id para búsquedas de reproducciones
        data_conn.reproducciones_collection.create_index([('cancion_id', pymongo.ASCENDING)])
        # Índice compuesto para búsquedas por día y hora
        data_conn.reproducciones_collection.create_index([('dia_semana', pymongo.ASCENDING), ('hora', pymongo.ASCENDING)])
        print("Índices creados exitosamente")
    except Exception as e:
        print(f"Error creando índices: {e}")

# Crear índices al iniciar
crear_indices()

# Carga de datos relevantes DOTENV (.env)
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Landing page   
@app.route('/')
def inicio():    
    return render_template('select.html', url=client.url_login(), url2=url_for('dashboard'))

# Ruta para el login de spotify
@app.route('/login')
def login():
    return redirect(client.url_login())

# Ruta del dashboard (admin)
@app.route('/dashboard')
def dashboard():
    return render_template('panel.html')

# Ruta de reproductor
@app.route('/player')
def player():
    return render_template('player.html')

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

def insertar_canciones(data_song):
    # Usar upsert para evitar duplicados y mejorar rendimiento
    result = data_conn.collection.update_one(
        {'spotify_id': data_song['spotify_id']},
        {'$set': data_song},
        upsert=True
    )
    return result.upserted_id if result.upserted_id else None

def insertar_reproduccion(data_reproduccion):
    result = data_conn.reproducciones_collection.insert_one(data_reproduccion)
    return result.inserted_id


# Cache para evitar búsquedas repetidas
cancion_cache = {}

def loop_player():
    print("loop iniciando correctamente :D")
    global ultima_cancion_id, cancion_cache
    ultima_cancion_id = None  # guardamos el último ID visto
    while True:
        try:
            token = globals().get('access_token_global')
            if not token:                
                time.sleep(2)  # Reducido para inicialización más rápida
                continue            
            url = 'https://api.spotify.com/v1/me/player'            
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url, headers=headers)   

            
            if response.status_code == 200:
                data_player = response.json()                
                id_cancion = data_player['item']['id']    
                artist_id = data_player['item']['artists'][0]['id']                                   
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
                    url_artist = f"https://api.spotify.com/v1/artists/{artist_id}"
                    resp_artist = requests.get(url_artist, headers=headers)
                    data_artist = resp_artist.json()
                    
                    generos = data_artist.get("genres", [])

                    datos_cancion = {
                        "spotify_id": id_cancion,
                        "artista": nombre_artista,
                        "imagen_album": img_album,
                        "album": nombre_album,
                        "duracion": duracion_formateada,
                        "cancion": name_song
                    }
                    insertar_canciones(datos_cancion)

                    # Cola de reproducciones - usar cache para evitar búsqueda
                    if id_cancion in cancion_cache:
                        cancion = cancion_cache[id_cancion]
                    else:
                        # Búsqueda optimizada con índice en spotify_id
                        cancion = data_conn.collection.find_one({'spotify_id': id_cancion})
                        if cancion:
                            cancion_cache[id_cancion] = cancion
                    
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
                            'hora': hora,
                            'genero': generos
                        }                        
                        insertar_reproduccion(reproduccion_data)
                        print(f"Reproducción registrada: {name_song} - Puntuación: {reproduccion_data['puntuacion']}")
                    
                    print(f" Nueva canción detectada y guardada: {name_song}")
            time.sleep(2)  # Reducido a 2 segundos para actualizaciones más rápidas
        except Exception as e:
            print("Error en el loop", e)
            time.sleep(2)  # Reducido también en caso de error

# Endpoint para verificar que cancion se esta reproduciendo 
@app.route('/estado')
def estado():
    try:
        # Intentar obtener el estado en tiempo real de Spotify
        token = session.get('access_token') or globals().get('access_token_global')
        if token:
            headers = {'Authorization': f'Bearer {token}'}
            url = 'https://api.spotify.com/v1/me/player'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'item' in data:
                    item = data['item']
                    return jsonify({
                        'cancion': item['name'],
                        'artista': item['artists'][0]['name'],
                        'album': item['album']['name'],
                        'imagen_album': item['album']['images'][0]['url'] if item['album']['images'] else '',
                        'duracion': f"{item['duration_ms'] // 60000}:{(item['duration_ms'] % 60000) // 1000:02d}",
                        'is_playing': data.get('is_playing', False)
                    })
        
        # Si no hay estado en tiempo real, usar la última canción de la BD
        ultimas = list(data_conn.collection.find().sort('_id', -1).limit(1))
        if ultimas:
            ultima = ultimas[0]
            ultima['_id'] = str(ultima['_id'])
            ultima['is_playing'] = False  # No sabemos el estado real
            return jsonify(ultima)
        else:
            return jsonify({"status": "No hay canciones registradas"})
    except Exception as e:
        print(f"Error en estado: {e}")
        # Fallback a BD
        ultimas = list(data_conn.collection.find().sort('_id', -1).limit(1))
        if ultimas:
            ultima = ultimas[0]
            ultima['_id'] = str(ultima['_id'])
            ultima['is_playing'] = False
            return jsonify(ultima)
        else:
            return jsonify({"status": "No hay canciones registradas"})
    
# Calcula métricas agregadas de una canción basándose en sus reproducciones.
def calcular_metricas_cancion(reproducciones_cancion):
    """
    Args:
        reproducciones_cancion: Lista de documentos de reproducción
    Returns:
        dict: Métricas calculadas (total, puntuación promedio, impacto promedio)
    """
    total = len(reproducciones_cancion)
    
    if total == 0:
        return {
            'total': 0,
            'puntuacion_promedio': 0.0,
            'impacto_promedio': 0.0
        }
    
    puntuacion_promedio = sum(r['puntuacion'] for r in reproducciones_cancion) / total
    impacto_promedio = sum(r['impacto_ventas'] for r in reproducciones_cancion) / total
    
    return {
        'total': total,
        'puntuacion_promedio': round(puntuacion_promedio, 1),
        'impacto_promedio': round(impacto_promedio, 1)
    }

# Formatea un documento de canción con sus métricas para la respuesta API.
def formatear_cancion(cancion, metricas):
    """
    Formatea un documento de canción con sus métricas para la respuesta API.
    
    Args:
        cancion: Documento de canción de MongoDB
        metricas: Dict con las métricas calculadas
        
    Returns:
        dict: Canción formateada para JSON
    """
    return {
        'id': str(cancion['_id']),
        'nombre': cancion['cancion'],
        'artista': cancion['artista'],
        'album': cancion['album'],
        'genero': cancion.get('genero', []),  # Array de géneros
        'imagen_url': cancion['imagen_album'],
        'reproducciones': metricas['total'],
        'puntuacion': metricas['puntuacion_promedio'],
        'impacto_ventas': metricas['impacto_promedio']
    }

# Agrupa reproducciones por cancion_id para búsqueda eficiente.
def agrupar_reproducciones_por_cancion(reproducciones):
    """
    Args:
        reproducciones: Lista de documentos de reproducción
    Returns:
        dict: Diccionario con cancion_id como key y lista de reproducciones como value
    """
    grupos = {}
    for repro in reproducciones:
        cancion_id = str(repro['cancion_id'])
        if cancion_id not in grupos:
            grupos[cancion_id] = []
        grupos[cancion_id].append(repro)
    return grupos

@app.route('/api/canciones-metricas')
def canciones_metricas():
    """
    Retorna lista de canciones con sus métricas calculadas.
    Ordena por puntuación promedio (mayor a menor).
    
    Respuesta esperada por el frontend:
    {
        'canciones': [
            {
                'id': str,
                'nombre': str,
                'artista': str,
                'album': str,
                'imagen_url': str,
                'reproducciones': int,
                'puntuacion': float,  # 0-10
                'impacto_ventas': float  # porcentaje
            }
        ]
    }
    """
    try:
        # Cargar solo las últimas 20 canciones ordenadas por ID (más recientes)
        canciones = list(data_conn.collection.find().sort('_id', -1).limit(20))
        
        # Obtener IDs de canciones para filtrar reproducciones
        cancion_ids = [cancion['_id'] for cancion in canciones]
        
        # Cargar solo reproducciones de las canciones seleccionadas (más eficiente)
        reproducciones = list(data_conn.reproducciones_collection.find(
            {'cancion_id': {'$in': cancion_ids}}
        ))
        
        # Agrupar reproducciones por canción para búsqueda O(1)
        repros_por_cancion = agrupar_reproducciones_por_cancion(reproducciones)
        
        # Procesar cada canción
        canciones_formateadas = []
        for cancion in canciones:
            cancion_id = str(cancion['_id'])
            reproducciones_cancion = repros_por_cancion.get(cancion_id, [])
            
            metricas = calcular_metricas_cancion(reproducciones_cancion)
            cancion_formateada = formatear_cancion(cancion, metricas)
            canciones_formateadas.append(cancion_formateada)
        
        # Ordenar por puntuación (mayor a menor)
        canciones_formateadas.sort(key=lambda x: x['puntuacion'], reverse=True)
        
        return jsonify({'canciones': canciones_formateadas})
        
    except Exception as e:
        print(f"Error en canciones-metricas: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar las canciones'}), 500
    
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
    """
    Retorna datos agregados de ventas por día de la semana.
    """
    try:
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        # Mapeo de nombres en inglés a español
        dias_esp = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        # Agrupar por día de la semana
        ventas_por_dia = {dia: [] for dia in dias_esp.keys()}
        
        for repro in reproducciones:
            dia = repro['dia_semana']
            if dia in ventas_por_dia:
                ventas_por_dia[dia].append(repro['impacto_ventas'])
        
        # Calcular promedios
        ventas_promedio = []
        for dia_en in dias_esp.keys():
            ventas = ventas_por_dia[dia_en]
            promedio = round(sum(ventas) / len(ventas), 1) if ventas else 0
            ventas_promedio.append(promedio)
        
        datos_grafica = {
            'dias': list(dias_esp.values()),
            'ventas_promedio': ventas_promedio
        }
        
        return jsonify(datos_grafica)
        
    except Exception as e:
        print(f"Error en grafica-ventas: {e}")
        return jsonify({'error': 'Error al cargar datos de ventas'}), 500
    
@app.route('/api/grafica-generos')
def grafica_generos():
    """
    Retorna estadísticas de géneros musicales basadas en reproducciones.
    Calcula el impacto promedio de ventas por género.
    
    IMPORTANTE: Asume que cada reproducción tiene un campo 'genero' que es un array.
    Si una reproducción tiene múltiples géneros, se cuenta para cada uno.
    
    Respuesta:
    {
        'generos': ['Pop', 'Rock', 'Electrónica', ...],
        'valores': [35.5, 20.3, 18.7, ...],  // impacto promedio por género
        'colores': ['#1DB954', '#9b59b6', ...]
    }
    """
    try:
        # Cargar solo reproducciones (ya tienen el género incluido)
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        # Agrupar impacto de ventas por género
        # Como género es un array, cada reproducción puede contar para múltiples géneros
        impacto_por_genero = {}
        
        for repro in reproducciones:
            generos = repro.get('genero', [])
            
            # Si genero no es una lista, convertirlo en lista
            if not isinstance(generos, list):
                generos = [generos] if generos else ['Otros']
            
            # Si la lista está vacía, usar 'Otros'
            if not generos:
                generos = ['Otros']
            
            # Tomar solo el primer genero
            primer_genero = generos[0] if generos else 'Otros'
            genero_limpio = primer_genero.strip() if isinstance(primer_genero, str) else str(primer_genero)
            
            if genero_limpio not in impacto_por_genero:
                impacto_por_genero[genero_limpio] = []
            
            impacto_por_genero[genero_limpio].append(repro['impacto_ventas'])
        
        # Calcular promedio de impacto por género
        generos_stats = []
        for genero, impactos in impacto_por_genero.items():
            promedio = sum(impactos) / len(impactos) if impactos else 0
            generos_stats.append({
                'genero': genero,
                'valor': round(promedio, 1),
                'count': len(impactos)  # Número de reproducciones con este género
            })
        
        # Ordenar por valor (mayor a menor) y tomar top 6
        generos_stats.sort(key=lambda x: x['valor'], reverse=True)
        top_generos = generos_stats[:6]
        
        # Colores predefinidos para géneros
        colores_generos = [
            '#1DB954',  # Verde Spotify
            '#9b59b6',  # Púrpura
            '#3498db',  # Azul
            '#e74c3c',  # Rojo
            '#f39c12',  # Naranja
            '#95a5a6'   # Gris
        ]
        
        datos_grafica = {
            'generos': [g['genero'] for g in top_generos],
            'valores': [g['valor'] for g in top_generos],
            'colores': colores_generos[:len(top_generos)]
        }
        
        return jsonify(datos_grafica)
        
    except Exception as e:
        print(f"Error en grafica-generos: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar datos de géneros'}), 500
    

@app.route('/api/estadisticas-generales')
def estadisticas_generales():
    """
    Retorna estadísticas generales para las tarjetas del dashboard.
    
    Respuesta:
    {
        'puntuacion_promedio': 8.2,
        'impacto_ventas_promedio': 18.5,
        'aforo_promedio': 74.3,
        'total_canciones': 142
    }
    """
    try:
        # Cargar datos
        canciones = list(data_conn.collection.find())
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        # Calcular métricas
        total_canciones = len(canciones)
        
        if reproducciones:
            # Puntuación promedio
            puntuacion_promedio = sum(r['puntuacion'] for r in reproducciones) / len(reproducciones)
            
            # Impacto en ventas promedio
            impacto_ventas_promedio = sum(r['impacto_ventas'] for r in reproducciones) / len(reproducciones)
            
            # Aforo promedio
            aforo_promedio = sum(r.get('aforo', 0) for r in reproducciones) / len(reproducciones)
        else:
            puntuacion_promedio = 0
            impacto_ventas_promedio = 0
            aforo_promedio = 0
        
        estadisticas = {
            'puntuacion_promedio': round(puntuacion_promedio, 1),
            'impacto_ventas_promedio': round(impacto_ventas_promedio, 1),
            'aforo_promedio': round(aforo_promedio, 1),
            'total_canciones': total_canciones,
            'total_reproducciones': len(reproducciones)
        }
        
        return jsonify(estadisticas)
        
    except Exception as e:
        print(f"Error en estadisticas-generales: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar estadísticas'}), 500

# Endpoint para pausar/reanudar la reproducción
@app.route('/api/play-pause', methods=['POST'])
def play_pause():
    try:
        token = session.get('access_token') or globals().get('access_token_global')
        if not token:
            print("Error: No hay token disponible")
            return jsonify({'error': 'No autenticado'}), 401
        
        headers = {'Authorization': f'Bearer {token}'}
        
        # Primero obtenemos el estado actual
        estado_url = 'https://api.spotify.com/v1/me/player'
        estado_response = requests.get(estado_url, headers=headers)
        
        print(f"Estado response: {estado_response.status_code}")
        
        if estado_response.status_code == 204:
            # No hay dispositivo activo
            print("Error: No hay dispositivo de Spotify activo")
            return jsonify({'error': 'No hay dispositivo de Spotify activo. Abre Spotify en tu dispositivo.'}), 400
        
        if estado_response.status_code == 200:
            data = estado_response.json()
            is_playing = data.get('is_playing', False)
            
            print(f"Estado actual - is_playing: {is_playing}")
            
            # Si está reproduciendo, pausamos; si está pausado, reanudamos
            if is_playing:
                pause_url = 'https://api.spotify.com/v1/me/player/pause'
                response = requests.put(pause_url, headers=headers)
                print(f"Pause response: {response.status_code}")
                if response.status_code in [204, 200]:
                    return jsonify({'status': 'paused'})
                else:
                    error_msg = response.json() if response.text else 'Error desconocido'
                    print(f"Error pausando: {error_msg}")
                    return jsonify({'error': 'No se pudo pausar', 'details': error_msg}), 400
            else:
                play_url = 'https://api.spotify.com/v1/me/player/play'
                response = requests.put(play_url, headers=headers)
                print(f"Play response: {response.status_code}")
                if response.status_code in [204, 200]:
                    return jsonify({'status': 'playing'})
                else:
                    error_msg = response.json() if response.text else 'Error desconocido'
                    print(f"Error reproduciendo: {error_msg}")
                    return jsonify({'error': 'No se pudo reproducir', 'details': error_msg}), 400
        
        error_msg = estado_response.json() if estado_response.text else 'Error desconocido'
        print(f"Error obteniendo estado: {estado_response.status_code} - {error_msg}")
        return jsonify({'error': 'No se pudo obtener el estado del reproductor', 'details': error_msg}), 400
        
    except Exception as e:
        print(f"Exception en play-pause: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Endpoint para siguiente canción
@app.route('/api/next', methods=['POST'])
def next_track():
    try:
        token = session.get('access_token') or globals().get('access_token_global')
        if not token:
            print("Error: No hay token disponible")
            return jsonify({'error': 'No autenticado'}), 401
        
        headers = {'Authorization': f'Bearer {token}'}
        url = 'https://api.spotify.com/v1/me/player/next'
        
        response = requests.post(url, headers=headers)
        print(f"Next track response: {response.status_code}")
        
        if response.status_code in [204, 200]:
            return jsonify({'status': 'next'})
        elif response.status_code == 403:
            error_msg = response.json() if response.text else {}
            reason = error_msg.get('error', {}).get('reason', 'unknown')
            print(f"Error 403 en next: {reason}")
            if reason == 'PREMIUM_REQUIRED':
                return jsonify({'error': 'Se requiere cuenta Premium de Spotify'}), 403
            return jsonify({'error': 'Acción no permitida', 'details': error_msg}), 403
        elif response.status_code == 404:
            print("Error 404: No hay dispositivo activo")
            return jsonify({'error': 'No hay dispositivo de Spotify activo'}), 404
        else:
            error_msg = response.json() if response.text else 'Error desconocido'
            print(f"Error en next: {response.status_code} - {error_msg}")
            return jsonify({'error': 'No se pudo cambiar a la siguiente canción', 'details': error_msg}), 400
            
    except Exception as e:
        print(f"Exception en next: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Endpoint para canción anterior
@app.route('/api/previous', methods=['POST'])
def previous_track():
    try:
        token = session.get('access_token') or globals().get('access_token_global')
        if not token:
            print("Error: No hay token disponible")
            return jsonify({'error': 'No autenticado'}), 401
        
        headers = {'Authorization': f'Bearer {token}'}
        url = 'https://api.spotify.com/v1/me/player/previous'
        
        response = requests.post(url, headers=headers)
        print(f"Previous track response: {response.status_code}")
        
        if response.status_code in [204, 200]:
            return jsonify({'status': 'previous'})
        elif response.status_code == 403:
            error_msg = response.json() if response.text else {}
            reason = error_msg.get('error', {}).get('reason', 'unknown')
            print(f"Error 403 en previous: {reason}")
            if reason == 'PREMIUM_REQUIRED':
                return jsonify({'error': 'Se requiere cuenta Premium de Spotify'}), 403
            return jsonify({'error': 'Acción no permitida', 'details': error_msg}), 403
        elif response.status_code == 404:
            print("Error 404: No hay dispositivo activo")
            return jsonify({'error': 'No hay dispositivo de Spotify activo'}), 404
        else:
            error_msg = response.json() if response.text else 'Error desconocido'
            print(f"Error en previous: {response.status_code} - {error_msg}")
            return jsonify({'error': 'No se pudo cambiar a la canción anterior', 'details': error_msg}), 400
            
    except Exception as e:
        print(f"Exception en previous: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    hilo = threading.Thread(target=loop_player, daemon=True)
    hilo.start()    
    app.run(debug=True, use_reloader=False)
