from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

# Lista de seminarios disponibles
SEMINARIOS = ['Inteligencia Artificial', 'Machine Learning', 'Simulación en Arena', 'Robótica Educativa']

# Inicializa la lista de inscritos en la sesión si no existe
def init_session():
    if 'inscritos' not in session:
        session['inscritos'] = []

# Ruta para registrar un nuevo inscrito
@app.route('/', methods=['GET', 'POST'])
def registrar():
    init_session()
    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')

        # Crear el nuevo inscrito
        nuevo_inscrito = {
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios
        }

        # Guardar en session
        inscritos = session['inscritos']
        inscritos.append(nuevo_inscrito)
        session['inscritos'] = inscritos  # Actualiza la sesión con la lista modificada

        return redirect(url_for('listar'))

    return render_template('registrar.html', seminarios=SEMINARIOS)

# Ruta para listar los inscritos
@app.route('/listar')
def listar():
    init_session()
    inscritos = session.get('inscritos', [])
    return render_template('listar.html', inscritos=inscritos)

# Ruta para eliminar un inscrito
@app.route('/eliminar/<int:index>')
def eliminar(index):
    init_session()
    inscritos = session.get('inscritos', [])
    if 0 <= index < len(inscritos):
        del inscritos[index]
        session['inscritos'] = inscritos  # Actualiza la lista en la sesión
    return redirect(url_for('listar'))

if __name__ == '__main__':
    app.run(debug=True)
