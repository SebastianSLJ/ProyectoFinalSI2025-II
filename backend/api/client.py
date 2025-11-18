import random
import string
from flask import session
from urllib.parse import urlencode
from config import Config


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
        'client_id' : Config.CLIENT_ID, #Client ID proporcionado en el dashboard de spotify
        'scope' : scope, # Permisos que estamos solicitando (especificado anteriormente)
        'redirect_uri' : Config.REDIRECT_URI, # URI de redirección especificado en el dashboard de spotify. 
        'state' : state # Es un token de seguridad que previene ataques (Opcional pero recomendado)
    }
    return f'https://accounts.spotify.com/authorize?{urlencode(params)}'