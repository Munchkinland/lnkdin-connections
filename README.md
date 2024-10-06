# lnkdin-connections

# Visualizador de Conexiones de LinkedIn

![circular_network_plot](https://github.com/user-attachments/assets/25c85e0a-4907-46a9-a297-fb80680ea0f3)

Esta es una aplicación de escritorio desarrollada en Python que permite visualizar datos de conexiones de LinkedIn a partir de un archivo CSV. La aplicación genera diferentes gráficos basados en los datos de las conexiones como empresa, puesto, red de conexiones y conexiones por fecha.

## Características

- **Cargar CSV**: Selecciona y carga un archivo CSV exportado de LinkedIn con los detalles de las conexiones.
- **Gráfico de Compañía**: Visualiza las 20 empresas con más conexiones en tu red.
- **Gráfico de Puestos**: Visualiza los 20 puestos con más conexiones en tu red.
- **Gráfico de Red**: Visualiza una red de conexiones entre empresas y puestos en tu red de LinkedIn.
- **Conexiones por Fecha**: Muestra un gráfico de líneas con la evolución de las conexiones por fecha.

## Tecnologías Utilizadas

- `pandas`: Para la manipulación y análisis de datos.
- `plotly`: Para la creación de gráficos interactivos.
- `networkx`: Para la visualización de redes.
- `tkinter`: Para la creación de la interfaz gráfica de la aplicación.
- `matplotlib`: Para la visualización y personalización de gráficos de redes.

## Requisitos

- Python 3.x
- Bibliotecas adicionales que puedes instalar con el siguiente comando:
  

pip install pandas plotly networkx matplotlib numpy
Uso

## Descargar el archivo CSV de LinkedIn:
Desde tu perfil de LinkedIn, ve a la sección de exportación de datos y descarga un archivo CSV con tus conexiones.

    Ejecutar la aplicación:
        Clona este repositorio o descarga el código fuente.
        Ejecuta el archivo main.py para iniciar la aplicación.

## Cargar archivo CSV:

    Haz clic en el botón 📂 Cargar CSV para seleccionar el archivo descargado de tus conexiones.

## Seleccionar tipo de visualización:

    Escoge entre las opciones disponibles:
        Gráfico de Compañía
        Gráfico de Puestos
        Gráfico de Red
        Conexiones por Fecha

## Mostrar visualización:

    Haz clic en 📊 Mostrar Visualización para generar el gráfico seleccionado.

## Estructura del Proyecto

.
├── main.py                      # Archivo principal para ejecutar la aplicación.

├── README.md                    # Documentación de la aplicación.

├── requirements.txt             # Dependencias del proyecto.

└── assets/                      # Carpeta para almacenar imágenes o gráficos generados.

## Licencia

Este proyecto está bajo la licencia MIT.
