from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'root',
    'password': 'tu_contraseña',
    'host': 'localhost',
    'database': 'crud_libros'
}

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    conn.close()
    return render_template('index.html', libros=libros)

@app.route('/create', methods=['POST'])
def create():
    titulo = request.form['titulo']
    autor = request.form['autor']
    anio = request.form['anio']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO libros (titulo, autor, anio) VALUES (%s, %s, %s)', (titulo, autor, anio))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM libros WHERE id = %s', (id,))
    libro = cursor.fetchone()

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        anio = request.form['anio']
        
        cursor.execute('UPDATE libros SET titulo = %s, autor = %s, anio = %s WHERE id = %s', 
                       (titulo, autor, anio, id))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('update.html', libro=libro)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM libros WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
