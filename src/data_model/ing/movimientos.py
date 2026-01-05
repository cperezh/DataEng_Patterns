import datetime as dt

class MovimientosCSV:
    
    def __init__(self, 
                 fecha_valor: str, 
                 importe: float, 
                 saldo: float, 
                 categoria: str,
                 subcategoria: str,
                 descripcion: str):
        self.fecha_valor = fecha_valor
        self.importe = importe
        self.saldo = saldo
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.descripcion = descripcion
    
class MovimientoStaging:

    def __init__(self, 
                 id: int, 
                 fecha_valor: str, 
                 importe: float, 
                 saldo: float, 
                 categoria: str,
                 subcategoria: str,
                 descripcion: str):
        self.id = id
        self.fecha_valor = dt.datetime.strptime(fecha_valor, '%d/%m/%Y').date()
        self.importe = importe
        self.saldo = saldo
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.descripcion = descripcion
