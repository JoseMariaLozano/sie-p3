from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..sql.db import get_db_cursor

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')


@cliente_bp.route('/register', methods=['GET', 'POST'])
<<<<<<< HEAD
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        db = get_db()
=======
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        db = get_db_cursor()
>>>>>>> ce336c6edcb8e4432e7c1317758d9c64e52ae808
        error = None

        if not nombre or not email or not password:
            error = 'Todos los campos son obligatorios.'
<<<<<<< HEAD
        elif db.execute('SELECT id FROM cliente WHERE email = ?', (email,)).fetchone():
            error = 'Ya existe un cliente con ese email.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO cliente (nombre, email, password) VALUES (?, ?, ?)',
                    (nombre, email, generate_password_hash(password))
                )
                db.commit()
                flash('¡Registro exitoso! Ahora puedes iniciar sesión.')
                return redirect(url_for('cliente.login'))
            except Exception as e:
                db.rollback()
                error = f'Error al registrar cliente: {str(e)}'
=======
        elif db.execute('SELECT id FROM cliente WHERE email = %s', (email,)).fetchone():
            error = 'Ya existe un cliente con ese email.'

        if error is None:
            db.execute(
                'INSERT INTO cliente (nombre, email, password) VALUES (%s, %s, %s)',
                (nombre, email, generate_password_hash(password))
            )
            db.commit()
            flash('¡Registro exitoso!')
            return redirect(url_for('cliente.login'))
>>>>>>> ce336c6edcb8e4432e7c1317758d9c64e52ae808

        flash(error)

    return render_template('cliente/registro.html')


@cliente_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
<<<<<<< HEAD
        email = request.form.get('email')
        password = request.form.get('password')

        db = get_db()
=======
        email = request.form['email']
        password = request.form['password']
        db = get_db_cursor()
>>>>>>> ce336c6edcb8e4432e7c1317758d9c64e52ae808
        error = None

        cliente = db.execute(
<<<<<<< HEAD
            'SELECT * FROM cliente WHERE email = ?', (email,)
=======
            'SELECT * FROM cliente WHERE email = %s', (email,)
>>>>>>> ce336c6edcb8e4432e7c1317758d9c64e52ae808
        ).fetchone()

        if cliente is None:
            error = 'Usuario no encontrado.'
        elif not check_password_hash(cliente['password'], password):
            error = 'Contraseña incorrecta.'

        if error is None:
            session.clear()
            session['cliente_id'] = cliente['id']
            session['cliente_nombre'] = cliente['nombre']
            return redirect(url_for('index'))

        flash(error)

    return render_template('cliente/login.html')


@cliente_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

