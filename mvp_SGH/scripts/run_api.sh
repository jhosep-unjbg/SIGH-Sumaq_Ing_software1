#!/bin/bash
# Script para levantar la API en modo desarrollo (MVP)

set -e

cd "$(dirname "$0")/../apps/api"

echo "→ Instalando dependencias..."
pip install -r requirements.txt --quiet

echo "→ Iniciando SUMAQ API en http://localhost:8000"
echo "→ Documentación: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
