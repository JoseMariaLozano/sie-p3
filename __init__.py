import os
from flask import Flask, render_template
import click

# No necesitamos SQLAlchemy ni psycopg2
# db = SQLAlchemy()

def create_app(test_config=None):
    # Crear y configurar la app
    app = Flask(__name__, instance_relative_config=True)

    # Configuración sin base de datos
    app.config.from_mapping(
        SECRET_KEY='dev',
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

    # Registrar todos los blueprints de módulos
    from .compras_proveedores.compras import compras_bp
    from .ventas_comercial.ventas import ventas_bp
    from .inventario_almacenes.inventario import inventario_bp
    from .cliente.cliente import cliente_bp
    from .sql.db import db_bp, get_db_cursor

    # Registrar los blueprints
    app.register_blueprint(compras_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(db_bp)

    # Ruta raíz de la aplicación
    @app.route('/')
    def index():
        """
        cur = get_db_cursor()
        cur.execute("SELECT nombre, descripcion, precio FROM producto")
        productos = cur.fetchall()
        """
        return render_template("index.html")

    return app

