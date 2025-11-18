from config import Config
import requests

# Función para revisar errores con el codigo y el state recibidos. 
def handle_oauth_callback(code, stored_state, received_state):
    if stored_state is None:
        return 'Error: No se inicio correctamente'
    if received_state != stored_state:
        return 'Error: State no coincide'
    
    token_response = UserToken(code)
    return token_response

# Petición al API para obtención del codigo de inicio 
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
        'redirect_uri' : Config.REDIRECT_URI, 
        'client_id' : Config.CLIENT_ID,        
        'client_secret': Config.CLIENT_SECRET,      
    }
    response = requests.post(url, headers= headers, data=body)
    return response.json()