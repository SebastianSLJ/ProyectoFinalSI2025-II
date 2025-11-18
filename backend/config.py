from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    # Puedes agregar más variables aquí
    
    @classmethod
    def validate(cls):
        """Valida que las variables requeridas estén presentes"""
        required = ['CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URI']
        for var in required:
            if not getattr(cls, var):
                raise ValueError(f"Falta la variable de entorno: {var}")
