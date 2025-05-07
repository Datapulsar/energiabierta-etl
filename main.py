import os
import requests
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuración
SHORT_URL = "https://3b9x.short.gy/IlgSPa"
EXCEL_PATH = 'data.xlsx'
CSV_PATH = 'data.csv'
CREDENTIALS_PATH = 'credentials/client_secret_904574209764-ps80ppu2snj7rm8cukoqrpakrltlifan.apps.googleusercontent.com.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# 1. Descargar archivo desde la web
def download_excel(short_url, save_path):
    response = requests.get(short_url, allow_redirects=True)
    if response.status_code == 200:
        content_type = response.headers.get("Content-Type", "")
        if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in content_type or b'PK' in response.content[:2]:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Archivo Excel descargado: {save_path}")
        else:
            print("⚠️ El contenido no parece ser un archivo Excel.")
            print("Primeros caracteres:", response.content[:200])
    else:
        print(f"❌ Error al descargar el archivo: {response.status_code}")

# 2. Convertir Excel a CSV
def excel_to_csv(excel_path, csv_path):
    try:
        df = pd.read_excel(excel_path)
        df.to_csv(csv_path, index=False)
        print(f"✅ Archivo convertido a CSV: {csv_path}")
    except Exception as e:
        print(f"❌ Error al convertir Excel a CSV: {e}")

# 3. Subir archivo a Google Drive
def upload_to_drive(file_path, file_name):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='text/csv', resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ Archivo subido a Google Drive con ID: {file.get('id')}")

# 4. Ejecutar flujo completo
if __name__ == "__main__":
    download_excel(SHORT_URL, EXCEL_PATH)
    excel_to_csv(EXCEL_PATH, CSV_PATH)
    upload_to_drive(CSV_PATH, 'data.csv')
