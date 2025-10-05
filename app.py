from flask import Flask, render_template, request
from sintacticocurp import generar_curp_desde_formulario

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/generar_curp', methods=['POST'])

def ejecutar_generar_curp():
    nombre = request.form.get('nombre', '').strip().upper()
    apellido = request.form.get('apellido', '').strip().upper()
    segundo_apellido = request.form.get('segundo_apellido', '').strip().upper()
    dia = request.form.get('dia', '').strip()
    mes = request.form.get('mes', '').strip()
    anio = request.form.get('anio', '').strip()
    sexo = request.form.get('sexo', '').strip().upper()
    estado = request.form.get('estado', '').strip().upper()
    resultado = generar_curp_desde_formulario(
        nombre, apellido, segundo_apellido, 
        dia, mes, anio, sexo, estado
    )
    return render_template("index.html", resultado=resultado, nombre=nombre, apellido=apellido, 
                           segundo_apellido=segundo_apellido, dia=dia, mes=mes, anio=anio, sexo=sexo, estado=estado)
if __name__ == "__main__":
    app.run(debug=False)