from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "supersecreto"

# URL de la API de FastAPI
FASTAPI_URL = "http://127.0.0.1:5001"

# Ruta para el formulario
@app.route("/", methods=['GET'])
def home():
    return render_template("registro.html")

# Ruta para la consulta
@app.route("/consulta", methods=['GET'])
def consulta():
    return render_template("consulta.html")

# Ruta para agregar un nuevo usuario en FastAPI
@app.route("/usuariosFastAPI", methods=['POST'])
def post_usuario():
    try:
        usuarioNuevo = {
            "name": request.form['txtNombre'],
            "age": int(request.form['txtEdad']),
            "email": request.form['txtCorreo']
        }

        response = requests.post(f"{FASTAPI_URL}/agregarusuariodb", json=usuarioNuevo)

        if response.status_code == 200 or response.status_code == 201:
            flash("Usuario guardado correctamente", "success")
        else:
            flash(f"Error al guardar usuario: {response.json().get('detail', 'Error desconocido')}", "danger")

        return redirect(url_for('home'))

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "No se pudo conectar con la API", "detalle": str(e)}), 500

# Endpoint para obtener todos los usuarios desde FastAPI
@app.route("/ConsultUsuarios", methods=['GET'])
def get_usuarios():
    try:
        response = requests.get(f"{FASTAPI_URL}/todosusuarios/")
        response.raise_for_status()
        usuarios = response.json()

        return render_template("consulta.html", usuarios=usuarios)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "No se pudo conectar con la API", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8002)
