import pytest
import datetime as dt
import extract.extract_ing as ext_ing
from data_model.ing.movimientos import MovimientosCSV
from db.connection import ConexionBD
from db.ing.movimientos import MovimientosStaging
from decimal import Decimal


@pytest.fixture(autouse=True)
def test_filepath(monkeypatch):
    monkeypatch.setattr("extract.extract_ing._get_file_path", lambda: "./tests/data/movements_ing.csv")


def test_read_movimientos():

    movimientos_csv = ext_ing.read_movimientos()

    assert len(movimientos_csv) == 2
    assert movimientos_csv[0].fecha_valor == "15/11/2025"
    assert movimientos_csv[1].fecha_valor == "14/11/2025"
    assert movimientos_csv[0].importe == 100.00
    assert movimientos_csv[1].importe == -160.70
    assert movimientos_csv[0].saldo == 7.59
    assert movimientos_csv[1].saldo == -92.41


def test_transformar_movimientos_csv_staging(movimientos_csv):

    movimientos_staging = ext_ing.transformar_movimientos_csv_staging(movimientos_csv)
    
    assert len(movimientos_csv) == 2
    assert movimientos_staging[0].fecha_valor == dt.date(2025,11,15)
    assert movimientos_staging[1].fecha_valor == dt.date(2025,11,14)
    assert movimientos_staging[0].importe == 100.00
    assert movimientos_staging[1].importe == -160.70
    assert movimientos_staging[0].saldo == 7.59
    assert movimientos_staging[1].saldo == -92.41


@pytest.mark.usefixtures("borrar_movimientos_staging")
def test_insertar_movimientos_staging(movimientos_staging):
    
    ext_ing.insertar_movimientos_staging(movimientos_staging)

    movs_staging = MovimientosStaging.obtener_todos()
    
    assert len(movs_staging) == 4
    assert movs_staging[0].fecha_valor == dt.date(2025, 11, 14)
    assert movs_staging[1].fecha_valor == dt.date(2025, 11, 15) 
    assert sum(mov.importe for mov in movs_staging) == Decimal("-60.70")
    assert sum(mov.saldo for mov in movs_staging) == Decimal("-84.82")

