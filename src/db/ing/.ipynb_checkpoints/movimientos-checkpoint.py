
from db.connection import ConexionBD
import data_model.ing.movimientos as dm
import psycopg
from psycopg.rows import class_row
import datetime as dt

class MovimientosStaging:
    

    @staticmethod
    def obtener_todos() -> list[dm.MovimientoStaging]:
        """
        Obtiene todos los movimientos de la base de datos.
        
        Returns:
            Lista de MovimientoStaging
        """

        conn = ConexionBD.obtener_conexion()
        
        results = conn.cursor(row_factory=class_row(dm.MovimientoStaging)).execute(
            """
                SELECT 
                    id, 
                    TO_CHAR(fecha_valor, 'DD/MM/YYYY') as fecha_valor, 
                    importe, 
                    saldo
                FROM bancapp.movimientos_staging
                ORDER BY bancapp.movimientos_staging.fecha_valor ASC, id ASC
            """
        ).fetchall()
        
        return results
        
    @staticmethod
    def insertar_movimientos_bulk(movs: list[dm.MovimientoStaging], fecha_lote: dt.datetime):

        conn = ConexionBD.obtener_conexion()

        with conn.cursor().copy(
            """
            COPY bancapp.movimientos_staging (fecha_valor, importe, saldo, created_at) FROM STDIN
            """
            ) as copy:
            for mov in movs:
                values =(mov.fecha_valor, mov.importe, mov.saldo, fecha_lote)
                copy.write_row(values)
        
        conn.commit()


