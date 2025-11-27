from flask import Flask, redirect, request, render_template, session, url_for, jsonify
import threading 
import time
import requests
from datetime import datetime, timedelta
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

@app.route('/metricas')
def metricas():
    return render_template('metricas.html', url=url_for('metricas'))

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
                            'hora': hora,
                            'genero': generos
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
    try:
        # Cargar datos
        canciones = list(data_conn.collection.find().limit(20))
        reproducciones = list(data_conn.reproducciones_collection.find())
        
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
    
@app.route('/api/detalles-dia/<dia>')
def detalles_dia(dia):   
    try:
        # Mapeo de días español a inglés
        dias_map = {
            'Lunes': 'Monday',
            'Martes': 'Tuesday',
            'Miércoles': 'Wednesday',
            'Jueves': 'Thursday',
            'Viernes': 'Friday',
            'Sábado': 'Saturday',
            'Domingo': 'Sunday'
        }
        
        dia_ingles = dias_map.get(dia)
        if not dia_ingles:
            return jsonify({'error': 'Día no válido'}), 400
        
        # Obtener reproducciones del día
        reproducciones = list(data_conn.reproducciones_collection.find({'dia_semana': dia_ingles}))
        
        if not reproducciones:
            return jsonify({
                'dia': dia,
                'impacto_promedio': 0,
                'puntuacion_promedio': 0,
                'aforo_maximo': 0,
                'aforo_minimo': 0,
                'aforo_por_hora': [],
                'total_reproducciones': 0,
                'canciones': [],
                'horas_pico': []
            })
        
        # Calcular métricas generales del día
        total_reproducciones = len(reproducciones)
        impacto_promedio = round(sum(r['impacto_ventas'] for r in reproducciones) / total_reproducciones, 1)
        puntuacion_promedio = round(sum(r['puntuacion'] for r in reproducciones) / total_reproducciones, 1)
        
        # NUEVA LÓGICA DE AFORO: Agrupar por hora y tomar el aforo más representativo
        aforo_por_hora = {}
        
        for repro in reproducciones:
            hora = repro.get('hora', 0)
            aforo = repro.get('aforo', 0)
            
            if hora not in aforo_por_hora:
                aforo_por_hora[hora] = []
            
            aforo_por_hora[hora].append(aforo)
        
        # Calcular aforo promedio por hora (más representativo)
        aforo_hora_promedio = {
            hora: round(sum(aforos) / len(aforos)) 
            for hora, aforos in aforo_por_hora.items()
        }
        
        # Métricas de aforo
        if aforo_hora_promedio:
            aforo_maximo = max(aforo_hora_promedio.values())
            aforo_minimo = min(aforo_hora_promedio.values())
            hora_mas_llena = max(aforo_hora_promedio.items(), key=lambda x: x[1])[0]
        else:
            aforo_maximo = 0
            aforo_minimo = 0
            hora_mas_llena = 0
        
        # Agrupar reproducciones por canción
        canciones_dict = {}
        horas_count = {}
        
        for repro in reproducciones:
            cancion_id = str(repro['cancion_id'])
            hora = repro.get('hora', 0)
            
            # Contar horas
            horas_count[hora] = horas_count.get(hora, 0) + 1
            
            if cancion_id not in canciones_dict:
                canciones_dict[cancion_id] = {
                    'cancion_id': cancion_id,
                    'reproducciones': 0,
                    'puntuaciones': [],
                    'impactos': [],
                    'aforos': []  # Agregar aforos
                }
            
            canciones_dict[cancion_id]['reproducciones'] += 1
            canciones_dict[cancion_id]['puntuaciones'].append(repro['puntuacion'])
            canciones_dict[cancion_id]['impactos'].append(repro['impacto_ventas'])
            canciones_dict[cancion_id]['aforos'].append(repro.get('aforo', 0))
        
        # Obtener IDs de canciones
        cancion_ids = [ObjectId(cid) for cid in canciones_dict.keys()]
        canciones_info = list(data_conn.collection.find({'_id': {'$in': cancion_ids}}))
        
        # Crear mapa de canciones
        canciones_map = {str(c['_id']): c for c in canciones_info}
        
        # Formatear canciones para respuesta
        canciones_formateadas = []
        for cancion_id, stats in canciones_dict.items():
            cancion = canciones_map.get(cancion_id)
            if cancion:
                puntuacion_prom = round(sum(stats['puntuaciones']) / len(stats['puntuaciones']), 1)
                impacto_prom = round(sum(stats['impactos']) / len(stats['impactos']), 1)
                # Aforo promedio cuando sonaba esta canción
                aforo_cancion = round(sum(stats['aforos']) / len(stats['aforos'])) if stats['aforos'] else 0
                
                canciones_formateadas.append({
                    'nombre': cancion['cancion'],
                    'artista': cancion['artista'],
                    'album': cancion['album'],
                    'reproducciones': stats['reproducciones'],
                    'puntuacion': puntuacion_prom,
                    'impacto': impacto_prom,
                    'aforo_promedio': aforo_cancion,  # Aforo cuando sonaba
                    'imagen_url': cancion['imagen_album']
                })
        
        # Ordenar canciones por reproducciones
        canciones_formateadas.sort(key=lambda x: x['reproducciones'], reverse=True)
        
        # Obtener las 3 horas con más actividad
        horas_pico = sorted(horas_count.items(), key=lambda x: x[1], reverse=True)[:3]
        horas_pico_formateadas = []
        
        for hora, count in horas_pico:
            aforo_hora = aforo_hora_promedio.get(hora, 0)
            hora_formato = f"{hora}:00 - {hora+1}:00"
            horas_pico_formateadas.append({
                'hora': hora_formato,
                'reproducciones': count,
                'aforo': aforo_hora
            })
        
        # Preparar datos de aforo por hora para gráfica
        aforo_por_hora_grafica = [
            {
                'hora': f"{h}:00",
                'aforo': aforo_hora_promedio.get(h, 0)
            }
            for h in sorted(aforo_hora_promedio.keys())
        ]
        
        respuesta = {
            'dia': dia,
            'impacto_promedio': impacto_promedio,
            'puntuacion_promedio': puntuacion_promedio,
            'aforo_maximo': aforo_maximo,
            'aforo_minimo': aforo_minimo,
            'hora_mas_llena': hora_mas_llena,
            'aforo_por_hora': aforo_por_hora_grafica,
            'total_reproducciones': total_reproducciones,
            'canciones': canciones_formateadas[:10],
            'horas_pico': horas_pico_formateadas
        }
        
        return jsonify(respuesta)
        
    except Exception as e:
        print(f"Error en detalles-dia: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar detalles del día'}), 500
    

@app.route('/api/kpis-rendimiento')
def kpis_rendimiento():    
    try:
        # Cargar datos
        canciones = list(data_conn.collection.find())
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        if not reproducciones or not canciones:
            return jsonify({
                'mejor_cancion': 'N/A',                
                'mejor_cancion_artista': 'N/A',
                'mejor_cancion_puntuacion': 0,
                'mejor_artista': 'N/A',
                'mejor_artista_impacto': 0,
                'genero_top': 'N/A',
                'genero_reproducciones': 0,
                'hora_pico': 'N/A',
                'mejor_dia': 'N/A',
                'mejor_dia_ventas': 0,
                'tendencia': 'N/A',
                'tendencia_estado': 'Sin datos'
            })
        
        # 1. MEJOR CANCIÓN (por puntuación promedio)
        canciones_stats = {}
        for repro in reproducciones:
            cancion_id = str(repro['cancion_id'])
            if cancion_id not in canciones_stats:
                canciones_stats[cancion_id] = {
                    'puntuaciones': [],
                    'impactos': []
                }
            canciones_stats[cancion_id]['puntuaciones'].append(repro['puntuacion'])
            canciones_stats[cancion_id]['impactos'].append(repro['impacto_ventas'])
        
        mejor_cancion_id = None
        mejor_puntuacion = 0
        
        for cancion_id, stats in canciones_stats.items():
            puntuacion_prom = sum(stats['puntuaciones']) / len(stats['puntuaciones'])
            if puntuacion_prom > mejor_puntuacion:
                mejor_puntuacion = puntuacion_prom
                mejor_cancion_id = cancion_id
        
        mejor_cancion_obj = data_conn.collection.find_one({'_id': ObjectId(mejor_cancion_id)}) if mejor_cancion_id else None
        mejor_cancion = mejor_cancion_obj['cancion'] if mejor_cancion_obj else 'N/A'
        mejor_cancion_artista = mejor_cancion_obj['artista'] if mejor_cancion_obj else 'N/A'
        mejor_cancion_puntuacion = round(mejor_puntuacion, 1)
        
        # 2. MEJOR ARTISTA (por impacto promedio en ventas)
        artistas_stats = {}
        for repro in reproducciones:
            cancion_id = repro['cancion_id']
            cancion = next((c for c in canciones if c['_id'] == cancion_id), None)
            
            if cancion:
                artista = cancion['artista']
                if artista not in artistas_stats:
                    artistas_stats[artista] = []
                artistas_stats[artista].append(repro['impacto_ventas'])
        
        mejor_artista = 'N/A'
        mejor_artista_impacto = 0
        
        for artista, impactos in artistas_stats.items():
            impacto_prom = sum(impactos) / len(impactos)
            if impacto_prom > mejor_artista_impacto:
                mejor_artista_impacto = impacto_prom
                mejor_artista = artista
        
        mejor_artista_impacto = round(mejor_artista_impacto, 1)
        
        # 3. GÉNERO TOP (por número de reproducciones)
        generos_count = {}
        for repro in reproducciones:
            generos = repro.get('genero', [])
            
            if not isinstance(generos, list):
                generos = [generos] if generos else ['Otros']
            
            if not generos:
                generos = ['Otros']
            
            # Tomar solo el primer género
            primer_genero = generos[0] if generos else 'Otros'
            genero_limpio = primer_genero.strip() if isinstance(primer_genero, str) else str(primer_genero)
            
            generos_count[genero_limpio] = generos_count.get(genero_limpio, 0) + 1
        
        if generos_count:
            genero_top = max(generos_count.items(), key=lambda x: x[1])
            genero_top_nombre = genero_top[0]
            genero_reproducciones = genero_top[1]
        else:
            genero_top_nombre = 'N/A'
            genero_reproducciones = 0
        
        # 4. HORA PICO (hora con más reproducciones)
        horas_count = {}
        for repro in reproducciones:
            hora = repro.get('hora', 0)
            horas_count[hora] = horas_count.get(hora, 0) + 1
        
        if horas_count:
            hora_pico_num = max(horas_count.items(), key=lambda x: x[1])[0]
            # Formatear hora pico (ej: "10 PM - 11 PM")
            if hora_pico_num >= 12:
                if hora_pico_num == 12:
                    hora_inicio = "12 PM"
                    hora_fin = "1 PM"
                else:
                    hora_inicio = f"{hora_pico_num - 12} PM"
                    hora_fin = f"{hora_pico_num - 11} PM" if hora_pico_num < 23 else "12 AM"
            else:
                hora_inicio = f"{hora_pico_num} AM" if hora_pico_num > 0 else "12 AM"
                hora_fin = f"{hora_pico_num + 1} AM" if hora_pico_num < 11 else "12 PM"
            
            hora_pico = f"{hora_inicio} - {hora_fin}"
        else:
            hora_pico = 'N/A'
        
        # 5. MEJOR DÍA (día con mayor impacto promedio en ventas)
        dias_map = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        dias_stats = {}
        for repro in reproducciones:
            dia = repro['dia_semana']
            if dia not in dias_stats:
                dias_stats[dia] = []
            dias_stats[dia].append(repro['impacto_ventas'])
        
        mejor_dia = 'N/A'
        mejor_dia_ventas = 0
        
        for dia, impactos in dias_stats.items():
            impacto_prom = sum(impactos) / len(impactos)
            if impacto_prom > mejor_dia_ventas:
                mejor_dia_ventas = impacto_prom
                mejor_dia = dias_map.get(dia, dia)
        
        mejor_dia_ventas = round(mejor_dia_ventas, 1)
        
        # 6. TENDENCIA ACTUAL (género con mayor crecimiento reciente)
        # Comparar últimas 50 reproducciones vs anteriores
        reproducciones_ordenadas = sorted(reproducciones, key=lambda x: x['fecha'], reverse=True)
        
        ultimas_50 = reproducciones_ordenadas[:50] if len(reproducciones_ordenadas) >= 50 else reproducciones_ordenadas
        anteriores_50 = reproducciones_ordenadas[50:100] if len(reproducciones_ordenadas) >= 100 else []
        
        # Contar géneros en cada grupo
        def contar_generos(grupo):
            conteo = {}
            for repro in grupo:
                generos = repro.get('genero', [])
                if isinstance(generos, list) and generos:
                    primer_genero = generos[0].strip() if isinstance(generos[0], str) else str(generos[0])
                    conteo[primer_genero] = conteo.get(primer_genero, 0) + 1
            return conteo
        
        generos_recientes = contar_generos(ultimas_50)
        generos_anteriores = contar_generos(anteriores_50)
        
        # Calcular crecimiento
        mayor_crecimiento = 0
        tendencia = 'N/A'
        tendencia_estado = 'Estable'
        
        for genero in generos_recientes:
            count_reciente = generos_recientes[genero]
            count_anterior = generos_anteriores.get(genero, 0)
            
            if count_anterior > 0:
                crecimiento = ((count_reciente - count_anterior) / count_anterior) * 100
            else:
                crecimiento = 100 if count_reciente > 0 else 0
            
            if crecimiento > mayor_crecimiento:
                mayor_crecimiento = crecimiento
                tendencia = genero
        
        if mayor_crecimiento > 10:
            tendencia_estado = 'En aumento'
        elif mayor_crecimiento < -10:
            tendencia_estado = 'En descenso'
        else:
            tendencia_estado = 'Estable'
        
        # Construir respuesta
        kpis = {
            'mejor_cancion': mejor_cancion,
            'mejor_cancion_puntuacion': mejor_cancion_puntuacion,
            'mejor_cancion_artista': mejor_cancion_artista,
            'mejor_artista': mejor_artista,
            'mejor_artista_impacto': mejor_artista_impacto,
            'genero_top': genero_top_nombre,
            'genero_reproducciones': genero_reproducciones,
            'hora_pico': hora_pico,
            'mejor_dia': mejor_dia,
            'mejor_dia_ventas': mejor_dia_ventas,
            'tendencia': tendencia,
            'tendencia_estado': tendencia_estado
        }
        
        return jsonify(kpis)
        
    except Exception as e:
        print(f"Error en kpis-rendimiento: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar KPIs de rendimiento'}), 500


@app.route('/api/kpis-principales')
def kpis_principales():    
    try:
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        if not reproducciones:
            return jsonify({
                'puntuacion_promedio': 0,
                'puntuacion_cambio': 0,
                'impacto_ventas': 0,
                'impacto_cambio': 0,
                'aforo_promedio': 0,
                'aforo_cambio': 0,
                'reproducciones_totales': 0,
                'reproducciones_cambio': 0
            })        
        
        ahora = datetime.datetime.now()
        hace_7_dias = ahora - timedelta(days=1)
        hace_14_dias = ahora - timedelta(days=2)
        
        # Dividir por períodos reales
        periodo_actual = [r for r in reproducciones if r['fecha'] > hace_7_dias]
        periodo_anterior = [r for r in reproducciones if hace_14_dias < r['fecha'] <= hace_7_dias]
        
        # Si no hay suficientes datos en algún período, usar toda la data disponible
        if not periodo_actual:
            periodo_actual = reproducciones
            periodo_anterior = []
        
        # Función auxiliar para calcular promedios
        def calcular_promedios(periodo):
            if not periodo:
                return {'puntuacion': 0, 'impacto': 0, 'aforo': 0, 'count': 0}
            
            return {
                'puntuacion': sum(r['puntuacion'] for r in periodo) / len(periodo),
                'impacto': sum(r['impacto_ventas'] for r in periodo) / len(periodo),
                'aforo': sum(r.get('aforo', 0) for r in periodo) / len(periodo),
                'count': len(periodo)
            }
        
        stats_anterior = calcular_promedios(periodo_anterior)
        stats_actual = calcular_promedios(periodo_actual)
        
        # Calcular cambios porcentuales
        def calcular_cambio(actual, anterior):
            if anterior == 0:
                return 100 if actual > 0 else 0
            return round(((actual - anterior) / anterior) * 100, 1)
        
        kpis = {
            'puntuacion_promedio': round(stats_actual['puntuacion'], 1),
            'puntuacion_cambio': calcular_cambio(stats_actual['puntuacion'], stats_anterior['puntuacion']),
            'impacto_ventas': round(stats_actual['impacto'], 1),
            'impacto_cambio': calcular_cambio(stats_actual['impacto'], stats_anterior['impacto']),
            'aforo_promedio': round(stats_actual['aforo']),
            'aforo_cambio': calcular_cambio(stats_actual['aforo'], stats_anterior['aforo']),
            'reproducciones_totales': len(reproducciones),
            'reproducciones_cambio': calcular_cambio(stats_actual['count'], stats_anterior['count'])
        }
        
        return jsonify(kpis)
        
    except Exception as e:
        print(f"Error en kpis-principales: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar KPIs principales'}), 500


@app.route('/api/metricas-negocio')
def metricas_negocio():    
    try:
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        if not reproducciones:
            return jsonify({
                'ingresos_totales': 0,
                'ingresos_cambio': 0,
                'ticket_promedio': 0,
                'ticket_cambio': 0,
                'conversion_musical': 0,
                'conversion_cambio': 0
            })   
        
        ahora = datetime.datetime.now()
        hace_7_dias = ahora - timedelta(days=7)
        hace_14_dias = ahora - timedelta(days=14)
        
        # Dividir por períodos 
        periodo_actual = [r for r in reproducciones if r['fecha'] > hace_7_dias]
        periodo_anterior = [r for r in reproducciones if hace_14_dias < r['fecha'] <= hace_7_dias]
        
        # Si no hay datos suficientes, usar mitades como fallback
        if not periodo_actual or not periodo_anterior:
            mitad = len(reproducciones) // 2
            periodo_anterior = reproducciones[:mitad]
            periodo_actual = reproducciones[mitad:]
        
        # Función para calcular métricas de negocio
        def calcular_metricas_negocio(periodo):
            if not periodo:
                return {
                    'ingresos': 0,
                    'ticket': 0,
                    'conversion': 0
                }
            
            # Simular ingresos basados en impacto de ventas y aforo
            # (impacto_ventas * aforo * 10) = ingresos estimados
            ingresos_total = sum(
                (r['impacto_ventas'] * r.get('aforo', 50) * 10) 
                for r in periodo
            )
            
            # Ticket promedio: ingresos / número de reproducciones
            ticket_promedio = ingresos_total / len(periodo)
            
            # Conversión musical: % de canciones con impacto positivo
            impactos_positivos = sum(1 for r in periodo if r['impacto_ventas'] > 0)
            conversion = (impactos_positivos / len(periodo)) * 100           

            return {
                'ingresos': ingresos_total,
                'ticket': ticket_promedio,
                'conversion': conversion
            }
        
        metricas_anterior = calcular_metricas_negocio(periodo_anterior)
        metricas_actual = calcular_metricas_negocio(periodo_actual)
        
        # Calcular cambios
        def calcular_cambio(actual, anterior):
            if anterior == 0:
                return 100 if actual > 0 else 0
            return round(((actual - anterior) / anterior) * 100, 1)
        
        respuesta = {
            'ingresos_totales': round(metricas_actual['ingresos']),
            'ingresos_cambio': calcular_cambio(metricas_actual['ingresos'], metricas_anterior['ingresos']),
            'ticket_promedio': round(metricas_actual['ticket']),
            'ticket_cambio': calcular_cambio(metricas_actual['ticket'], metricas_anterior['ticket']),
            'conversion_musical': round(metricas_actual['conversion']),
            'conversion_cambio': calcular_cambio(metricas_actual['conversion'], metricas_anterior['conversion'])
        }
        
        return jsonify(respuesta)
        
    except Exception as e:
        print(f"Error en metricas-negocio: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar métricas de negocio'}), 500


@app.route('/api/resumen-rapido')
def resumen_rapido():    
    try:
        canciones = list(data_conn.collection.find())
        reproducciones = list(data_conn.reproducciones_collection.find())
        
        if not canciones:
            return jsonify({
                'total_canciones': 0,
                'generos_unicos': 0,
                'artistas_unicos': 0,
                'tiempo_total': 0
            })
        
        # Total de canciones únicas
        total_canciones = len(canciones)
        
        # Artistas únicos
        artistas_unicos = len(set(c['artista'] for c in canciones))
        
        # Géneros únicos (de las reproducciones)
        generos_set = set()
        for repro in reproducciones:
            generos = repro.get('genero', [])
            if isinstance(generos, list):
                for genero in generos:
                    if genero:
                        generos_set.add(genero.strip() if isinstance(genero, str) else str(genero))
            elif generos:
                generos_set.add(generos.strip() if isinstance(generos, str) else str(generos))
        
        generos_unicos = len(generos_set)
        
        # Tiempo total (calculado por reproducciones)
        tiempo_total_minutos = len(reproducciones) * 3.5 # Ejemplo Cambiar - Falta logica de timestamp :((((
        tiempo_total_horas = round(tiempo_total_minutos / 60) #Ejemplo Cambiar - Falta logica de timestamp :(((
        
        resumen = {
            'total_canciones': total_canciones,
            'generos_unicos': generos_unicos,
            'artistas_unicos': artistas_unicos,
            'tiempo_total': tiempo_total_horas
        }
        
        return jsonify(resumen)
        
    except Exception as e:
        print(f"Error en resumen-rapido: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error al cargar resumen rápido'}), 500  

if __name__ == '__main__':
    hilo = threading.Thread(target=loop_player, daemon=True)
    hilo.start()    
    app.run(debug=True, use_reloader=False)
