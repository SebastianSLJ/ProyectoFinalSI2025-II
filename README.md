# Proyecto Integrador grupo No_Name

## Información de contacto

| **Nombre** | **Correo** |
|------------|------------|
|Jefferson Jair Figueroa Escobar | Jfigueroa@unal.edu.co | 
|Juan David Beltran Orjuela | jbeltrano@unal.edu.co |
|John Jairo Paez Albino | jopaeza@unal.edu.co |
|Juan Sebastain Leguizamón Silva | jleguizamons@unal.edu.co |



## Descripción

<p align="justify">
Este proyecto se basa en un ERP que será utilizado por un Bar ubicado en Bogotá, el cual le permite conectarse con la API de Spotify para controlar las canciones en su negocio y hacer procesos de BI (Business Inteligente)
</p>

# Pasos de instalación

1. Clonar el repositorio 
    1. Abrir una terminal y ejecutar:

```jsx
git clone https://github.com/bastianSLJ/ProyectoFinalSI2025-II
cd ProyectoFinalSI2025-II
```

1. Crear y activar un entorno virtual 

```jsx
python -m venv venv
venv\Scripts\activate       
```

1. Instalar dependencias

```jsx
pip install

Flask
requests
pymongo
python-dotenv
threading
```

1. Configurar las variables de entorno 

```jsx
SPOTIFY_CLIENT_ID=tu_client_id
SPOTIFY_CLIENT_SECRET=tu_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
MONGO_URI=tu_uri_de_mongodb_atlas
SECRET_KEY=una_clave_secreta_segura

```

1. Ejecutar la aplicación 

```jsx
python app.py
```

1. Configuración de base de datos
    1. Crear una cuenta en MongoDB Atlas 
    2. Crear un cluster gratuito 
    3. Dentro del cluster 
        1. Crear una base de datos 
        2. Crear una colección (canciones)
    4. Copiar el URI de conexión en el archivo .env, en la variable: 

```jsx
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/spotify_data
```
