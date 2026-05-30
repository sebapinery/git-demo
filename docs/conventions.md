# Convenciones de código

> Homogeneidad extrema. La IA predice mejor cuando el repositorio se parece
> a sí mismo en todas partes.

## Lenguaje y versiones

- **TypeScript** 5, strict mode activado (`"strict": true` en tsconfig.json).
- **Node.js** 20 LTS.
- **Next.js** 14 App Router. No usar Pages Router.

## Estilo

- Formato: Prettier por defecto (sin configuración adicional).
- Líneas: máximo 100 caracteres.
- Comillas: dobles `"..."` en TypeScript/TSX.
- Punto y coma: sí.

## Nombres

| Tipo | Convención | Ejemplo |
|---|---|---|
| Archivos de componente | `PascalCase.tsx` | `TaskFormModal.tsx` |
| Archivos de utilidad / lib | `camelCase.ts` | `mongodb.ts` |
| Archivos de modelo | `PascalCase.ts` | `Task.ts` |
| Archivos de repositorio | `camelCase.ts` | `taskRepository.ts` |
| Interfaces / Types | `PascalCase` | `Task`, `CreateTaskInput` |
| Componentes React | `PascalCase` | `TaskTable` |
| Funciones / variables | `camelCase` | `findAll`, `taskId` |
| Constantes de módulo | `UPPER_SNAKE` | `MONGODB_URI` |

## Estructura de archivo TypeScript

Cada archivo en `src/` sigue este orden:

```typescript
// 1. Imports externos (next, react, mongoose, etc.)
import { NextResponse } from "next/server";

// 2. Imports internos (lib, models, types, repositories)
import { connectToDatabase } from "@/lib/mongodb";
import { Task } from "@/models/Task";

// 3. Tipos locales si aplica
type CreateInput = { title: string; description?: string };

// 4. Implementación
```

## Alias de paths

Usar `@/` para imports absolutos desde `src/`:

```typescript
import { connectToDatabase } from "@/lib/mongodb";   // ✅
import { connectToDatabase } from "../../lib/mongodb"; // ❌
```

## API Routes (App Router)

- Usar `NextResponse.json()` para todas las respuestas.
- Códigos HTTP: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 404 (Not Found), 500 (Internal Server Error).
- Estructura de respuesta consistente:
  ```typescript
  // éxito
  NextResponse.json({ data: result }, { status: 200 })
  // error
  NextResponse.json({ error: "mensaje legible" }, { status: 400 })
  ```

## Tests estructurales (Python / pytest)

Los tests de infraestructura y scaffold se escriben en Python con pytest
porque el entorno de CI dispone de Python y los archivos a verificar son
de configuración (YAML, JSON, texto plano).

- Un archivo por feature de scaffold: `tests/test_<feature_name>.py`.
- Cada test function verifica exactamente un requisito (`R<n>`).
- Nombre descriptivo: `test_r1_compose_has_two_services`.
- Usar `pathlib.Path` para rutas, `re` o `yaml` para parsear contenido.

## Manejo de errores

- Las funciones de repositorio propagan errores de Mongoose sin capturar.
- Las API Routes capturan con `try/catch` y devuelven `{ error }` con el código HTTP apropiado.
- No usar `throw new Error("...")` con mensajes genéricos. El mensaje debe ser legible por el operador.

## Comentarios

Por defecto **no** se escriben. Solo cuando explican un *por qué* no obvio
(workaround documentado, invariante sutil). Los nombres deben hacer el resto.
