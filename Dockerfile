# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . /app

# Instala las dependencias necesarias
RUN pip install --no-cache-dir requests beautifulsoup4 selenium

# Instala herramientas adicionales para capturas de pantalla
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Descarga e instala el controlador de ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/ \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Expone el puerto 22 para SSH
EXPOSE 22

# Comando por defecto
CMD ["bash"]