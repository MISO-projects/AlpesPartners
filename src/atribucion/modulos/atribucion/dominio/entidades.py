from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from atribucion.seedwork.dominio.entidades import AgregacionRaiz


from . import objetos_valor as ov

class EstadoJourney(Enum):
    ACTIVO = "ACTIVO"
    CONVERTIDO = "CONVERTIDO"
    EXPIRADO = "EXPIRADO"

class TipoModeloAtribucion(Enum):
    FIRST_TOUCH = "FIRST_TOUCH"
    LAST_TOUCH = "LAST_TOUCH"
    LINEAR = "LINEAR"
    POSITION_BASED = "POSITION_BASED"
    TIME_DECAY = "TIME_DECAY"
    DATA_DRIVEN = "DATA_DRIVEN"

@dataclass
class Touchpoint:
    orden: int
    interaccion_id: str
    timestamp: datetime
    campania_id: str
    afiliado_id: str 
    canal: str
    tipo_interaccion: str

@dataclass
class Conversion:
    timestamp: datetime
    tipo: str
    valor: float
    moneda: str = "USD"


@dataclass
class Journey(AgregacionRaiz):
    usuario_id: str = field(hash=True, default=None)
    estado: EstadoJourney = field(default=EstadoJourney.ACTIVO)
    fecha_inicio: datetime = field(default_factory=datetime.now)
    fecha_ultima_actividad: datetime = field(default_factory=datetime.now)
    touchpoints: list[Touchpoint] = field(default_factory=list)
    conversiones: list[Conversion] = field(default_factory=list)

    def agregar_touchpoint(self, datos_evento: dict):
        if self.estado != EstadoJourney.ACTIVO:
            print(f"WARN: Journey {self.id} ya no está activo.")
            return
        timestamp_num = datos_evento.get('marca_temporal', 0)
        timestamp_obj = datetime.fromtimestamp(timestamp_num / 1000, tz=timezone.utc)

        nuevo_touchpoint = Touchpoint(
            orden=len(self.touchpoints) + 1,
            interaccion_id=datos_evento.get('id_interaccion'),
            timestamp=timestamp_obj,
            campania_id=datos_evento.get('parametros_tracking', {}).get('campania'),
            afiliado_id=datos_evento.get('parametros_tracking', {}).get('id_afiliado'),
            canal=datos_evento.get('parametros_tracking', {}).get('medio'),
            tipo_interaccion=datos_evento.get('tipo')
        )
        self.touchpoints.append(nuevo_touchpoint)
        self.fecha_ultima_actividad = datetime.now()
        print(f"ENTIDAD: Touchpoint tipo '{nuevo_touchpoint.tipo_interaccion}' agregado al Journey {self.id}.")

    def calcular_valor_conversion_dinamico(self, datos_evento: dict) -> float:
        """Calcula el valor de conversión basado en los datos del evento recibido por tracking"""
        
        # Valores base por tipo de conversión
        valores_base = {
            'PURCHASE': 150.0,
            'SIGNUP': 25.0,
            'SUBSCRIBE': 50.0,
            'DOWNLOAD': 15.0,
            'CLICK': 30.0,
            'VIEW': 5.0,
            'CONVERSION': 100.0
        }
        
        tipo_conversion = datos_evento.get('tipo', 'UNKNOWN')
        valor_base = valores_base.get(tipo_conversion, 50.0)
        
        # Multiplicadores por fuente
        parametros = datos_evento.get('parametros_tracking', {})
        fuente = parametros.get('fuente', 'unknown')
        
        multiplicadores_fuente = {
            'google': 1.3,
            'facebook': 1.1,
            'instagram': 1.0,
            'twitter': 0.9,
            'linkedin': 1.4,
            'email': 1.2,
            'direct': 1.5,
            'organic': 1.6
        }
        
        multiplicador_fuente = multiplicadores_fuente.get(fuente.lower(), 1.0)
        print(f"CALCULO VALOR: Fuente '{fuente}' -> multiplicador: {multiplicador_fuente}")
        
        # Multiplicadores por medio
        medio = parametros.get('medio', 'unknown')
        multiplicadores_medio = {
            'cpc': 1.1,
            'organic': 1.3,
            'social': 0.9,
            'email': 1.2,
            'referral': 1.1,
            'display': 0.8
        }
        
        multiplicador_medio = multiplicadores_medio.get(medio.lower(), 1.0)
        
        campania = parametros.get('campania')
        bonus_campania = 1.15 if campania else 1.0
        if campania:
            print(f"CALCULO VALOR: Campaña definida -> bonus: {bonus_campania}")
        
        valor_final = valor_base * multiplicador_fuente * multiplicador_medio * bonus_campania
        valor_final = round(valor_final, 2)
        return valor_final

    def registrar_conversion(self, datos_evento: dict) -> Conversion:
        self.estado = EstadoJourney.CONVERTIDO
        timestamp_num = datos_evento.get('marca_temporal', 0)
        timestamp_obj = datetime.fromtimestamp(timestamp_num / 1000, tz=timezone.utc)
        
        valor_calculado = self.calcular_valor_conversion_dinamico(datos_evento)
        
        nueva_conversion = Conversion(
            timestamp=timestamp_obj,
            tipo=datos_evento.get('tipo'),
            valor=valor_calculado
        )
        self.conversiones.append(nueva_conversion)
        print(f"ENTIDAD: Conversión registrada en Journey {self.id} por valor de {nueva_conversion.valor}.")
        return nueva_conversion

@dataclass
class ModeloAtribucion(AgregacionRaiz):
    nombre: str = field(default="")
    tipo: TipoModeloAtribucion = field(default=TipoModeloAtribucion.LAST_TOUCH)
    activo: bool = field(default=False)
    configuracion: ov.ConfiguracionAtribucion = field(default_factory=ov.ConfiguracionAtribucion)
      
    def calcular_atribucion(self, journey: Journey, conversion: Conversion) -> list[ov.AtribucionCalculada]:
        if not self.activo:
            raise Exception(f"El modelo de atribución {self.nombre} no está activo.")
            
        touchpoints_elegibles = journey.touchpoints
        if not touchpoints_elegibles:
            return []

        if self.tipo == TipoModeloAtribucion.FIRST_TOUCH:
            return self._atribucion_first_touch(touchpoints_elegibles, conversion)
        elif self.tipo == TipoModeloAtribucion.LAST_TOUCH:
            return self._atribucion_last_touch(touchpoints_elegibles, conversion)
        elif self.tipo == TipoModeloAtribucion.LINEAR:
            return self._atribucion_linear(touchpoints_elegibles, conversion)
        elif self.tipo == TipoModeloAtribucion.POSITION_BASED:
            return self._atribucion_position_based(touchpoints_elegibles, conversion, self.configuracion)
        elif self.tipo == TipoModeloAtribucion.TIME_DECAY:
            return self._atribucion_time_decay(touchpoints_elegibles, conversion, self.configuracion)
        else:
            print(f"WARN: Modelo {self.tipo.value} no implementado, usando LAST_TOUCH como fallback.")
            return self._atribucion_last_touch(touchpoints_elegibles, conversion)

    def _atribucion_first_touch(self, touchpoints, conversion):
        primer_touchpoint = touchpoints[0]
        return [ov.AtribucionCalculada(touchpoint=primer_touchpoint, peso_atribucion=1.0, valor_atribuido=conversion.valor, modelo_usado=self.tipo)]

    def _atribucion_last_touch(self, touchpoints, conversion):
        ultimo_touchpoint = touchpoints[-1]
        return [ov.AtribucionCalculada(touchpoint=ultimo_touchpoint, peso_atribucion=1.0, valor_atribuido=conversion.valor, modelo_usado=self.tipo)]

    def _atribucion_linear(self, touchpoints, conversion):
        peso = 1.0 / len(touchpoints)
        return [ov.AtribucionCalculada(touchpoint=tp, peso_atribucion=peso, valor_atribuido=conversion.valor * peso, modelo_usado=self.tipo) for tp in touchpoints]

    def _atribucion_position_based(self, touchpoints, conversion, config: ov.ConfiguracionAtribucion):
        if len(touchpoints) == 1:
            return self._atribucion_last_touch(touchpoints, conversion)
        
        p_peso = config.peso_primer_touch
        u_peso = config.peso_ultimo_touch
        i_peso_total = 1.0 - (p_peso + u_peso)
        
        intermedios = touchpoints[1:-1]
        i_peso_individual = i_peso_total / len(intermedios) if intermedios else 0
        
        atribuciones = []
        atribuciones.append(ov.AtribucionCalculada(touchpoint=touchpoints[0], peso_atribucion=p_peso, valor_atribuido=conversion.valor * p_peso, modelo_usado=self.tipo))
        for tp in intermedios:
            atribuciones.append(ov.AtribucionCalculada(touchpoint=tp, peso_atribucion=i_peso_individual, valor_atribuido=conversion.valor * i_peso_individual, modelo_usado=self.tipo))
        atribuciones.append(ov.AtribucionCalculada(touchpoint=touchpoints[-1], peso_atribucion=u_peso, valor_atribuido=conversion.valor * u_peso, modelo_usado=self.tipo))
        
        return atribuciones

    def _atribucion_time_decay(self, touchpoints, conversion, config: ov.ConfiguracionAtribucion):
        total_peso_bruto = 0
        pesos_brutos = []
        factor_dias = config.factor_decaimiento or 7.0

        for tp in touchpoints:
            delta_segundos = (conversion.timestamp - tp.timestamp).total_seconds()
            delta_dias = delta_segundos / 86400
            peso = 2 ** (-delta_dias / factor_dias)
            pesos_brutos.append(peso)
            total_peso_bruto += peso
        
        if total_peso_bruto == 0:
            return self._atribucion_linear(touchpoints, conversion)

        return [
            ov.AtribucionCalculada(touchpoint=tp, peso_atribucion=(peso / total_peso_bruto), valor_atribuido=conversion.valor * (peso / total_peso_bruto), modelo_usado=self.tipo)
            for tp, peso in zip(touchpoints, pesos_brutos)
        ]