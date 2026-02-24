from etl.bronze import extract_ing
from etl.silver import silver_ing

def run():
    extract_ing.extract_movimientos()
    silver_ing.refresh_movimientos()