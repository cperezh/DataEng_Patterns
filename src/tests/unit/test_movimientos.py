"""
Tests para el módulo de movimientos.
Usando TDD: primero escribimos los tests, luego implementamos.
"""
import pytest
from datetime import date
from decimal import Decimal
from core.movimientos import Movimiento, BDMovimientos


class TestMovimiento:
    """Tests para la clase Movimiento"""

    def test_crear_movimiento_con_datos_validos(self):
        """Un movimiento debe crearse con fecha, comentario e importe válidos"""
        
        fecha = date(2025, 11, 13)
        comentario = "Pago de factura"
        importe = Decimal("100.50")
        
        movimiento = Movimiento(
            fecha_movimiento=fecha,
            comentario=comentario,
            importe=importe
        )
        
        assert movimiento.fecha_movimiento == fecha
        assert movimiento.comentario == comentario
        assert movimiento.importe == importe

    def test_movimiento_requiere_fecha_valida(self):
        """Un movimiento debe tener una fecha válida"""
        
        with pytest.raises(TypeError):
            Movimiento(
                fecha_movimiento="2025-11-13",  # String, no date
                concepto="Pago",
                importe=Decimal("100.00")
            )

    def test_movimiento_requiere_concepto_no_vacio(self):
        """Un movimiento debe tener un comentario no vacío"""
        
        with pytest.raises(ValueError):
            Movimiento(
                fecha_movimiento=date(2025, 11, 13),
                comentario="",  # Vacío
                importe=Decimal("100.00")
            )

    def test_movimiento_requiere_importe_positivo_o_negativo(self):
        """Un movimiento puede tener importe positivo (ingreso) o negativo (gasto)"""
        
        # Importe positivo (ingreso)
        movimiento_positivo = Movimiento(
            fecha_movimiento=date(2025, 11, 13),
            comentario="Ingreso",
            importe=Decimal("100.00")
        )
        assert movimiento_positivo.importe == Decimal("100.00")
        
        # Importe negativo (gasto)
        movimiento_negativo = Movimiento(
            fecha_movimiento=date(2025, 11, 13),
            comentario="Gasto",
            importe=Decimal("-50.00")
        )
        assert movimiento_negativo.importe == Decimal("-50.00")

    def test_movimiento_requiere_importe_valido(self):
        """Un movimiento debe tener un importe de tipo Decimal"""
        
        with pytest.raises(TypeError):
            Movimiento(
                fecha_movimiento=date(2025, 11, 13),
                comentario="Pago",
                importe="100.00"  # String, no Decimal
            )

    def test_movimiento_str_representation(self):
        """La representación en string de un movimiento debe ser legible"""
        
        movimiento = Movimiento(
            fecha_movimiento=date(2025, 11, 13),
            comentario="Pago de factura",
            importe=Decimal("100.50")
        )
        
        resultado = str(movimiento)
        assert "2025-11-13" in resultado
        assert "Pago de factura" in resultado
        assert "100.50" in resultado


class TestBDMovimientos:
    """Tests para el repositorio de movimientos"""

    def test_guardar_movimiento(self):
        """Debe poder guardar un movimiento en la BD"""
        
        repositorio = BDMovimientos()
        movimiento = Movimiento(
            fecha_movimiento=date(2025, 11, 13),
            comentario="Pago de factura",
            importe=Decimal("100.50")
        )
        
        movimiento_guardado = repositorio.guardar(movimiento)
        assert movimiento_guardado.id is not None

    def test_obtener_movimiento_por_id(self):
        """Debe poder obtener un movimiento por su ID"""
        
        repositorio = BDMovimientos()
        movimiento = Movimiento(
            fecha_movimiento=date(2025, 11, 13),
            comentario="Pago de factura",
            importe=Decimal("100.50")
        )
        
        movimiento_guardado = repositorio.guardar(movimiento)
        movimiento_recuperado = repositorio.obtener_por_id(movimiento_guardado.id)
        
        assert movimiento_recuperado.id == movimiento_guardado.id
        assert movimiento_recuperado.comentario == "Pago de factura"
        assert movimiento_recuperado.importe == Decimal("100.50")

    def test_obtener_todos_los_movimientos(self):
        """Debe poder obtener todos los movimientos"""
        
        repositorio = BDMovimientos()
        
        # Guardar varios movimientos
        m1 = repositorio.guardar(Movimiento(date(2025, 11, 13), "Pago 1", Decimal("100.00")))
        m2 = repositorio.guardar(Movimiento(date(2025, 11, 14), "Pago 2", Decimal("50.00")))
        
        movimientos = repositorio.obtener_todos()
        
        assert len(movimientos) >= 2
        assert any(m.id == m1.id for m in movimientos)
        assert any(m.id == m2.id for m in movimientos)

    def test_eliminar_movimiento(self):
        """Debe poder eliminar un movimiento"""
        
        repositorio = BDMovimientos()
        movimiento = repositorio.guardar(Movimiento(
            date(2025, 11, 13),
            "Pago a eliminar",
            Decimal("100.00")
        ))
        
        repositorio.eliminar(movimiento.id)
        movimiento_eliminado = repositorio.obtener_por_id(movimiento.id)
        
        assert movimiento_eliminado is None

    def test_obtener_movimientos_por_rango_fechas(self):
        """Debe poder obtener movimientos en un rango de fechas"""
        
        repositorio = BDMovimientos()
        
        # Guardar movimientos en diferentes fechas
        m1 = repositorio.guardar(Movimiento(date(2025, 11, 10), "Pago 1", Decimal("100.00")))
        m2 = repositorio.guardar(Movimiento(date(2025, 11, 15), "Pago 2", Decimal("50.00")))
        m3 = repositorio.guardar(Movimiento(date(2025, 11, 20), "Pago 3", Decimal("75.00")))
        
        # Obtener movimientos entre el 12 y 18
        movimientos = repositorio.obtener_por_rango_fechas(
            date(2025, 11, 12),
            date(2025, 11, 18)
        )
        
        ids_resultado = [m.id for m in movimientos]
        assert m2.id in ids_resultado
        assert m1.id not in ids_resultado
        assert m3.id not in ids_resultado
