from db.ing.movimientos import MovimientosStaging
import data_model.ing.movimientos as dm
from db.connection import ConexionBD
from psycopg import sql
import pytest
import datetime as dt
from decimal import Decimal

@pytest.fixture
def movimientos_staging():

    movs_staging : list[dm.MovimientoStaging] = []

    movs_staging.append(dm.MovimientoStaging(-1, "31/12/2025", 1000, 1000))
    movs_staging.append(dm.MovimientoStaging(-1, "01/01/2026", -500, 500))
    movs_staging.append(dm.MovimientoStaging(-1, "15/02/2026", 200.65, 700.65))
    movs_staging.append(dm.MovimientoStaging(-1, "30/03/2026", -150.55, 550.10))

    return movs_staging

class TestMovimientosStaging:

    @pytest.mark.usefixtures("borrar_movimientos_staging")
    def test_insertarMovimientosStaging_y_obtener_todos(self, movimientos_staging):

        MovimientosStaging.insertar_movimientos_bulk(movimientos_staging)

        movs_staging = MovimientosStaging.obtener_todos()

        assert len(movs_staging) == 4
        assert movs_staging[0].fecha_valor == dt.date(2025, 12, 31)
        assert movs_staging[3].fecha_valor == dt.date(2026, 3, 30) 
        assert sum(mov.importe for mov in movs_staging) == Decimal("550.10")
        assert sum(mov.saldo for mov in movs_staging) == 2750.75

