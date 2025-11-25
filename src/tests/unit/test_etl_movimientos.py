"""
Unit tests for src.etl.etl_movimientos
"""
import tempfile
from datetime import date
from decimal import Decimal
import io

import pytest

from etl import etl_movimientos as etl
from core.movimientos import Movimiento


def test_normalizar_numero_basic_cases():
    assert etl.normalizar_numero(None) is None
    assert etl.normalizar_numero("") is None
    assert etl.normalizar_numero('1,234.56') == Decimal('1234.56')
    # comma as decimal separator
    assert etl.normalizar_numero('1234,56') == Decimal('1234.56')
    # both dot and comma where dot is thousand separator (behavior: remove commas)
    assert etl.normalizar_numero('1,234,567.89') == Decimal('1234567.89')


def test_parse_fecha_various_formats():
    assert etl.parse_fecha('13/11/2025') == date(2025, 11, 13)
    assert etl.parse_fecha('13/11/25') == date(2025, 11, 13)
    assert etl.parse_fecha('2025-11-13') == date(2025, 11, 13)
    with pytest.raises(ValueError):
        etl.parse_fecha('')
    with pytest.raises(ValueError):
        etl.parse_fecha(None)


def test_fila_a_movimiento_happy_path():
    row = {
        'F. VALOR': '13/11/2025',
        'COMENTARIO': 'Pago de factura',
        'IMPORTE': '100.50',
        'SALDO': '1000.00',
        'DESCRIPCION': 'Factura 123',
    }

    mov = etl.fila_a_movimiento(row)
    assert isinstance(mov, Movimiento)
    assert mov.fecha_movimiento == date(2025, 11, 13)
    assert mov.comentario == 'Pago de factura'
    assert mov.importe == Decimal('100.50')
    assert mov.saldo == Decimal('1000.00')
    assert mov.descripcion == 'Factura 123'


def test_fila_a_movimiento_missing_fields_raises():
    row_missing = {
        'F. VALOR': '13/11/2025',
        'COMENTARIO': '',
        'IMPORTE': '100.50',
        'SALDO': '1000.00'
    }
    with pytest.raises(ValueError):
        etl.fila_a_movimiento(row_missing)


def _make_sample_csv_content():
    # Some preamble lines, then header starting with 'F. VALOR'
    content = io.StringIO()
    content.write('Preamble line 1\n')
    content.write('Preamble line 2\n')
    content.write('F. VALOR,COMENTARIO,IMPORTE,SALDO\n')
    content.write('13/11/2025,Pago de factura,100.50,1000.00\n')
    content.write('14/11/2025,,200.00,800.00\n')  # second row has empty comentario -> should be error
    content.seek(0)
    return content.getvalue()


def test_extraer_movimientos_from_csv(tmp_path):
    csv_text = _make_sample_csv_content()
    p = tmp_path / 'sample.csv'
    p.write_text(csv_text, encoding='utf-8')

    movimientos, errores = etl.extraer_movimientos(str(p))
    # first row valid, second should be in errors
    assert len(movimientos) == 1
    assert len(errores) == 1
    assert movimientos[0].comentario == 'Pago de factura'


class _DummyConn:
    def __init__(self, existing_row=None):
        self._existing = existing_row

    def execute(self, query, params):
        class _Res:
            def __init__(self, val):
                self._val = val

            def fetchone(self):
                return self._val

        return _Res(self._existing)


class _DummyRepo:
    def __init__(self):
        self.saved = []

    def guardar(self, mov: Movimiento):
        # emulate assigning an id
        mov.id = 999
        self.saved.append(mov)
        return mov


def test_cargar_movimientos_en_bd_inserts_and_skips(monkeypatch):
    # Prepare a movement to insert
    mov = Movimiento(date(2025, 11, 13), 'Pago', Decimal('100.00'))

    # Case 1: no existing -> insert via repo
    dummy_repo = _DummyRepo()

    # monkeypatch ConexionBD in module to return connection with no existing
    monkeypatch.setattr(etl, 'ConexionBD', lambda: type('C', (), {'obtener_conexion': lambda self: _DummyConn(None)})())

    res = etl.cargar_movimientos_en_bd([mov], repo=dummy_repo)
    assert len(res) == 1
    assert res[0].id == 999
    assert dummy_repo.saved

    # Case 2: existing found -> should set id and not call repo.guardar
    mov2 = Movimiento(date(2025, 11, 14), 'Pago2', Decimal('50.00'))

    dummy_repo2 = _DummyRepo()
    # connection returns an existing id
    monkeypatch.setattr(etl, 'ConexionBD', lambda: type('C', (), {'obtener_conexion': lambda self: _DummyConn({'id': 123})})())

    res2 = etl.cargar_movimientos_en_bd([mov2], repo=dummy_repo2)
    assert len(res2) == 1
    assert res2[0].id == 123
    # repo should not have saved this movement
    assert not dummy_repo2.saved


def test_run_etl_integration(monkeypatch, tmp_path):
    # Create a sample csv file
    csv_text = _make_sample_csv_content()
    p = tmp_path / 'sample.csv'
    p.write_text(csv_text, encoding='utf-8')

    # dummy repo that saves and assigns ids
    class DummyRepoAll(_DummyRepo):
        pass

    dummy_repo = DummyRepoAll()

    # monkeypatch ConexionBD to return a connection with no existing rows
    monkeypatch.setattr(etl, 'ConexionBD', lambda: type('C', (), {'obtener_conexion': lambda self: _DummyConn(None)})())

    movimientos_cargados, errores = etl.run_etl(str(p), repo=dummy_repo)
    # Should load 1 movimiento (first row) and have 1 error (second row)
    assert len(movimientos_cargados) == 1
    assert len(errores) == 1
    assert movimientos_cargados[0].id == 999
    assert movimientos_cargados[0].comentario == 'Pago de factura'
