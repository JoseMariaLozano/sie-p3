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

CATEGORIAS = {
    'mudanza': {'tipo': 1, 'nombre': 'Cajas para Mudanza', 'imagen': 'mudanza.jpeg'},
    'contapa': {'tipo': 2, 'nombre': 'Cajas con Tapa', 'imagen': 'contapa.jpeg'},
    'almacenaje': {'tipo': 3, 'nombre': 'Cajas para Almacenaje', 'imagen': 'almacenaje.jpeg'}
}

@inventario_bp.route('/<categoria>', methods=['GET'])
def mostrar_categoria(categoria):
    if categoria not in CATEGORIAS:
        return "Categoría no encontrada", 404

    tipo = CATEGORIAS[categoria]['tipo']
    nombre_categoria = CATEGORIAS[categoria]['nombre']
    imagen_categoria = CATEGORIAS[categoria]['imagen']

    db = get_db_cursor()
    db.execute('''
        SELECT id_producto, precio, descripcion 
        FROM producto 
        WHERE tipo = %s
    ''', (tipo,))
    productos = db.fetchall()

    return render_template(
        'inventario/categoria.html',
        productos=productos,
        nombre_categoria=nombre_categoria,
        imagen_categoria=imagen_categoria
    )
