
from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.repositorios import Mapeador
from alpespartners.modulos.comisiones.dominio.entidades import Comision
from alpespartners.modulos.comisiones.dominio.objetos_valor import (
    MontoComision,
    ConfiguracionComision,
    PoliticaFraude,
    InteraccionAtribuida,
    DetallesReserva,
    DetallesConfirmacion,
    TipoComision,
    TipoPoliticaFraude,
    EstadoComision
)
from alpespartners.modulos.comisiones.aplicacion.dto import (
    ComisionDTO,
    MontoComisionDTO,
    ConfiguracionComisionDTO,
    PoliticaFraudeDTO,
    InteraccionAtribuidaDTO,
    DetallesReservaDTO,
    DetallesConfirmacionDTO
)

class MapeadorComision(AppMap):

    def obtener_tipo(self) -> type:
        return Comision.__class__

    def entidad_a_dto(self, entidad: Comision) -> ComisionDTO:

        configuracion_dto = None
        if entidad.configuracion:
            configuracion_dto = self._configuracion_a_dto(entidad.configuracion)

        politica_fraude_dto = None
        if entidad.politica_fraude_aplicada:
            politica_fraude_dto = self._politica_fraude_a_dto(entidad.politica_fraude_aplicada)

        return ComisionDTO(
            id=entidad.id,
            id_interaccion=entidad.id_interaccion,
            id_campania=entidad.id_campania,
            monto=self._monto_a_dto(entidad.monto),
            estado=entidad.estado.value,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            configuracion=configuracion_dto,
            fecha_vencimiento=entidad.fecha_vencimiento,
            politica_fraude_aplicada=politica_fraude_dto
        )

    def dto_a_entidad(self, dto: ComisionDTO) -> Comision:

        configuracion = None
        if dto.configuracion:
            configuracion = self._dto_a_configuracion(dto.configuracion)

        politica_fraude = None
        if dto.politica_fraude_aplicada:
            politica_fraude = self._dto_a_politica_fraude(dto.politica_fraude_aplicada)

        comision = Comision(
            id=dto.id,
            id_interaccion=dto.id_interaccion,
            id_campania=dto.id_campania,
            monto=self._dto_a_monto(dto.monto),
            estado=EstadoComision(dto.estado),
            configuracion=configuracion,
            fecha_vencimiento=dto.fecha_vencimiento,
            politica_fraude_aplicada=politica_fraude,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )

        return comision

    def _monto_a_dto(self, monto: MontoComision) -> MontoComisionDTO:

        if not monto:
            return None
        return MontoComisionDTO(
            valor=monto.valor,
            moneda=monto.moneda
        )

    def _dto_a_monto(self, dto: MontoComisionDTO) -> MontoComision:

        if not dto:
            return None
        return MontoComision(
            valor=dto.valor,
            moneda=dto.moneda
        )

    def _configuracion_a_dto(self, configuracion: ConfiguracionComision) -> ConfiguracionComisionDTO:

        monto_fijo_dto = None
        if configuracion.monto_fijo:
            monto_fijo_dto = self._monto_a_dto(configuracion.monto_fijo)

        minimo_dto = None
        if configuracion.minimo:
            minimo_dto = self._monto_a_dto(configuracion.minimo)

        maximo_dto = None
        if configuracion.maximo:
            maximo_dto = self._monto_a_dto(configuracion.maximo)

        return ConfiguracionComisionDTO(
            tipo=configuracion.tipo.value,
            porcentaje=configuracion.porcentaje,
            monto_fijo=monto_fijo_dto,
            escalones=configuracion.escalones,
            minimo=minimo_dto,
            maximo=maximo_dto
        )

    def _dto_a_configuracion(self, dto: ConfiguracionComisionDTO) -> ConfiguracionComision:

        monto_fijo = None
        if dto.monto_fijo:
            monto_fijo = self._dto_a_monto(dto.monto_fijo)

        minimo = None
        if dto.minimo:
            minimo = self._dto_a_monto(dto.minimo)

        maximo = None
        if dto.maximo:
            maximo = self._dto_a_monto(dto.maximo)

        return ConfiguracionComision(
            tipo=TipoComision(dto.tipo),
            porcentaje=dto.porcentaje,
            monto_fijo=monto_fijo,
            escalones=dto.escalones,
            minimo=minimo,
            maximo=maximo
        )

    def _politica_fraude_a_dto(self, politica: PoliticaFraude) -> PoliticaFraudeDTO:

        return PoliticaFraudeDTO(
            tipo=politica.tipo.value,
            threshold_score=politica.threshold_score,
            requiere_revision_manual=politica.requiere_revision_manual,
            tiempo_espera_minutos=politica.tiempo_espera_minutos
        )

    def _dto_a_politica_fraude(self, dto: PoliticaFraudeDTO) -> PoliticaFraude:

        return PoliticaFraude(
            tipo=TipoPoliticaFraude(dto.tipo),
            threshold_score=dto.threshold_score,
            requiere_revision_manual=dto.requiere_revision_manual,
            tiempo_espera_minutos=dto.tiempo_espera_minutos
        )

class MapeadorInteraccionAtribuida(AppMap):

    def obtener_tipo(self) -> type:
        return InteraccionAtribuida.__class__

    def entidad_a_dto(self, entidad: InteraccionAtribuida) -> InteraccionAtribuidaDTO:

        return InteraccionAtribuidaDTO(
            id_interaccion=entidad.id_interaccion,
            id_campania=entidad.id_campania,
            tipo_interaccion=entidad.tipo_interaccion,
            valor_interaccion=MontoComisionDTO(
                valor=entidad.valor_interaccion.valor,
                moneda=entidad.valor_interaccion.moneda
            ),
            fraud_ok=entidad.fraud_ok,
            score_fraude=entidad.score_fraude,
            timestamp=entidad.timestamp,
            parametros_adicionales=entidad.parametros_adicionales
        )

    def dto_a_entidad(self, dto: InteraccionAtribuidaDTO) -> InteraccionAtribuida:

        return InteraccionAtribuida(
            id_interaccion=dto.id_interaccion,
            id_campania=dto.id_campania,
            tipo_interaccion=dto.tipo_interaccion,
            valor_interaccion=MontoComision(
                valor=dto.valor_interaccion.valor,
                moneda=dto.valor_interaccion.moneda
            ),
            fraud_ok=dto.fraud_ok,
            score_fraude=dto.score_fraude,
            timestamp=dto.timestamp,
            parametros_adicionales=dto.parametros_adicionales
        )
