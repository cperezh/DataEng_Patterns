
from db.connection import ConexionBD
from data_model.ing.movimientos import MovimientoStaging
import psycopg
from psycopg import sql

class MovimientosStaging:
    

    @staticmethod
    def obtener_todos() -> list[MovimientoStaging]:
        """
        Obtiene todos los movimientos de la base de datos.
        
        Returns:
            Lista de MovimientoStaging
        """
        try:
            conn: psycopg.Connection = ConexionBD.obtener_conexion()
            
            results = conn.execute(
                sql.SQL("""
                    SELECT id, fecha_valor, importe, saldo
                    FROM movimientos_stagings
                """)
            ).fetchall()
            
            movimientos = []
            for row in results:
                movimiento = MovimientoStaging(
                    id = row['id'],
                    fecha_valor=row['fecha_valor'],
                    importe=row['comentario'],
                    saldo=row['importe']
                )
                movimientos.append(movimiento)
            
            return movimientos
        except psycopg.Error as e:
            raise Exception(f"Error al obtener movimientos: {e}")
