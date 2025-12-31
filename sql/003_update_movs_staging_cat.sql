ALTER TABLE bancapp.movimientos_staging ADD COLUMN categoria text;

COMMENT ON COLUMN bancapp.movimientos_staging.categoria IS 'Categoria del movimiento';

DROP MATERIALIZED VIEW bancapp.movimientos_mview;

CREATE MATERIALIZED VIEW bancapp.movimientos_mview AS
    select distinct fecha_valor, importe, saldo, categoria
    from bancapp.movimientos_staging;

CREATE UNIQUE INDEX idx_movimientos_composite 
ON bancapp.movimientos_mview (fecha_valor, importe, saldo);