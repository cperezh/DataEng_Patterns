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

## Testing

### Ejecutar todos los tests
```bash
pytest
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

Coloca tu código en `src/` y crea tests correspondientes en `test`.

Los tests deben:
- Empezar con `test_`
- Estar en archivos que empiecen con `test_` o terminen con `_test.py`
- Usar fixtures de `conftest.py` cuando sea posible
- Incluir marcadores (`@pytest.mark.unit`, `@pytest.mark.integration`, etc.)

## Ejecución en local

La aplicación está preparada para ejecutarse en Docker, con docker-compose.
Desde el docker-compose se inyectan las variables de entorno necesarias para la ejecución,
como los parámetros de conexión a la base de datos.
Para la ejecución en local, podemos utilizar un fichero de variables de entorno `run_local.env`
e indicarlo en el fichero `settings.json` de VSC:

```
"python.envFile": "${workspaceFolder}/run_local.env"
```
De esta manera, VSC utiliza este fichero para la ejecución de test como para la ejecución normal.