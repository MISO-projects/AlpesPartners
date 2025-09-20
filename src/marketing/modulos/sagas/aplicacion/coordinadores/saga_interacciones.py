from marketing.seedwork.aplicacion.sagas import (
    CoordinadorCoreografia,
    Transaccion,
    Inicio,
    Fin,
)
from marketing.seedwork.aplicacion.comandos import Comando, ejecutar_commando
from marketing.seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass
import uuid
from datetime import datetime
from marketing.modulos.sagas.aplicacion.comandos.comisiones import RevertirComision
from marketing.modulos.sagas.aplicacion.comandos.atribucion import RevertirAtribucion
from marketing.modulos.sagas.aplicacion.comandos.tracking import DescartarInteracciones
from marketing.modulos.sagas.dominio.eventos.tracking import InteraccionRegistrada
from marketing.modulos.sagas.dominio.eventos.atribucion import ConversionAtribuida
from marketing.modulos.sagas.dominio.eventos.comisiones import ComisionReservada

from marketing.modulos.sagas.dominio.eventos.comisiones import (
    FraudeDetectado,
    ComisionRevertida,
)
from marketing.modulos.sagas.dominio.eventos.atribucion import AtribucionRevertida
from marketing.modulos.sagas.dominio.eventos.tracking import InteraccionesDescartadas
from marketing.modulos.sagas.dominio.entidades import SagaLog
from marketing.config.db import db
from marketing.modulos.sagas.infraestructura.fabricas import FabricaRepositorio
from marketing.modulos.sagas.dominio.repositorios import RepositorioSagaLog


@dataclass
class SagaLogEntry:
    """Entrada del log de saga para persistir el estado"""

    id_correlacion: uuid.UUID
    tipo_paso: str  # 'INICIO', 'EVENTO_NORMAL', 'COMPENSACION', 'FIN', 'ERROR'
    evento: str = None
    comando: str = None
    estado: str = None  # 'EXITOSO', 'FALLIDO', 'PROCESANDO'
    timestamp: datetime = None
    datos_adicionales: dict = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.datos_adicionales is None:
            self.datos_adicionales = {}


class CoordinadorInteracciones(CoordinadorCoreografia):
    """
    Coordinador de saga para el flujo de interacciones de marketing con compensación por fraude.

    Flujo normal:
    1. RegistrarInteraccion → InteraccionRegistrada
    2. RegistrarAtribucion → ConversionAtribuida
    3. ReservarComision → ComisionReservada

    Flujo de compensación (cuando se detecta fraude):
    1. FraudeDetectado → RevertirComision → ComisionRevertida
    2. ComisionRevertida → RevertirAtribucion → AtribucionRevertida
    3. AtribucionRevertida → DescartarInteracciones → InteraccionesDescartadas
    """

    def __init__(self, id_correlacion: uuid.UUID = None):
        self.id_correlacion = id_correlacion or uuid.uuid4()
        self.saga_log: list[SagaLogEntry] = []
        self.estado_actual = "INICIADO"
        self.fabrica_repositorio = FabricaRepositorio()
        self.repositorio_saga_log = self.fabrica_repositorio.crear_objeto(
            RepositorioSagaLog.__class__
        )
        self.inicializar_pasos()

        # Cargar logs existentes si la saga ya existe
        self._cargar_logs_existentes()

    def _cargar_logs_existentes(self):
        """Carga los logs existentes de la saga desde la base de datos"""
        try:
            logs_existentes = self.repositorio_saga_log.obtener_todos(
                self.id_correlacion
            )
            for log_entidad in logs_existentes:
                # Convertir la entidad SagaLog a SagaLogEntry para compatibilidad
                entrada = SagaLogEntry(
                    id_correlacion=log_entidad.id_correlacion,
                    tipo_paso=log_entidad.tipo_paso,
                    evento=log_entidad.evento,
                    comando=log_entidad.comando,
                    estado=log_entidad.estado,
                    timestamp=log_entidad.timestamp,
                    datos_adicionales=log_entidad.datos_adicionales,
                )
                self.saga_log.append(entrada)

            # Actualizar estado basado en logs existentes
            if self.saga_log:
                ultimo_log = self.saga_log[-1]
                if ultimo_log.tipo_paso == "FIN":
                    if ultimo_log.estado == "REVERTIDO":
                        self.estado_actual = "REVERTIDO"
                    else:
                        self.estado_actual = "COMPLETADO"
                elif any(log.tipo_paso == "COMPENSACION" for log in self.saga_log):
                    self.estado_actual = "COMPENSANDO"
                else:
                    self.estado_actual = "EN_PROGRESO"

        except Exception as e:
            print(f"Error cargando logs existentes: {e}")
            # Continuar con saga vacía si hay error

    def inicializar_pasos(self):
        """Mapeo simple: qué comando de compensación ejecutar para cada evento"""
        self.compensaciones = {
            FraudeDetectado: RevertirComision,
            ComisionRevertida: RevertirAtribucion,
            AtribucionRevertida: DescartarInteracciones,
        }

    def iniciar(self):
        """Inicia la saga registrando el paso inicial"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            tipo_paso="INICIO",
            estado="EXITOSO",
        )
        self.persistir_en_saga_log(entrada_log)
        self.estado_actual = "EN_PROGRESO"

    def terminar(self):
        """Termina la saga exitosamente"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            tipo_paso="FIN",
            estado="EXITOSO",
        )
        self.persistir_en_saga_log(entrada_log)
        self.estado_actual = "COMPLETADO"

    def terminar_con_compensacion(self):
        """Termina la saga después de completar todas las compensaciones"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            tipo_paso="FIN",
            estado="REVERTIDO",
        )
        self.persistir_en_saga_log(entrada_log)
        self.estado_actual = "REVERTIDO"

    def persistir_en_saga_log(self, entrada: SagaLogEntry):
        """Persiste una entrada en el log de saga"""
        # Agregar a memoria local
        self.saga_log.append(entrada)

        # Convertir a entidad de dominio
        saga_log_entidad = SagaLog(
            id=uuid.uuid4(),
            id_correlacion=entrada.id_correlacion,
            tipo_paso=entrada.tipo_paso,
            evento=entrada.evento or "",
            comando=entrada.comando or "",
            estado=entrada.estado,
            timestamp=entrada.timestamp,
            datos_adicionales=entrada.datos_adicionales,
        )

        try:
            # Persistir en base de datos
            self.repositorio_saga_log.agregar(saga_log_entidad)
            db.session.commit()

            print(
                f"SAGA LOG [{entrada.id_correlacion}]: {entrada.tipo_paso} - {entrada.evento or entrada.comando or 'N/A'} - {entrada.estado}"
            )
        except Exception as e:
            print(f"Error persistiendo saga log: {e}")
            db.session.rollback()
            # Re-lanzar la excepción para que el coordinador pueda manejarla
            raise

    def construir_comando(self, evento: EventoDominio, tipo_comando: type) -> Comando:
        """
        Construye un comando a partir de un evento de dominio.
        Mapea los atributos del evento a los parámetros del comando.
        """
        if tipo_comando == RevertirComision and isinstance(evento, FraudeDetectado):
            return RevertirComision(
                id_correlacion=evento.id_correlacion,
                journey_id=evento.journey_id,
                motivo="FRAUDE_DETECTADO",
            )

        elif tipo_comando == RevertirAtribucion and isinstance(
            evento, ComisionRevertida
        ):
            return RevertirAtribucion(
                id_correlacion=evento.id_correlacion, journey_id=evento.journey_id
            )

        elif tipo_comando == DescartarInteracciones and isinstance(
            evento, AtribucionRevertida
        ):
            return DescartarInteracciones(
                id_correlacion=evento.id_correlacion, interacciones=evento.interacciones
            )

        else:
            raise NotImplementedError(
                f"No se puede construir comando {tipo_comando.__name__} desde evento {type(evento).__name__}"
            )

    def procesar_evento(self, evento: EventoDominio):
        """
        Procesa eventos de dominio para avanzar la saga o ejecutar compensaciones.
        """
        try:
            # Procesar eventos del flujo normal
            if isinstance(evento, InteraccionRegistrada):
                self._registrar_evento_exitoso(evento, "EVENTO_NORMAL")
                print(f"✅ Interacción {evento.id_interaccion} registrada exitosamente")

            elif isinstance(evento, ConversionAtribuida):
                self._registrar_evento_exitoso(evento, "EVENTO_NORMAL")
                print(
                    f"✅ Conversión {evento.id_interaccion_atribuida} atribuida exitosamente"
                )

            elif isinstance(evento, ComisionReservada):
                self._registrar_evento_exitoso(evento, "EVENTO_NORMAL")
                print(
                    f"✅ Comisión reservada exitosamente para journey {evento.id_journey}"
                )

                # Si todos los pasos están completos, terminar saga
                if self._saga_completa():
                    self.terminar()

            # Procesar eventos de compensación
            elif isinstance(evento, FraudeDetectado):
                self._registrar_evento_compensacion(evento)
                print(
                    f"🚨 Fraude detectado para journey {evento.journey_id}, iniciando compensación..."
                )
                self._iniciar_compensacion(evento)

            elif isinstance(evento, ComisionRevertida):
                self._registrar_evento_compensacion(evento)
                print(f"↩️ Comisión revertida para journey {evento.journey_id}")
                self._continuar_compensacion(evento)

            elif isinstance(evento, AtribucionRevertida):
                self._registrar_evento_compensacion(evento)
                print(
                    f"↩️ Atribución revertida para journey {evento.journey_id_revertido}"
                )
                print(f"Interacciones: {evento.interacciones}")
                self._continuar_compensacion(evento)

            elif isinstance(evento, InteraccionesDescartadas):
                self._registrar_evento_compensacion(evento)
                print(
                    f"↩️ Interacciónes {evento.interacciones} descartadas, compensación completada"
                )
                self.terminar_con_compensacion()

            else:
                print(f"⚠️ Evento no reconocido: {type(evento).__name__}")

        except Exception as e:
            self._registrar_error(evento, str(e))
            print(f"❌ Error procesando evento {type(evento).__name__}: {e}")
            raise

    def _registrar_evento_exitoso(self, evento: EventoDominio, tipo_paso: str):
        """Registra un evento exitoso del flujo normal"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            tipo_paso=tipo_paso,
            evento=type(evento).__name__,
            estado="EXITOSO",
        )
        self.persistir_en_saga_log(entrada_log)

    def _registrar_evento_compensacion(self, evento: EventoDominio):
        """Registra un evento de compensación"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            tipo_paso="COMPENSACION",
            evento=type(evento).__name__,
            estado="EXITOSO",
        )
        self.persistir_en_saga_log(entrada_log)

    def _registrar_error(self, evento: EventoDominio, error: str):
        """Registra un error"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            tipo_paso="ERROR",
            evento=type(evento).__name__,
            estado="FALLIDO",
            datos_adicionales={"error": error},
        )
        self.persistir_en_saga_log(entrada_log)

    def _saga_completa(self) -> bool:
        """Verifica si todos los pasos de la saga normal están completos basándose en el log"""
        eventos_exitosos = {
            entrada.evento
            for entrada in self.saga_log
            if entrada.tipo_paso == "EVENTO_NORMAL" and entrada.estado == "EXITOSO"
        }

        eventos_requeridos = {
            "InteraccionRegistrada",
            "ConversionAtribuida",
            "ComisionReservada",
        }

        return eventos_requeridos.issubset(eventos_exitosos)

    def _iniciar_compensacion(self, evento: EventoDominio):
        """Inicia el proceso de compensación"""
        self.estado_actual = "COMPENSANDO"
        self._continuar_compensacion(evento)

    def _continuar_compensacion(self, evento: EventoDominio):
        """Continúa el proceso de compensación ejecutando el siguiente comando"""
        tipo_evento = type(evento)

        if tipo_evento in self.compensaciones:
            tipo_comando = self.compensaciones[tipo_evento]

            try:
                comando = self.construir_comando(evento, tipo_comando)

                # Registrar que vamos a ejecutar un comando de compensación
                entrada_log = SagaLogEntry(
                    id_correlacion=self.id_correlacion,
                    tipo_paso="COMPENSACION",
                    comando=type(comando).__name__,
                    estado="DESPACHADO",
                )
                self.persistir_en_saga_log(entrada_log)

                # Ejecutar comando de compensación
                self.publicar_comando(evento, tipo_comando)

            except Exception as e:
                self._registrar_error(evento, str(e))
                raise

    def obtener_estado_saga(self) -> dict:
        """Retorna el estado actual de la saga para monitoreo"""
        eventos_completados = [
            entrada.evento
            for entrada in self.saga_log
            if entrada.tipo_paso == "EVENTO_NORMAL" and entrada.estado == "EXITOSO"
        ]

        return {
            "id_correlacion": str(self.id_correlacion),
            "estado": self.estado_actual,
            "eventos_completados": eventos_completados,
            "log_entries": len(self.saga_log),
            "ultima_actividad": self.saga_log[-1].timestamp if self.saga_log else None,
        }


# Handler principal para eventos de dominio
def procesar_evento_saga(evento: EventoDominio, id_correlacion: uuid.UUID = None):
    """
    Función principal para procesar eventos de dominio en la saga de interacciones.
    """
    if not isinstance(evento, EventoDominio):
        raise ValueError("El mensaje debe ser un evento de dominio")

    coordinador = CoordinadorInteracciones(id_correlacion)

    try:
        coordinador.procesar_evento(evento)
        return coordinador.obtener_estado_saga()
    except Exception as e:
        print(f"Error procesando evento en saga: {e}")
        raise


# Función de utilidad para iniciar una nueva saga
def iniciar_saga_interacciones() -> uuid.UUID:
    """Inicia una nueva saga de interacciones y retorna su ID de correlación"""
    coordinador = CoordinadorInteracciones()
    coordinador.iniciar()
    return coordinador.id_correlacion
