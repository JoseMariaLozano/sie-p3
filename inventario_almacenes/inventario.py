import flask 

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import abort

from ..sql.db import get_db_cursor

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')

CATEGORIAS = {
    'mudanza': {'tipo': 1, 'nombre': 'Cajas para Mudanza', 'imagen': 'mudanza.jpeg'},
    'contapa': {'tipo': 2, 'nombre': 'Cajas con Tapa', 'imagen': 'contapa.jpeg'},
    'almacenaje': {'tipo': 3, 'nombre': 'Cajas para Almacenaje', 'imagen': 'almacenaje.jpeg'}
}

def obtener_categoria_por_tipo(tipo):
    for clave, datos in CATEGORIAS.items():
        if datos['tipo'] == tipo:
            return clave
    return None


def obtener_producto_por_id(producto_id):
    try:
        db = get_db_cursor()
        db.execute('''
            SELECT id_producto, precio, descripcion, tamano, tipo, cantidad
            FROM producto
            WHERE id_producto = %s
        ''', (producto_id,))
        producto = db.fetchone()
        return producto
    except Exception as e:
        print(f"[ERROR] Fallo al consultar producto por id: {e}")
        return None

@inventario_bp.route('/<categoria>', methods=['GET'])
def mostrar_categoria(categoria):
    if categoria not in CATEGORIAS:
        return "Categoría no encontrada", 404

    tipo = CATEGORIAS[categoria]['tipo']
    nombre_categoria = CATEGORIAS[categoria]['nombre']
    imagen_categoria = CATEGORIAS[categoria]['imagen']

    # Obtener parámetros GET
    size_filter = request.args.get('size')
    sort_order = request.args.get('sort')  # puede ser 'asc' o 'desc'

    query = '''
        SELECT id_producto, precio, descripcion, tamano
        FROM producto
        WHERE tipo = %s
    '''
    params = [tipo]

    # Agregar filtro por tamaño si se proporciona
    if size_filter in ['pequeño', 'mediano', 'grande']:
        query += ' AND tamano = %s'
        params.append(size_filter)

    # Agregar orden por precio si se proporciona
    if sort_order == 'asc':
        query += ' ORDER BY precio ASC'
    elif sort_order == 'desc':
        query += ' ORDER BY precio DESC'

    try:
        db = get_db_cursor()
        db.execute(query, tuple(params))
        productos = db.fetchall()
    except Exception as e:
        print(f"[ERROR] Fallo al consultar productos: {e}")
        flash("Hubo un error al cargar los productos. Por favor, inténtalo más tarde.", "error")
        productos = []

    return render_template(
        'inventario/categoria.html',
        productos=productos,
        nombre_categoria=nombre_categoria,
        imagen_categoria=imagen_categoria,
        categoria=categoria
    )

@inventario_bp.route("/producto/<int:producto_id>")
def detalle_producto(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if producto is None:
        abort(404)

    categoria = obtener_categoria_por_tipo(producto['tipo'])
    if categoria is None:
        abort(500)  # Si no se encuentra la categoría, es un error del sistema

    imagen_categoria = CATEGORIAS[categoria]['imagen']

    return render_template("detalles_productos.html", producto=producto, imagen_categoria=imagen_categoria)

