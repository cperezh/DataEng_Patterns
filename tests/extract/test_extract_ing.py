import pytest
import datetime as dt
import extract.extract_ing as ext_ing
from data_model.ing.movimientos import MovimientosCSV
from db.connection import ConexionBD
from db.ing.movimientos import MovimientosStaging
from decimal import Decimal





@pytest.mark.usefixtures("borrar_movimientos_staging")
def test_extract_movimientos():

    ext_ing.extract_movimientos()

    movs_staging = MovimientosStaging.obtener_todos()
    
    assert len(movs_staging) == 2
    assert movs_staging[1].fecha_valor == dt.date(2025, 11, 15)
    assert movs_staging[0].fecha_valor == dt.date(2025, 11, 14)
    assert movs_staging[1].importe == 100.00
    assert movs_staging[0].importe == Decimal("-160.70")
    assert movs_staging[1].saldo == Decimal("7.59")
    assert movs_staging[0].saldo == Decimal("-92.41")


def test_read_movimientos():

    movimientos_csv = ext_ing._read_movimientos()

    assert len(movimientos_csv) == 2
    assert movimientos_csv[0].fecha_valor == "15/11/2025"
    assert movimientos_csv[1].fecha_valor == "14/11/2025"
    assert movimientos_csv[0].importe == 100.00
    assert movimientos_csv[1].importe == -160.70
    assert movimientos_csv[0].saldo == 7.59
    assert movimientos_csv[1].saldo == -92.41


def test_transformar_movimientos_csv_staging(movimientos_csv):

    movs_staging = ext_ing._transformar_movimientos_csv_staging(movimientos_csv)
    
    assert len(movs_staging) == 3
    assert movs_staging[0].fecha_valor == dt.date(2025, 12, 30)
    assert movs_staging[2].fecha_valor == dt.date(2026, 2, 10) 
    assert sum(mov.importe for mov in movs_staging) == 1880.65
    assert sum(mov.saldo for mov in movs_staging) == Decimal("549.75")


@pytest.mark.usefixtures("borrar_movimientos_staging")
def test_insertar_movimientos_staging(movimientos_staging):
    
    ext_ing._insertar_movimientos_staging(movimientos_staging)

    movs_staging = MovimientosStaging.obtener_todos()
    
    assert len(movs_staging) == 4
    assert movs_staging[0].fecha_valor == dt.date(2025, 12, 31)
    assert movs_staging[3].fecha_valor == dt.date(2026, 3, 30) 
    assert sum(mov.importe for mov in movs_staging) == Decimal("550.10")
    assert sum(mov.saldo for mov in movs_staging) == Decimal("2200.55")

