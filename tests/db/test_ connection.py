import pytest
from db.connection import ConexionBD
import os

class TestConexionDB:

    def test_obtener_conexion(self):

        conn = ConexionBD.obtener_conexion()

        result = conn.execute("SELECT current_database() as db").fetchone()

        assert os.getenv("DB_NAME") == result["db"]
    
    def test_cerrar(self):
        
        ConexionBD.cerrar()

        assert ConexionBD._conexion == None
    
    def test_cerrar_cerrada(self):

        ConexionBD.cerrar()

        ConexionBD.cerrar()

        assert ConexionBD._conexion is None
    
    def test_obtener_conexion_cerrada(self):

        ConexionBD.obtener_conexion().close()

        conn = ConexionBD.obtener_conexion()
        
        assert conn != None

    def test_obtener_conexion_otravez(self):

        conn1 = ConexionBD.obtener_conexion()

        conn2 = ConexionBD.obtener_conexion()
    
        assert conn1 is conn2
