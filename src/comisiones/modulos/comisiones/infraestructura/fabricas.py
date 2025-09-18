
from comisiones.seedwork.dominio.fabricas import Fabrica
from comisiones.modulos.comisiones.dominio.repositorios import (
    RepositorioComision,
    RepositorioConfiguracionComision,
    RepositorioPoliticaFraude
)
from comisiones.modulos.comisiones.infraestructura.repositorios import (
    RepositorioComisionSQLite,
    RepositorioComisionMongoDB,
    RepositorioConfiguracionComisionSQLite,
    RepositorioPoliticaFraudeSQLite
)
import os

class FabricaRepositorio(Fabrica):

    def crear_objeto(self, obj: any, mapeador: any = None) -> any:

        db_type = os.getenv('COMISIONES_DB_TYPE', 'mongodb').lower()
        
        if obj == RepositorioComision.__class__:
            if db_type == 'mongodb':
                return RepositorioComisionMongoDB()
            else:
                return RepositorioComisionSQLite()
        
        elif obj == RepositorioConfiguracionComision.__class__:
            return RepositorioConfiguracionComisionSQLite()
        
        elif obj == RepositorioPoliticaFraude.__class__:
            return RepositorioPoliticaFraudeSQLite()
        
        else:
            raise ValueError(f"Tipo de repositorio no soportado: {obj}")

class FabricaServiciosInfraestructura(Fabrica):

    def crear_repositorio_comision(self) -> RepositorioComision:

        fabrica = FabricaRepositorio()
        return fabrica.crear_objeto(RepositorioComision.__class__)

    def crear_repositorio_configuracion(self) -> RepositorioConfiguracionComision:

        fabrica = FabricaRepositorio()
        return fabrica.crear_objeto(RepositorioConfiguracionComision.__class__)

    def crear_repositorio_politica_fraude(self) -> RepositorioPoliticaFraude:

        fabrica = FabricaRepositorio()
        return fabrica.crear_objeto(RepositorioPoliticaFraude.__class__)

    def crear_objeto(self, obj: any, mapeador: any = None) -> any:

        if obj == 'repositorio_comision':
            return self.crear_repositorio_comision()
        elif obj == 'repositorio_configuracion':
            return self.crear_repositorio_configuracion()
        elif obj == 'repositorio_politica_fraude':
            return self.crear_repositorio_politica_fraude()
        else:
            raise ValueError(f"Tipo de servicio no soportado: {obj}")

class FabricaConsumidoresEventos(Fabrica):

    def crear_consumidor_interaccion_atribuida(self):

        from comisiones.modulos.comisiones.infraestructura.consumidores import ConsumidorInteraccionAtribuida
        return ConsumidorInteraccionAtribuida()

    def crear_objeto(self, obj: any, mapeador: any = None) -> any:

        if obj == 'consumidor_interaccion_atribuida':
            return self.crear_consumidor_interaccion_atribuida()
        else:
            raise ValueError(f"Tipo de consumidor no soportado: {obj}")

class FabricaDespachadores(Fabrica):

    def crear_despachador_eventos_comision(self):

        from comisiones.modulos.comisiones.infraestructura.despachadores import DespachadorEventosComision
        return DespachadorEventosComision()

    def crear_objeto(self, obj: any, mapeador: any = None) -> any:

        if obj == 'despachador_eventos_comision':
            return self.crear_despachador_eventos_comision()
        else:
            raise ValueError(f"Tipo de despachador no soportado: {obj}")
