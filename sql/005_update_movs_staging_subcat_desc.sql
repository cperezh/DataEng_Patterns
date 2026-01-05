ALTER TABLE bancapp.movimientos_staging ADD COLUMN subcategoria text;
ALTER TABLE bancapp.movimientos_staging ADD COLUMN descripcion text;

COMMENT ON COLUMN bancapp.movimientos_staging.subcategoria IS 'Subcategoría del movimiento';
COMMENT ON COLUMN bancapp.movimientos_staging.descripcion IS 'Descripción';
