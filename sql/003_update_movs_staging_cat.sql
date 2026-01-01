ALTER TABLE bancapp.movimientos_staging ADD COLUMN categoria text;

COMMENT ON COLUMN bancapp.movimientos_staging.categoria IS 'Categoria del movimiento';

