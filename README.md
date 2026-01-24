# DataEng Patterns

**Proyecto para la gestión de los gastos bancarios familiares.**

El proyecto está montado en una arquitectura sobre Docker, utilizando docker compose para los servicios de base de datos, la ETL de carga, el notebook de jupyter para el análisis, los test de la ETL y el entorno de debuging. Python es el lenguaje de programación.

Visual Studio Code se utiliza para el desarrollo y debugging local y la ejecución local de los tests, aunque tanto la ETL como los tests están también dockerizados, para máxima compatibilidad con el entorno de producción durante el desarrollo. 

El proyecto consta de dos base de datos, una de **test** para desarrollo y pruebas y otra de **producción** donde sólo se ejecuta la versión dockerizada y testeada de la ETL de carga.

Existen tres artefactos ejecutables:
- La ETL de carga de datos bancarios.
- La base de datos de almacenamiento.
- El jupyter notebook analítico.

![](/diagrams/artifacts.png)

## Ejecución del proyecto

Existen dos acciones principales a realizar en el proyecto: actualizar la base de datos con nuevos datos y revisar y analizar los mismos a través del notebook. En ambos casos, la primera acción a realizar es levantar la base de datos.

```bash
docker-compose -f compose.db.yml up -d
```

También podemos acceder directamente a la base de datos, a través del servicio de **CloudBeaver**

```bash
http://localhost:8978/
```

Nos logamos en CloudBeaver como administradores, para acceder a todas las bases de datos registradas

- usr: cbadmin
-  pass: s5Z@33FHaGukh5B


### Actualizar datos en la base de datos

1. Actualizar el nombre del fichero de datos a cargar.
   - Para ello, editar el fichero ```src\extract\extract_ing.py```, cambiando la función ```_get_file_path``` para que devuelva el fichero a cargar.
   - El sistema deduplica los movimientos por fecha_valor, importe y saldo, quedándose con el más reciente en caso de conflicto.
2. Ejecutar la ETL ``` docker-compose -f compose.etl.run.prod.yml up -d ```
3. Refrescar la vista materializada.
   - Ejecutar ```REFRESH MATERIALIZED VIEW CONCURRENTLY bancapp.movimientos_mview``` en la base de datos.

### Revisar y refinar la analítica del proyecto

Para ello, vamos a utilizar la imagen de docker del código de la ETL, dado que tiene las clases de conexión a la base de datos y las vamos a utilizar en el notebook de análisis.

Lanzamos el comando para levantar una sesión de jupyter dockerizada

```bash
docker-compose -f compose.analytics.prod.yaml up -d
```
y accedemos a [Jupyter](http://127.0.0.1:8888/lab/workspaces/auto-p/tree/notebooks)

## Estructura del Proyecto

```
.
├── src/                            # Código fuente
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
├── notebooks/                      # Notebooks de análisis
├── querys/                         # Consultas SQL ad-hoc
├── compose.db.yml                  # Fichero principal de la aplicación.
├── compose.etl.tests.yaml          # Compose para ejecutar/depurar tests en Docker
├── compose.etl.debug.yaml          # Compose para debugging
├── compose.analytics.prod.yaml     # Compose para la ejecución de jupyter lab (prod bd)
├── compose.analytics.test.yaml     # Compose para la ejecución de jupyter lab (test bd)
├── compose.etl.prod.yml            # Compose para la ejecución de la etl(prod bd)
├── Dockerfile                      # Imagen Docker de la aplicación.
├── requirements.txt                # Dependencias Python de al aplicación
├── pytest.ini                      # Configuración pytest
├── run_local.env                   # Variables de entorno para ejecución local
├── diagrams.dio                    # Diagramas (draw.io)
├── Run ETL.sduml                   # Diagrama de secuencia (https://sequencediagram.org/)
├── .gitignore                      # Git ignore
└── README.md                       # Este archivo
```

## Desarrollo

## Instalación de Python en local

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

Coloca tu código en `src/` y crea tests correspondientes en `tests/`.

## Ejecución

### Local desde VSC

- Para la ejecución en local desde VS Code, podemos utilizar un fichero de variables de entorno run_local.env` e indicarlo en el fichero `settings.json` de VSC:

```bash
"python.envFile": "${workspaceFolder}/run_local.env"
```

De esta manera, VS Code utiliza este fichero tanto para la ejecución de tests como para la ejecución normal.

### Docker

- La aplicación está preparada para ejecutarse en Docker, con docker-compose.
Desde el docker-compose se inyectan las variables de entorno necesarias para la ejecución,
como los parámetros de conexión a la base de datos.

```bash
docker compose -f <compose.yaml> up --build
```


## Testing

### Ejecutar todos los tests

- En local, ejecutar: `pytest` en la raiz del proyecto, que es donde está definido `pytest.ini`. 
- El plugin de "Python" de VSC también permite depurar desde el editor. Interpreta automáticamente el fichero de configuración de los tests.
- Para depurar en Dockervhay que arrancar el servicio definido en `compose.tests.yaml`. Tiene definida la app para arrancar con `pytest`.

## Debugging

### Local
- Con el plugin "Python Debugger", podemos depurar a través del entorno virtual instalado. VSC utilizará el fichero `run_local.env` para inyectar la configuración de entorno.
- Es necesario elegir la configuración de debugging de VSC "Python Debugger: Python File"

### Docker
- Para depurar en Docker, es necesario arrancar la aplicación en modo "debug" con el fichero `compose.etl.debug.yaml`. Este servicio arranca la aplicación con "debugpy":
      
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

## Ejecución de la ETL



## Source Control

### Git commands

- Sincronizar con remoto (+borrado de ramas no existentes)

   ```bash
      git fetch --prune
   ```

- Revisar ramas existentes en local y remoto

   ```
      git branch -avv
   ```

   - -a: ramas en local y remoto
   - -v: verboso
   - -v: indica el enlace entre las ramas locales y las remotas

- Diferencias a nivel de fichero entre la rama actual y otra rama

   ```
      git diff --stat main 
   ```

   Compara la rama actual con "main".
