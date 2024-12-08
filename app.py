from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'autorack.proxy.rlwy.net',
    'user': 'root',
    'password': 'gdyeJxAyIROKBOyACzomwnshJbkTsmUH',
    'database': 'railway',
    'port': 36293
}

# Rutas
@app.route('/')
def index():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    connection.close()
    return render_template('index.html', libros=libros)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        anio = request.form['anio']
        
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, autor, anio) VALUES (%s, %s, %s)",
            (titulo, autor, anio)
        )
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    
    return render_template('create.html')


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=False)
