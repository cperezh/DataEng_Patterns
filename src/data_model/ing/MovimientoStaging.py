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
    

    def __post_init__(self):
        self.fecha_valor = dt.datetime.strptime(self.fecha_valor, "%d/%m/%Y").date()