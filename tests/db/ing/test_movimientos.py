from db.ing.MovimientosStaging import MovimientosStaging
import pytest
import datetime as dt
from decimal import Decimal

class TestMovimientosStaging:

    @pytest.mark.usefixtures("insertar_movimientos_staging")
    @pytest.mark.usefixtures("borrar_movimientos_staging")
    def test_insertarMovimientosStaging_y_obtener_todos(self):

        movs_staging = MovimientosStaging.obtener_todos()

        assert len(movs_staging) == 4
        assert movs_staging[0].fecha_valor == dt.date(2025, 12, 31)
        assert movs_staging[3].fecha_valor == dt.date(2026, 3, 30) 
        assert movs_staging[3].importe == "-150.55"
        assert movs_staging[3].saldo == "-0.10"

