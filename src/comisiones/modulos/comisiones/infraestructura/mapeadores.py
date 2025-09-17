
from comisiones.seedwork.dominio.repositorios import Mapeador
from comisiones.modulos.comisiones.dominio.entidades import Comision
from comisiones.modulos.comisiones.dominio.objetos_valor import (
    MontoComision,
    ConfiguracionComision,
    PoliticaFraude,
    DetallesReserva,
    DetallesConfirmacion,
    EstadoComision,
    TipoComision,
    TipoPoliticaFraude
)
from comisiones.modulos.comisiones.infraestructura.dto import (
    ComisionDbDto,
    ConfiguracionComisionDbDto,
    PoliticaFraudeDbDto
)
from datetime import datetime
from decimal import Decimal
import uuid
import json

class MapeadorComisionSQLite(Mapeador):

    def obtener_tipo(self) -> type:
        return ComisionDbDto

    def entidad_a_dto(self, entidad: Comision) -> ComisionDbDto:
        configuracion_json = None
        if entidad.configuracion:
            configuracion_json = {
                "tipo": entidad.configuracion.tipo.value,
                "porcentaje": str(entidad.configuracion.porcentaje) if entidad.configuracion.porcentaje else None,
                "monto_fijo": {
                    "valor": str(entidad.configuracion.monto_fijo.valor),
                    "moneda": entidad.configuracion.monto_fijo.moneda
                } if entidad.configuracion.monto_fijo else None,
                "escalones": entidad.configuracion.escalones,
                "minimo": {
                    "valor": str(entidad.configuracion.minimo.valor),
                    "moneda": entidad.configuracion.minimo.moneda
                } if entidad.configuracion.minimo else None,
                "maximo": {
                    "valor": str(entidad.configuracion.maximo.valor),
                    "moneda": entidad.configuracion.maximo.moneda
                } if entidad.configuracion.maximo else None
            }
        politica_fraude_json = None
        if entidad.politica_fraude_aplicada:
            politica_fraude_json = {
                "tipo": entidad.politica_fraude_aplicada.tipo.value,
                "threshold_score": entidad.politica_fraude_aplicada.threshold_score,
                "requiere_revision_manual": entidad.politica_fraude_aplicada.requiere_revision_manual,
                "tiempo_espera_minutos": entidad.politica_fraude_aplicada.tiempo_espera_minutos
            }
        detalles_reserva_json = None
        if entidad.detalles_reserva:
            detalles_reserva_json = {
                "id_comision": str(entidad.detalles_reserva.id_comision),
                "monto_reservado": {
                    "valor": str(entidad.detalles_reserva.monto_reservado.valor),
                    "moneda": entidad.detalles_reserva.monto_reservado.moneda
                },
                "fecha_reserva": entidad.detalles_reserva.fecha_reserva.isoformat(),
                "referencia_interaccion": str(entidad.detalles_reserva.referencia_interaccion),
                "motivo": entidad.detalles_reserva.motivo,
                "metadata": entidad.detalles_reserva.metadata
            }
        detalles_confirmacion_json = None
        if entidad.detalles_confirmacion:
            detalles_confirmacion_json = {
                "fecha_confirmacion": entidad.detalles_confirmacion.fecha_confirmacion.isoformat(),
                "monto_confirmado": {
                    "valor": str(entidad.detalles_confirmacion.monto_confirmado.valor),
                    "moneda": entidad.detalles_confirmacion.monto_confirmado.moneda
                },
                "lote_confirmacion": entidad.detalles_confirmacion.lote_confirmacion,
                "referencia_pago": entidad.detalles_confirmacion.referencia_pago,
                "metadata": entidad.detalles_confirmacion.metadata
            }

        return ComisionDbDto(
            id=str(entidad.id),
            id_interaccion=entidad.id_interaccion,
            id_campania=entidad.id_campania,
            monto_valor=entidad.monto.valor,
            monto_moneda=entidad.monto.moneda,
            estado=entidad.estado.value,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            fecha_vencimiento=entidad.fecha_vencimiento,
            configuracion=configuracion_json,
            politica_fraude=politica_fraude_json,
            detalles_reserva=detalles_reserva_json,
            detalles_confirmacion=detalles_confirmacion_json
        )

    def dto_a_entidad(self, dto: ComisionDbDto) -> Comision:
        configuracion = None
        if dto.configuracion:
            config_data = dto.configuracion
            
            monto_fijo = None
            if config_data.get("monto_fijo"):
                monto_fijo = MontoComision(
                    valor=Decimal(config_data["monto_fijo"]["valor"]),
                    moneda=config_data["monto_fijo"]["moneda"]
                )
            
            minimo = None
            if config_data.get("minimo"):
                minimo = MontoComision(
                    valor=Decimal(config_data["minimo"]["valor"]),
                    moneda=config_data["minimo"]["moneda"]
                )
            
            maximo = None
            if config_data.get("maximo"):
                maximo = MontoComision(
                    valor=Decimal(config_data["maximo"]["valor"]),
                    moneda=config_data["maximo"]["moneda"]
                )
            
            configuracion = ConfiguracionComision(
                tipo=TipoComision(config_data["tipo"]),
                porcentaje=Decimal(config_data["porcentaje"]) if config_data.get("porcentaje") else Decimal('0'),
                monto_fijo=monto_fijo,
                escalones=config_data.get("escalones", []),
                minimo=minimo,
                maximo=maximo
            )
        politica_fraude = None
        if dto.politica_fraude:
            pf_data = dto.politica_fraude
            politica_fraude = PoliticaFraude(
                tipo=TipoPoliticaFraude(pf_data["tipo"]),
                threshold_score=pf_data["threshold_score"],
                requiere_revision_manual=pf_data["requiere_revision_manual"],
                tiempo_espera_minutos=pf_data["tiempo_espera_minutos"]
            )
        detalles_reserva = None
        if dto.detalles_reserva:
            dr_data = dto.detalles_reserva
            detalles_reserva = DetallesReserva(
                id_comision=uuid.UUID(dr_data["id_comision"]),
                monto_reservado=MontoComision(
                    valor=Decimal(dr_data["monto_reservado"]["valor"]),
                    moneda=dr_data["monto_reservado"]["moneda"]
                ),
                fecha_reserva=datetime.fromisoformat(dr_data["fecha_reserva"]),
                referencia_interaccion=uuid.UUID(dr_data["referencia_interaccion"]),
                motivo=dr_data["motivo"],
                metadata=dr_data["metadata"]
            )
        detalles_confirmacion = None
        if dto.detalles_confirmacion:
            dc_data = dto.detalles_confirmacion
            detalles_confirmacion = DetallesConfirmacion(
                fecha_confirmacion=datetime.fromisoformat(dc_data["fecha_confirmacion"]),
                monto_confirmado=MontoComision(
                    valor=Decimal(dc_data["monto_confirmado"]["valor"]),
                    moneda=dc_data["monto_confirmado"]["moneda"]
                ),
                lote_confirmacion=dc_data["lote_confirmacion"],
                referencia_pago=dc_data["referencia_pago"],
                metadata=dc_data["metadata"]
            )

        comision = Comision(
            id=uuid.UUID(dto.id),
            id_interaccion=dto.id_interaccion,
            id_campania=dto.id_campania,
            monto=MontoComision(valor=dto.monto_valor, moneda=dto.monto_moneda),
            estado=EstadoComision(dto.estado),
            configuracion=configuracion,
            detalles_reserva=detalles_reserva,
            detalles_confirmacion=detalles_confirmacion,
            fecha_vencimiento=dto.fecha_vencimiento,
            politica_fraude_aplicada=politica_fraude,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )

        return comision

class MapeadorComisionMongoDB(Mapeador):

    def obtener_tipo(self) -> type:
        return Comision.__class__

    def entidad_a_dto(self, entidad: Comision) -> dict:

        documento = {
            "_id": str(entidad.id),
            "id_interaccion": entidad.id_interaccion,
            "id_campania": entidad.id_campania,
            "monto": {
                "valor": str(entidad.monto.valor),
                "moneda": entidad.monto.moneda
            },
            "estado": entidad.estado.value,
            "fecha_creacion": entidad.fecha_creacion,
            "fecha_actualizacion": entidad.fecha_actualizacion,
            "fecha_vencimiento": entidad.fecha_vencimiento
        }
        if entidad.configuracion:
            documento["configuracion"] = {
                "tipo": entidad.configuracion.tipo.value,
                "porcentaje": str(entidad.configuracion.porcentaje) if entidad.configuracion.porcentaje else None,
                "monto_fijo": {
                    "valor": str(entidad.configuracion.monto_fijo.valor),
                    "moneda": entidad.configuracion.monto_fijo.moneda
                } if entidad.configuracion.monto_fijo else None,
                "escalones": entidad.configuracion.escalones,
                "minimo": {
                    "valor": str(entidad.configuracion.minimo.valor),
                    "moneda": entidad.configuracion.minimo.moneda
                } if entidad.configuracion.minimo else None,
                "maximo": {
                    "valor": str(entidad.configuracion.maximo.valor),
                    "moneda": entidad.configuracion.maximo.moneda
                } if entidad.configuracion.maximo else None
            }


        return documento

    def dto_a_entidad(self, documento: dict) -> Comision:
        configuracion = None
        if documento.get("configuracion"):
            config_data = documento["configuracion"]
            
            monto_fijo = None
            if config_data.get("monto_fijo"):
                monto_fijo = MontoComision(
                    valor=Decimal(config_data["monto_fijo"]["valor"]),
                    moneda=config_data["monto_fijo"]["moneda"]
                )
            
            configuracion = ConfiguracionComision(
                tipo=TipoComision(config_data["tipo"]),
                porcentaje=Decimal(config_data["porcentaje"]) if config_data.get("porcentaje") else Decimal('0'),
                monto_fijo=monto_fijo,
                escalones=config_data.get("escalones", [])
            )
        politica_fraude = None
        if documento.get("politica_fraude"):
            pf_data = documento["politica_fraude"]
            politica_fraude = PoliticaFraude(
                tipo=TipoPoliticaFraude(pf_data["tipo"]),
                threshold_score=pf_data["threshold_score"],
                requiere_revision_manual=pf_data["requiere_revision_manual"],
                tiempo_espera_minutos=pf_data["tiempo_espera_minutos"]
            )

        comision = Comision(
            id=uuid.UUID(documento["_id"]),
            id_interaccion=documento["id_interaccion"],
            id_campania=documento["id_campania"],
            monto=MontoComision(
                valor=Decimal(documento["monto"]["valor"]),
                moneda=documento["monto"]["moneda"]
            ),
            estado=EstadoComision(documento["estado"]),
            configuracion=configuracion,
            fecha_vencimiento=documento.get("fecha_vencimiento"),
            politica_fraude_aplicada=politica_fraude,
            fecha_creacion=documento["fecha_creacion"],
            fecha_actualizacion=documento["fecha_actualizacion"]
        )

        return comision
