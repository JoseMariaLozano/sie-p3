import flask 

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from ..sql.db import get_db_cursor

rrhh_bp = Blueprint('rrhh', __name__, url_prefix='/rrhh')

# Registrar empleado
@rrhh_bp.route('/registrar', methods=['GET', 'POST'])
def registrar_empleado():
    if request.method == 'POST':
        # Verificamos los datos antes de enviarlos a la base de datos

        dni = request.form['dni']
    
