"""
Módulo de movimientos de cuenta.
Implementa las clases Movimiento y RepositorioMovimientos usando psycopg3 con patrón Singleton.
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from ...common.db_connection import ConexionBD


class Movimiento:
    """Representa un movimiento de cuenta"""
    def __init__(
        self,
        fecha_movimiento: date,
        comentario: Optional[str] = None,
        importe: Optional[Decimal] = None,
        categoria: Optional[str] = None,
        subcategoria: Optional[str] = None,
        descripcion: Optional[str] = None,
        saldo: Optional[Decimal] = None,
    ):
        """Inicializa un movimiento.

        Campos principales:
        - fecha_movimiento (date)
        - comentario (texto descriptivo del movimiento)
        - importe (Decimal)
        - categoria, subcategoria, descripcion, saldo (opcionales)
        """
        if not isinstance(fecha_movimiento, date):
            raise TypeError(f"fecha_movimiento debe ser date, recibido {type(fecha_movimiento)}")

        if importe is not None and not isinstance(importe, Decimal):
            raise TypeError(f"importe debe ser Decimal si se proporciona, recibido {type(importe)}")

        # Validación: comentario no puede estar vacío (ni solo espacios)
        if comentario is None or (isinstance(comentario, str) and comentario.strip() == ""):
            raise ValueError("El campo 'comentario' es obligatorio y no puede estar vacío")

        self.id: Optional[int] = None
        self.fecha_movimiento = fecha_movimiento
        self.comentario = comentario
        self.descripcion = descripcion
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.importe = importe
        self.saldo = saldo

    def __str__(self) -> str:
        """Representación en string del movimiento"""
        return f"{self.fecha_movimiento} - {self.comentario}: {self.importe}"

    def __repr__(self) -> str:
        """Representación para debug"""
        return f"Movimiento(id={self.id}, fecha={self.fecha_movimiento}, comentario='{self.comentario}', importe={self.importe})"


class BDMovimientos:
    """Repositorio para gestionar movimientos en la base de datos"""

    def __init__(self):
        """
        Inicializa el repositorio con la conexión Singleton.
        """
        self.conexion_bd = ConexionBD()

    def _get_connection(self) -> psycopg.Connection:
        """
        Obtiene la conexión Singleton a la base de datos.
        
        Returns:
            Conexión psycopg3 compartida (Singleton)
        """
        return self.conexion_bd.obtener_conexion()

    def guardar(self, movimiento: Movimiento) -> Movimiento:
        """
        Guarda un movimiento en la base de datos.
        
        Args:
            movimiento: Movimiento a guardar
            
        Returns:
            Movimiento con ID asignado
        """
        try:
            conn = self._get_connection()
            result = conn.execute(
                sql.SQL("""
                    INSERT INTO movimientos (fecha_movimiento, comentario, importe)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """),
                (movimiento.fecha_movimiento, movimiento.comentario, movimiento.importe)
            ).fetchone()
            movimiento.id = result['id']
            conn.commit()
            
            return movimiento
        except psycopg.Error as e:
            raise Exception(f"Error al guardar movimiento: {e}")

    def obtener_por_id(self, movimiento_id: int) -> Optional[Movimiento]:
        """
        Obtiene un movimiento por su ID.
        
        Args:
            movimiento_id: ID del movimiento
            
        Returns:
            Movimiento si existe, None en caso contrario
        """
        try:
            conn = self._get_connection()
            result = conn.execute(
                sql.SQL("""
                    SELECT id, fecha_movimiento, comentario, importe
                    FROM movimientos
                    WHERE id = %s
                """),
                (movimiento_id,)
            ).fetchone()
            
            if result:
                movimiento = Movimiento(
                    fecha_movimiento=result['fecha_movimiento'],
                    comentario=result['comentario'],
                    importe=result['importe']
                )
                movimiento.id = result['id']
                return movimiento
            
            return None
        except psycopg.Error as e:
            raise Exception(f"Error al obtener movimiento: {e}")

    def obtener_todos(self) -> List[Movimiento]:
        """
        Obtiene todos los movimientos de la base de datos.
        
        Returns:
            Lista de Movimientos
        """
        try:
            conn = self._get_connection()
            results = conn.execute(
                sql.SQL("""
                    SELECT id, fecha_movimiento, comentario, importe
                    FROM movimientos
                    ORDER BY fecha_movimiento DESC
                """)
            ).fetchall()
            
            movimientos = []
            for row in results:
                movimiento = Movimiento(
                    fecha_movimiento=row['fecha_movimiento'],
                    comentario=row['comentario'],
                    importe=row['importe']
                )
                movimiento.id = row['id']
                movimientos.append(movimiento)
            
            return movimientos
        except psycopg.Error as e:
            raise Exception(f"Error al obtener movimientos: {e}")

    def eliminar(self, movimiento_id: int) -> bool:
        """
        Elimina un movimiento de la base de datos.
        
        Args:
            movimiento_id: ID del movimiento a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        try:
            conn = self._get_connection()
            conn.execute(
                sql.SQL("DELETE FROM movimientos WHERE id = %s"),
                (movimiento_id,)
            )
            conn.commit()
            
            return True
        except psycopg.Error as e:
            raise Exception(f"Error al eliminar movimiento: {e}")

    def obtener_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> List[Movimiento]:
        """
        Obtiene movimientos en un rango de fechas.
        
        Args:
            fecha_inicio: Fecha de inicio (inclusive)
            fecha_fin: Fecha de fin (inclusive)
            
        Returns:
            Lista de Movimientos en el rango especificado
        """
        try:
            conn = self._get_connection()
            results = conn.execute(
                sql.SQL("""
                    SELECT id, fecha_movimiento, comentario, importe
                    FROM movimientos
                    WHERE fecha_movimiento BETWEEN %s AND %s
                    ORDER BY fecha_movimiento DESC
                """),
                (fecha_inicio, fecha_fin)
            ).fetchall()
            
            movimientos = []
            for row in results:
                movimiento = Movimiento(
                    fecha_movimiento=row['fecha_movimiento'],
                    comentario=row['comentario'],
                    importe=row['importe']
                )
                movimiento.id = row['id']
                movimientos.append(movimiento)
            
            return movimientos
        except psycopg.Error as e:
            raise Exception(f"Error al obtener movimientos por rango de fechas: {e}")
