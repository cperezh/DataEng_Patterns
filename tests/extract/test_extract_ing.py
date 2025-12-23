import pytest
import datetime as dt
from extract.extract_ing import \
    read_movimientos, \
    transformar_movimientos_csv_staging, \
    insertar_movimientos_staging
from data_model.ing.movimientos import MovimientosCSV
from db.connection import ConexionBD
from db.ing.movimientos import MovimientosStaging


@pytest.fixture(autouse=True)
def test_filepath(monkeypatch):
    monkeypatch.setattr("extract.extract_ing._get_file_path", lambda: "./tests/data/movements_ing.csv")

def test_read_movimientos():

    movimientos_csv = read_movimientos()

    assert len(movimientos_csv) == 2
    assert movimientos_csv[0].fecha_valor == "15/11/2025"
    assert movimientos_csv[1].fecha_valor == "14/11/2025"
    assert movimientos_csv[0].importe == 100.00
    assert movimientos_csv[1].importe == -160.70
    assert movimientos_csv[0].saldo == 7.59
    assert movimientos_csv[1].saldo == -92.41


def test_transformar_movimientos_csv_staging(monkeypatch):

    movimientos_csv = read_movimientos()

    movimientos_staging = transformar_movimientos_csv_staging(movimientos_csv)
    
    assert len(movimientos_csv) == 2
    assert movimientos_staging[0].fecha_valor == dt.date(2025,11,15)
    assert movimientos_staging[1].fecha_valor == dt.date(2025,11,14)
    assert movimientos_staging[0].importe == 100.00
    assert movimientos_staging[1].importe == -160.70
    assert movimientos_staging[0].saldo == 7.59
    assert movimientos_staging[1].saldo == -92.41


def test_insertar_movimientos_staging():
    
    movimientos_csv = read_movimientos()

    movimientos_staging = transformar_movimientos_csv_staging(movimientos_csv)

    insertar_movimientos_staging(movimientos_staging)

    movs = MovimientosStaging.obtener_todos()
    
    assert False