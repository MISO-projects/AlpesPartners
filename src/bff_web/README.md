# BFF AlpesPartners - Documentación API

## Descripción General

El BFF (Backend For Frontend) de AlpesPartners es una capa de API que actúa como intermediario entre las aplicaciones cliente y los microservicios de backend. Facilita la comunicación con los servicios de Marketing y Tracking, proporcionando endpoints optimizados para el frontend.

## Características Principales

- **API RESTful** con FastAPI
- **Integración asíncrona** con microservicios
- **Server-Sent Events (SSE)** para notificaciones en tiempo real
- **Validación de datos** con Pydantic
- **CORS habilitado** para aplicaciones web
- **Health check** para monitoreo

## URL Base

```
http://localhost:8004
```

## Endpoints Disponibles

### Health Check

#### GET /health
Verifica que el BFF esté funcionando correctamente.

**Response:**
```json
{
    "status": "healthy",
    "service": "BFF AlpesPartners"
}
```

### Marketing

#### POST /api/v1/marketing/campanias
Crea una nueva campaña de marketing.

**Request Body:**
```json
{
    "nombre": "string",
    "descripcion": "string",
    "fecha_inicio": "2024-01-01T00:00:00Z",
    "fecha_fin": "2024-12-31T23:59:59Z",
    "tipo": "DIGITAL",
    "edad_minima": 18,
    "edad_maxima": 65,
    "genero": "TODOS",
    "ubicacion": "Colombia",
    "intereses": ["tecnologia", "viajes"],
    "presupuesto": 10000.0,
    "canales": ["WEB", "EMAIL", "SOCIAL"]
}
```

**Response (200):**
```json
{
    "message": "Comando de creación enviado para procesamiento"
}
```

**Campos obligatorios:**
- `nombre`: Nombre de la campaña
- `descripcion`: Descripción de la campaña
- `fecha_inicio`: Fecha de inicio (formato ISO 8601)
- `fecha_fin`: Fecha de finalización (formato ISO 8601)

**Campos opcionales:**
- `tipo`: Tipo de campaña (default: "DIGITAL")
- `edad_minima`: Edad mínima del público objetivo
- `edad_maxima`: Edad máxima del público objetivo
- `genero`: Género del público objetivo
- `ubicacion`: Ubicación geográfica
- `intereses`: Lista de intereses del público objetivo
- `presupuesto`: Presupuesto asignado (default: 0.0)
- `canales`: Canales de distribución (default: ["WEB", "EMAIL"])

#### PUT /api/v1/marketing/campanias/{campania_id}/activar
Activa una campaña existente.

**Path Parameters:**
- `campania_id`: ID de la campaña a activar

**Response (200):**
```json
{
    "message": "Comando de activación enviado para procesamiento"
}
```

### Tracking

#### POST /api/v1/tracking/interaccion
Registra una nueva interacción de usuario.

**Request Body:**
```json
{
    "tipo": "CLICK",
    "marca_temporal": "2024-01-15T10:30:00Z",
    "identidad_usuario": "usuario-test-123",
    "parametros_tracking": {
        "utm_source": "bff_test",
        "utm_medium": "postman",
        "utm_campaign": "test_campaign"
    },
    "elemento_objetivo": "boton_registro",
    "contexto": {
        "pagina": "landing",
        "seccion": "hero",
        "device": "desktop",
        "browser": "chrome"
    }
}
```

**Response (200):**
```json
{
    "message": "Interacción registrada exitosamente"
}
```

**Campos obligatorios:**
- `tipo`: Tipo de interacción (ej: "CLICK", "VIEW", "SUBMIT")
- `marca_temporal`: Timestamp de la interacción (formato ISO 8601)
- `identidad_usuario`: Identificador del usuario
- `parametros_tracking`: Parámetros de seguimiento (objeto)
- `elemento_objetivo`: Elemento con el que interactuó
- `contexto`: Contexto de la interacción (objeto)

### Server-Sent Events (SSE)

#### GET /stream/campanias
Endpoint de Server-Sent Events para recibir notificaciones en tiempo real sobre campañas.

**Eventos disponibles:**
- `campania_creada`: Cuando se crea una nueva campaña
- `campania_activada`: Cuando se activa una campaña

## Códigos de Respuesta HTTP

- **200**: Operación exitosa
- **202**: Comando enviado para procesamiento
- **400**: Error en la petición (datos inválidos)
- **500**: Error interno del servidor
- **503**: Servicio no disponible (error de conexión con microservicios)

## Formato de Errores

```json
{
    "error": "Descripción del error"
}
```

## Configuración del Entorno

### Variables de Entorno

- `MARKETING_SERVICE_URL`: URL del servicio de marketing (default: "http://marketing:8000")
- `TRACKING_SERVICE_URL`: URL del servicio de tracking (default: "http://tracking:8000")
- `APP_VERSION`: Versión de la aplicación (default: "1")

### Ejecutar el BFF

```bash
# Con Docker Compose
docker-compose --profile alpespartners up

# Puerto por defecto: 8004
```

## Integración con Postman

### Collection de Postman

La collection incluye:
- Health Check
- Crear Campaña
- Activar Campaña
- Registrar Interacción

Ubicación: `./collection/BFF_AlpesPartners.postman_collection.json`

## Arquitectura

### Patrones Implementados

- **Command Query Responsibility Segregation (CQRS)**
- **Event-Driven Architecture** con Apache Pulsar
- **Asynchronous Processing** con background tasks

## Monitoreo y Observabilidad

### Health Check
Utiliza el endpoint `/health` para verificar el estado del servicio.

### Logs
El BFF registra eventos importantes como:
- Conexiones SSE de clientes
- Comandos enviados a microservicios
- Errores de conexión

### Logs de Depuración

```bash
# Ver logs del contenedor BFF
docker logs <container_name>
```