import pytest

from core.connection import ConexionBD


@pytest.mark.db
def test_singleton_instancia_unica():

    # La conexión interna también debe ser la misma referencia
    conn1 = ConexionBD().obtener_conexion()
    conn2 = ConexionBD().obtener_conexion()
    assert conn1 is conn2


@pytest.mark.db
def test_reconectar_despues_de_cerrar():
    """Cerrar la conexión y obtener una nueva debe crear un nuevo objeto de conexión."""
    c = ConexionBD()
    conn1 = c.obtener_conexion()
    # Cerrar mediante la API
    c.cerrar()

    # Obtener una nueva conexión
    conn2 = c.obtener_conexion()

    assert conn1 is not conn2
    assert not getattr(conn2, 'closed', False)


@pytest.mark.db
def test_row_factory_devuelve_diccionario():
    """La conexión debe devolver filas como diccionarios (row_factory=dict_row)."""
    c = ConexionBD()
    conn = c.obtener_conexion()

    row = conn.execute("SELECT 1 as one").fetchone()
    assert isinstance(row, dict)
    assert 'one' in row and row['one'] == 1
