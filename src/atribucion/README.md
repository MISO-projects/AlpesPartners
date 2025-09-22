# Microservicio de Atribución

Este servicio actúa como el cerebro analítico del sistema de marketing. Su principal responsabilidad es determinar qué campañas o socios (`partners`) merecen el crédito por las conversiones de los usuarios (como compras o registros), aplicando diferentes modelos de atribución.

---

## Contratos Asíncronos (Eventos y Comandos)

Esta es la interfaz pública del servicio. Se comunica con otros microservicios a través de los siguientes tópicos en Apache Pulsar.

### Eventos Consumidos (Lo que escucha)

#### 👂 Evento: `InteraccionRegistrada`
- **Tópico:** interaccion-registrada
- **Producido por:** Servicio de tracking
- **Propósito:** Notifica cada interacción de un usuario (clics, vistas, etc.). El servicio de Atribución usa estos eventos para construir el historial (`Journey`) de cada usuario.
- **Schema (Payload):**
```json
{
  "id_interaccion": "uuid-del-clic",
  "tipo": "CLICK",
  "marca_temporal": 1733047200000,
  "identidad_usuario": {
    "id_usuario": "user-123",
    "id_anonimo": "anon-xyz"
  },
  "parametros_tracking": {
    "fuente": "facebook.com",
    "medio": "social",
    "campania": "campania-verano-2025",
    "id_afiliado": "influencer-abc"
  }
}
```
### Comandos Consumidos (Órdenes que recibe)
#### 📥 Comando: RevertirAtribucion
- **Tópico:** revertir-atribucion
- **Propósito:** Ordena al servicio de Atribución que revierta una conversión previamente atribuida, cambiando el estado del Journey a REVERTIDO_POR_FRAUDE.
- **Schema (Payload):**

```json
{
  "journey_id": "uuid-del-journey-a-revertir"
}
```

### Eventos Publicados (Lo que notifica)
#### 📣 Evento: ConversionAtribuida
- **Tópico:** eventos-atribucion
- **Consumido por:** Servicio de comisión
- **Propósito:** Notifica el resultado final de un cálculo de atribución. Contiene toda la información necesaria ("carga de estado") para que el servicio de Comisiones pueda iniciar el proceso de pago.
- **Schema (Payload):**
```json
{
    "id_interaccion_atribuida": "uuid-del-calculo-de-atribucion",
    "id_campania": "la-campania-que-gano-el-credito",
    "tipo_conversion": "PURCHASE",
    "monto_atribuido": {
        "valor": 150.75,
        "moneda": "USD"
    },
    "id_interaccion_original": "el-id-de-la-compra-original",
    "score_fraude": 15
}
```

#### 📣 Evento: AtribucionRevertida
- **Tópico:** atribucion-revertida
- **Propósito:** Notifica que una atribución ha sido revertida. El servicio de Comisiones usaría este evento para cancelar una comisión que estaba en estado "Reservada".
- **Schema (Payload):**

```json
{
  "journey_id_revertido": "uuid-del-journey-que-fue-revertido",
  "interacciones": [ //revertidas
    "orden:1,campania:campania-verano-2025",
    "orden:2,campania:campania-invierno-2025"
  ]
}
```

