
from comisiones.seedwork.aplicacion.comandos import Comando, ComandoHandler, ejecutar_commando as comando
from comisiones.modulos.comisiones.dominio.repositorios import RepositorioComision
from comisiones.modulos.comisiones.dominio.excepciones import ComisionNoEncontradaExcepcion
from comisiones.modulos.comisiones.infraestructura.fabricas import FabricaRepositorio
from comisiones.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from dataclasses import dataclass
import uuid

@dataclass
class ConfirmarComision(Comando):

    id_comision: uuid.UUID
    lote_confirmacion: str = ""
    referencia_pago: str = ""

@dataclass
class ConfirmarComisionesEnLote(Comando):

    limite_comisiones: int = 100
    lote_id: str = None

class ConfirmarComisionHandler(ComandoHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: ConfirmarComision):

        try:
            repositorio = self._fabrica_repositorio.crear_objeto(
                RepositorioComision.__class__
            )
            comision = repositorio.obtener_por_id(comando.id_comision)
            if not comision:
                raise ComisionNoEncontradaExcepcion(f"Comisión {comando.id_comision} no encontrada")
            comision.confirmar_comision(
                lote_confirmacion=comando.lote_confirmacion,
                referencia_pago=comando.referencia_pago
            )
            UnidadTrabajoPuerto.registrar_batch(repositorio.actualizar, comision)
            UnidadTrabajoPuerto.savepoint()
            UnidadTrabajoPuerto.commit()

            print(f"Comisión {comision.id} confirmada exitosamente")
            return comision

        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            print(f"Error confirmando comisión: {e}")
            raise e

class ConfirmarComisionesEnLoteHandler(ComandoHandler):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    def handle(self, comando: ConfirmarComisionesEnLote):

        try:
            from comisiones.modulos.comisiones.dominio.servicios import ServicioComision
            from comisiones.modulos.comisiones.dominio.repositorios import (
                RepositorioConfiguracionComision,
                RepositorioPoliticaFraude
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
            comisiones_confirmadas, lote_id = servicio_comision.confirmar_comisiones_en_lote(
                limite_comisiones=comando.limite_comisiones,
                lote_id=comando.lote_id
            )

            if comisiones_confirmadas:
                for comision in comisiones_confirmadas:
                    UnidadTrabajoPuerto.registrar_batch(repositorio_comision.actualizar, comision)

                UnidadTrabajoPuerto.savepoint()
                UnidadTrabajoPuerto.commit()

                print(f"Lote {lote_id}: {len(comisiones_confirmadas)} comisiones confirmadas exitosamente")
                return {
                    "lote_id": lote_id,
                    "cantidad_confirmadas": len(comisiones_confirmadas),
                    "comisiones": comisiones_confirmadas
                }
            else:
                print("No hay comisiones reservadas para confirmar")
                return {
                    "lote_id": "",
                    "cantidad_confirmadas": 0,
                    "comisiones": []
                }

        except Exception as e:
            UnidadTrabajoPuerto.rollback()
            print(f"Error confirmando comisiones en lote: {e}")
            raise e

@comando.register(ConfirmarComision)
def ejecutar_comando_individual(comando: ConfirmarComision):
    handler = ConfirmarComisionHandler()
    return handler.handle(comando)

@comando.register(ConfirmarComisionesEnLote)
def ejecutar_comando_lote(comando: ConfirmarComisionesEnLote):
    handler = ConfirmarComisionesEnLoteHandler()
    return handler.handle(comando)
