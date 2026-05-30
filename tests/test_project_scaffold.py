"""
Tests estructurales para la feature project_scaffold.
Cubren R1-R18 de specs/project_scaffold/requirements.md sin necesitar
Docker en ejecucion.
"""
import re
from pathlib import Path

import pytest

# Raiz del repositorio (dos niveles por encima de tests/)
ROOT = Path(__file__).parent.parent

COMPOSE = ROOT / "docker-compose.yml"
DOCKERFILE = ROOT / "Dockerfile"
NEXT_CONFIG = ROOT / "next.config.ts"
ENV_EXAMPLE = ROOT / ".env.example"
MONGODB_TS = ROOT / "src" / "lib" / "mongodb.ts"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compose_text() -> str:
    return COMPOSE.read_text()


def _dockerfile_text() -> str:
    return DOCKERFILE.read_text()


# ---------------------------------------------------------------------------
# R1 — docker-compose.yml define exactamente los servicios nextjs y mongodb
# ---------------------------------------------------------------------------

def test_r1_compose_has_two_services():
    text = _compose_text()
    # Detecta las claves de primer nivel bajo "services:"
    # Buscamos patron: linea que empieza con dos espacios + nombre + ":"
    services = re.findall(r"^\s{2}(\w[\w-]*):\s*$", text, re.MULTILINE)
    # Filtramos solo los que estan despues de "services:" y antes de
    # "volumes:" / "networks:" usando el bloque services del texto
    services_block_match = re.search(
        r"^services:\n(.*?)(?=^\w|\Z)", text, re.MULTILINE | re.DOTALL
    )
    assert services_block_match, "No se encontro el bloque 'services:' en docker-compose.yml"
    services_block = services_block_match.group(1)
    top_keys = re.findall(r"^\s{2}(\w[\w-]*):\s*$", services_block, re.MULTILINE)
    assert set(top_keys) == {"nextjs", "mongodb"}, (
        f"Se esperaban exactamente los servicios 'nextjs' y 'mongodb', "
        f"pero se encontraron: {top_keys}"
    )


# ---------------------------------------------------------------------------
# R2, R3 — puertos configurados (test estructural)
# ---------------------------------------------------------------------------

def test_r2_r3_ports_configured():
    text = _compose_text()
    assert "3000:3000" in text, "Puerto 3000:3000 no encontrado en docker-compose.yml"
    assert "27017:27017" in text, "Puerto 27017:27017 no encontrado en docker-compose.yml"


# ---------------------------------------------------------------------------
# R4 — depends_on con condition: service_healthy
# ---------------------------------------------------------------------------

def test_r4_depends_on_service_healthy():
    text = _compose_text()
    assert "condition: service_healthy" in text, (
        "No se encontro 'condition: service_healthy' en docker-compose.yml"
    )


# ---------------------------------------------------------------------------
# R5 — Dockerfile tiene exactamente una etapa builder y una etapa runner
# ---------------------------------------------------------------------------

def test_r5_dockerfile_two_stages():
    text = _dockerfile_text()
    builder_lines = re.findall(r"^FROM\s+\S+\s+AS\s+builder\s*$", text, re.MULTILINE | re.IGNORECASE)
    runner_lines = re.findall(r"^FROM\s+\S+\s+AS\s+runner\s*$", text, re.MULTILINE | re.IGNORECASE)
    assert len(builder_lines) == 1, (
        f"Se esperaba exactamente 1 linea 'FROM ... AS builder', se encontraron: {len(builder_lines)}"
    )
    assert len(runner_lines) == 1, (
        f"Se esperaba exactamente 1 linea 'FROM ... AS runner', se encontraron: {len(runner_lines)}"
    )


# ---------------------------------------------------------------------------
# R6 — la etapa builder usa node:20
# ---------------------------------------------------------------------------

def test_r6_builder_uses_node20():
    text = _dockerfile_text()
    # Linea de la forma: FROM node:20... AS builder
    match = re.search(r"^FROM\s+(node:20\S*)\s+AS\s+builder\s*$", text, re.MULTILINE | re.IGNORECASE)
    assert match, (
        "La etapa 'builder' en Dockerfile no usa una imagen node:20"
    )


# ---------------------------------------------------------------------------
# R7 — next.config.ts tiene output standalone
# ---------------------------------------------------------------------------

def test_r7_standalone_output():
    text = NEXT_CONFIG.read_text()
    assert "standalone" in text, (
        "'standalone' no encontrado en next.config.ts"
    )


# ---------------------------------------------------------------------------
# R8 — .env.example contiene MONGODB_URI con valor que empieza por mongodb://
# ---------------------------------------------------------------------------

def test_r8_env_example_has_mongodb_uri():
    text = ENV_EXAMPLE.read_text()
    match = re.search(r"^MONGODB_URI\s*=\s*(mongodb://\S+)", text, re.MULTILINE)
    assert match, (
        ".env.example no contiene 'MONGODB_URI=mongodb://...' con valor valido"
    )


# ---------------------------------------------------------------------------
# R9 — env_file configurado en el servicio nextjs (test estructural)
# ---------------------------------------------------------------------------

def test_r9_env_file_configured():
    text = _compose_text()
    assert "env_file" in text, (
        "No se encontro 'env_file' en docker-compose.yml"
    )


# ---------------------------------------------------------------------------
# R10 — healthcheck de mongodb contiene mongosh y db.adminCommand
# ---------------------------------------------------------------------------

def test_r10_healthcheck_mongodb():
    text = _compose_text()
    assert "mongosh" in text, "Healthcheck de mongodb no contiene 'mongosh'"
    assert "db.adminCommand" in text, (
        "Healthcheck de mongodb no contiene 'db.adminCommand'"
    )


# ---------------------------------------------------------------------------
# R11 — healthcheck de nextjs contiene curl y localhost:3000
# ---------------------------------------------------------------------------

def test_r11_healthcheck_nextjs():
    text = _compose_text()
    assert "curl" in text, "Healthcheck de nextjs no contiene 'curl'"
    assert "localhost:3000" in text, (
        "Healthcheck de nextjs no contiene 'localhost:3000'"
    )


# ---------------------------------------------------------------------------
# R12 — paginas raiz existen (test estructural)
# ---------------------------------------------------------------------------

def test_r12_root_page_exists():
    page = ROOT / "src" / "app" / "page.tsx"
    layout = ROOT / "src" / "app" / "layout.tsx"
    assert page.exists(), f"No se encontro {page}"
    assert layout.exists(), f"No se encontro {layout}"


# ---------------------------------------------------------------------------
# R13 — estructura de directorios del proyecto
# ---------------------------------------------------------------------------

def test_r13_directory_structure():
    expected_dirs = [
        ROOT / "src" / "app",
        ROOT / "src" / "lib",
        ROOT / "src" / "models",
        ROOT / "src" / "repositories",
        ROOT / "src" / "types",
        ROOT / "src" / "components",
    ]
    for d in expected_dirs:
        assert d.is_dir(), f"Directorio esperado no encontrado: {d}"


# ---------------------------------------------------------------------------
# R14 — src/lib/mongodb.ts exporta connectToDatabase
# ---------------------------------------------------------------------------

def test_r14_mongodb_ts_exports_connect():
    text = MONGODB_TS.read_text()
    assert "connectToDatabase" in text, (
        "src/lib/mongodb.ts no contiene 'connectToDatabase'"
    )


# ---------------------------------------------------------------------------
# R15 — volumen mongo_data montado en /data/db
# ---------------------------------------------------------------------------

def test_r15_mongo_volume():
    text = _compose_text()
    assert "mongo_data" in text, "No se encontro 'mongo_data' en docker-compose.yml"
    assert "/data/db" in text, "No se encontro '/data/db' en docker-compose.yml"


# ---------------------------------------------------------------------------
# R16 — red app-network compartida entre ambos servicios
# ---------------------------------------------------------------------------

def test_r16_shared_network():
    text = _compose_text()
    # app-network debe aparecer al menos 3 veces:
    # una por servicio y una en la declaracion de redes
    occurrences = text.count("app-network")
    assert occurrences >= 3, (
        f"'app-network' aparece solo {occurrences} veces en docker-compose.yml; "
        "se esperaban al menos 3 (una por servicio + declaracion)"
    )


# ---------------------------------------------------------------------------
# R17 — .env.example tiene al menos una linea de comentario
# ---------------------------------------------------------------------------

def test_r17_env_example_has_comment():
    text = ENV_EXAMPLE.read_text()
    comment_lines = [line for line in text.splitlines() if line.strip().startswith("#")]
    assert len(comment_lines) >= 1, (
        ".env.example no contiene ninguna linea de comentario (#)"
    )


# ---------------------------------------------------------------------------
# R18 — mongodb.ts lanza error mencionando MONGODB_URI si no esta definida
# ---------------------------------------------------------------------------

def test_r18_mongodb_uri_error():
    text = MONGODB_TS.read_text()
    assert "MONGODB_URI" in text, (
        "src/lib/mongodb.ts no menciona 'MONGODB_URI' en su mensaje de error"
    )
    # Verificamos que hay un throw/raise o similar junto a MONGODB_URI
    error_pattern = re.search(
        r"(throw|Error|raise).*MONGODB_URI|MONGODB_URI.*(throw|Error|raise)",
        text,
        re.DOTALL,
    )
    assert error_pattern, (
        "src/lib/mongodb.ts no contiene un lanzamiento de error relacionado con MONGODB_URI"
    )
