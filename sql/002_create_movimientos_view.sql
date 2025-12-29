CREATE MATERIALIZED VIEW bancapp.movimientos_mview AS
    select distinct fecha_valor, importe, saldo
    from movimientos_staging

CREATE UNIQUE INDEX idx_movimientos_composite 
ON bancapp.movimientos_mview (fecha_valor, importe, saldo);

--REFRESH MATERIALIZED VIEW CONCURRENTLY bancapp.movimientos_mview;
