from db.ing.movimientos import MovimientosStaging
import data_model.ing.movimientos as dm
from db.connection import ConexionBD
from psycopg import sql
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
        assert sum(mov.importe for mov in movs_staging) == Decimal("550.10")
        assert sum(mov.saldo for mov in movs_staging) == Decimal("2200.55")

