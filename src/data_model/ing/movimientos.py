import datetime as dt

class MovimientosCSV:
    
    def __init__(self, fecha_valor: str, importe: float, saldo: float):
        self.fecha_valor = fecha_valor
        self.importe = importe
        self.saldo = saldo
    
class MovimientoStaging:

    def __init__(self, id: int, fecha_valor: str, importe: float, saldo: float):
        self.id = id
        self.fecha_valor = dt.datetime.strptime(fecha_valor, '%d/%m/%Y').date()
        self.importe = importe
        self.saldo = saldo
