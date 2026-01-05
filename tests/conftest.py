import pytest
from db.connection import ConexionBD
import db.ing.movimientos as db
import data_model.ing.movimientos as dm
import datetime as dt

@pytest.fixture(autouse=True)
def test_filepath(monkeypatch):
    monkeypatch.setattr("extract.extract_ing._get_file_path", lambda: "./tests/data/movements_ing.csv")

@pytest.fixture
def movimientos_staging():

    movs_staging : list[dm.MovimientoStaging] = []

    movs_staging.append(dm.MovimientoStaging(-1, "31/12/2025", 1000, 1000, "Educación y salud", "Deporte y gimnasio", "Pago en DECATHLON ALCOBENDAS ALCOBENDAS ES"))
    movs_staging.append(dm.MovimientoStaging(-1, "01/01/2026", -500, 500, "Ocio y viajes", "Libros, música y videojuegos", "Pago en Nintendo EM9861ff0c2d5"))
    movs_staging.append(dm.MovimientoStaging(-1, "15/02/2026", 200.65, 700.65, "Alimentación", "Supermercados y alimentación","Pago en DIA 9098 CANDELEDA ES"))
    movs_staging.append(dm.MovimientoStaging(-1, "30/03/2026", -150.55, -0.10, "Vehículo y transporte", "Gasolina y combustible" , "Pago en E.S. CEDIPSA MONTILLA S ENRIQUE GUAES"))
    

    return movs_staging

@pytest.fixture
def movimientos_csv():

    movs_csv : list[dm.MovimientosCSV] = []

    movs_csv.append(dm.MovimientosCSV("30/12/2025", 2000, 250.15, "Movimientos excluidos", "Traspaso entre cuentas" ,"Traspaso recibido Cuenta Nómina Descubierto"))
    movs_csv.append(dm.MovimientosCSV("02/01/2026", 0.75, -0.4, "Alimentación", "Supermercados y alimentación", "Pago en MERCADONA SAN ROQUE ES"))
    movs_csv.append(dm.MovimientosCSV("10/02/2026", -120.1, 300, "Vehículo y transporte", "Gasolina y combustible" , "Pago en SANCHINARRO MADRID ES"))

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

    db.MovimientosStaging.insertar_movimientos_bulk(movimientos_staging, dt.datetime.now())

@pytest.fixture()
def borrar_movimientos_staging():

    _borrar_movimientos_staging()

