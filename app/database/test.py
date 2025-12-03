from mongo_connection import db, test_connection

def main():
    print("🔍 Iniciando test...")
    
    # Probar conexión
    conexion_exitosa = test_connection()
    print(f"🔍 Resultado de conexión: {conexion_exitosa}")
    
    if not conexion_exitosa:
        print("❌ No se pudo conectar, abortando...")
        return
    
    print("🔍 Procediendo con operaciones...")
    
    # Tus operaciones
    collection = db["usuarios"]
    
    # Insertar
    result = collection.insert_one({"nombre": "Ana", "edad": 30})
    print(f"✅ Insertado con ID: {result.inserted_id}")
    
    # Consultar
    print("\n👥 Consultando usuarios:")
    usuarios = collection.find()
    for usuario in usuarios:
        print(f"  - {usuario}")

if __name__ == "__main__":
    main()