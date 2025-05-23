import flask 

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import jsonify

from ..sql.db import get_db_cursor, get_db

ventas_bp = Blueprint("ventas", __name__, url_prefix="/ventas")

@ventas_bp.route("/carrito", methods=["GET", "POST"])
def mostrar_carrito():
    id_cliente = session.get("id_cliente")

    if not id_cliente:
        return "Usuario no autenticado", 401

    cur = get_db_cursor()

    # 1. Obtener el ticket abierto
    cur.execute("""
        SELECT id
        FROM ticket
        WHERE id_cliente = %s AND estado = 'abierto'
        LIMIT 1;
    """, (id_cliente,))
    ticket = cur.fetchone()

    if not ticket:
        return render_template("carrito.html", carrito=[], precio_total=0, facturacion={})

    id_ticket = ticket["id"]

    # 2. Obtener los productos del carrito junto con la cantidad disponible en producto
    cur.execute("""
        SELECT
            c.id_producto AS id,
            p.descripcion,
            c.precio_unitario,
            c.cantidad,
            p.cantidad AS cantidad_disponible
        FROM carrito c
        JOIN producto p ON c.id_producto = p.id_producto
        WHERE c.id_ticket = %s;
    """, (id_ticket,))
    productos = cur.fetchall()

    # 3. Calcular el precio total
    precio_total = sum(p["precio_unitario"] * p["cantidad"] for p in productos)

    # 4. Obtener los datos de facturación del cliente
    cur.execute("""
        SELECT tarjeta_numero, tarjeta_mes_expiracion, tarjeta_anio_expiracion, tarjeta_cvv
        FROM cliente
        WHERE id = %s;
    """, (id_cliente,))
    cliente = cur.fetchone()

    facturacion = {
        "numero_tarjeta": cliente["tarjeta_numero"],
        "mes_caducidad": cliente["tarjeta_mes_expiracion"],
        "ano_caducidad": cliente["tarjeta_anio_expiracion"],
        "cvv": cliente["tarjeta_cvv"],
    }

    return render_template("compras/carrito.html", carrito=productos, precio_total=precio_total, facturacion=facturacion)



@ventas_bp.route("/añadir", methods=["POST"])
def añadir_carrito():
    if "id_cliente" not in session:
        return redirect(url_for("cliente.login"))

    id_cliente = session["id_cliente"]
    id_producto = int(request.form["id_producto"])
    cantidad = int(request.form["cantidad"])
    precio_unitario = float(request.form["precio_unitario"])

    conn = get_db()
    cur = conn.cursor()

    try:
        # 1. Verificar si el cliente ya tiene un ticket 'abierto'
        try:
            cur.execute("""
                SELECT id FROM ticket
                WHERE id_cliente = %s AND estado = 'abierto'
                ORDER BY fecha DESC LIMIT 1;
            """, (id_cliente,))
            resultado = cur.fetchone()
        except Exception as e:
            flash(f"Error al consultar ticket abierto: {str(e)}", "error")
            return redirect(url_for("inventario.detalle_producto", producto_id=id_producto))

        if resultado is not None:
            id_ticket = resultado[0]
        else:
            # 2. Crear ticket nuevo (estado abierto)
            try:
                cur.execute("""
                    INSERT INTO ticket (id_cliente, estado)
                    VALUES (%s, 'abierto')
                    RETURNING id;
                """, (id_cliente,))
                id_ticket = cur.fetchone()[0]
            except Exception as e:
                flash(f"Error al crear nuevo ticket: {str(e)}", "error")
                conn.rollback()
                return redirect(url_for("inventario.detalle_producto", producto_id=id_producto))

        # 3. Guardar en carrito (creamos savepoint solo si hay ticket válido)
        try:
            cur.execute("SAVEPOINT save_carrito;")
        except Exception as e:
            flash(f"Error al crear savepoint: {str(e)}", "error")
            conn.rollback()
            return redirect(url_for("inventario.detalle_producto", producto_id=id_producto))

        try:
            cur.execute("""
                INSERT INTO carrito (id_ticket, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s);
            """, (id_ticket, id_producto, cantidad, precio_unitario))
        except Exception as e:
            try:
                cur.execute("ROLLBACK TO SAVEPOINT save_carrito;")
            except Exception:
                conn.rollback()
            flash(f"Error al insertar en carrito: {str(e)}", "error")
            return redirect(url_for("inventario.detalle_producto", producto_id=id_producto))

        # Commit general si todo va bien
        try:
            conn.commit()
        except Exception as e:
            flash(f"Error al hacer commit: {str(e)}", "error")
            conn.rollback()
            return redirect(url_for("inventario.detalle_producto", producto_id=id_producto))

        flash("Producto añadido al carrito correctamente.", "success")
        return redirect(url_for("inventario.detalle_producto", producto_id=id_producto))

    except Exception as e:
        # Error inesperado general
        conn.rollback()
        flash(f"Error inesperado en añadir al carrito: {str(e)}", "error")
        return redirect(url_for("inventario.detalle_producto", producto_id=id_producto))


@ventas_bp.route("/carrito/actualizar", methods=["POST"])
def actualizar_carrito():
    if "id_cliente" not in session:
        return redirect(url_for("cliente.login"))

    id_cliente = session["id_cliente"]
    conn = get_db()
    cur = get_db_cursor()

    try:
        cur.execute("""
            SELECT id FROM ticket
            WHERE id_cliente = %s AND estado = 'abierto'
            LIMIT 1;
        """, (id_cliente,))
        ticket = cur.fetchone()
    except Exception as e:
        flash(f"Error al obtener el ticket abierto: {e}", "error")
        return redirect(url_for("ventas.mostrar_carrito"))

    if not ticket:
        flash("No tienes un carrito activo.", "error")
        return redirect(url_for("ventas.mostrar_carrito"))

    id_ticket = ticket['id']

    try:
        for key, value in request.form.items():
            if key.startswith("cantidad_"):
                try:
                    id_producto = int(key.split("_")[1])
                    nueva_cantidad = int(value)

                    # Consultar la cantidad disponible del producto
                    try:
                        cur.execute("SELECT cantidad FROM producto WHERE id_producto = %s;", (id_producto,))
                        row = cur.fetchone()
                        if not row:
                            flash(f"Producto con ID {id_producto} no encontrado.", "warning")
                            continue
                        cantidad_disponible = row["cantidad"]
                    except Exception as e:
                        flash(f"Error al consultar stock de producto {id_producto}: {e}", "error")
                        continue

                    # Ajuste si excede cantidad
                    if nueva_cantidad > cantidad_disponible:
                        nueva_cantidad = cantidad_disponible
                        flash(f"Cantidad ajustada para producto {id_producto}: solo hay {cantidad_disponible} disponibles.", "warning")

                    if nueva_cantidad <= 0:
                        flash(f"Cantidad inválida para producto {id_producto}.", "warning")
                        continue

                    try:
                        cur.execute("""
                            UPDATE carrito
                            SET cantidad = %s
                            WHERE id_ticket = %s AND id_producto = %s;
                        """, (nueva_cantidad, id_ticket, id_producto))
                    except Exception as e:
                        flash(f"Error al actualizar carrito para producto {id_producto}: {e}", "error")

                except ValueError:
                    flash(f"Cantidad inválida enviada en el campo {key}.", "warning")
    except Exception as e:
        flash(f"Error general al procesar el formulario: {e}", "error")
        return redirect(url_for("ventas.mostrar_carrito"))

    try:
        conn.commit()
        flash("Carrito actualizado correctamente.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error al guardar cambios: {e}", "error")

    return redirect(url_for("ventas.mostrar_carrito"))


@ventas_bp.route("/realizar_pago", methods=["POST"])
def realizar_pago():
    if "id_cliente" not in session:
        return redirect(url_for("cliente.login"))

    id_cliente = session["id_cliente"]
    conn = get_db()
    cur = conn.cursor()

    # Obtener el ticket abierto del cliente
    cur.execute("""
        SELECT id FROM ticket
        WHERE id_cliente = %s AND estado = 'abierto'
        LIMIT 1;
    """, (id_cliente,))
    ticket = cur.fetchone()

    if not ticket:
        flash("No tienes ningún carrito activo para pagar.", "error")
        return redirect(url_for("ventas.mostrar_carrito"))

    id_ticket = ticket[0]

    try:
        # Marcar el ticket como cerrado
        cur.execute("""
            UPDATE ticket
            SET estado = 'cerrado', fecha = NOW()
            WHERE id = %s;
        """, (id_ticket,))
        conn.commit()
        flash("Pago realizado con éxito. Gracias por tu compra.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error al cerrar el ticket: {e}", "error")

    return render_template("index.html")

