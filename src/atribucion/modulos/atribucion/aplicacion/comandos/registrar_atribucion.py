# src/attribution/modulos/attribution/aplicacion/comandos/registrar_atribucion.py
import uuid
from dataclasses import dataclass, field
from atribucion.seedwork.aplicacion.comandos import Comando, ejecutar_commando as comando
from atribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from atribucion.modulos.atribucion.aplicacion.dto import AtribucionDTO
from atribucion.modulos.atribucion.dominio.entidades import Journey, ModeloAtribucion, TipoModeloAtribucion
from atribucion.modulos.atribucion.dominio.repositorios import RepositorioJourney
from atribucion.modulos.atribucion.infraestructura.despachadores import DespachadorEventosAtribucion
from atribucion.modulos.atribucion.aplicacion.mapeadores import MapeadorAtribucion
from .base import RegistrarAtribucionBaseHandler

@dataclass
class RegistrarAtribucion(Comando): 
    atribucion_dto: AtribucionDTO
    datos_evento_dict: dict = field(default_factory=dict)

class RegistrarAtribucionHandler(RegistrarAtribucionBaseHandler):  
    def handle(self, comando: RegistrarAtribucion):
        print("HANDLER: Ejecutando RegistrarAtribucionHandler...")
        
        atribucion_dto = comando.atribucion_dto
        datos_evento_dict = comando.datos_evento_dict
        usuario_id = atribucion_dto.identidad_usuario.id_usuario
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioJourney.__class__)
        journey: Journey = repositorio.obtener_por_usuario(usuario_id)
        is_new_journey = journey is None
        
        if is_new_journey:
            print(f"HANDLER: No se encontró Journey, creando uno nuevo para el usuario {usuario_id}")
            journey = self.fabrica_atribucion.crear_objeto(atribucion_dto, MapeadorAtribucion())
        
        if atribucion_dto.tipo == 'PURCHASE':
            print(f"HANDLER: Interacción de COMPRA detectada. Calculando atribución...")
            if not is_new_journey:
                journey.agregar_touchpoint(datos_evento_dict)
            conversion_obj = journey.registrar_conversion(datos_evento_dict)
            
            modelo_activo = ModeloAtribucion(nombre="Last Touch Activo", tipo=TipoModeloAtribucion.LAST_TOUCH, activo=True)
            resultado_atribucion = modelo_activo.calcular_atribucion(journey, conversion_obj)
            despachador = DespachadorEventosAtribucion()
            despachador.publicar_evento_conversion_atribuida(journey, resultado_atribucion, datos_evento_dict)
            
        elif not is_new_journey:
            print(f"HANDLER: Interacción de tipo '{atribucion_dto.tipo}' detectada. Agregando touchpoint...")
            journey.agregar_touchpoint(datos_evento_dict)
        
        if is_new_journey:
            UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, journey)
        else:
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, journey)
        
        print("HANDLER: Realizando commit en la Unidad de Trabajo...")
        UnidadTrabajoPuerto.commit()
        print("HANDLER: Commit realizado. Proceso terminado.")


@comando.register(RegistrarAtribucion)
def ejecutar_comando_registrar_atribucion(comando: RegistrarAtribucion):
    handler = RegistrarAtribucionHandler()
    handler.handle(comando)