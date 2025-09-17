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
from marketing.modulos.sagas.aplicacion.comandos.comisiones import (
    ReservarComision,
    RevertirComision,
)
from marketing.modulos.sagas.aplicacion.comandos.atribucion import (
    RegistrarAtribucion,
    RevertirAtribucion,
)
from marketing.modulos.sagas.aplicacion.comandos.tracking import (
    RegistrarInteraccion,
    DescartarInteraccion,
)
from marketing.modulos.sagas.dominio.eventos.tracking import InteraccionRegistrada
from marketing.modulos.sagas.dominio.eventos.atribucion import ConversionAtribuida
from marketing.modulos.sagas.dominio.eventos.comisiones import ComisionReservada

from marketing.modulos.sagas.dominio.eventos.comisiones import (
    FraudeDetectado,
    ComisionRevertida,
)
from marketing.modulos.sagas.dominio.eventos.atribucion import AtribucionRevertida
from marketing.modulos.sagas.dominio.eventos.tracking import InteraccionDescartada


@dataclass
class SagaLogEntry:
    """Entrada del log de saga para persistir el estado"""

    id_correlacion: uuid.UUID
    paso_index: int
    tipo_paso: str  # 'INICIO', 'TRANSACCION', 'COMPENSACION', 'FIN'
    comando: str = None
    evento: str = None
    estado: str = None  # 'PENDIENTE', 'EXITOSO', 'FALLIDO'
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
    3. AtribucionRevertida → DescartarInteraccion → InteraccionDescartada
    """

    def __init__(self, id_correlacion: uuid.UUID = None):
        self.id_correlacion = id_correlacion or uuid.uuid4()
        self.saga_log: list[SagaLogEntry] = []
        self.estado_actual = "INICIADO"
        self.inicializar_pasos()

    def inicializar_pasos(self):
        """Define los pasos de la saga con sus comandos, eventos y compensaciones"""
        self.pasos = [
            Inicio(index=0),
            Transaccion(
                index=1,
                comando=RegistrarInteraccion,
                evento=InteraccionRegistrada,
                error=None,  # En coreografía no manejamos errores directamente aquí
                compensacion=DescartarInteraccion,
                exitosa=False,
            ),
            Transaccion(
                index=2,
                comando=RegistrarAtribucion,
                evento=ConversionAtribuida,
                error=None,
                compensacion=RevertirAtribucion,
                exitosa=False,
            ),
            Transaccion(
                index=3,
                comando=ReservarComision,
                evento=ComisionReservada,
                error=None,
                compensacion=RevertirComision,
                exitosa=False,
            ),
            Fin(index=4),
        ]

        # Mapeo de eventos de compensación para el flujo reverso
        self.eventos_compensacion = {
            FraudeDetectado: 3,  # Empezar compensación desde el paso 3 (ReservarComision)
            ComisionRevertida: 2,  # Continuar con paso 2 (RegistrarAtribucion)
            AtribucionRevertida: 1,  # Continuar con paso 1 (RegistrarInteraccion)
            InteraccionDescartada: 0,  # Terminar compensación
        }

    def iniciar(self):
        """Inicia la saga registrando el paso inicial"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            paso_index=0,
            tipo_paso="INICIO",
            estado="EXITOSO",
        )
        self.persistir_en_saga_log(entrada_log)
        self.estado_actual = "EN_PROGRESO"

    def terminar(self):
        """Termina la saga exitosamente"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            paso_index=len(self.pasos) - 1,
            tipo_paso="FIN",
            estado="EXITOSO",
        )
        self.persistir_en_saga_log(entrada_log)
        self.estado_actual = "COMPLETADO"

    def terminar_con_compensacion(self):
        """Termina la saga después de completar todas las compensaciones"""
        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            paso_index=-1,
            tipo_paso="COMPENSACION_COMPLETADA",
            estado="REVERTIDO",
        )
        self.persistir_en_saga_log(entrada_log)
        self.estado_actual = "REVERTIDO"

    def persistir_en_saga_log(self, entrada: SagaLogEntry):
        """Persiste una entrada en el log de saga"""
        self.saga_log.append(entrada)
        # TODO: Implementar persistencia real en base de datos
        print(
            f"SAGA LOG [{entrada.id_correlacion}]: {entrada.tipo_paso} - {entrada.estado} - Paso {entrada.paso_index}"
        )

    def construir_comando(self, evento: EventoDominio, tipo_comando: type) -> Comando:
        """
        Construye un comando a partir de un evento de dominio.
        Mapea los atributos del evento a los parámetros del comando.
        """
        if tipo_comando == RevertirComision and isinstance(evento, FraudeDetectado):
            return RevertirComision(id_interaccion=evento.id_interaccion)

        elif tipo_comando == RevertirAtribucion and isinstance(
            evento, ComisionRevertida
        ):
            return RevertirAtribucion(id_interaccion=evento.id_interaccion)

        elif tipo_comando == DescartarInteraccion and isinstance(
            evento, AtribucionRevertida
        ):
            return DescartarInteraccion(id_interaccion=evento.id_interaccion)

        else:
            raise NotImplementedError(
                f"No se puede construir comando {tipo_comando.__name__} desde evento {type(evento).__name__}"
            )

    def procesar_evento(self, evento: EventoDominio):
        """
        Procesa eventos de dominio para avanzar la saga o ejecutar compensaciones.

        En coreografía, los eventos llegan de forma asíncrona y el coordinador
        debe determinar qué acción tomar basándose en el tipo de evento.
        """
        try:
            # Registrar el evento recibido
            entrada_log = SagaLogEntry(
                id_correlacion=self.id_correlacion,
                paso_index=-1,
                tipo_paso="EVENTO_RECIBIDO",
                evento=type(evento).__name__,
                estado="PROCESANDO",
                datos_adicionales={"evento_data": str(evento)},
            )
            self.persistir_en_saga_log(entrada_log)

            # Procesar eventos del flujo normal
            if isinstance(evento, InteraccionRegistrada):
                self._marcar_transaccion_exitosa(1)
                print(f"✅ Interacción {evento.id_interaccion} registrada exitosamente")

            elif isinstance(evento, ConversionAtribuida):
                self._marcar_transaccion_exitosa(2)
                print(
                    f"✅ Conversión {evento.id_interaccion_atribuida} atribuida exitosamente"
                )

            elif isinstance(evento, ComisionReservada):
                self._marcar_transaccion_exitosa(3)
                print(
                    f"✅ Comisión reservada exitosamente para interacción {evento.id_interaccion}"
                )
                # Si todas las transacciones están completas, terminar saga
                if self._todas_transacciones_exitosas():
                    self.terminar()

            # Procesar eventos de compensación
            elif isinstance(evento, FraudeDetectado):
                print(
                    f"🚨 Fraude detectado para interacción {evento.id_interaccion}, iniciando compensación..."
                )
                self._iniciar_compensacion(evento)

            elif isinstance(evento, ComisionRevertida):
                print(f"↩️ Comisión revertida para interacción {evento.id_interaccion}")
                self._continuar_compensacion(evento)

            elif isinstance(evento, AtribucionRevertida):
                print(
                    f"↩️ Atribución revertida para interacción {evento.id_interaccion}"
                )
                self._continuar_compensacion(evento)

            elif isinstance(evento, InteraccionDescartada):
                print(
                    f"↩️ Interacción {evento.id_interaccion} descartada, compensación completada"
                )
                self.terminar_con_compensacion()

            else:
                print(f"⚠️ Evento no reconocido: {type(evento).__name__}")

        except Exception as e:
            entrada_log = SagaLogEntry(
                id_correlacion=self.id_correlacion,
                paso_index=-1,
                tipo_paso="ERROR",
                estado="FALLIDO",
                datos_adicionales={"error": str(e)},
            )
            self.persistir_en_saga_log(entrada_log)
            print(f"❌ Error procesando evento {type(evento).__name__}: {e}")
            raise

    def _marcar_transaccion_exitosa(self, index: int):
        """Marca una transacción como exitosa"""
        if index < len(self.pasos) and isinstance(self.pasos[index], Transaccion):
            self.pasos[index].exitosa = True

            entrada_log = SagaLogEntry(
                id_correlacion=self.id_correlacion,
                paso_index=index,
                tipo_paso="TRANSACCION",
                estado="EXITOSO",
            )
            self.persistir_en_saga_log(entrada_log)

    def _todas_transacciones_exitosas(self) -> bool:
        """Verifica si todas las transacciones han sido completadas exitosamente"""
        for paso in self.pasos:
            if isinstance(paso, Transaccion) and not paso.exitosa:
                return False
        return True

    def _iniciar_compensacion(self, evento: EventoDominio):
        """Inicia el proceso de compensación"""
        self.estado_actual = "COMPENSANDO"

        entrada_log = SagaLogEntry(
            id_correlacion=self.id_correlacion,
            paso_index=-1,
            tipo_paso="INICIO_COMPENSACION",
            estado="INICIADO",
            datos_adicionales={"trigger_evento": type(evento).__name__},
        )
        self.persistir_en_saga_log(entrada_log)

        # Comenzar compensación desde el último paso completado
        self._continuar_compensacion(evento)

    def _continuar_compensacion(self, evento: EventoDominio):
        """Continúa el proceso de compensación ejecutando el siguiente comando"""
        tipo_evento = type(evento)

        if tipo_evento in self.eventos_compensacion:
            paso_index = self.eventos_compensacion[tipo_evento]

            if paso_index > 0:  # Hay más pasos para compensar
                paso = self.pasos[paso_index]
                if isinstance(paso, Transaccion):
                    try:
                        comando = self.construir_comando(evento, paso.compensacion)

                        entrada_log = SagaLogEntry(
                            id_correlacion=self.id_correlacion,
                            paso_index=paso_index,
                            tipo_paso="COMPENSACION",
                            comando=type(comando).__name__,
                            estado="EJECUTANDO",
                        )
                        self.persistir_en_saga_log(entrada_log)

                        # Ejecutar comando de compensación
                        self.publicar_comando(evento, paso.compensacion)

                    except Exception as e:
                        entrada_log = SagaLogEntry(
                            id_correlacion=self.id_correlacion,
                            paso_index=paso_index,
                            tipo_paso="COMPENSACION",
                            estado="FALLIDO",
                            datos_adicionales={"error": str(e)},
                        )
                        self.persistir_en_saga_log(entrada_log)
                        raise
            else:
                # No hay más pasos para compensar, terminar
                self.terminar_con_compensacion()

    def obtener_estado_saga(self) -> dict:
        """Retorna el estado actual de la saga para monitoreo"""
        return {
            "id_correlacion": str(self.id_correlacion),
            "estado": self.estado_actual,
            "pasos_completados": len(
                [p for p in self.pasos if isinstance(p, Transaccion) and p.exitosa]
            ),
            "total_pasos": len([p for p in self.pasos if isinstance(p, Transaccion)]),
            "log_entries": len(self.saga_log),
            "ultima_actividad": self.saga_log[-1].timestamp if self.saga_log else None,
        }


# Handler principal para eventos de dominio
def procesar_evento_saga(evento: EventoDominio, id_correlacion: uuid.UUID = None):
    """
    Función principal para procesar eventos de dominio en la saga de interacciones.

    Esta función actúa como punto de entrada para todos los eventos relacionados
    con el flujo de interacciones de marketing.
    """
    if not isinstance(evento, EventoDominio):
        raise ValueError("El mensaje debe ser un evento de dominio")

    # Crear o recuperar coordinador basado en el ID de correlación
    # En una implementación real, recuperaríamos el estado desde la base de datos
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
