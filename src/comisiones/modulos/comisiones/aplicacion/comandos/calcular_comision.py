from comisiones.seedwork.aplicacion.comandos import Comando, ComandoHandler, ejecutar_commando as comando
from comisiones.modulos.comisiones.dominio.entidades import Comision
from comisiones.modulos.comisiones.dominio.objetos_valor import (
    InteraccionAtribuida,
    MontoComision,
    ConfiguracionComision,
    PoliticaFraude,
    TipoComision,
    TipoPoliticaFraude
)
from comisiones.modulos.comisiones.dominio.servicios import ServicioComision
from comisiones.modulos.comisiones.dominio.repositorios import (
    RepositorioComision,
    RepositorioConfiguracionComision,
    RepositorioPoliticaFraude
)
from comisiones.modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from comisiones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from comisiones.modulos.comisiones.dominio.eventos import ComisionCalculada
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import uuid

@dataclass
class CalcularComision(Comando):

    id_interaccion: uuid.UUID = None
    id_campania: uuid.UUID = None
    tipo_interaccion: str = None
    valor_interaccion: Decimal = None
    moneda_interaccion: str = "USD"
    fraud_ok: bool = True
    score_fraude: int = 0
    parametros_adicionales: dict = None

class CalcularComisionHandler(ComandoHandler):
    
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: CalcularComision):

        try:
            interaccion = InteraccionAtribuida(
                id_interaccion=comando.id_interaccion,
                id_campania=comando.id_campania,
                tipo_interaccion=comando.tipo_interaccion,
                valor_interaccion=MontoComision(
                    valor=comando.valor_interaccion,
                    moneda=comando.moneda_interaccion
                ),
                fraud_ok=comando.fraud_ok,
                score_fraude=comando.score_fraude,
                timestamp=datetime.now(),
                parametros_adicionales=comando.parametros_adicionales or {}
            )
            
            repositorio_comision = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            repositorio_configuracion = self._fabrica_repositorio.crear_objeto(
                RepositorioConfiguracionComision.__class__
            )
            repositorio_politica_fraude = self._fabrica_repositorio.crear_objeto(
                RepositorioPoliticaFraude.__class__
            )
            
            servicio_comision = ServicioComision(
                repositorio_comision=repositorio_comision,
                repositorio_configuracion=repositorio_configuracion,
                repositorio_politica_fraude=repositorio_politica_fraude
            )
            
            comision = servicio_comision.procesar_interaccion_atribuida(interaccion)
            
            if comision:
                UnidadTrabajoPuerto.registrar_batch(repositorio_comision.agregar, comision)
                UnidadTrabajoPuerto.savepoint()
                
                evento_comision_calculada = ComisionCalculada(
                    id_comision=comision.id,
                    id_interaccion=interaccion.id_interaccion,
                    id_campania=interaccion.id_campania,
                    monto=comision.monto,
                    configuracion=comision.configuracion,
                    timestamp=datetime.now(),
                    politica_fraude=comision.politica_fraude_aplicada,
                    tipo_calculo="CONVERSION_ATRIBUIDA"
                )
                
                UnidadTrabajoPuerto.publicar_evento(evento_comision_calculada)
                
                return comision
            else:
                print(f"No se calculó comisión para interacción {comando.id_interaccion}")
                return None
                
        except Exception as e:
            print(f"Error calculando comisión: {e}")
            raise e

@comando.register(CalcularComision)
def ejecutar_comando(comando: CalcularComision):
    handler = CalcularComisionHandler()
    return handler.handle(comando)
