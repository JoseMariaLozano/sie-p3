from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..sql.db import get_db_cursor

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')


from flask import flash

@cliente_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        direccion = request.form['direccion']
        telefono = request.form.get('telefono', '')
        es_empresa = 'es_empresa' in request.form
        nombre_empresa = request.form.get('nombre_empresa') if es_empresa else 'default'

        tarjeta_numero = request.form['tarjeta_numero']
        try:
            tarjeta_mes_expiracion = int(request.form['tarjeta_mes_expiracion'])
            tarjeta_anio_expiracion = int(request.form['tarjeta_anio_expiracion'])
        except ValueError:
            flash('Mes y año de expiración deben ser números válidos.', 'error')
            return render_template('cliente/register.html')

        tarjeta_cvv = request.form['tarjeta_cvv']

        # Validación de mes y año
        if not (1 <= tarjeta_mes_expiracion <= 12):
            flash('El mes de expiración debe estar entre 1 y 12.', 'error')
            return render_template('cliente/register.html')
        if tarjeta_anio_expiracion < 2024:
            flash('El año de expiración debe ser 2024 o superior.', 'error')
            return render_template('cliente/register.html')

        # Aquí irían más validaciones o hashing de password

        
        try:
            cur = get_db_cursor()
            cur.execute("""
                INSERT INTO cliente (
                    nombre, email, password, direccion, telefono, es_empresa, nombre_empresa,
                    tarjeta_numero, tarjeta_mes_expiracion, tarjeta_anio_expiracion, tarjeta_cvv
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nombre, email, password, direccion, telefono, es_empresa, nombre_empresa,
                tarjeta_numero, tarjeta_mes_expiracion, tarjeta_anio_expiracion, tarjeta_cvv
            ))
            cur.execute('COMMIT;')
            flash('Registro completado con éxito', 'success')
            return redirect(url_for('cliente.login'))
        except Exception as e:
            flash(f'Error al registrar cliente: {e}', 'error')
            return render_template('cliente/register.html')

    return render_template('cliente/register.html')



@cliente_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        try:
            cur = get_db_cursor()
            cur.execute('SELECT * FROM cliente WHERE email = %s', (email,))
            cliente = cur.fetchone()
            cur.execute('COMMIT;')

            if cliente is None:
                error = 'Usuario no encontrado.'
            elif not cliente['password'] == password:
                error = 'Contraseña incorrecta.'
            else:
                session.clear()
                session['id_cliente'] = cliente['id']
                session['cliente_nombre'] = cliente['nombre']
                return redirect(url_for('index'))

        except Exception as e:
            error = f'Ocurrió un error al iniciar sesión: {str(e)}'

        flash(error, 'error')

    return render_template('cliente/login.html')


@cliente_bp.route('/logout')
def logout():
    id_cliente = session.get("id_cliente")
    cur = get_db_cursor()

    if id_cliente:
        cur.execute("""
            DELETE FROM ticket
            WHERE id_cliente = %s AND estado = 'abierto';
        """, (id_cliente,))
        cur.execute("COMMIT;")

    session.clear()
    flash("Sesión cerrada y carrito cancelado.", "info")
    return render_template("index.html")

