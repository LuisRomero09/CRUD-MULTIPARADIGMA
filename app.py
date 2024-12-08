from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configuración de la base de datos usando variables de entorno
db_config = {
    'host': os.environ.get('DB_HOST', 'autorack.proxy.rlwy.net'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'gdyeJxAyIROKBOyACzomwnshJbkTsmUH'),
    'database': os.environ.get('DB_NAME', 'railway'),
    'port': int(os.environ.get('DB_PORT', 36293))
}

# Ruta principal - Listar libros
@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    conn.close()
    return render_template('index.html', libros=libros)

# Crear un nuevo libro
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        anio = request.form['anio']
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO libros (titulo, autor, anio) VALUES (%s, %s, %s)", (titulo, autor, anio))
        conn.commit()
        conn.close()
        flash('Libro agregado con éxito.', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

# Actualizar un libro
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        anio = request.form['anio']
        cursor.execute("UPDATE libros SET titulo = %s, autor = %s, anio = %s WHERE id = %s", (titulo, autor, anio, id))
        conn.commit()
        conn.close()
        flash('Libro actualizado con éxito.', 'success')
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM libros WHERE id = %s", (id,))
        libro = cursor.fetchone()
        conn.close()
        return render_template('update.html', libro=libro)

# Eliminar un libro
@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash('Libro eliminado con éxito.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8083))  # Render asigna dinámicamente el puerto
    app.run(host='0.0.0.0', port=port)
