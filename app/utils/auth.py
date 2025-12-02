import hashlib
import base64
import os
from app.database.mongo_connection import db

# Configuración de hash
ITERATIONS = 130000

def hash_password(password, salt=None):
    """Hashea la contraseña con PBKDF2"""
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = base64.b64decode(salt)
    
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        ITERATIONS
    )
    
    return {
        'salt': base64.b64encode(salt).decode('utf-8'),
        'hash': base64.b64encode(pwd_hash).decode('utf-8')
    }

def verify_user(username, password):
    """Verifica las credenciales del usuario en MongoDB"""
    try:
        collection = db["users"]
        user = collection.find_one({"username": username, "active": True})
        
        if not user:
            print(f"❌ Usuario no encontrado: {username}")
            return False
        
        # Hashear la contraseña ingresada con el salt del usuario
        hashed = hash_password(password, user['salt'])
        
        # Comparar hashes
        if hashed['hash'] == user['hash']:
            print(f"✅ Autenticación exitosa: {username}")
            return True
        else:
            print(f"❌ Contraseña incorrecta para: {username}")
            return False
            
    except Exception as e:
        print(f"❌ Error en verify_user: {e}")
        return False

def register_user(username, password):
    """Registra un nuevo usuario en MongoDB"""
    try:
        collection = db["users"]
        
        # Verificar si el usuario ya existe
        if collection.find_one({"username": username}):
            return False, "El usuario ya existe"
        
        # Hashear la contraseña
        hashed = hash_password(password)
        
        # Crear documento del usuario
        new_user = {
            "username": username,
            "salt": hashed['salt'],
            "hash": hashed['hash'],
            "iterations": ITERATIONS,
            "role": "user",
            "active": True
        }
        
        # Insertar en MongoDB
        result = collection.insert_one(new_user)
        
        if result.inserted_id:
            print(f"✅ Usuario registrado: {username} (ID: {result.inserted_id})")
            return True, "Usuario registrado exitosamente"
        else:
            return False, "Error al insertar en la base de datos"
            
    except Exception as e:
        print(f"❌ Error en register_user: {e}")
        return False, f"Error: {str(e)}"

def user_exists(username):
    """Verifica si un usuario existe en MongoDB"""
    try:
        collection = db["users"]
        return collection.count_documents({"username": username}) > 0
    except Exception as e:
        print(f"❌ Error verificando usuario: {e}")
        return False

def get_user_info(username):
    """Obtiene la información completa de un usuario"""
    try:
        collection = db["users"]
        user = collection.find_one({"username": username}, {"hash": 0, "salt": 0})
        return user
    except Exception as e:
        print(f"❌ Error obteniendo info de usuario: {e}")
        return None