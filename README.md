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

1. Inicia los servicios: `docker-compose up -d`
2. Abre tu navegador en: http://localhost:8978
- Datos de conexión:
   - **Server Host**: `db` (nombre del servicio en Docker)
   - **Port**: `5432`
   - **Database**: `pruebas`
   - **Username**: `myuser`
   - **Password**: `mypassword`


## Estructura del Proyecto

```
.
├── src/                            # Código fuente
│   ├── main.py
│   ├── pytest.ini                  # Config pytest (si ejecutas desde src/)
│   ├── data_model/                 # Modelos de datos / entidades
│   ├── db/                         # Acceso a datos / repositorios / conexiones
│   ├── extract/                    # Extracción de datos (ej: ficheros/APIs)
│   └── etl/                        # Orquestación ETL
├── tests/                          # Tests (pytest)
│   ├── data/                       # Datos de test
│   ├── extract/
│   └── db/
├── data/                           # Datos de ejemplo / entrada
├── sql/                            # Scripts SQL
├── docker-compose.yml              # Servicios Docker (DB, CloudBeaver, etc.)
├── compose.tests.yaml              # Compose para ejecutar/depurar tests en Docker
├── compose.debug.yaml              # Compose para debugging
├── Dockerfile                      # Imagen Docker
├── requirements.txt                # Dependencias Python
├── pytest.ini                      # Configuración pytest
├── run_local.env                   # Variables de entorno para ejecución local
├── diagrams.dio                    # Diagramas (draw.io)
├── Run ETL.sduml                   # Diagrama/flujo (StarUML)
├── .vscode/
│   └── settings.json               # Config VS Code (opcional)
├── .gitignore                      # Git ignore
└── README.md                       # Este archivo
```

## Desarrollo

Coloca tu código en `src/` y crea tests correspondientes en `tests/`.

## Ejecución en local

- La aplicación está preparada para ejecutarse en Docker, con docker-compose.
Desde el docker-compose se inyectan las variables de entorno necesarias para la ejecución,
como los parámetros de conexión a la base de datos.
- Para la ejecución en local desde VS Code, podemos utilizar un fichero de variables de entorno `run_local.env`
e indicarlo en el fichero `settings.json` de VSC:

```bash
"python.envFile": "${workspaceFolder}/run_local.env"
```

De esta manera, VS Code utiliza este fichero tanto para la ejecución de tests como para la ejecución normal.

## Testing

### Ejecutar todos los tests

- En local, ejecutar: `pytest`

- Para depurar en Docker, arrancar el servicio definido en `compose.tests.yaml`. Tiene definida la app para arrancar con `pytest`.

## Debugging

- En local, con el plugin "Python Debugger", podemos depurar a través del entorno virtual instalado.
