# AlpesPartners

## Configuración inicial:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar el proyecto en docker

```sh
docker-compose --profile alpespartners up
```
# Arquitectura
Se utiliza una arquitectura hexagonal con separación de la capa de presentación utilizando flask. Los modulos contienen las capas de aplicacion, dominio e infraestructura.

## API

En la carpeta collections se puede encontrar un collection de postman con los endpoints de cada módulo

Endpoints tracking:
- Crear interaccion

Endpoints marketing:
- Crear campania
- Listar campanias
- Obtener campania especifica
- Estadisticas campanias
- Activar campania

Para cada endpoint se utiliza el patron de diseño Command Query Responsibility Segregation (CQRS)

## Modulos

- Marketing: Modulo encargado de la gestion de campanias y sus estadisticas
- Tracking: Modulo encargado de la gestion de interacciones 

![Arquitectura](./docs/Diagrama_POC.svg)


# Persistencia

Se utiliza MongoDB como base de datos. Se agregan los repositorios esta base de datos y se actualiza la unidad de trabajo para soportar la persistencia en MongoDB.
