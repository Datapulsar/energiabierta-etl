# 🔌 Energía Abierta ETL

Este proyecto realiza un proceso ETL (Extract, Transform, Load) utilizando información pública del portal [Energía Abierta](https://energiaabierta.cl/). El flujo incluye la descarga de archivos `.xlsx`, su conversión a `.csv` y posterior carga a Google Drive.

## 🚀 Características

- Descarga automatizada de datos en formato Excel desde enlaces dinámicos.
- Conversión y limpieza de los datos usando `pandas`.
- Subida del archivo procesado a una carpeta de Google Drive con autenticación OAuth.

## 🧰 Requisitos

- Python 3.8+
- Entorno virtual (`venv`)
- Archivo de credenciales OAuth de Google (`client_secret_XXXX.json`)

## 📦 Instalación

```bash
# Clona el repositorio
git clone https://github.com/Datapulsar/energiabierta-etl.git
cd energiaabierta-etl

# Crea y activa el entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# Instala dependencias
pip install -r requirements.txt
