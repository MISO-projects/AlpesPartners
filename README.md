# AlpesPartners

## Configuración inicial:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar el proyecto en docker

```sh
docker-compose --profile monolito up
```

## Endpoints

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