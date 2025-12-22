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
│   ├── data_model/                 # Modelos de datos / entidades
│   ├── db/                         # Acceso a base de datos
│   ├── extract/                    # Extracción de datos (ej: ficheros/APIs)
│   └── etl/                        # Orquestación ETL
├── tests/                          # Tests (pytest)
│   ├── data/                       # Datos de test
│   ├── extract/
│   └── db/
├── data/                           # Datos entrada. Se mapea como volumen de docker.
├── sql/                            # Scripts SQL para la creación de la base de datos.
├── docker-compose.yml              # Fichero principal de la aplicación.
├── compose.tests.yaml              # Compose para ejecutar/depurar tests en Docker
├── compose.debug.yaml              # Compose para debugging
├── Dockerfile                      # Imagen Docker de la aplicación.
├── requirements.txt                # Dependencias Python de al aplicación
├── pytest.ini                      # Configuración pytest
├── run_local.env                   # Variables de entorno para ejecución local
├── diagrams.dio                    # Diagramas (draw.io)
├── Run ETL.sduml                   # Diagrama de secuencia (https://sequencediagram.org/)
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

- En local, ejecutar: `pytest` en la raiz del proyecto, que es donde está definido `pytest.ini`. 
- El plugin de "Python" de VSC también permite depurar desde el editor. Interpreta automáticamente el fichero de configuración de los tests.
- Para depurar en Docker, primero es necesario arrancar el servicio de base de datos del `docker-compose.yml`. Después arrancar el servicio definido en `compose.tests.yaml`. Tiene definida la app para arrancar con `pytest`.

## Debugging

### Local
- Con el plugin "Python Debugger", podemos depurar a través del entorno virtual instalado. VSC utilizará el fichero `run_local.env` para inyectar la configuración de entorno.
- Es necesario elegir la configuración de debugging de VSC "Python Debugger: Python File"

### Docker
- Para depurar en Docker, es necesario arrancar la aplicación en modo "debug" con el fichero `compose.debug.yaml`. Este servicio arranca la aplicación con "debugpy":
      
      /tmp/debugpy --wait-for-client --listen 0.0.0.0:5678 src/main.py 
      
   Y deja en espera el contenedor sin ejecutar, hasta que se reciba una conexión remota. Es **MUY IMPORTANTE** la configuración `restart: "unless-stopped"` que cada vez que termina un ciclo de depuración, reinicia el contenedor con el debugger, para que nos podamos volver a conectar con "remote attach" y así hacer más sencilla la depuración. 
   
   En VSC, tenemos que crear una conexión de RUN AND DEBUG "Python Debugger: Remote Attach", para conectarnos al contenedor en espera:
   
    ```bash
    {
      "name": "Python Debugger: Remote Attach",
      "type": "debugpy",
      "request": "attach",
      "connect": {
            "host": "localhost",
            "port": 5678
      },
      "pathMappings": [
            {
               "localRoot": "${workspaceFolder}/src", # ruta local al código
               "remoteRoot": "/app/src" # ruta al código en el contenedor
            }
      ]
   }
    ```
   La clave está en mapear el código local al código en el contenedor, a través de la propiedad `pathMappings` y definir el puerto de escucha del debugger en `connect`