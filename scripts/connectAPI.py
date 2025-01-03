import requests
import os
import time
from pymongo import MongoClient

# Configuración desde variables de entorno
mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongoDB:27017/')
db_name = os.getenv('DB_NAME', 'bicis_db')
collection_name = os.getenv('COLLECTION_NAME', 'bicicorunha')

# URL de la API
url = "http://api.citybik.es/v2/networks/bicicorunha"
intervalo_minutos = 2  

# Conexión a Mongodb
try:
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    exit(1)

# Función para hacer la solicitud a la API
def obtener_datos():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            stations = data["network"]["stations"]
            
            # Insertar todas las estaciones a la vez
            collection.insert_many(stations)
            print(f"{len(stations)} estaciones almacenadas correctamente.")
        else:
            error_message = f"Error {response.status_code}: {response.text}"
            print(error_message)
            raise Exception(error_message)  # Lanzar una excepción para detener el bucle
    except Exception as e:
        print(f"Error al conectar a la API o almacenar datos en MongoDB: {e}")
        raise  # Volver a lanzar la excepción para manejarla en el nivel superior

# Bucle principal para ejecutar la solicitud periódicamente
try:
    while True:
        obtener_datos()
        time.sleep(intervalo_minutos * 60)  
except KeyboardInterrupt:
    print("\nEjecución interrumpida por el usuario. Finalizando el programa...")
except Exception as e:
    print(f"Ejecución detenida debido a un error{e}")
finally:
    client.close()
    print("Conexión a MongoDB cerrada.")
