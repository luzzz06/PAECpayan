from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Conexión a MongoDB
url = "mongodb+srv://MedinaOscar_db_user:Dentista123@cluster0.dngjgxh.mongodb.net/?retryWrites=true&w=majority"
bd = MongoClient(url)["proyecto_payan"]["encuestas_emociones"]

@app.route('/css/<path:archivo>')
def archivos(archivo):
    return send_from_directory('css', archivo)

# Página principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Página de encuesta
@app.route('/formulario.html')
def encuesta():
    return render_template('formulario.html')

# Página nueva para mostrar resultados, tabla y gráfica
@app.route('/resultados.html')
def resultados():
    return render_template('resultados.html')

# Guarda los datos del estudiante en MongoDB
@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.json
    bd.insert_one({
        "nombre": datos["nombre"],
        "edad": int(datos["edad"]),
        "respuestas": datos["respuestas"],
        "emocion": datos["emocion"],
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    return jsonify({"ok": True})

# Obtiene todos los registros de MongoDB para la tabla y gráfica
@app.route('/datos', methods=['GET'])
def obtener_datos():
    lista = list(bd.find({}, {"_id": 0}))
    return jsonify(lista)

if __name__ == '__main__':
    app.run(debug=True, port=5600)