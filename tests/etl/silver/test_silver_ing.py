import pytest
from etl.silver import silver_ing
import db.ing


@pytest.mark.usefixtures("movimientos_staging_duplicates")
def test_refresh_movimientos():

    silver_ing.refresh_movimientos()

    movimientos_silver = db.ing.MovimientosSilver.obtener_todos()

    assert len(movimientos_silver)==4
    assert movimientos_silver[0].descripcion=="POSTERIOR - Pago en DECATHLON ALCOBENDAS ALCOBENDAS ES"