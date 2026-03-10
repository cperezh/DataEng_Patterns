DROP MATERIALIZED VIEW bancapp.movimientos_mview;

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
          CASE
              WHEN importe LIKE '%,__'::text THEN replace(replace(importe, '.'::text, ''::text), ','::text, '.'::text)
              WHEN importe LIKE '%.__'::text THEN replace(importe, ','::text, ''::text)
          END AS importe,
          CASE
              WHEN saldo LIKE '%,__'::text THEN replace(replace(saldo, '.'::text, ''::text), ','::text, '.'::text)
              WHEN saldo LIKE '%.__'::text THEN replace(saldo, ','::text, ''::text)
              ELSE NULL::text
          END AS saldo,
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