"""
Módulo que expone la clase ConexionBD (Singleton) para la conexión a PostgreSQL.

Este módulo contiene la implementación del Singleton para centralizar la
gestión de la conexión usando psycopg3.
"""
from typing import Optional
import psycopg
from psycopg.rows import dict_row

class ConexionBD:
    """Singleton para gestionar la conexión a la base de datos"""

    _conexion: Optional[psycopg.Connection] = None
     
    def __init__(self, host: str = "db", port: int = 5432,
                 database: str = "pruebas", user: str = "myuser",
                 password: str = "mypassword"):
        """Constructor (no hace nada si ya se inicializó)"""

        if ConexionBD._conexion is None or ConexionBD._conexion.closed:
            self._inicializar(host, port, database, user, password)


    def _inicializar(self, host: str, port: int, database: str, user: str, password: str):
        """Inicializa la conexión una sola vez"""

        conninfo = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        
        # Configuramos row_factory para devolver filas como diccionarios
        self._conexion = psycopg.connect(conninfo, row_factory=dict_row)

    def obtener_conexion(self) -> psycopg.Connection:
        """
        Obtiene la conexión singleton a la base de datos.

        Returns:
            Conexión psycopg3 compartida
        """
        return self._conexion

    def cerrar(self):
        """Cierra la conexión singleton"""
        if self._conexion and not getattr(self._conexion, 'closed', False):
            self._conexion.close()
            self._conexion = None
