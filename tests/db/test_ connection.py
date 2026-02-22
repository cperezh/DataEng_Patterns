import db
import os

class TestConexionDB:

    def test_obtener_conexion(self):

        conn = db.ConexionBD.obtener_conexion()

        result = conn.execute("SELECT current_database() as db").fetchone()

        assert os.getenv("DB_NAME") == result["db"]
    
    def test_cerrar(self):
        
        db.ConexionBD.cerrar()

        assert db.ConexionBD._conexion == None
    
    def test_cerrar_cerrada(self):

        db.ConexionBD.cerrar()

        db.ConexionBD.cerrar()

        assert db.ConexionBD._conexion is None
    
    def test_obtener_conexion_cerrada(self):

        db.ConexionBD.obtener_conexion().close()

        conn = db.ConexionBD.obtener_conexion()
        
        assert conn != None

    def test_obtener_conexion_otravez(self):

        conn1 = db.ConexionBD.obtener_conexion()

        conn2 = db.ConexionBD.obtener_conexion()
    
        assert conn1 is conn2
