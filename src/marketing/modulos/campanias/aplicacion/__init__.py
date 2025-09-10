from pydispatch import dispatcher
from .handlers import HandlerCampaniaIntegracion

# dispatcher.connect(
#     HandlerCampaniaIntegracion.handle_campania_creada, 
#     signal='CampaniaCreadaDominio'
# )
# dispatcher.connect(
#     HandlerCampaniaIntegracion.handle_campania_activada,
#     signal='CampaniaActivadaDominio'
# )
# dispatcher.connect(
#     HandlerCampaniaIntegracion.handle_campania_desactivada,
#     signal='CampaniaDesactivadaDominio'
# )
# dispatcher.connect(
#     HandlerCampaniaIntegracion.handle_interaccion_recibida,
#     signal='InteraccionRecibidaDominio'
# )
