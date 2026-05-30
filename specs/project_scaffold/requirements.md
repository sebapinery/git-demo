# Requirements — project_scaffold

> Notación EARS estricta. Cada requirement es verificable por al menos un test concreto.
> Cobertura total de los acceptance criteria originales.

---

## R1

El sistema DEBE contener un archivo `docker-compose.yml` en la raíz del repositorio que defina exactamente dos servicios: `nextjs` y `mongodb`.

## R2

CUANDO el operador ejecuta `docker compose up`, el sistema DEBE levantar el servicio `nextjs` escuchando en el puerto 3000 del host sin errores de arranque.

## R3

CUANDO el operador ejecuta `docker compose up`, el sistema DEBE levantar el servicio `mongodb` escuchando en el puerto 27017 del host sin errores de arranque.

## R4

CUANDO el servicio `nextjs` intenta conectarse a MongoDB durante el arranque, el sistema DEBE garantizar que el servicio `mongodb` esté disponible antes de que `nextjs` procese peticiones, usando la directiva `depends_on` con `condition: service_healthy`.

## R5

El sistema DEBE contener un `Dockerfile` en la raíz del repositorio que use exactamente dos etapas: `builder` y `runner`.

## R6

MIENTRAS la etapa `builder` del `Dockerfile` se ejecuta, el sistema DEBE instalar dependencias y compilar la aplicación Next.js usando Node 20 LTS como imagen base.

## R7

MIENTRAS la etapa `runner` del `Dockerfile` se ejecuta, el sistema DEBE copiar únicamente los artefactos de build desde la etapa `builder`, sin incluir dependencias de desarrollo ni código fuente.

## R8

El sistema DEBE contener un archivo `.env.example` en la raíz del repositorio con la variable `MONGODB_URI` documentada con un valor de ejemplo válido.

## R9

CUANDO el contenedor `nextjs` está en ejecución, el sistema DEBE exponer la variable de entorno `MONGODB_URI` dentro del contenedor con el valor configurado en el archivo de entorno del operador.

## R10

El sistema DEBE definir un healthcheck para el servicio `mongodb` en `docker-compose.yml` que verifique la disponibilidad del servidor mediante `mongosh --eval "db.adminCommand('ping')"`.

## R11

El sistema DEBE definir un healthcheck para el servicio `nextjs` en `docker-compose.yml` que verifique que la página raíz responde HTTP 200 en `http://localhost:3000`.

## R12

CUANDO el operador realiza una petición HTTP GET a `http://localhost:3000`, el sistema DEBE responder con código de estado 200.

## R13

El sistema DEBE contener la siguiente estructura de directorios del proyecto Next.js:
- `src/app/` — rutas y layouts del App Router
- `src/lib/` — utilidades compartidas y configuración de conexión a MongoDB
- `src/models/` — modelos Mongoose
- `src/repositories/` — capa de acceso a datos
- `src/types/` — definiciones TypeScript
- `src/components/` — componentes React reutilizables

## R14

El sistema DEBE contener un archivo `src/lib/mongodb.ts` que exporte una función o instancia de conexión a MongoDB usando Mongoose 8, leyendo `MONGODB_URI` desde las variables de entorno.

## R15

El sistema DEBE definir en `docker-compose.yml` un volumen nombrado persistente para los datos de MongoDB, montado en `/data/db` dentro del contenedor `mongodb`.

## R16

El sistema DEBE definir en `docker-compose.yml` una red interna compartida que conecte los servicios `nextjs` y `mongodb`, de forma que `nextjs` pueda alcanzar a `mongodb` por nombre de servicio.

## R17

El sistema DEBE contener un archivo `.env.example` que documente todas las variables de entorno requeridas por la aplicación, con un comentario descriptivo por cada variable.

## R18

SI la variable de entorno `MONGODB_URI` no está definida al arrancar el contenedor `nextjs` ENTONCES el sistema DEBE fallar el arranque de forma explícita con un mensaje de error legible en los logs.
