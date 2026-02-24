from dataclasses import dataclass
import datetime as dt

@dataclass
class MovimientosSilver:
    
    fecha_valor: dt.datetime.date
    importe: float
    saldo: float
    categoria: str
    subcategoria: str
    descripcion: str
    created_at: dt.datetime.date

