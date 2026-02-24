from etl.bronze import extract_ing
from etl.silver import silver_ing

def run(file_name: str):
    extract_ing.extract_movimientos(file_name)
    silver_ing.refresh_movimientos()