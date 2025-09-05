from alpespartners.seedwork.aplicacion.handlers import Handler
from alpespartners.modulos.marketing.infraestructura.despachadores import DespachadorMarketing
from alpespartners.modulos.marketing.dominio.repositorios import RepositorioCampania
from alpespartners.modulos.marketing.infraestructura.fabricas import FabricaRepositorio
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto


class HandlerCampaniaIntegracion(Handler):

    @staticmethod
    def handle_campania_creada(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_campania_creada(evento)
        print(f" Evento CampaniaCreada publicado vía Pulsar: {evento.nombre}")

    @staticmethod  
    def handle_campania_activada(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_campania_activada(evento)
        print(f" Evento CampaniaActivada publicado vía Pulsar: {evento.nombre}")

    @staticmethod
    def handle_campania_desactivada(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_campania_desactivada(evento)
        print(f" Evento CampaniaDesactivada publicado vía Pulsar: {evento.razon}")

    @staticmethod
    def handle_interaccion_recibida(evento):
        despachador = DespachadorMarketing()
        despachador.publicar_interaccion_recibida(evento)
        print(f" Evento InteraccionRecibida publicado vía Pulsar para campaña: {evento.id_campania}")


class HandlerInteraccionTrackingRecibida(Handler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        
    def handle(self, evento_tracking):
        try:
            print(f" Procesando evento de tracking en Marketing...")
            print(f"   Tipo: {evento_tracking.data.tipo}")
            print(f"   Parámetros: {evento_tracking.data.parametros_tracking}")
            
            repositorio = self._fabrica_repositorio.crear_objeto(RepositorioCampania)
            
            parametros = evento_tracking.data.parametros_tracking
            campania_nombre = parametros.campania if hasattr(parametros, 'campania') else None
            
            if campania_nombre:
                campania = repositorio.obtener_por_nombre(campania_nombre)
                if campania:
                    campania.procesar_interaccion(evento_tracking.data)
                    
                    UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, campania)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                    
                    print(f" Interacción procesada para campaña: {campania.nombre}")
                    print(f"   Nuevas métricas: {campania.metricas}")
                else:
                    print(f" No se encontró campaña activa con nombre: {campania_nombre}")
            else:
                campanias_activas = repositorio.obtener_activas()
                if campanias_activas:
                    campania = campanias_activas[0]
                    campania.procesar_interaccion(evento_tracking.data)
                    
                    UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, campania)
                    UnidadTrabajoPuerto.savepoint()
                    UnidadTrabajoPuerto.commit()
                    
                    print(f" Interacción asociada a campaña por defecto: {campania.nombre}")
                else:
                    print(" No hay campañas activas para procesar la interacción")
                    
        except Exception as e:
            print(f" Error procesando interacción en Marketing: {e}")
            UnidadTrabajoPuerto.rollback()
            raise e


class HandlerComandoCrearCampania(Handler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        
    def handle(self, comando_data):
        try:
            from alpespartners.modulos.marketing.dominio.entidades import Campania
            from alpespartners.modulos.marketing.dominio.objetos_valor import (
                SegmentoAudiencia, ConfiguracionCampania, MetricasCampania
            )
            from datetime import datetime
            
            campania = Campania(
                nombre=comando_data.data.nombre,
                descripcion=comando_data.data.descripcion,
                fecha_inicio=datetime.fromtimestamp(comando_data.data.fecha_inicio / 1000),
                fecha_fin=datetime.fromtimestamp(comando_data.data.fecha_fin / 1000),
                tipo=comando_data.data.tipo,
                segmento=SegmentoAudiencia(),
                configuracion=ConfiguracionCampania(),
                metricas=MetricasCampania()
            )
            
            campania.crear_campania()
            
            repositorio = self._fabrica_repositorio.crear_objeto(RepositorioCampania)
            UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, campania)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()
            
            print(f" Campaña creada exitosamente vía comando: {campania.nombre}")
            
        except Exception as e:
            print(f" Error creando campaña via comando: {e}")
            UnidadTrabajoPuerto.rollback()
            raise e
