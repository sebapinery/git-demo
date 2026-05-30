# Tasks — project_scaffold

> El implementer marca `[x]` cada tarea al completarla.
> El reviewer rechaza si queda alguna `[ ]` sin justificación documentada.

---

- [x] T1 — Crear `package.json` con dependencias: `next@14`, `react`, `react-dom`, `mongoose@8`, `typescript`, `@types/node`, `@types/react`. Añadir scripts `dev`, `build`, `start`. Cubre: R6, R13.

- [x] T2 — Crear `tsconfig.json` con configuración base de Next.js 14 (target ES2017, paths, strict mode). Cubre: R13.

- [x] T3 — Crear `next.config.ts` con `output: 'standalone'` habilitado para soporte del Dockerfile multi-stage runner. Cubre: R5, R7.

- [x] T4 — Crear `Dockerfile` con etapa `builder` (FROM node:20-alpine, instala deps, compila) y etapa `runner` (FROM node:20-alpine, copia artefactos standalone). Cubre: R5, R6, R7.

- [x] T5 — Crear `.dockerignore` excluyendo `node_modules`, `.next`, `.env`, `.git` para evitar que el contexto de build incluya archivos innecesarios o sensibles. Cubre: R5, R7.

- [x] T6 — Crear `.env.example` con la variable `MONGODB_URI=mongodb://mongodb:27017/taskmanager` y un comentario descriptivo. Cubre: R8, R17.

- [x] T7 — Crear `docker-compose.yml` con el servicio `mongodb` (imagen mongo:7, puerto 27017:27017, volumen mongo_data:/data/db, healthcheck con mongosh ping, red app-network). Cubre: R1, R3, R10, R15, R16.

- [x] T8 — Añadir el servicio `nextjs` en `docker-compose.yml` (build desde raíz, puerto 3000:3000, env_file .env, depends_on mongodb con condition: service_healthy, healthcheck curl localhost:3000, red app-network). Cubre: R1, R2, R4, R9, R11, R16.

- [x] T9 — Añadir declaraciones de volúmenes y redes al final de `docker-compose.yml` (`volumes: mongo_data:` y `networks: app-network: driver: bridge`). Cubre: R15, R16.

- [x] T10 — Crear estructura de directorios `src/app/`, `src/lib/`, `src/models/`, `src/repositories/`, `src/types/`, `src/components/`. Añadir `.gitkeep` en los directorios vacíos (models, repositories, types, components). Cubre: R13.

- [x] T11 — Crear `src/app/layout.tsx` con el `RootLayout` mínimo requerido por el App Router (html + body). Cubre: R12, R13.

- [x] T12 — Crear `src/app/page.tsx` con una página raíz que retorne un componente React válido (texto estático "Task Manager"). Esto garantiza que GET / responda 200. Cubre: R12.

- [x] T13 — Crear `src/lib/mongodb.ts` con la función `connectToDatabase()` que: (a) valida que `MONGODB_URI` esté definida lanzando un error explícito si no lo está, (b) usa el patrón singleton para evitar múltiples conexiones en desarrollo. Cubre: R14, R18.

- [x] T14 — Verificar el arranque completo ejecutando `docker compose up --build` y comprobar que: ambos servicios levantan sin errores, `curl http://localhost:3000` retorna 200, y los logs de `nextjs` no muestran errores de conexión. Cubre: R2, R3, R4, R12.

- [x] T15 — Verificar que la variable `MONGODB_URI` está disponible dentro del contenedor `nextjs` ejecutando `docker compose exec nextjs printenv MONGODB_URI` y comprobando que retorna el valor configurado en `.env`. Cubre: R9.
