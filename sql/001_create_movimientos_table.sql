-- Crear tabla de movimientos de cuenta
CREATE TABLE IF NOT EXISTS movimientos (
    id SERIAL PRIMARY KEY,
    fecha_movimiento DATE NOT NULL,
    comentario VARCHAR(1024) NOT NULL,
    importe DECIMAL(15, 2) NOT NULL,
    categoria VARCHAR(255),
    subcategoria VARCHAR(255),
    descripcion TEXT,
    saldo DECIMAL(18, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índice en fecha_movimiento para optimizar búsquedas
CREATE INDEX IF NOT EXISTS idx_movimientos_fecha ON movimientos(fecha_movimiento);

-- Comentarios descriptivos de la tabla y columnas
COMMENT ON TABLE movimientos IS 'Tabla que almacena los movimientos de cuenta';
COMMENT ON COLUMN movimientos.id IS 'Identificador único del movimiento';
COMMENT ON COLUMN movimientos.fecha_movimiento IS 'Fecha en la que se realizó el movimiento';
COMMENT ON COLUMN movimientos.comentario IS 'Comentario/descripcion del movimiento (antes llamado concepto)';
COMMENT ON COLUMN movimientos.importe IS 'Importe del movimiento (puede ser positivo o negativo)';
COMMENT ON COLUMN movimientos.categoria IS 'Categoría asignada al movimiento (p. ej. Alimentación, Hogar)';
COMMENT ON COLUMN movimientos.subcategoria IS 'Subcategoría del movimiento (p. ej. Supermercados)';
COMMENT ON COLUMN movimientos.descripcion IS 'Descripción detallada proveniente del extracto';
COMMENT ON COLUMN movimientos.saldo IS 'Saldo resultante después del movimiento';
COMMENT ON COLUMN movimientos.created_at IS 'Fecha y hora de creación del registro';
COMMENT ON COLUMN movimientos.updated_at IS 'Fecha y hora de última modificación del registro';
