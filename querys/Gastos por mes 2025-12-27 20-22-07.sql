with 
  drop_duplicates as(
   select distinct fecha_valor, importe, saldo
   from movimientos_staging
  )


  select 
    DATE_TRUNC('month', fecha_valor) AS mes,
    sum(
      case when importe < 0 then importe else 0 end
    ) as total_gasto
  from  drop_duplicates
  group by mes
  order by mes