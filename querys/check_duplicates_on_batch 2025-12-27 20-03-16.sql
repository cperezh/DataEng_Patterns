select fecha_valor, importe, saldo, created_at, count(*)
from movimientos_staging
group by 1, 2, 3, 4
order by 5 DESC