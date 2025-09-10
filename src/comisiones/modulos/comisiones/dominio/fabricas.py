
from alpespartners.seedwork.dominio.fabricas import Fabrica
from alpespartners.modulos.comisiones.dominio.entidades import Comision
from alpespartners.modulos.comisiones.dominio.objetos_valor import (
    MontoComision,
    ConfiguracionComision,
    PoliticaFraude,
    TipoComision,
    TipoPoliticaFraude,
    InteraccionAtribuida
)
from decimal import Decimal
from datetime import datetime
import uuid

class FabricaComision(Fabrica):

    def crear_objeto(self, obj: any, mapeador: any = None) -> Comision:

        if mapeador:
            return mapeador.obtener_tipo().crear_objeto(obj, mapeador)
        
        return obj

class FabricaConfiguracionComision(Fabrica):

    def crear_configuracion_porcentaje(
        self,
        porcentaje: Decimal,
        minimo: MontoComision = None,
        maximo: MontoComision = None
    ) -> ConfiguracionComision:

        return ConfiguracionComision(
            tipo=TipoComision.PORCENTAJE,
            porcentaje=porcentaje,
            minimo=minimo,
            maximo=maximo
        )

    def crear_configuracion_fija(self, monto_fijo: MontoComision) -> ConfiguracionComision:

        return ConfiguracionComision(
            tipo=TipoComision.FIJO,
            monto_fijo=monto_fijo
        )

    def crear_configuracion_escalonada(
        self,
        escalones: list,
        minimo: MontoComision = None,
        maximo: MontoComision = None
    ) -> ConfiguracionComision:

        return ConfiguracionComision(
            tipo=TipoComision.ESCALONADO,
            escalones=escalones,
            minimo=minimo,
            maximo=maximo
        )

    def crear_objeto(self, obj: any, mapeador: any = None) -> ConfiguracionComision:

        if mapeador:
            return mapeador.obtener_tipo().crear_objeto(obj, mapeador)
        
        return obj

class FabricaPoliticaFraude(Fabrica):

    def crear_politica_estricta(self, threshold_score: int = 30) -> PoliticaFraude:

        return PoliticaFraude(
            tipo=TipoPoliticaFraude.STRICT,
            threshold_score=threshold_score,
            requiere_revision_manual=True,
            tiempo_espera_minutos=60
        )

    def crear_politica_moderada(self, threshold_score: int = 50) -> PoliticaFraude:

        return PoliticaFraude(
            tipo=TipoPoliticaFraude.MODERATE,
            threshold_score=threshold_score,
            requiere_revision_manual=False,
            tiempo_espera_minutos=15
        )

    def crear_politica_permisiva(self, threshold_score: int = 80) -> PoliticaFraude:

        return PoliticaFraude(
            tipo=TipoPoliticaFraude.PERMISSIVE,
            threshold_score=threshold_score,
            requiere_revision_manual=False,
            tiempo_espera_minutos=0
        )

    def crear_objeto(self, obj: any, mapeador: any = None) -> PoliticaFraude:

        if mapeador:
            return mapeador.obtener_tipo().crear_objeto(obj, mapeador)
        
        return obj

class FabricaInteraccionAtribuida(Fabrica):

    def crear_desde_evento_tracking(
        self,
        id_interaccion: uuid.UUID,
        id_campania: uuid.UUID,
        tipo_interaccion: str,
        valor_interaccion: MontoComision,
        fraud_ok: bool,
        score_fraude: int = 0,
        parametros_adicionales: dict = None
    ) -> InteraccionAtribuida:

        return InteraccionAtribuida(
            id_interaccion=id_interaccion,
            id_campania=id_campania,
            tipo_interaccion=tipo_interaccion,
            valor_interaccion=valor_interaccion,
            fraud_ok=fraud_ok,
            score_fraude=score_fraude,
            timestamp=datetime.now(),
            parametros_adicionales=parametros_adicionales or {}
        )

    def crear_objeto(self, obj: any, mapeador: any = None) -> InteraccionAtribuida:

        if mapeador:
            return mapeador.obtener_tipo().crear_objeto(obj, mapeador)
        
        return obj
