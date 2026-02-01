from data_model.ing import movimientos
import pandas as pd
import db.ing.movimientos as db_ing_movs
import datetime as dt

data_path = "data/"

def extract_movimientos():
   
   movimientos_csv = _read_movimientos()
   movimientos_staging = _transformar_movimientos_csv_staging(movimientos_csv)
   _insertar_movimientos_staging(movimientos_staging)  


def _get_file_path() -> str:

    return data_path + "/movements-2026.csv"


def _read_movimientos_df() -> pd.DataFrame:

    data_file = _get_file_path()
    
    df_movimientos_csv = pd.read_csv(data_file, skiprows=3, sep=",", header=0)

    # eliminamos los separadores de miles en el importe y el saldo y convertimos a numerico
    df_movimientos_csv["SALDO (€)"] = df_movimientos_csv["SALDO (€)"].apply(lambda x: x.replace(",",""))
    df_movimientos_csv["SALDO (€)"] = pd.to_numeric(df_movimientos_csv["SALDO (€)"])
    df_movimientos_csv["IMPORTE (€)"] = df_movimientos_csv["IMPORTE (€)"].apply(lambda x: x.replace(",",""))
    df_movimientos_csv["IMPORTE (€)"] = pd.to_numeric(df_movimientos_csv["IMPORTE (€)"])
    
    return df_movimientos_csv


def _read_movimientos() -> list[movimientos.MovimientosCSV]:

    movimientos_csv : list[movimientos.MovimientosCSV] = []

    df_movimientos_csv = _read_movimientos_df()
    
    for _, movimiento_csv in df_movimientos_csv.iterrows():

        movimiento_csv = movimientos.MovimientosCSV(
            movimiento_csv.loc["F. VALOR"],
            movimiento_csv.loc["IMPORTE (€)"],
            movimiento_csv.loc["SALDO (€)"],
            movimiento_csv.loc["CATEGORÍA"],
            movimiento_csv.loc["SUBCATEGORÍA"],
            movimiento_csv.loc["DESCRIPCIÓN"])

        movimientos_csv.append(movimiento_csv)
    
    return movimientos_csv


def _transformar_movimientos_csv_staging(
        movimientos_csv: list[movimientos.MovimientosCSV]
        ) -> list[movimientos.MovimientoStaging]:
    
    movimientos_staging  = []

    for mov_csv in movimientos_csv:
        mov_staging = movimientos.MovimientoStaging(
            -1,
            mov_csv.fecha_valor,
            mov_csv.importe,
            mov_csv.saldo,
            mov_csv.categoria,
            mov_csv.subcategoria,
            mov_csv.descripcion)
    
        movimientos_staging.append(mov_staging)
    
    return movimientos_staging


def _insertar_movimientos_staging(movimientos_staging: list[movimientos.MovimientoStaging]):
    
    db_ing_movs.MovimientosStaging.insertar_movimientos_bulk(movimientos_staging, 
                                                             dt.datetime.now())
