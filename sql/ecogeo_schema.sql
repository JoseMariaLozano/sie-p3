-- Borramos las tablas si existen, para evitar conflictos en la recreación
DROP TABLE IF EXISTS empleado_almacen CASCADE;
DROP TABLE IF EXISTS empleado_proveedor CASCADE;
DROP TABLE IF EXISTS evaluacion CASCADE;
DROP TABLE IF EXISTS empleado_cargo CASCADE;
DROP TABLE IF EXISTS cargo CASCADE;
DROP TABLE IF EXISTS ausencia CASCADE;
DROP TABLE IF EXISTS horario_trabajo CASCADE;
DROP TABLE IF EXISTS contrato CASCADE;
DROP TABLE IF EXISTS almacen CASCADE;
DROP TABLE IF EXISTS empleado CASCADE;
DROP TABLE IF EXISTS factura_insumo CASCADE;
DROP TABLE IF EXISTS orden_compra CASCADE;
DROP TABLE IF EXISTS factura CASCADE;
DROP TABLE IF EXISTS insumo CASCADE;
DROP TABLE IF EXISTS proveedor CASCADE;
DROP TABLE IF EXISTS producto CASCADE;
DROP TABLE IF EXISTS cliente CASCADE;
DROP TABLE IF EXISTS ticket CASCADE;
DROP TABLE IF EXISTS carrito CASCADE;

CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    alerta INTEGER NOT NULL CHECK (alerta >= 0),
    id_almacen INTEGER NOT NULL,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    descripcion TEXT,
    tipo SMALLINT NOT NULL CHECK (tipo IN (1, 2, 3)),
    tamano TEXT CHECK (tamano IN ('pequeño', 'mediano', 'grande'))
);

-- Tabla Empleado
CREATE TABLE empleado (
    dni VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    tipo VARCHAR(50),
    fecha_nacimiento DATE
);

-- Tabla Almacen
CREATE TABLE almacen (
    id_almacen SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    capacidad_material INTEGER,
    direccion VARCHAR(200),
    capacidad_empleados INTEGER
);

-- Tabla Contrato
CREATE TABLE contrato (
    id_contrato SERIAL PRIMARY KEY,
    dni_empleado VARCHAR(20) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    tipo_contrato VARCHAR(50),
    sueldo NUMERIC(10,2),
    CONSTRAINT fk_contrato_empleado FOREIGN KEY (dni_empleado)
        REFERENCES empleado (dni)
);

-- Tabla HorarioTrabajo
CREATE TABLE horario_trabajo (
    id_horario SERIAL PRIMARY KEY,
    dni_empleado VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    hora_entrada TIME,
    hora_salida TIME,
    CONSTRAINT fk_horario_empleado FOREIGN KEY (dni_empleado)
        REFERENCES empleado (dni)
);

-- Tabla Ausencia
CREATE TABLE ausencia (
    id_ausencia SERIAL PRIMARY KEY,
    dni_empleado VARCHAR(20) NOT NULL,
    tipo VARCHAR(50),
    fecha_inicio DATE NOT NULL,
    duracion_dias INTEGER,
    CONSTRAINT fk_ausencia_empleado FOREIGN KEY (dni_empleado)
        REFERENCES empleado (dni)
);

-- Tabla Cargo
CREATE TABLE cargo (
    id_cargo SERIAL PRIMARY KEY,
    nombre_cargo VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla Empleado_Cargo (relación entre empleado y cargo)
CREATE TABLE empleado_cargo (
    id_ec SERIAL PRIMARY KEY,
    dni_empleado VARCHAR(20) NOT NULL,
    id_cargo INTEGER NOT NULL,
    fecha_asignacion DATE NOT NULL,
    CONSTRAINT fk_empleado_cargo_empleado FOREIGN KEY (dni_empleado)
        REFERENCES empleado (dni),
    CONSTRAINT fk_empleado_cargo_cargo FOREIGN KEY (id_cargo)
        REFERENCES cargo (id_cargo)
);

-- Tabla Evaluación
CREATE TABLE evaluacion (
    id_eval SERIAL PRIMARY KEY,
    dni_empleado VARCHAR(20) NOT NULL,
    fecha_eval DATE NOT NULL,
    calificacion INTEGER,
    observaciones TEXT,
    CONSTRAINT fk_evaluacion_empleado FOREIGN KEY (dni_empleado)
        REFERENCES empleado (dni)
);

-- Tabla Empleado_Proveedor (no se si borrar esta relación)
CREATE TABLE empleado_proveedor (
    id_relacion SERIAL PRIMARY KEY,
    dni_empleado VARCHAR(20) NOT NULL,
    id_proveedor INTEGER,
    CONSTRAINT fk_empleado_proveedor_empleado FOREIGN KEY (dni_empleado)
        REFERENCES empleado (dni)
    
);

-- Tabla Empleado_Almacen (relación entre empleado y almacen)
CREATE TABLE empleado_almacen (
    id_trabaja SERIAL PRIMARY KEY,
    dni_empleado VARCHAR(20) NOT NULL,
    id_almacen INTEGER NOT NULL,
    CONSTRAINT fk_empleado_almacen_empleado FOREIGN KEY (dni_empleado)
        REFERENCES empleado (dni),
    CONSTRAINT fk_empleado_almacen_almacen FOREIGN KEY (id_almacen)
        REFERENCES almacen (id_almacen)
);

CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(20),
    es_empresa BOOLEAN NOT NULL DEFAULT FALSE,
    nombre_empresa VARCHAR(100) NOT NULL DEFAULT 'default',
    tarjeta_numero VARCHAR(20) NOT NULL,
    tarjeta_mes_expiracion INT NOT NULL,
    tarjeta_anio_expiracion INT NOT NULL,
    tarjeta_cvv VARCHAR(4) NOT NULL
);


-- Tabla Proveedor
CREATE TABLE Proveedor (
    ID_Proveedor SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Direccion VARCHAR(200) NOT NULL,
    Telefono VARCHAR(20) NOT NULL,
    Correo_electronico VARCHAR(100) NOT NULL,
    Estado VARCHAR(50) NOT NULL
);

-- Tabla Insumo
CREATE TABLE Insumo (
    GTIN_Insumo VARCHAR(20) PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Medidas VARCHAR(50),
    Stock_actual INTEGER NOT NULL,
    Precio_estimado NUMERIC(10, 2) NOT NULL
);

-- Tabla Factura
CREATE TABLE Factura (
    ID_Factura SERIAL PRIMARY KEY,
    ID_Proveedor INTEGER NOT NULL,
    Fecha_Emision DATE DEFAULT CURRENT_DATE,
    Coste NUMERIC(10, 2) NOT NULL,
    Insumo_Solicitado TEXT,
    Fecha_Pago DATE,
    Estado VARCHAR(50) NOT NULL,
    FOREIGN KEY (ID_Proveedor) REFERENCES Proveedor(ID_Proveedor)
);

-- Tabla Orden de Compra
CREATE TABLE Orden_Compra (
    ID_Compra SERIAL PRIMARY KEY,
    ID_Proveedor INTEGER NOT NULL,
    ID_Factura INTEGER,
    Fecha_Emision DATE DEFAULT CURRENT_DATE,
    Estado VARCHAR(50) NOT NULL,
    Fecha_Entrega DATE,
    Informacion_Material TEXT,
    Observaciones TEXT,
    FOREIGN KEY (ID_Proveedor) REFERENCES Proveedor(ID_Proveedor),
    FOREIGN KEY (ID_Factura) REFERENCES Factura(ID_Factura)
);

-- Tabla intermedia: Factura_Insumo
CREATE TABLE Factura_Insumo (
    ID_Factura INTEGER NOT NULL,
    GTIN_Insumo VARCHAR(20) NOT NULL,
    Cantidad INTEGER DEFAULT 1,
    Precio_Unitario NUMERIC(10, 2),
    PRIMARY KEY (ID_Factura, GTIN_Insumo),
    FOREIGN KEY (ID_Factura) REFERENCES Factura(ID_Factura) ON DELETE CASCADE,
    FOREIGN KEY (GTIN_Insumo) REFERENCES Insumo(GTIN_Insumo) ON DELETE CASCADE
);

CREATE TABLE ticket (
    id SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL REFERENCES cliente(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'abierto' -- abierto, pagado, cancelado, etc.
);

CREATE TABLE carrito (
    id SERIAL PRIMARY KEY,
    id_ticket INT NOT NULL REFERENCES ticket(id) ON DELETE CASCADE,
    id_producto INT NOT NULL REFERENCES producto(id_producto) ON DELETE CASCADE,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0)
);
