import numpy_financial as npf
from src.precios import PreciosAlquiler

class DatosCalculadora:
    def __init__(self, nombre, precio, metros, poblacion):
            precioMetroAlquiler = PreciosAlquiler()
            self.nombre = str(nombre)
            self.precio = int(precio)
            self.metros = int(metros)
            self.poblacion = str(poblacion)
            self.p_compra = int(precio)
            self.itp = int(float(precio) * 0.1)
            self.reforma = 6000
            self.notaria = 1000
            self.registro = 0
            self.agencia = 0
            self.tasacion = 200
            self.total_compra = self.p_compra+self.itp+self.notaria+self.registro+self.reforma+self.agencia+self.tasacion
            self.ibi = 450
            self.basuras = 0
            self.comunidad = 400
            self.seguros = 400
            self.total_gastos = self.ibi+self.basuras+self.seguros+self.comunidad
            self.alquiler = int(float(self.metros) * float(getattr(precioMetroAlquiler, self.poblacion)))
            self.financiado = 80
            self.hipoteca = int((self.financiado/100)*self.p_compra)
            self.a_aportar = int(self.p_compra+self.itp+self.reforma+self.notaria+self.registro+self.agencia+self.tasacion-self.hipoteca)
            self.plazo = 30
            self.interes_anuales = 3.5/100
            self.interes_mensuales = self.interes_anuales/12
            self.cuota = -1*npf.pmt(self.interes_mensuales, nper=self.plazo*12, pv=self.hipoteca, fv=0)
            self.cuota_intereses = ((self.cuota*12*self.plazo)-self.hipoteca)/(self.plazo*12)
            self.cuota_amortizacion = self.cuota-self.cuota_intereses
            self.r_bruta = ((self.alquiler*12)/self.total_compra)
            self.r_neta = ((self.alquiler*12)-self.total_gastos-(self.cuota_intereses*12))/self.total_compra
            self.c_flow = self.alquiler-self.cuota-self.total_gastos/12
            self.c_oncash = (self.c_flow*12)/self.a_aportar
            self.roce = 12*(self.c_flow+self.cuota_amortizacion)/self.a_aportar