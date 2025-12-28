-- Crea el esquema y la tabla de staging para movimientos ING
-- Nota: requiere permisos para crear esquema.

-- 1) Esquema
CREATE SCHEMA IF NOT EXISTS bancapp;

-- 2) Tabla staging
CREATE TABLE IF NOT EXISTS bancapp.movimientos_staging (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_valor DATE NOT NULL,
    importe NUMERIC(15, 2) NOT NULL,
    saldo   NUMERIC(18, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE bancapp.movimientos_staging IS 'Tabla staging para cargar movimientos (ING) desde CSV antes de transformarlos al modelo final';
COMMENT ON COLUMN bancapp.movimientos_staging.id IS 'Identificador autoincremental (IDENTITY)';
COMMENT ON COLUMN bancapp.movimientos_staging.fecha_valor IS 'Fecha valor del movimiento (dd/mm/yyyy en origen)';
COMMENT ON COLUMN bancapp.movimientos_staging.importe IS 'Importe del movimiento';
COMMENT ON COLUMN bancapp.movimientos_staging.saldo IS 'Saldo resultante tras el movimiento';
COMMENT ON COLUMN bancapp.movimientos_staging.created_at IS 'Timestamp de inserción en staging';
