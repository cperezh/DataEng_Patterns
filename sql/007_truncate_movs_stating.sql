TRUNCATE TABLE bancapp.movimientos_staging;

DROP MATERIALIZED VIEW bancapp.movimientos_mview;

ALTER TABLE  bancapp.movimientos_staging ALTER COLUMN importe TYPE text;
ALTER TABLE  bancapp.movimientos_staging ALTER COLUMN saldo TYPE text;

CREATE MATERIALIZED VIEW bancapp.movimientos_mview AS
    select fecha_valor, importe, saldo, categoria, subcategoria, descripcion, created_at
    from (
        -- Ordenamos los movimientos por fecha de carga
        select 
        row_number() over (partition by fecha_valor, importe, saldo order by created_at desc) as row_id,
        *
        from bancapp.movimientos_staging
    )
    -- Seleccionamos la version mas reciente del movimiento
    where row_id = 1;

CREATE UNIQUE INDEX idx_movimientos_composite 
ON bancapp.movimientos_mview (fecha_valor, importe, saldo);