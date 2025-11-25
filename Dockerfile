FROM python:3.11-slim

# Ruta absoluta dentro del contenedor donde se instala la aplicación
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

CMD ["python", "main.py"]