import os
import psycopg2 as pg
import psycopg2.extras as extras
from flask import Flask, render_template, current_app, g
from flask_sqlalchemy import SQLAlchemy
import click

# Instanciamos la base de datos
db = SQLAlchemy()

def get_db():
    """Conectar a la base de datos configurada de la aplicación. La conexión es única para cada solicitud y se reutiliza si se llama de nuevo."""
    if "db" not in g:
        g.db = pg.connect(
            database='ecogeo',  # Reemplaza con tu base de datos
            user='jose',        # Reemplaza con tu usuario de PostgreSQL
            password='ecogeo',   # Reemplaza con tu contraseña
            host='localhost',
        )
        g.db.autocommit = False
    return g.db

def get_db_cursor():
    """Obtener el cursor de la base de datos."""
    db = get_db()
    return db.cursor(cursor_factory=extras.RealDictCursor)

def close_db(e=None):
    """Si esta solicitud está conectada a la base de datos, cierra la conexión."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Función para inicializar la base de datos (en tu caso, ejecutar los scripts SQL necesarios)."""
    cur = get_db_cursor()
    
    # Lista de archivos SQL a ejecutar
    sql_files = [
        "schema.sql",
        "insertar.sql",
        "trigger-clientes.sql",
        "trigger-empleados.sql",
        "trigger-vehiculos.sql",
        "trigger-pedidos.sql"
    ]
    
    for sql_file in sql_files:
        with current_app.open_resource(f"./sql/{sql_file}") as f:
            cur.execute(f.read().decode("utf8"))
            cur.execute("COMMIT;")

@click.command('init-db')
def init_db_command():
    """Limpiar los datos existentes y crear nuevas tablas"""
    init_db()
    click.echo("Base de datos inicializada")

# Definición del Blueprint para la base de datos
db_bp = Blueprint("db", __name__, url_prefix="/db")

@db_bp.route("/init_db_from_app", methods=("GET", "POST"))
def init_db_from_app():
    init_db()
    return redirect(url_for("index"))

def init_app(app):
    """Registrar el Blueprint y los comandos en la aplicación"""
    app.teardown_appcontext(close_db)  # Cerrar la conexión después de cada solicitud
    app.cli.add_command(init_db_command)  # Registrar el comando init-db

def create_app(test_config=None):
    # Crear y configurar la app
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración de la base de datos (usando PostgreSQL y SQLAlchemy)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://jose:ecogeo@localhost/ecogeo',  # Cambia con tu configuración de PostgreSQL
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # Cargar config por defecto desde config.py (si existe)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Cargar configuración de testing
        app.config.from_mapping(test_config)

    # Crear la carpeta 'instance' si no existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializamos la base de datos con la aplicación Flask
    db.init_app(app)

    # Registrar todos los blueprints de módulos
    from .compras_proveedores.compras import compras_bp
    from .ventas_comercial.ventas import ventas_bp
    from .inventario_almacenes.inventario import inventario_bp
    from cliente import cliente_bp

    # Registrar los blueprints
    app.register_blueprint(compras_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(db_bp)  # Registrar el blueprint de db
    app.register_blueprint(cliente_bp)

    # Ruta raíz de la aplicación
    @app.route('/')
    def index():
        return render_template('index.html')

    # Inicializar la base de datos (función de inicialización en CLI)
    init_app(app)

    return app

