import pytest
from db.connection import ConexionBD
import db.ing.movimientos as db
import data_model.ing.movimientos as dm

@pytest.fixture(autouse=True)
def test_filepath(monkeypatch):
    monkeypatch.setattr("extract.extract_ing._get_file_path", lambda: "./tests/data/movements_ing.csv")

@pytest.fixture
def movimientos_staging():

    movs_staging : list[dm.MovimientoStaging] = []

    movs_staging.append(dm.MovimientoStaging(-1, "31/12/2025", 1000, 1000))
    movs_staging.append(dm.MovimientoStaging(-1, "01/01/2026", -500, 500))
    movs_staging.append(dm.MovimientoStaging(-1, "15/02/2026", 200.65, 700.65))
    movs_staging.append(dm.MovimientoStaging(-1, "30/03/2026", -150.55, -0.10))

    return movs_staging

@pytest.fixture
def movimientos_csv():

    movs_csv : list[dm.MovimientosCSV] = []

    movs_csv.append(dm.MovimientosCSV("30/12/2025", 2000, 250.15))
    movs_csv.append(dm.MovimientosCSV("02/01/2026", 0.75, -0.4))
    movs_csv.append(dm.MovimientosCSV("10/02/2026", -120.1, 300))

    return movs_csv


def _borrar_movimientos_staging():
    """
    Función auxiliar para borrar movimientos de la tabla de staging.
    Sirve a los fixtures que trabajan sobre la tabla de staging
    """

    conn = ConexionBD.obtener_conexion()
    conn.execute("TRUNCATE TABLE bancapp.movimientos_staging")
    conn.commit()

@pytest.fixture()
def insertar_movimientos_staging(movimientos_staging):

    _borrar_movimientos_staging()

    db.MovimientosStaging.insertar_movimientos_bulk(movimientos_staging)

@pytest.fixture()
def borrar_movimientos_staging():

    _borrar_movimientos_staging()

