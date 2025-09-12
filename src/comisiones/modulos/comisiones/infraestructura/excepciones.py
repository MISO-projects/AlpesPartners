
from comisiones.seedwork.infraestructura.uow import ExcepcionUoW

class ExcepcionInfraestructuraComision(ExcepcionUoW):

    pass

class ExcepcionRepositorioComision(ExcepcionInfraestructuraComision):

    pass

class ExcepcionBaseDatosComision(ExcepcionInfraestructuraComision):

    pass

class ExcepcionConexionBaseDatos(ExcepcionBaseDatosComision):

    pass

class ExcepcionMapeoComision(ExcepcionInfraestructuraComision):

    pass

class ExcepcionConsumidorEventos(ExcepcionInfraestructuraComision):

    pass

class ExcepcionDespachadorEventos(ExcepcionInfraestructuraComision):

    pass

class ExcepcionConfiguracionComision(ExcepcionInfraestructuraComision):

    pass

class ExcepcionPoliticaFraude(ExcepcionInfraestructuraComision):

    pass

class ExcepcionIntegracionExterna(ExcepcionInfraestructuraComision):

    pass
