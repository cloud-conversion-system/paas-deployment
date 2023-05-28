# PaaS Deployment

REST Backend + Asynchronous Processing Layer. Design and implementation of a PaaS web application in public cloud.

This application allows compressing files using different utilities and/or algorithms: ZIP, 7Z, TAR.GZ, TAR.BZ2

## Video Explicativo

TODO: [YouTube Link]()

## ¿Cómo desplegar la aplicación en GCP?

### Despliegue de la base de datos - Cloud SQL

En primer lugar cree una instancia de Cloud SQL en la misma región en la que creó las instancias de Compute Engine. Asegurese que utilice PostgreSQL 14.

Luego, chequee la opción de asignar IP privada, esta es la que va a utilizar para hacer llamado en la base de datos.
Verifique que la maquina pertenezca a la misma VPC que las demás maquinas desplegadas.

Luego de haber chequeado la opción, en caso de que su proyecto no tenga activadas las APIs necesarias, GCP lo redirigirá a un tutorial para activarlas y asignar correctamente esa IP privada a la VPC correspondiente.

Una vez la instancia se haya creado, reemplace la IP pública de la base de datos contenida en los archivos `worker/app` y `__init__.py`. Solo debe reemplazar la parte contenida después del @ y antes del /.

### Despliegue del sistema de Cloud Storage

Para comenzar, se creó un bucket en Cloud Storage y se otorgaron los permisos necesarios para que las instancias pueda acceder a él. En los containers del worker y de la aplicación, se configuraron un par de parámetros adicionales para realizar la conexión con el bucket de Cloud Storage.

### Configuración del Secret Manager
Recuerde crear un secret con las credenciales de autenticación en formato JSON, para que los contenedores puedan utilizar servicios, como por ejemplo Cloud Storage.

### Configuración de Pub/Sub
En primer lugar, se debe crear un tópico al que llegaran eventos con el nombre de "file_system_notification". Luego de esto, asocie una subsripción, llamada "worker_subscription" de tipo push hacia el endpoint del worker que más tarde configurará en Cloud Run.

### Creación de servicios en Cloud Run
1. En Cloud Run, seleccione "Create Service".
2. Seleccione la opción "Continuously deploy new revisions from a source repository", y siga los pasos para conectar un repositorio con Google Cloud Build. Esto creará un trigger que actualizará automáticamente los contenedores del servico.
3. Configure reglas de autoscaling, capacidad y puertos.
4. Añada un secret que enlace el creado para las credenciales. Debe estar montado como volumen en `/app/credentials/`, con el nombre de `google-credentials.json`.
5. Opcionalmente, podrá crear un health check del servicio.
6. Cree una conexión a la base de datos en Cloud SQL.

## Documentación del API
[Postman Documentation](https://documenter.getpostman.com/view/11708390/2s93Y5NeWB)

## License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](LICENSE)**
- Copyright 2023 © Cloud Conversion System
