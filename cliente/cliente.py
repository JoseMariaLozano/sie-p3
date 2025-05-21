from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..sql.db import get_db_cursor

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')


@cliente_bp.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor, conn = get_db_cursor()
        error = None

        if not nombre or not email or not password:
            error = 'Todos los campos son obligatorios.'
        else:
            cursor.execute('SELECT id FROM cliente WHERE email = %s', (email,))
            if cursor.fetchone():
                error = 'Ya existe un cliente con ese email.'

        if error is None:
            try:
                cursor.execute(
                    'INSERT INTO cliente (nombre, email, password) VALUES (%s, %s, %s)',
                    (nombre, email, generate_password_hash(password))
                )
                conn.commit()
                flash('¡Registro exitoso! Ahora puedes iniciar sesión.')
                return redirect(url_for('cliente.login'))
            except Exception as e:
                conn.rollback()
                error = f'Error al registrar cliente: {str(e)}'

        flash(error)

    return render_template('cliente/registro.html')


@cliente_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        cursor, _ = get_db_cursor()

        try:
            cursor.execute('SELECT * FROM cliente WHERE email = %s', (email,))
            cliente = cursor.fetchone()

            if cliente is None:
                error = 'Usuario no encontrado.'
            elif not check_password_hash(cliente['password'], password):
                error = 'Contraseña incorrecta.'
            else:
                session.clear()
                session['cliente_id'] = cliente['id']
                session['cliente_nombre'] = cliente['nombre']
                return redirect(url_for('index'))

        except Exception as e:
            error = f'Ocurrió un error al iniciar sesión: {str(e)}'

        flash(error)

    return render_template('cliente/login.html')


@cliente_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
