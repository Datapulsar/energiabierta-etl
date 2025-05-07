import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from drive_functions import (
    load_csv_from_drive,
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

def main():
    service = authenticate_google_drive()

    # Buscar carpeta destino
    carpeta_drive_id = buscar_o_crear_carpeta(service, "Datos Energía Abierta")

    # Buscar archivo existente en la carpeta
    nombre_archivo = "archivo.csv"
    file_id = buscar_archivo_por_nombre(service, nombre_archivo, carpeta_drive_id)

    if file_id:
        # Si el archivo ya existe, lo eliminamos primero
        eliminar_archivo_de_drive(service, file_id)
        print(f"Archivo '{nombre_archivo}' existente eliminado de Google Drive.")

    # Crear nuevo DataFrame (aquí puedes insertar tu lógica ETL real)
    import pandas as pd
    df = pd.DataFrame([{"mensaje": "nuevo archivo generado"}])  # Cambiar por tus datos reales
    print("Nuevo archivo generado:")
    print(df.head())

    # Guardar localmente
    os.makedirs("data", exist_ok=True)
    ruta_csv = os.path.join("data", nombre_archivo)
    df.to_csv(ruta_csv, index=False)
    print(f"Archivo CSV guardado en: {ruta_csv}")

    # Subir el archivo nuevo a la carpeta de Google Drive
    subir_csv_a_drive(service, ruta_csv, carpeta_drive_id)

if __name__ == '__main__':
    main()
