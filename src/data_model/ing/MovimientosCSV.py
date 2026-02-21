from dataclasses import dataclass

@dataclass
class MovimientosCSV:
    
    fecha_valor: str
    importe: float
    saldo: float
    categoria: str
    subcategoria: str
    descripcion: str