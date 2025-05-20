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
