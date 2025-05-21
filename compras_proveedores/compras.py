# compras_proveedores/compras.py

from flask import Blueprint

compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/comprar')
def comprar():
    return "Página de compras mega epica"