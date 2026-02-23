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

    def __post_init__(self):
        self.fecha_valor = dt.datetime.strptime(self.fecha_valor, "%d/%m/%Y").date()
        self.created_at = dt.datetime.strptime(self.created_at, "%d/%m/%Y").date()
