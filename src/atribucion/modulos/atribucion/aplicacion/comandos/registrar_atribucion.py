# src/attribution/modulos/attribution/aplicacion/comandos/registrar_atribucion.py
import uuid
from dataclasses import dataclass
from atribucion.seedwork.aplicacion.comandos import Comando, ejecutar_commando as comando
from atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from atribucion.modulos.atribucion.aplicacion.dto import AtribucionDTO
from atribucion.modulos.atribucion.dominio.entidades import Journey, ModeloAtribucion, TipoModeloAtribucion
from atribucion.modulos.atribucion.dominio.repositorios import RepositorioJourney
from atribucion.modulos.atribucion.infraestructura.despachadores import DespachadorEventosAtribucion
from .base import RegistrarAtribucionBaseHandler
from ..mapeadores import MapeadorAtribucion 

@dataclass
class RegistrarAtribucion(Comando): 
    atribucion: AtribucionDTO

class RegistrarAtribucionHandler(RegistrarAtribucionBaseHandler):  
    def handle(self, comando: RegistrarAtribucion):
        atribucion_dto = comando.atribucion
        datos_evento_dict = atribucion_dto.to_dict() 
        usuario_id = atribucion_dto.identidad_usuario.id_usuario

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioJourney.__class__)
        journey: Journey = repositorio.obtener_por_usuario(usuario_id)
        if not journey:
            journey = self.fabrica_atribucion.crear_objeto(atribucion_dto, MapeadorAtribucion())
            repositorio.agregar(journey)
        
        if atribucion_dto.tipo == 'PURCHASE':
            conversion_obj = journey.registrar_conversion(datos_evento_dict)
            
            modelo_activo = ModeloAtribucion(tipo=TipoModeloAtribucion.LAST_TOUCH, activo=True)
            resultado_atribucion = modelo_activo.calcular_atribucion(journey, conversion_obj)
            despachador = DespachadorEventosAtribucion()
            despachador.publicar_evento_conversion_atribuida(resultado_atribucion, datos_evento_dict)
            
        else:
            journey.agregar_touchpoint(datos_evento_dict)

        UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, journey)
        UnidadTrabajoPuerto.commit()
@comando.register(RegistrarAtribucion)
def ejecutar_comando_registrar_atribucion(comando: RegistrarAtribucion):
    handler = RegistrarAtribucionHandler()
    handler.handle(comando)