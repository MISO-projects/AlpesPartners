
from alpespartners.seedwork.dominio.reglas import ReglaNegocio
from alpespartners.modulos.comisiones.dominio.objetos_valor import (
    EstadoComision,
    MontoComision,
    PoliticaFraude,
    InteraccionAtribuida
)
from decimal import Decimal

class ComisionDebeEstarReservadaParaConfirmar(ReglaNegocio):

    estado_comision: EstadoComision

    def __init__(self, estado_comision: EstadoComision, mensaje: str = "La comisión debe estar reservada para confirmarla"):
        super().__init__(mensaje)
        self.estado_comision = estado_comision

    def es_valido(self) -> bool:
        return self.estado_comision == EstadoComision.RESERVADA

class ComisionDebeEstarActivaParaRevertir(ReglaNegocio):

    estado_comision: EstadoComision

    def __init__(self, estado_comision: EstadoComision, mensaje: str = "La comisión debe estar activa para revertirla"):
        super().__init__(mensaje)
        self.estado_comision = estado_comision

    def es_valido(self) -> bool:
        return self.estado_comision in [EstadoComision.RESERVADA, EstadoComision.CONFIRMADA]

class MontoComisionDebeSerPositivo(ReglaNegocio):

    monto: MontoComision

    def __init__(self, monto: MontoComision, mensaje: str = "El monto de comisión debe ser positivo"):
        super().__init__(mensaje)
        self.monto = monto

    def es_valido(self) -> bool:
        return self.monto.valor > Decimal('0')

class InteraccionDebeEstarAprobadaPorFraude(ReglaNegocio):

    interaccion: InteraccionAtribuida

    def __init__(self, interaccion: InteraccionAtribuida, mensaje: str = "La interacción debe estar aprobada por fraude"):
        super().__init__(mensaje)
        self.interaccion = interaccion

    def es_valido(self) -> bool:
        return self.interaccion.fraud_ok

class ScoreFraudeDebeEstarDentroDeThreshold(ReglaNegocio):

    score_fraude: int
    politica_fraude: PoliticaFraude

    def __init__(
        self,
        score_fraude: int,
        politica_fraude: PoliticaFraude,
        mensaje: str = "El score de fraude excede el threshold permitido"
    ):
        super().__init__(mensaje)
        self.score_fraude = score_fraude
        self.politica_fraude = politica_fraude

    def es_valido(self) -> bool:
        return self.score_fraude <= self.politica_fraude.threshold_score

class InteraccionNoDebeYaTenerComision(ReglaNegocio):

    ya_tiene_comision: bool

    def __init__(self, ya_tiene_comision: bool, mensaje: str = "La interacción ya tiene una comisión asociada"):
        super().__init__(mensaje)
        self.ya_tiene_comision = ya_tiene_comision

    def es_valido(self) -> bool:
        return not self.ya_tiene_comision

class ConfiguracionComisionDebeSerValida(ReglaNegocio):

    configuracion: object

    def __init__(self, configuracion: object, mensaje: str = "La configuración de comisión no es válida"):
        super().__init__(mensaje)
        self.configuracion = configuracion

    def es_valido(self) -> bool:
        return self.configuracion is not None

class LoteComisionesDebeSerValido(ReglaNegocio):

    cantidad_comisiones: int

    def __init__(self, cantidad_comisiones: int, mensaje: str = "El lote debe contener al menos una comisión"):
        super().__init__(mensaje)
        self.cantidad_comisiones = cantidad_comisiones

    def es_valido(self) -> bool:
        return self.cantidad_comisiones > 0

class MontoInteraccionDebeSerPositivo(ReglaNegocio):

    valor_interaccion: MontoComision

    def __init__(self, valor_interaccion: MontoComision, mensaje: str = "El valor de la interacción debe ser positivo"):
        super().__init__(mensaje)
        self.valor_interaccion = valor_interaccion

    def es_valido(self) -> bool:
        return self.valor_interaccion and self.valor_interaccion.valor > Decimal('0')

class ComisionNoDebeEstarFinalizada(ReglaNegocio):

    estado_comision: EstadoComision

    def __init__(self, estado_comision: EstadoComision, mensaje: str = "Una comisión finalizada no puede ser modificada"):
        super().__init__(mensaje)
        self.estado_comision = estado_comision

    def es_valido(self) -> bool:
        return self.estado_comision not in [EstadoComision.REVERTIDA, EstadoComision.CANCELADA]
