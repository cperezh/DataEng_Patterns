import pytest
from conftest import borrar_movimientos_staging
import db

@pytest.mark.usefixtures("borrar_movimientos_staging")
@pytest.mark.usefixtures("insertar_movimientos_staging")
def test_borrar_movimientos_staging():

    conn = db.ConexionBD.obtener_conexion()

    result = conn.execute("select count(*) as total from bancapp.movimientos_staging").fetchone()

    assert result["total"] == 0