import flask 

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from ..sql.db import get_db_cursor

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')
