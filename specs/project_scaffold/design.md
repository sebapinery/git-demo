# Design — project_scaffold

## Versiones fijadas

| Tecnología | Versión | Justificación |
|---|---|---|
| Node.js | 20 LTS (Alpine) | LTS activo, imagen Alpine minimiza tamaño del runner |
| Next.js | 14.x | App Router estable, soporte server components, RSC |
| TypeScript | 5.x | Incluido con Next.js 14 |
| MongoDB | 7.x | Última versión estable con soporte ARM/AMD64 |
| Mongoose | 8.x | Última versión con soporte completo a MongoDB 7 |

---

## Archivos a crear

```
.
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .dockerignore
├── next.config.ts
├── tsconfig.json
├── package.json
└── src/
    ├── app/
    │   ├── layout.tsx          # RootLayout del App Router
    │   └── page.tsx            # Página raíz (responde 200)
    ├── lib/
    │   └── mongodb.ts          # Singleton de conexión Mongoose
    ├── models/                 # (vacío, placeholder .gitkeep)
    ├── repositories/           # (vacío, placeholder .gitkeep)
    ├── types/                  # (vacío, placeholder .gitkeep)
    └── components/             # (vacío, placeholder .gitkeep)
```

Ningún archivo existente de `src/` o `tests/` se modifica (esta feature es el scaffold inicial).

---

## Dockerfile — estrategia multi-stage

```
Etapa 1: builder
  FROM node:20-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

Etapa 2: runner
  FROM node:20-alpine AS runner
  WORKDIR /app
  ENV NODE_ENV=production
  COPY --from=builder /app/.next/standalone ./
  COPY --from=builder /app/.next/static ./.next/static
  COPY --from=builder /app/public ./public
  EXPOSE 3000
  CMD ["node", "server.js"]
```

La salida `standalone` de Next.js (`output: 'standalone'` en `next.config.ts`) es la que permite copiar solo los artefactos necesarios sin `node_modules` completo. Esto reduce la imagen runner de ~1 GB a ~200 MB.

---

## docker-compose.yml — configuracion de servicios

### Servicio `mongodb`

- Imagen: `mongo:7`
- Puerto: `27017:27017`
- Volumen nombrado: `mongo_data:/data/db`
- Healthcheck: `mongosh --eval "db.adminCommand('ping')"` con `interval: 10s`, `timeout: 5s`, `retries: 5`, `start_period: 20s`
- Red: `app-network`

### Servicio `nextjs`

- Build: `.` (Dockerfile en raíz)
- Puerto: `3000:3000`
- Variables de entorno: `MONGODB_URI` tomada del archivo `.env` del operador via `env_file: .env`
- `depends_on: mongodb: condition: service_healthy`
- Healthcheck: `curl -f http://localhost:3000 || exit 1` con `interval: 15s`, `timeout: 5s`, `retries: 3`, `start_period: 30s`
- Red: `app-network`

### Volúmenes y redes

```yaml
volumes:
  mongo_data:

networks:
  app-network:
    driver: bridge
```

---

## src/lib/mongodb.ts — firma exportada

```typescript
// Singleton pattern para evitar múltiples conexiones en desarrollo (hot reload)
let cached: mongoose.Connection | null = null;

export async function connectToDatabase(): Promise<mongoose.Connection>
```

La función lee `process.env.MONGODB_URI`. Si la variable no está definida, lanza `Error('MONGODB_URI environment variable is not defined')` antes de intentar conectar. Este comportamiento cubre R18.

---

## Alternativa descartada: imagen base `node:20` (no Alpine)

Se evaluó usar `node:20` (Debian) como imagen base del runner por mayor compatibilidad de herramientas de sistema. Se descartó porque:

1. El tamaño de la imagen runner sería ~350 MB vs ~180 MB con Alpine.
2. El scaffold no requiere herramientas de sistema adicionales (compiladores nativos, `glibc`-only libs).
3. Alpine es la opción recomendada por la documentación oficial de Next.js para producción.

Si en el futuro una dependencia nativa requiere `glibc`, se migrará a `node:20-slim` (Debian slim).

---

## Alternativa descartada: conexión directa con `mongodb` driver (sin Mongoose)

Se evaluó usar el driver oficial `mongodb` (sin Mongoose) para la capa de persistencia. Se descartó porque:

1. El proyecto usará modelos con esquema (features futuras lo requieren: `src/models/`).
2. Mongoose 8 ofrece validación de esquema, middleware y tipado TypeScript con `@types/mongoose` integrado.
3. El overhead de Mongoose sobre el driver nativo es insignificante para el volumen esperado.
