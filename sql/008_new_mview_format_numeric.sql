DROP MATERIALIZED VIEW bancapp.movimientos_mview;

CREATE MATERIALIZED VIEW bancapp.movimientos_mview AS
    select 
        fecha_valor, 
        cast(
           -- Format numeric with group and decimal separators
           case 
             -- when ',' is the decimal separator
             when importe LIKE '%,__' then replace(replace(importe,'.',''),',','.')
             -- when '.' is the decimal separator
             when importe LIKE '%.__' then replace(importe,',','') 
           end as numeric) 
        as importe, 
        cast(
           -- Format numeric with group and decimal separators
           case 
             -- when ',' is the decimal separator
             when saldo LIKE '%,__' then replace(replace(saldo,'.',''),',','.')
             -- when '.' is the decimal separator
             when saldo LIKE '%.__' then replace(saldo,',','') 
           end as numeric) 
        as saldo, 
        categoria, 
        subcategoria, 
        descripcion, 
        created_at
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