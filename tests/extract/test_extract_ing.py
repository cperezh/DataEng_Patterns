import pytest
from src.extract.extract_ing import read_movimientos
from src.data_model.ing.movimientos import MovimientosCSV

def test_read_movimientos(monkeypatch):

    monkeypatch.setattr("src.extract.extract_ing._get_file_path", lambda: "./tests/data/movements_ing.csv")

    movimientos_csv = read_movimientos()

    assert False