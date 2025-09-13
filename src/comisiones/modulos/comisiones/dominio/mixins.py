
from comisiones.modulos.comisiones.dominio.objetos_valor import EstadoComision

class ComisionMixin:

    def es_confirmable(self) -> bool:

        return self.estado == EstadoComision.RESERVADA

    def es_revertible(self) -> bool:

        return self.estado in [EstadoComision.RESERVADA, EstadoComision.CONFIRMADA]

    def es_cancelable(self) -> bool:

        return self.estado == EstadoComision.RESERVADA

    def esta_activa(self) -> bool:

        return self.estado in [EstadoComision.RESERVADA, EstadoComision.CONFIRMADA]

    def esta_finalizada(self) -> bool:

        return self.estado in [EstadoComision.REVERTIDA, EstadoComision.CANCELADA]

class ValidacionFraudeMixin:

    def supera_threshold_fraude(self, score_fraude: int, threshold: int) -> bool:

        return score_fraude > threshold

    def requiere_revision_manual(self, score_fraude: int, politica) -> bool:

        return (
            politica.requiere_revision_manual and
            score_fraude > politica.threshold_score * 0.8
        )

class CalculoComisionMixin:

    def calcular_comision_porcentual(self, valor_base, porcentaje):

        from decimal import Decimal
        return valor_base * (porcentaje / Decimal('100'))

    def aplicar_limites(self, monto_calculado, minimo=None, maximo=None):

        if minimo and monto_calculado < minimo:
            return minimo
        
        if maximo and monto_calculado > maximo:
            return maximo
        
        return monto_calculado
