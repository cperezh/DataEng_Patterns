"""
ETL para movimientos.

Funciones:
- leer_csv
- normalizar_numero
- parse_fecha
- fila_a_movimiento
- extraer_movimientos
- cargar_movimientos_en_bd
- run_etl

Política: filas inválidas se omiten y se registran; deduplicación por (fecha_movimiento, importe, saldo).
"""
from __future__ import annotations

import csv
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from typing import List, Tuple, Optional, Dict, Any

from core.movimientos import Movimiento, RepositorioMovimientos
from core.connection import ConexionBD


def leer_csv(path: str):
    """Iterador de filas del CSV a partir de la línea de encabezado.

    Busca la línea que comienza con 'F. VALOR' y usa csv.DictReader a partir de ahí.
    """
    with open(path, newline='', encoding='utf-8') as fh:
        lines = fh.readlines()

    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('F. VALOR'):
            header_idx = i
            break

    if header_idx is None:
        raise ValueError("No se encontró la línea de encabezado 'F. VALOR' en el CSV")

    header_and_rows = lines[header_idx:]
    reader = csv.DictReader(header_and_rows, skipinitialspace=True)

    for row in reader:
        # Normalize keys by stripping BOM/whitespace
        yield {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items()}


def normalizar_numero(s: Optional[str]) -> Optional[Decimal]:
    """Normaliza cadenas numéricas y devuelve Decimal.

    Reglas:
    - Elimina comillas y espacios.
    - Si la cadena contiene ambos ',' y '.' se asume que la coma es separador de miles => eliminar comas.
    - Si contiene sólo ',' se asume coma decimal => reemplazar por '.'.
    - Devuelve None si entrada vacía o None.
    """
    if s is None:
        return None

    s = s.strip().replace('"', '').replace("'", '')
    if s == '':
        return None

    # Some CSVs use non-breaking spaces or other characters; remove spaces
    s = s.replace('\xa0', '').replace(' ', '')

    # If contains both comma and dot, remove commas (commas as thousand separators)
    if ',' in s and '.' in s:
        s = s.replace(',', '')
    elif ',' in s and '.' not in s:
        # Comma as decimal separator
        s = s.replace(',', '.')

    try:
        return Decimal(s)
    except (InvalidOperation, ValueError) as e:
        raise ValueError(f"No se pudo convertir a Decimal: '{s}'") from e


def parse_fecha(s: Optional[str]) -> date:
    """Parsea fecha en formato dd/mm/YYYY a datetime.date"""
    if s is None or s.strip() == '':
        raise ValueError("Fecha vacía")
    s = s.strip()
    # Algunos CSV pueden contener hora; solo tomar la parte de la fecha
    # Intentar varios formatos
    for fmt in ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'):
        try:
            return datetime.strptime(s.split()[0], fmt).date()
        except Exception:
            continue
    raise ValueError(f"Formato de fecha no reconocido: '{s}'")


def _find_key(row: Dict[str, Any], candidates: List[str]) -> Optional[str]:
    for c in candidates:
        for k in row.keys():
            if c.lower() in k.lower():
                return k
    return None


def fila_a_movimiento(row: Dict[str, str]) -> Movimiento:
    """Convierte una fila del CSV (dict) en un objeto Movimiento.

    Lanza ValueError si faltan campos obligatorios o no son válidos.
    """
    # Buscar claves posibles
    fecha_key = _find_key(row, ['F. VALOR', 'FECHA', 'F. VALOR']) or list(row.keys())[0]
    comentario_key = _find_key(row, ['COMENTARIO', 'COMENTARIO'])
    descripcion_key = _find_key(row, ['DESCRIPC', 'DESCRIPCIÓN', 'DESCRIPCION'])
    importe_key = _find_key(row, ['IMPORTE'])
    saldo_key = _find_key(row, ['SALDO'])
    categoria_key = _find_key(row, ['CATEGOR', 'CATEGORÍA', 'CATEGORIA'])
    subcategoria_key = _find_key(row, ['SUBCATEG', 'SUBCATEGORÍA', 'SUBCATEGORIA'])

    # Extraer valores raw
    fecha_raw = row.get(fecha_key)
    # Preferir comentario; si no existe, usar descripción
    comentario_raw = None
    if comentario_key:
        comentario_raw = row.get(comentario_key)
    if (comentario_raw is None or comentario_raw.strip() == '') and descripcion_key:
        comentario_raw = row.get(descripcion_key)

    importe_raw = row.get(importe_key) if importe_key else None
    saldo_raw = row.get(saldo_key) if saldo_key else None
    categoria = row.get(categoria_key) if categoria_key else None
    subcategoria = row.get(subcategoria_key) if subcategoria_key else None
    descripcion = row.get(descripcion_key) if descripcion_key else None

    # Validaciones: comentario, importe y saldo son obligatorios segun tus reglas
    if comentario_raw is None or comentario_raw.strip() == '':
        raise ValueError('Comentario vacío')
    if importe_raw is None or importe_raw.strip() == '':
        raise ValueError('Importe vacío')
    if saldo_raw is None or saldo_raw.strip() == '':
        raise ValueError('Saldo vacío')

    fecha = parse_fecha(fecha_raw)
    importe = normalizar_numero(importe_raw)
    saldo = normalizar_numero(saldo_raw)

    if importe is None:
        raise ValueError('Importe no convertible')
    if saldo is None:
        raise ValueError('Saldo no convertible')

    movimiento = Movimiento(
        fecha_movimiento=fecha,
        comentario=comentario_raw,
        importe=importe,
        categoria=categoria,
        subcategoria=subcategoria,
        descripcion=descripcion,
        saldo=saldo,
    )

    return movimiento


def extraer_movimientos(path: str) -> Tuple[List[Movimiento], List[Dict[str, Any]]]:
    """Extrae movimientos desde el CSV.

    Devuelve (movimientos_validos, errores) donde errores es una lista de dicts {row, reason}.
    """
    movimientos: List[Movimiento] = []
    errores: List[Dict[str, Any]] = []

    for idx, row in enumerate(leer_csv(path)):
        try:
            mov = fila_a_movimiento(row)
            movimientos.append(mov)
        except Exception as e:
            errores.append({'index': idx, 'row': row, 'reason': str(e)})
            # Omitir fila inválida
            print(f"Omitida fila {idx}: {e}")

    return movimientos, errores


def cargar_movimientos_en_bd(movimientos: List[Movimiento], repo: Optional[RepositorioMovimientos] = None) -> List[Movimiento]:
    """Carga movimientos en la BD. Evita duplicados por (fecha, importe, saldo).

    Si encuentra duplicado, asigna el id existente al objeto movimiento y no inserta.
    Devuelve la lista de movimientos (algunos con id ya asignado).
    """
    if repo is None:
        repo = RepositorioMovimientos()

    conn = ConexionBD().obtener_conexion()

    movimientos_guardados: List[Movimiento] = []
    for mov in movimientos:
        # Usar parámetros exactos; saldo e importe deben existir (requisitos)
        try:
            existing = conn.execute(
                "SELECT id FROM movimientos WHERE fecha_movimiento = %s AND importe = %s AND saldo = %s",
                (mov.fecha_movimiento, mov.importe, mov.saldo)
            ).fetchone()
        except Exception as e:
            raise Exception(f"Error consultando duplicados en BD: {e}")

        if existing:
            mov.id = existing['id']
            print(f"Omitido duplicado: fecha={mov.fecha_movimiento} importe={mov.importe} saldo={mov.saldo} (id={mov.id})")
        else:
            # Insertar usando repositorio para mantener lógica existente
            mov = repo.guardar(mov)
            print(f"Insertado movimiento id={mov.id} fecha={mov.fecha_movimiento} importe={mov.importe} saldo={mov.saldo}")

        movimientos_guardados.append(mov)

    return movimientos_guardados


def run_etl(path: str, repo: Optional[RepositorioMovimientos] = None) -> Tuple[List[Movimiento], List[Dict[str, Any]]]:
    """Flujo completo ETL: extraer, transformar y cargar.

    Devuelve (movimientos_cargados, errores_de_extraccion)
    """
    movimientos, errores = extraer_movimientos(path)
    movimientos_cargados = cargar_movimientos_en_bd(movimientos, repo=repo)
    return movimientos_cargados, errores
