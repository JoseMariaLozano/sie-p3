-- Inserción de empleados
INSERT INTO empleado (dni, nombre, apellidos, telefono, correo, tipo, fecha_nacimiento) VALUES
('12345678A', 'Juan', 'Pérez Gómez', '600111222', 'juan@example.com', 'Administrador', '1985-06-15'),
('23456789B', 'Laura', 'Martínez Ruiz', '600333444', 'laura@example.com', 'Logística', '1990-08-10'),
('34567890C', 'Carlos', 'López Díaz', '600555666', 'carlos@example.com', 'Contable', '1988-04-20'),
('45678901D', 'Ana', 'García Mora', '600777888', 'ana@example.com', 'RRHH', '1992-01-30');

-- Inserción de almacenes
INSERT INTO almacen (nombre, capacidad_material, direccion, capacidad_empleados) VALUES
('Almacén Central', 5000, 'Calle Falsa 123, Madrid', 20),
('Almacén Norte', 3000, 'Avenida Norte 45, Bilbao', 15),
('Almacén Sur', 2000, 'Calle Sur 78, Sevilla', 10),
('Almacén Este', 4000, 'Camino Este 12, Valencia', 18);

-- Relación empleados-almacenes
INSERT INTO empleado_almacen (dni_empleado, id_almacen) VALUES
('12345678A', 1),
('23456789B', 2),
('34567890C', 3),
('45678901D', 4);

-- Contratos
INSERT INTO contrato (dni_empleado, fecha_inicio, fecha_fin, tipo_contrato, sueldo) VALUES
('12345678A', '2023-01-01', NULL, 'Indefinido', 30000),
('23456789B', '2023-03-15', '2024-03-15', 'Temporal', 25000),
('34567890C', '2022-06-01', NULL, 'Indefinido', 27000),
('45678901D', '2024-01-10', '2025-01-10', 'Temporal', 26000);

-- Horarios
INSERT INTO horario_trabajo (dni_empleado, fecha, hora_entrada, hora_salida) VALUES
('12345678A', '2025-05-20', '08:00:00', '16:00:00'),
('23456789B', '2025-05-20', '09:00:00', '17:00:00'),
('34567890C', '2025-05-20', '07:30:00', '15:30:00'),
('45678901D', '2025-05-20', '10:00:00', '18:00:00');

-- Ausencias
INSERT INTO ausencia (dni_empleado, tipo, fecha_inicio, duracion_dias) VALUES
('12345678A', 'Vacaciones', '2025-07-01', 10),
('23456789B', 'Baja médica', '2025-03-01', 5),
('34567890C', 'Vacaciones', '2025-08-15', 7),
('45678901D', 'Asunto personal', '2025-04-20', 2);

-- Cargos
INSERT INTO cargo (nombre_cargo, descripcion) VALUES
('Supervisor', 'Supervisa el equipo de trabajo'),
('Operario', 'Encargado de manejar insumos'),
('Contador', 'Encargado de finanzas y facturas'),
('Recursos Humanos', 'Gestión del personal');

-- Relación empleados-cargos
INSERT INTO empleado_cargo (dni_empleado, id_cargo, fecha_asignacion) VALUES
('12345678A', 1, '2023-01-01'),
('23456789B', 2, '2023-03-15'),
('34567890C', 3, '2022-06-01'),
('45678901D', 4, '2024-01-10');

-- Evaluaciones
INSERT INTO evaluacion (dni_empleado, fecha_eval, calificacion, observaciones) VALUES
('12345678A', '2025-04-01', 9, 'Excelente rendimiento'),
('23456789B', '2025-04-10', 7, 'Buen desempeño con áreas de mejora'),
('34567890C', '2025-04-15', 8, 'Buen manejo de finanzas'),
('45678901D', '2025-04-20', 6, 'Debe mejorar puntualidad');

-- Proveedores
INSERT INTO proveedor (Nombre, Direccion, Telefono, Correo_electronico, Estado) VALUES
('Insumos S.A.', 'Calle Proveedor 1, Madrid', '911223344', 'contacto@insumos.com', 'Activo'),
('Distribuciones SL', 'Avenida Mayor 22, Sevilla', '954112233', 'info@distribuciones.com', 'Activo'),
('Suministros del Sur', 'Calle Sur 99, Málaga', '952445566', 'ventas@sursuministros.com', 'Inactivo'),
('Logística Global', 'Calle Global 5, Barcelona', '933889900', 'logistica@global.com', 'Activo');

-- Relación empleado-proveedor
INSERT INTO empleado_proveedor (dni_empleado, id_proveedor) VALUES
('12345678A', 1),
('23456789B', 2),
('34567890C', 3),
('45678901D', 4);

-- Insumos
INSERT INTO insumo (GTIN_Insumo, Nombre, Medidas, Stock_actual, Precio_estimado) VALUES
('0001234567890', 'Tornillos 5mm', 'Caja 100 uds', 500, 10.00),
('0001234567891', 'Tuercas 5mm', 'Caja 100 uds', 300, 8.50),
('0001234567892', 'Taladro Bosch', 'Unidad', 50, 120.99),
('0001234567893', 'Cinta Aislante', 'Rollo 10m', 200, 2.75);

-- Facturas
INSERT INTO factura (ID_Proveedor, Fecha_Emision, Coste, Insumo_Solicitado, Fecha_Pago, Estado) VALUES
(1, '2025-04-01', 100.00, 'Tornillos 5mm', '2025-04-05', 'Pagada'),
(2, '2025-04-02', 250.50, 'Taladro Bosch', NULL, 'Pendiente'),
(3, '2025-04-03', 75.25, 'Cinta Aislante', '2025-04-06', 'Pagada'),
(4, '2025-04-04', 120.00, 'Tuercas 5mm', NULL, 'Pendiente');

-- Factura-Insumo
INSERT INTO factura_insumo (ID_Factura, GTIN_Insumo, Cantidad, Precio_Unitario) VALUES
(1, '0001234567890', 10, 10.00),
(2, '0001234567892', 2, 125.25),
(3, '0001234567893', 20, 3.00),
(4, '0001234567891', 15, 8.00);

-- Órdenes de compra
INSERT INTO orden_compra (ID_Proveedor, ID_Factura, Fecha_Emision, Estado, Fecha_Entrega, Informacion_Material, Observaciones) VALUES
(1, 1, '2025-04-01', 'Entregado', '2025-04-05', 'Tornillos 5mm', 'Entrega a tiempo'),
(2, 2, '2025-04-02', 'Pendiente', NULL, 'Taladro Bosch', 'Pendiente confirmación'),
(3, 3, '2025-04-03', 'Entregado', '2025-04-06', 'Cinta Aislante', 'Sin incidencias'),
(4, 4, '2025-04-04', 'En camino', NULL, 'Tuercas 5mm', 'Revisión logística');

INSERT INTO cliente (
  nombre, email, password, direccion, telefono, es_empresa, nombre_empresa,
  tarjeta_numero, tarjeta_mes_expiracion, tarjeta_anio_expiracion, tarjeta_cvv
) VALUES
('María López', 'maria@example.com', 'hashpass1', 'Calle Sol 123, Madrid', '612345678', FALSE, 'default', '4111111111111111', 12, 2026, '123'),
('Luis Torres', 'luis@example.com', 'hashpass2', 'Avenida Luna 45, Valencia', '699998877', TRUE, 'Logística Torres SL', '4000123412341234', 8, 2025, '456'),
('Sofía Hernández', 'sofia@example.com', 'hashpass3', 'Calle Mayor 10, Sevilla', '633223344', FALSE, 'default', '5555555555554444', 3, 2027, '789'),
('Pablo Sánchez', 'pablo@example.com', 'hashpass4', 'Camino Verde 88, Zaragoza', '655112233', TRUE, 'PabloS Group', '378282246310005', 11, 2024, '321');


-- Insertar productos tipo 1 (mudanza)
INSERT INTO producto (cantidad, alerta, id_almacen, precio, descripcion, tipo, tamano)
VALUES 
(50, 10, 1, 25.00, 'Caja grande para mudanza con asas laterales', 1, 'grande'),
(40, 8, 1, 20.00, 'Caja mediana resistente para mudanza', 1, 'mediano'),
(30, 5, 2, 30.00, 'Caja reforzada para objetos pesados', 1, 'grande'),
(60, 12, 2, 18.00, 'Caja económica para mudanza', 1, 'pequeño');

-- Insertar productos tipo 2 (con tapa)
INSERT INTO producto (cantidad, alerta, id_almacen, precio, descripcion, tipo, tamano)
VALUES 
(70, 15, 1, 22.00, 'Caja con tapa rígida reutilizable', 2, 'mediano'),
(45, 10, 2, 24.00, 'Caja plástica con tapa hermética', 2, 'mediano'),
(55, 12, 1, 20.00, 'Caja con tapa y cierres de seguridad', 2, 'pequeño'),
(35, 8, 2, 26.00, 'Caja opaca con tapa para archivo', 2, 'grande');

-- Insertar productos tipo 3 (almacenaje)
INSERT INTO producto (cantidad, alerta, id_almacen, precio, descripcion, tipo, tamano)
VALUES 
(80, 20, 1, 15.00, 'Caja de cartón apilable para almacenaje', 3, 'mediano'),
(90, 25, 2, 17.50, 'Caja organizadora con separadores', 3, 'mediano'),
(65, 18, 1, 16.00, 'Caja multiuso para trastero', 3, 'pequeño'),
(75, 22, 2, 14.50, 'Caja plástica ligera para almacenaje', 3, 'pequeño');

