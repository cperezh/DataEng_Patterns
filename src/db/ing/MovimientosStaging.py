
import db
import data_model.ing as dm_ing
from psycopg.rows import class_row
import datetime as dt

class MovimientosStaging:
    

    @staticmethod
    def obtener_todos() -> list[dm_ing.MovimientoStaging]:
        """
        Obtiene todos los movimientos de la base de datos.
        
        Returns:
            Lista de MovimientoStaging
        """

        conn = db.ConexionBD.obtener_conexion()
        
        results = conn.cursor(row_factory=class_row(dm_ing.MovimientoStaging)).execute(
            """
                SELECT 
                    id, 
                    fecha_valor, 
                    importe, 
                    saldo,
                    categoria,  
                    subcategoria,
                    descripcion,
                    created_at
                FROM bancapp.movimientos_staging
                ORDER BY fecha_valor ASC, id ASC
            """
        ).fetchall()
        
        return results
        
    @staticmethod
    def insertar_movimientos_bulk(movs: list[dm_ing.MovimientoStaging], fecha_lote: dt.datetime):

        conn = db.ConexionBD.obtener_conexion()

        with conn.cursor().copy(
            """
            COPY bancapp.movimientos_staging(
                fecha_valor, 
                importe, 
                saldo, 
                created_at, 
                categoria, 
                subcategoria, 
                descripcion
                ) FROM STDIN
            """
            ) as copy:
            for mov in movs:
                values =(mov.fecha_valor, 
                         mov.importe, 
                         mov.saldo, 
                         fecha_lote, 
                         mov.categoria,
                         mov.subcategoria,
                         mov.descripcion)
                copy.write_row(values)
        
        conn.commit()


