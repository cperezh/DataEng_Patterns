import data_model.ing as dm_ing
import db
from psycopg.rows import class_row

class MovimientosSilver:

    @staticmethod
    def obtener_todos() -> list[dm_ing.MovimientosSilver]:
        """
        Obtiene todos los movimientos de la base de datos.
        
        Returns:
            Lista de MovimientoStaging
        """

        conn = db.ConexionBD.obtener_conexion()
        
        results = conn.cursor(row_factory=class_row(dm_ing.MovimientosSilver)).execute(
            """
                SELECT 
                    fecha_valor, 
                    importe, 
                    saldo,
                    categoria,  
                    subcategoria,
                    descripcion,
                    created_at
                FROM bancapp.movimientos_mview
                ORDER BY fecha_valor ASC
            """
        ).fetchall()
        
        return results