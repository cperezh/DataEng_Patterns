import pytest
import datetime as dt
from etl.bronze import extract_ing
from db.ing.MovimientosStaging import MovimientosStaging
from decimal import Decimal


def test_read_movimientos_df_types():

    df_movs = extract_ing._read_movimientos_df("")

    assert df_movs.dtypes.iloc[0] == "object"
    assert df_movs.dtypes.iloc[5] == "object"
    assert df_movs.dtypes.iloc[6] == "object"


@pytest.mark.usefixtures("borrar_movimientos_staging")
def test_extract_movimientos():

    extract_ing.extract_movimientos("")

    movs_staging = MovimientosStaging.obtener_todos()
    
    assert len(movs_staging) == 6
    assert movs_staging[0].fecha_valor == dt.date(2025, 11, 14)
    assert movs_staging[1].fecha_valor == dt.date(2025, 11, 15)
    assert movs_staging[2].fecha_valor == dt.date(2026, 11, 2)
    assert movs_staging[3].fecha_valor == dt.date(2026, 12, 25)        
    assert movs_staging[0].importe == "-160.70"
    assert movs_staging[1].importe == "100.00"
    assert movs_staging[2].importe == "-45.00"
    assert movs_staging[3].importe == "1,416.00"
    assert movs_staging[0].saldo == "-92.41"
    assert movs_staging[1].saldo == "7.59"
    assert movs_staging[2].saldo == "1,288.70"
    assert movs_staging[3].saldo == "1,664.88"

def test_read_movimientos():

    movimientos_csv = extract_ing._read_movimientos("")

    assert len(movimientos_csv) == 6
    assert movimientos_csv[0].fecha_valor == "15/11/2025"
    assert movimientos_csv[1].fecha_valor == "14/11/2025"
    assert movimientos_csv[2].fecha_valor == "02/11/2026"
    assert movimientos_csv[3].fecha_valor == "25/12/2026"
    assert movimientos_csv[0].importe == "100.00"
    assert movimientos_csv[1].importe == "-160.70"
    assert movimientos_csv[2].importe == "-45.00"
    assert movimientos_csv[3].importe == "1,416.00"
    assert movimientos_csv[0].saldo == "7.59"
    assert movimientos_csv[1].saldo == "-92.41"
    assert movimientos_csv[2].saldo == "1,288.70"
    assert movimientos_csv[3].saldo == "1,664.88"


def test_transformar_movimientos_csv_staging(movimientos_csv):

    movs_staging = extract_ing._transformar_movimientos_csv_staging(movimientos_csv)
    
    assert len(movs_staging) == 3
    assert movs_staging[0].fecha_valor == dt.date(2025, 12, 30)
    assert movs_staging[2].fecha_valor == dt.date(2026, 2, 10) 
    assert sum(mov.importe for mov in movs_staging) == 1880.65
    assert sum(mov.saldo for mov in movs_staging) == Decimal("549.75")


@pytest.mark.usefixtures("borrar_movimientos_staging")
def test_insertar_movimientos_staging(movimientos_staging):
    
    extract_ing._insertar_movimientos_staging(movimientos_staging)

    movs_staging = MovimientosStaging.obtener_todos()
    
    assert len(movs_staging) == 4
    assert movs_staging[0].fecha_valor == dt.date(2025, 12, 31)
    assert movs_staging[3].fecha_valor == dt.date(2026, 3, 30) 
    assert movs_staging[3].importe == "-150.55" 
    assert movs_staging[3].saldo == "-0.10"

