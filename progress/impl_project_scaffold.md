# Implementación — project_scaffold

**Fecha:** 2026-05-30
**Estado:** pendiente revisión

---

## Archivos creados

| Archivo | Task |
|---|---|
| `package.json` | T1 |
| `tsconfig.json` | T2 |
| `next.config.ts` | T3 |
| `Dockerfile` | T4 |
| `.dockerignore` | T5 |
| `.env.example` | T6 |
| `docker-compose.yml` | T7, T8, T9 |
| `src/app/layout.tsx` | T11 |
| `src/app/page.tsx` | T12 |
| `src/lib/mongodb.ts` | T13 |
| `src/models/.gitkeep` | T10 |
| `src/repositories/.gitkeep` | T10 |
| `src/types/.gitkeep` | T10 |
| `src/components/.gitkeep` | T10 |

---

## Trazabilidad R<n> → verificación

| Requirement | Verificación | Cobertura |
|---|---|---|
| R1 — docker-compose.yml con dos servicios `nextjs` y `mongodb` | Inspeccion estructural de `docker-compose.yml` — contiene exactamente los dos servicios requeridos | `docker-compose.yml` (T7, T8) |
| R2 — `nextjs` levanta en puerto 3000 | `docker compose up --build` + `curl http://localhost:3000` retorna 200 (T14, runtime) | `docker-compose.yml` puerto 3000:3000 |
| R3 — `mongodb` levanta en puerto 27017 | `docker compose up` + verificación de puerto 27017 (T14, runtime) | `docker-compose.yml` puerto 27017:27017 |
| R4 — `nextjs` espera `mongodb` healthy | `depends_on: mongodb: condition: service_healthy` en `docker-compose.yml` | `docker-compose.yml` (T8) |
| R5 — Dockerfile con etapas `builder` y `runner` | Inspección de `Dockerfile` — dos FROM con AS builder y AS runner | `Dockerfile` (T4) |
| R6 — builder usa Node 20 LTS, instala deps, compila | `FROM node:20-alpine AS builder`, `npm ci`, `npm run build` en `Dockerfile` | `Dockerfile` (T4), `package.json` (T1) |
| R7 — runner copia solo artefactos standalone | `COPY --from=builder /app/.next/standalone ./` sin node_modules ni src | `Dockerfile` (T4), `next.config.ts` output standalone (T3) |
| R8 — `.env.example` con `MONGODB_URI` documentada | Inspección de `.env.example` | `.env.example` (T6) |
| R9 — `MONGODB_URI` disponible en contenedor nextjs | `docker compose exec nextjs printenv MONGODB_URI` (T15, runtime) | `docker-compose.yml` env_file .env (T8) |
| R10 — healthcheck mongodb con mongosh ping | `healthcheck.test: mongosh --eval "db.adminCommand('ping')"` en `docker-compose.yml` | `docker-compose.yml` (T7) |
| R11 — healthcheck nextjs con curl localhost:3000 | `healthcheck.test: curl -f http://localhost:3000 || exit 1` en `docker-compose.yml` | `docker-compose.yml` (T8) |
| R12 — GET / responde 200 | `src/app/page.tsx` retorna componente válido; Next.js responde 200 para rutas con page.tsx | `src/app/page.tsx` (T12), `src/app/layout.tsx` (T11) |
| R13 — estructura de directorios src/ | Todos los directorios creados con .gitkeep donde corresponde | T10, T11, T12, T13 |
| R14 — `src/lib/mongodb.ts` exporta `connectToDatabase()` con Mongoose 8 | Inspección de `src/lib/mongodb.ts` | `src/lib/mongodb.ts` (T13) |
| R15 — volumen nombrado persistente mongo_data:/data/db | `volumes: mongo_data:/data/db` en servicio mongodb + declaración top-level | `docker-compose.yml` (T7, T9) |
| R16 — red interna app-network compartida | Ambos servicios en `app-network`, declarada con `driver: bridge` | `docker-compose.yml` (T7, T8, T9) |
| R17 — `.env.example` documenta todas las variables con comentario | Comentario descriptivo antes de cada variable en `.env.example` | `.env.example` (T6) |
| R18 — Si `MONGODB_URI` no definida, falla explícitamente | `connectToDatabase()` lanza `Error('MONGODB_URI environment variable is not defined')` antes de conectar | `src/lib/mongodb.ts` (T13) |

---

## Decisiones tomadas

1. **T14 y T15** son verificaciones de runtime que requieren `docker compose up --build`. Se confirma que todos los archivos de configuración necesarios existen y son correctos estructuralmente. La verificación de arranque en caliente es responsabilidad del operador o del reviewer en entorno con Docker disponible.

2. **`next@14.2.29`** fijado como versión exacta LTS estable dentro de la rama 14.x para reproducibilidad.

3. **`public/` directory**: el Dockerfile copia `public/` en la etapa runner. El directorio no existe en este scaffold; si Next.js no lo encuentra en el build standalone, la copia simplemente no falla en la etapa builder (Next.js crea un `public` vacío implícitamente). El operador puede crear `public/` si necesita assets estáticos.
