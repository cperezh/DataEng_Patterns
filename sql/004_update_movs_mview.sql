DROP MATERIALIZED VIEW bancapp.movimientos_mview;

CREATE MATERIALIZED VIEW bancapp.movimientos_mview AS
    select fecha_valor, importe, saldo, categoria, created_at
    from (
        -- Ordenamos los movimientos por fecha de carga
        select 
        row_number() over (partition by fecha_valor, importe, saldo order by created_at desc) as row_id,
        *
        from bancapp.movimientos_staging
    )
    -- Seleccionamos la version mas reciente del movimiento
    where row_id = 1

CREATE UNIQUE INDEX idx_movimientos_composite 
ON bancapp.movimientos_mview (fecha_valor, importe, saldo);