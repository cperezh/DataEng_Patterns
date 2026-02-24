import datetime as dt
from dataclasses import dataclass


@dataclass
class MovimientoStaging:
   
    id: int
    fecha_valor: dt.datetime.date
    importe: float
    saldo: float
    categoria: str
    subcategoria: str
    descripcion: str
    created_at: dt.datetime.date