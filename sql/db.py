import psycopg2 as pg
import psycopg2.extras as extras

from flask import Blueprint
import click
from flask import current_app
from flask import g
from flask import url_for, redirect

db_bp = Blueprint("db", __name__, url_prefix="/db")

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = pg.connect(
            database='ecogeo',   # Asegúrate de que los valores sean correctos
            user='jose',
            password='ecogeo',
            host='localhost',
        )
        g.db.autocommit = False

    return g.db

def get_db_cursor():
    db = get_db()
    return db.cursor(cursor_factory=extras.RealDictCursor)

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    """Inicializa la base de datos ejecutando scripts SQL."""
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
    """Clear the existing data and create new tables"""
    init_db()
    click.echo("Base de datos inicializada correctamente.")

@db_bp.route("/init_db_from_app", methods=("GET", "POST"))
def init_db_from_app():
    """Ruta para inicializar la base de datos desde la app"""
    init_db()
    return redirect(url_for("index"))

def init_app(app):
    """Registrar las funciones necesarias para la base de datos"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

