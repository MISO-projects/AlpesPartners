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

## Microservicios

Los detalles de los escenarios de calidad y

- Marketing: Microservicio encargado de la gestion de campanias y sus estadisticas
- Tracking: Microservicio encargado de la gestion de interacciones
- Atribucion: Microservicio encargado de la gestion de atribuciones
- Comisiones: Microservicio encargado de la gestion de comisiones

Los detalles de las responsabilidades de cada microservicio y escenarios de calidad favorecidos por la arquitecutra se pueden encontrar en el siguiente documento en la wiki del proyecto:

[Prueba de concepto (experimentación)](https://github.com/MISO-projects/AlpesPartners/wiki/Semana-06-%E2%80%90-Entrega-4:-Prueba-de-concepto-(experimentaci%C3%B3n))

![Context-Esc 3 drawio](https://github.com/user-attachments/assets/5ed9957d-0242-4e0a-8bf1-bf5d1ba39a80)

# Persistencia

Se utiliza MongoDB como base de datos. Se agregan los repositorios esta base de datos y se actualiza la unidad de trabajo para soportar la persistencia en MongoDB.

# Despliegue en GKE

Para desplegar en GKE, se debe tener un cluster de GKE creado y configurado.

```sh
kubectl apply -f k8s/mongodb-k8s.yaml
kubectl apply -f k8s/pulsar.yaml
kubectl apply -f k8s/microservices/
```

## Detener y reiniciar los servicios

Se pueden detener los servicios ejecutando los scripts en la carpeta k8s.

```sh
./k8s/stop-services.sh
```

Para iniciar los servicios, se debe ejecutar el script en la carpeta k8s.

```sh
./k8s/start-services.sh
```

## Probar los servicios

Haciendo post forward de los servicios, se pueden probar de forma local.

```sh
kubectl port-forward svc/marketing-service 8080:8000
kubectl port-forward svc/tracking-service 8081:8001
```

Para probar los servicios, se puede usar el collection de postman en la carpeta collections, ajustando las urls a los endpoints de los servicios.
