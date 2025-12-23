
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
            results = []
            
            if conn is not None:
                results = conn.cursor(row_factory=class_row(dm.MovimientoStaging)).execute(
                    sql.SQL("""
                        SELECT 
                            id, 
                            TO_CHAR(fecha_valor, 'DD/MM/YYYY') as fecha_valor, 
                            importe, 
                            saldo
                        FROM bancapp.movimientos_staging
                        ORDER BY bancapp.movimientos_staging.fecha_valor ASC, id ASC
                    """)
                ).fetchall()
            
            return results
        except psycopg.Error as e:
            raise Exception(f"Error al obtener movimientos: {e}")
        
    @staticmethod
    def insertar_movimientos_bulk(movs: list[dm.MovimientoStaging]):
        try:
            conn = ConexionBD.obtener_conexion()

            if conn:
                with conn.cursor().copy("""
                    COPY bancapp.movimientos_staging (fecha_valor, importe, saldo) FROM STDIN
                                        """
                                        ) as copy:
                    for mov in movs:
                        values =(mov.fecha_valor, mov.importe, mov.saldo)
                        copy.write_row(values)
                
                conn.commit()

        except psycopg.Error as e:
            raise Exception(f"Error al insertar_movimientos: {e}")
