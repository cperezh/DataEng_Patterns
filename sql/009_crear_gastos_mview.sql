DROP  MATERIALIZED VIEW IF EXISTS bancapp.gastos_mview;

CREATE MATERIALIZED VIEW bancapp.gastos_mview AS
    select 
	    mm.*,
	    abs(mm.importe) as abs_importe
    from bancapp.movimientos_mview mm
    where mm.importe < 0;

CREATE UNIQUE INDEX idx_gastos
ON bancapp.gastos_mview (fecha_valor, importe, saldo);