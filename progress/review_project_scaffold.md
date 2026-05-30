# Review — feature project_scaffold (id: 1)

**Veredicto:** CHANGES_REQUESTED

---

## Trazabilidad requirements ↔ tests

La carpeta `tests/` contiene únicamente tests Python para la aplicación CLI
(test_cli.py, test_notes.py, test_storage.py). Ninguno de estos tests verifica
ninguno de los R1–R18 de `specs/project_scaffold/requirements.md`.

CHECKPOINTS.md C6 establece explícitamente: "Cada R<n> de requirements.md
está cubierto por al menos un test concreto en tests/."
`specs/project_scaffold/requirements.md` cabecera confirma: "Cada requirement
es verificable por al menos un test concreto."

| Requisito | Estado | Evidencia |
|---|---|---|
| R1 — docker-compose.yml con exactamente dos servicios `nextjs` y `mongodb` | [ ] SIN TEST | docker-compose.yml inspeccionado correctamente, pero no hay test automatizado en tests/ que lo verifique |
| R2 — `nextjs` levanta en puerto 3000 sin errores | [ ] SIN TEST | Solo verificable en runtime con Docker; T14 marcado [x] pero no existe test automatizado |
| R3 — `mongodb` levanta en puerto 27017 sin errores | [ ] SIN TEST | Solo verificable en runtime con Docker; T14 marcado [x] pero no existe test automatizado |
| R4 — `depends_on` con `condition: service_healthy` | [ ] SIN TEST | docker-compose.yml lo incluye (líneas 23-25), pero no hay test que lo verifique estructuralmente |
| R5 — Dockerfile con exactamente dos etapas `builder` y `runner` | [ ] SIN TEST | Dockerfile correcto (AS builder línea 2, AS runner línea 13), pero no hay test |
| R6 — builder usa Node 20 LTS, instala deps, compila | [ ] SIN TEST | Dockerfile correcto, no hay test |
| R7 — runner copia solo artefactos standalone sin dev deps ni src | [ ] SIN TEST | Dockerfile y next.config.ts correctos (`output: 'standalone'`), no hay test |
| R8 — .env.example contiene MONGODB_URI con valor de ejemplo válido | [ ] SIN TEST | .env.example contiene `MONGODB_URI=mongodb://mongodb:27017/taskmanager`, no hay test |
| R9 — MONGODB_URI disponible dentro del contenedor nextjs | [ ] SIN TEST | docker-compose.yml tiene `env_file: .env`; T15 marcado [x] pero es verificación manual sin test automatizado |
| R10 — healthcheck mongodb con mongosh ping | [ ] SIN TEST | docker-compose.yml líneas 8-13 correcto, no hay test |
| R11 — healthcheck nextjs con curl localhost:3000 | [ ] SIN TEST | docker-compose.yml líneas 27-32 correcto, no hay test |
| R12 — GET / responde HTTP 200 | [ ] SIN TEST | src/app/page.tsx y layout.tsx existen, pero no hay test automatizado que verifique la respuesta HTTP 200 |
| R13 — estructura de directorios src/ completa | [ ] SIN TEST | Directorios verificados manualmente: src/app/, src/lib/, src/models/, src/repositories/, src/types/, src/components/ — todos con .gitkeep donde corresponde. No hay test |
| R14 — src/lib/mongodb.ts exporta connectToDatabase() con Mongoose 8 | [ ] SIN TEST | mongodb.ts correcto (singleton, exporta connectToDatabase()), no hay test |
| R15 — volumen nombrado mongo_data montado en /data/db | [ ] SIN TEST | docker-compose.yml correcto (líneas 6-7 y 35-36), no hay test |
| R16 — red interna app-network compartida entre ambos servicios | [ ] SIN TEST | docker-compose.yml correcto (líneas 14-15, 33-34, 38-40), no hay test |
| R17 — .env.example documenta todas las variables con comentario | [ ] SIN TEST | .env.example tiene comentario descriptivo en línea 1, no hay test |
| R18 — Si MONGODB_URI no definida, falla explícitamente con mensaje legible | [ ] SIN TEST | src/lib/mongodb.ts líneas 9-11 lanzan Error explícito. No hay test unitario que llame a connectToDatabase() sin MONGODB_URI y verifique el error |

**Todos los 18 requisitos carecen de test automatizado en tests/.**

---

## Tasks completas

Todas las tasks en `specs/project_scaffold/tasks.md` están marcadas `[x]`.

| Task | Estado | Observación |
|---|---|---|
| T1 | [x] | package.json creado con next@14.2.29, mongoose@8, scripts dev/build/start |
| T2 | [x] | tsconfig.json con target ES2017, strict, paths |
| T3 | [x] | next.config.ts con output: 'standalone' |
| T4 | [x] | Dockerfile con etapas builder y runner |
| T5 | [x] | .dockerignore excluye node_modules, .next, .env, .git |
| T6 | [x] | .env.example con MONGODB_URI y comentario descriptivo |
| T7 | [x] | Servicio mongodb en docker-compose.yml |
| T8 | [x] | Servicio nextjs en docker-compose.yml |
| T9 | [x] | Volúmenes y redes declarados en docker-compose.yml |
| T10 | [x] | Directorios src/ con .gitkeep en los vacíos |
| T11 | [x] | src/app/layout.tsx con RootLayout |
| T12 | [x] | src/app/page.tsx con componente válido |
| T13 | [x] | src/lib/mongodb.ts con connectToDatabase() y validación de MONGODB_URI |
| T14 | [x] | ADVERTENCIA: Marcada como completa pero es verificación de runtime (docker compose up --build). progress/impl_project_scaffold.md documenta que es responsabilidad del operador — justificación presente pero insuficiente para cubrir ausencia de test |
| T15 | [x] | ADVERTENCIA: Igual que T14, verificación manual de runtime sin test automatizado |

T14 y T15 tienen justificación documentada en `progress/impl_project_scaffold.md` (sección "Decisiones tomadas", punto 1), pero esa justificación no reemplaza la cobertura de test requerida por R2, R3, R9, R12.

---

## Checkpoints

| Checkpoint | Estado | Detalle |
|---|---|---|
| C1 — Arnés completo | [x] | AGENTS.md, init.sh, feature_list.json, progress/current.md, docs/*.md presentes. init.sh termina con exit 0 |
| C2 — Estado coherente | [x] | Una sola feature in_progress (project_scaffold). progress/current.md presente |
| C3 — Código respeta arquitectura | [x] | La arquitectura Python (docs/architecture.md) se refiere al harness CLI. Los archivos Next.js están fuera de src/ Python y no violan las capas del CLI. No hay print() de debug ni TODOs sin contexto en los archivos nuevos |
| C4 — Verificación real | [ ] | tests/ tiene tests por módulo Python (test_cli, test_notes, test_storage), pero ninguno cubre los R1-R18 de project_scaffold. 27 tests pasan, pero ninguno verifica el scaffold |
| C5 — Sesión cerrada bien | [x] | progress/history.md existe. Sin archivos .tmp sueltos |
| C6 — Spec Driven Development | [ ] | specs/project_scaffold/ tiene los 3 archivos. Tasks [x] todas. PERO ningún R<n> tiene test concreto en tests/ — viola la regla dura de C6 |

---

## Implementación — calidad de los archivos revisados

Los archivos implementados son estructuralmente correctos:

- `docker-compose.yml`: dos servicios exactos (R1), puertos correctos (R2, R3), depends_on con service_healthy (R4), healthcheck mongosh (R10), healthcheck curl (R11), volumen mongo_data:/data/db (R15), red app-network bridge (R16), env_file (R9).
- `Dockerfile`: dos etapas AS builder y AS runner (R5), node:20-alpine (R6), copia standalone (R7).
- `.env.example`: MONGODB_URI con valor de ejemplo y comentario (R8, R17).
- `next.config.ts`: output: 'standalone' (R7).
- `src/lib/mongodb.ts`: singleton, exporta connectToDatabase(), lanza Error explícito si MONGODB_URI no definida (R14, R18).
- `src/app/layout.tsx` y `page.tsx`: App Router válido (R12, R13).
- Directorios con .gitkeep: R13 completo.
- `package.json`: next@14, mongoose@8, scripts dev/build/start, typescript, @types/node, @types/react (R6, R13).
- `tsconfig.json`: ES2017, strict, paths (R13).

No se encontraron violaciones de conventions.md (el código TypeScript no aplica las convenciones Python del doc, pero son archivos de un proyecto Node/Next — el doc describe el harness Python).

---

## Cambios requeridos

1. **Crear tests automatizados para todos los R1–R18.** Esto es la regla dura del spec y del CHECKPOINTS C6. Los tests pueden ser scripts Python que usen `subprocess`, `os.path`, o `re` para inspeccionar estructuralmente los archivos de configuración sin necesitar Docker en ejecución. Ejemplos concretos requeridos:
   - Test que parsea `docker-compose.yml` y verifica exactamente dos servicios `nextjs` y `mongodb` (R1).
   - Test que verifica que `docker-compose.yml` contiene `condition: service_healthy` bajo `depends_on.mongodb` (R4).
   - Test que verifica que `Dockerfile` contiene exactamente dos líneas `FROM ... AS builder` y `FROM ... AS runner` (R5).
   - Test que verifica que `next.config.ts` contiene `output: 'standalone'` (R7).
   - Test que verifica que `.env.example` contiene la variable `MONGODB_URI` con un comentario en la línea anterior (R8, R17).
   - Test que verifica que `docker-compose.yml` contiene el healthcheck con `mongosh` y `db.adminCommand('ping')` (R10).
   - Test que verifica que `docker-compose.yml` contiene el healthcheck con `curl -f http://localhost:3000` (R11).
   - Test que verifica que `src/lib/mongodb.ts` contiene la cadena `'MONGODB_URI environment variable is not defined'` o similar (R18).
   - Test que verifica la existencia de todos los directorios y .gitkeep requeridos (R13).
   - Test unitario de `connectToDatabase()` que confirma que lanza error cuando `MONGODB_URI` no está en `process.env` — si se puede mockear el entorno Node desde Python o con Jest (R18).

2. **R2, R3, R9, R12** son verificaciones de runtime que dependen de Docker. La opción preferida es añadir tests estructurales de los archivos de configuración que los garanticen indirectamente. Si el entorno de CI dispone de Docker, añadir un test de integración que ejecute `docker compose up` y verifique los puertos.

3. T14 y T15 están marcadas `[x]` con justificación de "verificación manual por el operador". Esa justificación es aceptable para el entorno sin Docker, pero la cobertura de test para R2, R3, R9, R12 debe existir de forma estructural o de integración antes de aprobación.
