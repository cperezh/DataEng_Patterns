"""
Módulo que expone la clase ConexionBD (Singleton) para la conexión a PostgreSQL.

Este módulo contiene la implementación del Singleton para centralizar la
gestión de la conexión usando psycopg3.
"""
from typing import Optional
import psycopg
from psycopg.rows import dict_row
import os

class ConexionBD:
    """Singleton para gestionar la conexión a la base de datos"""

    _conexion: Optional[psycopg.Connection] = None

    @classmethod
    def _inicializar(cls):
        """Inicializa la conexión una sola vez"""

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")

        conninfo = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        
        # Configuramos row_factory para devolver filas como diccionarios
        cls._conexion = psycopg.connect(conninfo, row_factory=dict_row)

    @classmethod
    def obtener_conexion(cls) -> psycopg.Connection:
        """
        Obtiene la conexión singleton a la base de datos.

        Returns:
            Conexión psycopg3 compartida
        """

        if cls._conexion is None or cls._conexion.closed:
            cls._inicializar()

        return cls._conexion

    @classmethod
    def cerrar(cls):
        """Cierra la conexión singleton"""
        if cls._conexion and cls._conexion.closed == False:
            cls._conexion.close()
            cls._conexion = None
