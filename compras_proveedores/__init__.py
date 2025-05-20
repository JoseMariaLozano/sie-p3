# compras_proveedores/compras.py

from flask import Blueprint

compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/compras')
def compras():
    return "Página de compras"

