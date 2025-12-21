from data_model.ing import movimientos
import pandas as pd

data_path = "data/"

def extract_movimientos():
   
   movimientos_csv = read_movimientos()
   movimientos_staging = transformar_movimientos_csv_staging(movimientos_csv)
   insertar_movimientos_staging(movimientos_staging)  


def _get_file_path() -> str:

    return data_path + "/movements-15112025.csv"


def read_movimientos() -> list[movimientos.MovimientosCSV]:

    movimientos_csv : list[movimientos.MovimientosCSV] = []
    
    data_file = _get_file_path()
    
    df_movimientos_csv = pd.read_csv(data_file, skiprows=3, sep=",", header=0)

    print(df_movimientos_csv.shape)

    for _, movimiento_csv in df_movimientos_csv.iterrows():

        movimiento_csv = movimientos.MovimientosCSV(
            movimiento_csv.iloc[0],
            movimiento_csv.iloc[6],
            movimiento_csv.iloc[7])

        movimientos_csv.append(movimiento_csv)
    
    return movimientos_csv


def transformar_movimientos_csv_staging(
        movimientos_csv: list[movimientos.MovimientosCSV]
        ) -> list[movimientos.MovimientoStaging]:
    
    movimientos_staging  = []

    for mov_csv in movimientos_csv:
        mov_staging = movimientos.MovimientoStaging(
            -1,
            mov_csv.fecha_valor,
            mov_csv.importe,
            mov_csv.saldo)
    
        movimientos_staging.append(mov_staging)
    
    return movimientos_staging


def insertar_movimientos_staging(movimientos_staging: list[movimientos.MovimientoStaging]):
    pass