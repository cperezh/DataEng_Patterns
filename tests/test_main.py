import pytest
import db.ing.movimientos as db_ing
import datetime as dt
from decimal import Decimal
import db.connection as db
import main


@pytest.mark.usefixtures("borrar_movimientos_staging")
def test_main():
    
    main.main()

    assert db.ConexionBD._conexion == None

    movs_staging = db_ing.MovimientosStaging.obtener_todos()
    
    assert len(movs_staging) == 4
    assert movs_staging[0].fecha_valor == dt.date(2025, 11, 14)
    assert movs_staging[3].fecha_valor == dt.date(2026, 12, 25)
    assert sum(mov.importe for mov in movs_staging) == Decimal("1310.30")
    assert sum(mov.saldo for mov in movs_staging) == Decimal("2868.76")

    