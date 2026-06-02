DROP MATERIALIZED VIEW IF EXISTS bancapp.movimientos_mview;

CREATE MATERIALIZED VIEW bancapp.movimientos_mview AS
    SELECT 
      id,
      fecha_valor,
      importe,
      saldo,
      categoria,
      subcategoria,
      descripcion,
      created_at
    FROM
      (SELECT 
        row_number() OVER (
          PARTITION BY temp.fecha_valor, temp.importe, temp.saldo 
          ORDER BY temp.created_at DESC) 
        AS row_id,
        *
      FROM 
        -- CLEAN DATA
        (SELECT      
          id,
          fecha_valor,
          CAST(
            CASE
                WHEN importe LIKE '%,__' THEN replace(replace(importe, '.', ''), ',', '.')
                WHEN importe LIKE '%.__' THEN replace(importe, ',', '')
                ELSE importe
            END AS NUMERIC) AS importe,
          CAST(
            CASE
                WHEN saldo LIKE '%,__' THEN replace(replace(saldo, '.', ''), ',', '.')
                WHEN saldo LIKE '%.__' THEN replace(saldo, ',', '')
                ELSE saldo
            END AS NUMERIC) AS saldo,
          created_at,
          categoria,
          subcategoria,
          descripcion
          FROM bancapp.movimientos_staging 
        ) as temp
      ) as final
    WHERE row_id = 1;

CREATE UNIQUE INDEX idx_movimientos_composite 
ON bancapp.movimientos_mview (fecha_valor, importe, saldo);