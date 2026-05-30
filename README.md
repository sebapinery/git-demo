# Task Manager Fullstack

Aplicación fullstack para gestión de tareas construida con **Next.js 14 + MongoDB + Docker Compose**.
Sirve como ejemplo de **Harness Engineering**: un repositorio estructurado para que un agente de IA
pueda trabajar sobre él de forma autónoma y verificable.

> El código de la aplicación es deliberadamente simple. Lo importante de
> este repo no es **qué** hace, sino **cómo** está estructurado.

## La aplicación

- Tabla de tareas con columnas: título, descripción, estado, fecha de creación.
- Botones de **editar** y **eliminar** por fila.
- Botón **Nueva tarea** que abre un modal compartido de crear/editar.
- Persistencia en MongoDB, desplegado via Docker Compose.

## Cómo arrancar

```bash
# Requisito: Docker y Docker Compose instalados
cp .env.example .env
docker compose up --build
```

La app queda disponible en `http://localhost:3000`.

## Cómo está organizado el arnés

| Pilar | Manifestación en este repo |
|---|---|
| **El repositorio ES el sistema** | `AGENTS.md`, `init.sh`, `feature_list.json`, `specs/`, `progress/`, `docs/` |
| **Orquestación multi-agente** | `.claude/agents/leader.md`, `spec_author.md`, `implementer.md`, `reviewer.md` |
| **Spec Driven Development** | `docs/specs.md`, EARS notation, puerta de aprobación humana en `spec_ready` |
| **Supervisión y mejora** | `CHECKPOINTS.md`, hooks en `.claude/settings.json`, `tests/` |

## Para desarrollar con Claude Code

```bash
./init.sh   # debe terminar verde antes de cualquier sesión
```

Si todo está verde, abre `AGENTS.md` y sigue desde ahí.

## Flujo SDD

```
pending → [spec_author] → spec_ready → ⏸ HUMANO → in_progress → [implementer → reviewer] → done
```

1. El `leader` lanza `spec_author` → crea `specs/<feature>/{requirements,design,tasks}.md`.
2. La feature queda en `spec_ready`. **El leader para y pide aprobación humana.**
3. Aprobado → `in_progress`. El `implementer` sigue las tasks marcándolas `[x]`.
4. El `reviewer` verifica trazabilidad `R<n>` ↔ test. Si aprueba → `done`.

## Estructura

```
.
├── AGENTS.md              # Mapa para agentes (divulgación progresiva)
├── CHECKPOINTS.md         # Criterios de "estado final correcto"
├── feature_list.json      # Alcance: una feature a la vez
├── init.sh                # Verificación e inicialización (pytest)
├── docker-compose.yml     # Servicios nextjs + mongodb
├── Dockerfile             # Multi-stage build (builder + runner)
├── specs/<feature>/       # Spec por feature (Kiro-style)
│   ├── requirements.md    # EARS notation
│   ├── design.md          # Decisiones técnicas
│   └── tasks.md           # Checklist de implementación
├── progress/
│   ├── current.md         # Sesión activa (estado vivo)
│   └── history.md         # Bitácora append-only
├── docs/
│   ├── architecture.md    # Stack y capas del proyecto
│   ├── conventions.md     # TypeScript, Next.js, nombres
│   ├── specs.md           # Proceso SDD: EARS, 3 archivos, aprobación humana
│   └── verification.md    # Cómo demostrar que funciona
├── .claude/
│   ├── agents/            # leader, spec_author, implementer, reviewer
│   └── settings.json
├── src/
│   ├── app/               # Rutas y páginas Next.js (App Router)
│   ├── lib/               # Conexión MongoDB singleton
│   ├── models/            # Schemas Mongoose
│   ├── repositories/      # Capa de acceso a datos
│   ├── types/             # Interfaces TypeScript
│   └── components/        # Componentes React reutilizables
└── tests/
    └── test_project_scaffold.py   # Tests estructurales (pytest)
```
