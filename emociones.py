
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import os

class Emociones:

    def __init__(self, uri=None):
        try:
            uri = uri or os.getenv("MONGODB_URI")

            if not uri:
                raise ValueError("No se encontró la conexión de MongoDB")

            self.cliente = MongoClient(
                uri,
                serverSelectionTimeoutMS=5000
            )

            self.cliente.admin.command("ping")

            self.db = self.cliente["Emociones"]
            self.encuesta = self.db["Encuesta"]

            print("Conexión a MongoDB Atlas exitosa")

        except ConnectionFailure:
            print("Error: No se pudo conectar a MongoDB Atlas")
            raise

    def insertar_encuesta(self, edad, respuestas, emocion):
        try:
            resultado = self.encuesta.insert_one({
                "edad": edad,
                "respuestas": respuestas,
                "emocion": emocion,
                "fecha": datetime.now()
            })

            return str(resultado.inserted_id)

        except Exception as e:
            print(f"Error al guardar encuesta: {e}")
            return None

    def obtener_encuestas(self):
        try:
            return list(
                self.encuesta.find().sort("_id", -1)
            )

        except Exception as e:
            print(f"Error al obtener encuestas: {e}")
            return []

    def obtener_emociones(self):
        try:
            return list(
                self.encuesta.aggregate([
                    {
                        "$group": {
                            "_id": "$emocion",
                            "total": {"$sum": 1}
                        }
                    }
                ])
            )

        except Exception as e:
            print(f"Error al consultar emociones: {e}")
            return []

    def cerrar_conexion(self):
        self.cliente.close()
