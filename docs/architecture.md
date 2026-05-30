# Arquitectura — Qué significa "hacer un buen trabajo"

> Este documento define el estándar de calidad. Los agentes revisores
> evalúan código contra este archivo. Si no está aquí, no es un requisito.

## Stack

- **Frontend + Backend:** Next.js 14 (App Router, React Server Components)
- **Base de datos:** MongoDB 7 via Mongoose 8
- **Infraestructura:** Docker Compose (servicios `nextjs` y `mongodb`)
- **Lenguaje:** TypeScript 5 (strict mode)

## Capas y responsabilidades

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| Modelos | `src/models/` | Schema Mongoose, validación en base de datos |
| Repositorio | `src/repositories/` | Operaciones CRUD, abstracción de Mongoose |
| API Routes | `src/app/api/` | Endpoints REST, validación de entrada, respuestas HTTP |
| Componentes | `src/components/` | Componentes React reutilizables (tabla, modal, formulario) |
| Páginas | `src/app/` | Rutas Next.js, composición de componentes |
| Utilidades | `src/lib/` | Conexión DB singleton, helpers compartidos |
| Tipos | `src/types/` | Interfaces y tipos TypeScript compartidos |

## Flujo de datos

```
Navegador
  │
  ├─ GET / → src/app/page.tsx → fetch /api/tasks → taskRepository.findAll()
  │
  ├─ POST /api/tasks → src/app/api/tasks/route.ts → taskRepository.create()
  │
  ├─ PUT /api/tasks/[id] → src/app/api/tasks/[id]/route.ts → taskRepository.update()
  │
  └─ DELETE /api/tasks/[id] → src/app/api/tasks/[id]/route.ts → taskRepository.remove()
                                        │
                                  MongoDB (mongoose)
```

## Reglas de cada capa

### Modelos (`src/models/`)
- Un archivo por entidad: `Task.ts`.
- El schema define los campos, tipos, validaciones y timestamps.
- No contiene lógica de negocio.

### Repositorio (`src/repositories/`)
- Funciones puras que llaman a Mongoose. Sin lógica HTTP.
- Firma: `findAll()`, `findById(id)`, `create(data)`, `update(id, data)`, `remove(id)`.
- Propaga errores de Mongoose; no los captura.

### API Routes (`src/app/api/`)
- Validan la entrada con Early Return (400 si falta campo requerido).
- Llaman al repositorio y mapean errores a códigos HTTP (404, 500).
- Devuelven siempre JSON con `{ data }` en éxito o `{ error }` en fallo.

### Componentes (`src/components/`)
- Un componente por responsabilidad: `TaskTable`, `TaskFormModal`.
- Estado local con `useState`; comunicación padre→hijo via props.
- Actualizaciones de tabla via callback del padre, no recarga de página.

## Qué NO hacer

- No mezclar lógica de repositorio en las API Routes.
- No hacer fetch directamente desde componentes sin pasar por una API Route.
- No usar `any` en TypeScript. Definir tipos en `src/types/`.
- No dejar `console.log` de debug en producción.
- No gestionar la conexión a MongoDB fuera de `src/lib/mongodb.ts`.
