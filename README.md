# DataEng Patterns

Proyecto Python para patrones de ingeniería de datos.

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Docker

### Iniciar servicios con Docker Compose
```bash
# Iniciar todos los servicios en background
docker-compose up -d

# Ver logs de los servicios
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

## Conexión a Base de Datos

El proyecto incluye PostgreSQL y CloudBeaver en `docker-compose.yml`. 

### Opción 1: CloudBeaver (navegador web)
1. Inicia los servicios: `docker-compose up -d`
2. Abre tu navegador en: http://localhost:8978
3. Crea una nueva conexión a PostgreSQL:
   - Click en **Connections** → **Create New Connection**
   - Selecciona **PostgreSQL**
   - Completa los datos:
     - **Server Host**: `db` (nombre del servicio en Docker)
     - **Port**: `5432`
     - **Database**: `pruebas`
     - **Username**: `myuser`
     - **Password**: `mypassword`
   - Click en **Test Connection** para verificar
   - Click en **Finish** para guardar

### Opción 2: DBeaver Desktop (recomendado)
1. Descarga DBeaver desde: https://dbeaver.io/download/
2. Abre DBeaver
3. Crea una nueva conexión: **Database** → **New Database Connection**
4. Selecciona **PostgreSQL** y completa los siguientes datos:
   - **Server Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `pruebas`
   - **Username**: `myuser`
   - **Password**: `mypassword`
5. Click en **Test Connection** para verificar
6. Click en **Finish** para guardar

### Opción 3: Desde aplicación Python
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="pruebas",
    user="myuser",
    password="mypassword"
)
cursor = conn.cursor()
# Ejecutar queries...
cursor.close()
conn.close()
```

## Testing

### Ejecutar todos los tests
```bash
pytest
```

### Ejecutar solo tests unitarios
```bash
pytest -m unit
```

### Ejecutar solo tests de integración
```bash
pytest -m integration
```

### Ejecutar un archivo específico
```bash
pytest tests/unit/test_example.py
```

### Ejecutar un test específico
```bash
pytest tests/unit/test_example.py::test_sample_data
```

### Ver cobertura de código
```bash
pytest --cov=src --cov-report=html
```
Luego abre `htmlcov/index.html` en tu navegador.

### Ejecutar tests en modo verbose
```bash
pytest -v
```

## Estructura del Proyecto

```
.
├── src/                          # Código fuente
│   ├── __init__.py
│   └── core/                     # Módulo principal
│       └── __init__.py
├── tests/                        # Tests
│   ├── __init__.py
│   ├── conftest.py              # Configuración pytest y fixtures
│   ├── unit/                    # Tests unitarios
│   │   ├── __init__.py
│   │   └── test_example.py
│   ├── integration/             # Tests de integración
│   │   └── __init__.py
│   └── fixtures/                # Fixtures de datos
├── docker-compose.yml           # Servicios Docker
├── Dockerfile                   # Imagen Docker
├── requirements.txt             # Dependencias Python
├── pytest.ini                   # Configuración pytest
├── .gitignore                   # Git ignore
└── README.md                    # Este archivo
```

## Desarrollo

Coloca tu código en `src/` y crea tests correspondientes en `tests/unit/` o `tests/integration/`.

Los tests deben:
- Empezar con `test_`
- Estar en archivos que empiecen con `test_` o terminen con `_test.py`
- Usar fixtures de `conftest.py` cuando sea posible
- Incluir marcadores (`@pytest.mark.unit`, `@pytest.mark.integration`, etc.)
