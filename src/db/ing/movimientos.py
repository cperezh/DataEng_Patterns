
from db.connection import ConexionBD
import data_model.ing.movimientos as dm
import psycopg
from psycopg import sql
from psycopg.rows import class_row
from typing import Optional

class MovimientosStaging:
    

    @staticmethod
    def obtener_todos() -> list[dm.MovimientoStaging]:
        """
        Obtiene todos los movimientos de la base de datos.
        
        Returns:
            Lista de MovimientoStaging
        """

        movs_staging = []

        try:
            conn = ConexionBD.obtener_conexion()
            
            if conn is not None:
                results = conn.cursor(row_factory=class_row(dm.MovimientoStaging)).execute(
                    sql.SQL("""
                        SELECT id, fecha_valor, importe, saldo
                        FROM bancapp.movimientos_staging
                    """)
                ).fetchall()
            
                for mov_staging in results:
                    movs_staging.append(mov_staging)
            
            return movs_staging
        except psycopg.Error as e:
            raise Exception(f"Error al obtener movimientos: {e}")
