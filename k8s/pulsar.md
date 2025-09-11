# Configuración de Pulsar en k8s

## Prerequisitos

- kubectl: conectado al cluster de GKE en GCP.
- docker: para la creación de las imagenes de los microservicios
- helm: para la instalación de Pulsar. [Guia de instalación](https://helm.sh/docs/intro/install/)

## Pulsar Deployment

El despliegue de Pulsar se realiza usando el helm chart disponible en https://pulsar.apache.org/docs/next/getting-started-helm/ con los ajustes
correspondientes para el despliegue en GKE.

### Instalación del helm chart

```sh
helm repo add apache https://pulsar.apache.org/charts
helm repo update
```

En otro directorio en la maquina local se debe clonar el repositorio con el helm chart de Pulsar:

```sh
git clone https://github.com/apache/pulsar-helm-chart
cd pulsar-helm-chart
```

Se ejecuta el script para preparar el helm release, donde se puede especificar el nombre del namespace con -n y el release del helm del pulsar con -k. El parametro -c es para crear el namespace:

```sh
./scripts/pulsar/prepare_helm_release.sh \
    -n pulsar \
    -k pulsar-mini \
    -c
```

Una vez realizada la preparación, se puede instalar el helm chart con el siguiente comando desde el directorio de este repositorio:

```sh
helm install \
    --values k8s/values-pulsar-gke.yaml \
    --namespace pulsar \
    pulsar-mini apache/pulsar
```

Es posible que se generen algunos errores en el comando anterior, pero podemos monitorear el estado de la instalación con el siguiente comando:

```sh
kubectl get pods -n pulsar
```

### Probando el funcionamiento del cluster

Una vez los pods se encuentren en estado health, para probar el funcionamiento del cluster, se puede usar el siguiente comando para ingresar al pod toolset:

```sh
kubectl exec -it -n pulsar pulsar-mini-toolset-0 -- /bin/bash
```

Una vez dentro del pod, se pueden ejecutar los siguientes comandos para crear un tenant, un namespace y un topic:

```sh
bin/pulsar-admin tenants create apache
bin/pulsar-admin namespaces create apache/pulsar
bin/pulsar-admin topics create-partitioned-topic apache/pulsar/test-topic -p 4
```

Para verificar que el topic se haya creado correctamente, se puede usar el siguiente comando:

```sh
bin/pulsar-admin topics list-partitioned-topics apache/pulsar
```

Para generar una suscripción al topic, se puede usar el siguiente comando:

```sh
bin/pulsar-client consume -s sub apache/pulsar/test-topic -n 0
```

Abrimos otra terminal, ingresamos al pod y ejecutamos el siguiente comando:

```sh
bin/pulsar-client produce apache/pulsar/test-topic -m "---------hello apache pulsar-------" -n 10
```

En la terminal donde se generó la suscripción, se pueden ver los mensajes recibidos.

### Ingreso las interfaces de administración de pulsar

Para ingresar al pulsar-manager, se puede usar el siguiente comando:

```sh
kubectl port-forward -n pulsar svc/pulsar-mini-pulsar-manager 9527:9527
```

Para poder iniciar sesión se debe crear un usuario y contraseña con los siguientes pasos:

```sh
CSRF_TOKEN=$(curl http://localhost:9527/pulsar-manager/csrf-token)

curl \
    -H "X-XSRF-TOKEN: $CSRF_TOKEN" \
    -H "Cookie: XSRF-TOKEN=$CSRF_TOKEN;" \
    -H 'Content-Type: application/json' \
    -X PUT http://localhost:9527/pulsar-manager/users/superuser \
    -d '{"name": "username", "password": "password", "description": "test", "email": "user@gmail.com"}'
```

Con esto se puede ingresar al pulsar-manager a traves de http://localhost:9527 con el usuario y contraseña creado.

### Detener el cluster para ahorrar costos

```sh
./k8s/stop_pulsar.sh
```

Para reanudar el cluster, se puede usar el siguiente comando:

```sh
./k8s/start_pulsar.sh
```

En caso de que se requieran permisos para ejecutar los scripts, se puede usar el siguiente comando:

```sh
chmod +x k8s/stop_pulsar.sh k8s/start_pulsar.sh
```

## Eliminación del cluster de pulsar

Se puede eliminar el helm chart con el siguiente comando:

```sh
helm uninstall pulsar-mini -n pulsar
```

Se pueden eliminar secretos que hayan quedado en el namespace con el siguiente comando:

```sh
kubectl delete secret -n pulsar --all
```

Finalmente, se puede eliminar el namespace con el siguiente comando:

```sh
kubectl delete namespace pulsar
```
