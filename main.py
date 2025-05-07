import os
import requests
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from drive_functions import (
    subir_csv_a_drive,
    buscar_o_crear_carpeta,
    buscar_archivo_por_nombre,
    eliminar_archivo_de_drive
)

def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    token_path = 'token.json'
    client_secret_path = 'credentials/client_secret_904574209764-ps80ppu2snj7rm8cukoqrpakrltlifan.apps.googleusercontent.com.json'

    if os.path.exists(token_path):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def descargar_excel_desde_web(url, ruta_destino):
    response = requests.get(url)
    response.raise_for_status()
    with open(ruta_destino, 'wb') as f:
        f.write(response.content)
    print(f"Archivo Excel descargado en: {ruta_destino}")

def main():
    service = authenticate_google_drive()

    # 1. Descargar archivo Excel
    os.makedirs("data", exist_ok=True)
    ruta_excel = "data/archivo.xlsx"
    url = "https://3b9x.short.gy/IlgSPa"
    descargar_excel_desde_web(url, ruta_excel)

    # 2. Convertir a CSV
    df = pd.read_excel(ruta_excel)
    ruta_csv = "data/archivo.csv"
    df.to_csv(ruta_csv, index=False)
    print(f"Archivo CSV guardado en: {ruta_csv}")

    # 3. Buscar o crear carpeta en Google Drive
    carpeta_drive_id = buscar_o_crear_carpeta(service, "Datos Energía Abierta")

    # 4. Verificar si ya existe el archivo y eliminarlo
    file_id_existente = buscar_archivo_por_nombre(service, "archivo.csv", carpeta_drive_id)
    if file_id_existente:
        eliminar_archivo_de_drive(service, file_id_existente)
        print("Archivo existente en Google Drive eliminado.")

    # 5. Subir el nuevo archivo CSV
    subir_csv_a_drive(service, ruta_csv, carpeta_drive_id)

if __name__ == '__main__':
    main()
