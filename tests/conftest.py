import pytest
import db
import db.ing as db_ing
import data_model.ing as dm_ing
import datetime as dt

@pytest.fixture(autouse=True)
def test_filepath(monkeypatch):
    monkeypatch.setattr("etl.bronze.extract_ing._get_file_path", lambda filepath: "./tests/data/movements_ing.csv")

@pytest.fixture
def movimientos_staging():

    fecha_lote = dt.date(2025,3,25)

    movs_staging : list[dm_ing.MovimientoStaging] = []

    movs_staging.append(dm_ing.MovimientoStaging(-1, dt.datetime.strptime("31/12/2025","%d/%m/%Y").date(), 1000, 1000, "Educación y salud", "Deporte y gimnasio", "Pago en DECATHLON ALCOBENDAS ALCOBENDAS ES", fecha_lote))
    movs_staging.append(dm_ing.MovimientoStaging(-1, dt.datetime.strptime("01/01/2026","%d/%m/%Y").date(), -500, 500, "Ocio y viajes", "Libros, música y videojuegos", "Pago en Nintendo EM9861ff0c2d5", fecha_lote))
    movs_staging.append(dm_ing.MovimientoStaging(-1, dt.datetime.strptime("15/02/2026","%d/%m/%Y").date(), 200.65, 700.65, "Alimentación", "Supermercados y alimentación","Pago en DIA 9098 CANDELEDA ES", fecha_lote))
    movs_staging.append(dm_ing.MovimientoStaging(-1, dt.datetime.strptime("30/03/2026","%d/%m/%Y").date(), -150.55, -0.10, "Vehículo y transporte", "Gasolina y combustible" , "Pago en E.S. CEDIPSA MONTILLA S ENRIQUE GUAES", fecha_lote))
    

    return movs_staging

@pytest.fixture
def movimientos_staging_duplicates():
    '''
        duplicados creados con fecha posterior
    '''

    fecha_lote = dt.date(2025,3,30)

    movs_staging : list[dm_ing.MovimientoStaging] = []
    
    movs_staging.append(dm_ing.MovimientoStaging(-1, dt.datetime.strptime("31/12/2025","%d/%m/%Y").date(), 1000, 1000, "Educación y salud", "Deporte y gimnasio", "POSTERIOR - Pago en DECATHLON ALCOBENDAS ALCOBENDAS ES",fecha_lote))
    movs_staging.append(dm_ing.MovimientoStaging(-1, dt.datetime.strptime("01/01/2026","%d/%m/%Y").date(), -500, 500, "Ocio y viajes", "Libros, música y videojuegos", "POSTERIOR - Pago en Nintendo EM9861ff0c2d5", fecha_lote))

    return movs_staging

@pytest.fixture
def movimientos_csv():

    movs_csv : list[dm_ing.MovimientosCSV] = []

    movs_csv.append(dm_ing.MovimientosCSV("30/12/2025", 2000, 250.15, "Movimientos excluidos", "Traspaso entre cuentas" ,"Traspaso recibido Cuenta Nómina Descubierto"))
    movs_csv.append(dm_ing.MovimientosCSV("02/01/2026", 0.75, -0.4, "Alimentación", "Supermercados y alimentación", "Pago en MERCADONA SAN ROQUE ES"))
    movs_csv.append(dm_ing.MovimientosCSV("10/02/2026", -120.1, 300, "Vehículo y transporte", "Gasolina y combustible" , "Pago en SANCHINARRO MADRID ES"))

    return movs_csv


def _borrar_movimientos_staging():
    """
    Función auxiliar para borrar movimientos de la tabla de staging.
    Sirve a los fixtures que trabajan sobre la tabla de staging
    """

    conn = db.ConexionBD.obtener_conexion()
    conn.execute("TRUNCATE TABLE bancapp.movimientos_staging")
    conn.commit()

@pytest.fixture()
def insertar_movimientos_staging(movimientos_staging):

    _borrar_movimientos_staging()

    db_ing.MovimientosStaging.insertar_movimientos_bulk(movimientos_staging, dt.datetime.now())

@pytest.fixture()
def insertar_movimientos_staging_duplicates(movimientos_staging, movimientos_staging_duplicates):

    _borrar_movimientos_staging()

    db_ing.MovimientosStaging.insertar_movimientos_bulk(movimientos_staging, dt.date(2025,3,25))
    db_ing.MovimientosStaging.insertar_movimientos_bulk(movimientos_staging_duplicates, dt.date(2025,3,30))

@pytest.fixture()
def borrar_movimientos_staging():

    _borrar_movimientos_staging()

