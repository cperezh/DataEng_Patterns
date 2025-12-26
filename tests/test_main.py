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
    
    assert len(movs_staging) == 2
    assert movs_staging[1].fecha_valor == dt.date(2025, 11, 15)
    assert movs_staging[0].fecha_valor == dt.date(2025, 11, 14)
    assert movs_staging[1].importe == 100.00
    assert movs_staging[0].importe == Decimal("-160.70")
    assert movs_staging[1].saldo == Decimal("7.59")
    assert movs_staging[0].saldo == Decimal("-92.41")

    