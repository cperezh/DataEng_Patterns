from db.ing.movimientos import MovimientosStaging
import data_model.ing.movimientos as dm
import pytest


class TestMovimientosStaging:
    
    def test_obtener_todos(self, monkeypatch):
        
        movs_staging = MovimientosStaging.obtener_todos()
        
        assert False