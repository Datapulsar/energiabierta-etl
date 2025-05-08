import os
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import pandas as pd

def load_csv_from_drive(service, file_id):
    """Descarga un archivo CSV desde Google Drive y lo carga como DataFrame"""
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    df = pd.read_csv(fh)
    return df

def subir_csv_a_drive(service, ruta_local, folder_id=None):
    """Sube un archivo CSV a una carpeta específica en Google Drive"""
    file_metadata = {'name': os.path.basename(ruta_local)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    media = MediaFileUpload(ruta_local, mimetype='text/csv')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Archivo subido a Drive con ID: {file.get('id')}")

def subir_archivo_a_drive(service, ruta_local, folder_id=None):
    """Sube un archivo a una carpeta específica en Google Drive (generalizado para cualquier tipo de archivo)"""
    file_metadata = {'name': os.path.basename(ruta_local)}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    # Establecer el tipo MIME según la extensión del archivo
    if ruta_local.endswith('.csv'):
        mimetype = 'text/csv'
    elif ruta_local.endswith('.pdf'):
        mimetype = 'application/pdf'
    elif ruta_local.endswith('.docx'):
        mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    else:
        mimetype = 'application/octet-stream'  # Para otros tipos de archivo
    
    media = MediaFileUpload(ruta_local, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Archivo {os.path.basename(ruta_local)} subido a Google Drive con ID: {file.get('id')}")

def buscar_o_crear_carpeta(service, nombre_carpeta):
    """Busca una carpeta en Google Drive o la crea si no existe"""
    query = f"mimeType='application/vnd.google-apps.folder' and name='{nombre_carpeta}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']
    else:
        file_metadata = {'name': nombre_carpeta, 'mimeType': 'application/vnd.google-apps.folder'}
        file = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Carpeta '{nombre_carpeta}' creada en Google Drive.")
        return file.get('id')

def buscar_archivo_por_nombre(service, nombre_archivo, carpeta_id):
    """Busca un archivo dentro de una carpeta específica por su nombre"""
    query = f"name = '{nombre_archivo}' and '{carpeta_id}' in parents and trashed = false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    archivos = results.get('files', [])
    return archivos[0]['id'] if archivos else None

def eliminar_archivo_de_drive(service, file_id):
    """Elimina un archivo de Google Drive usando su ID"""
    service.files().delete(fileId=file_id).execute()
    print(f"Archivo con ID {file_id} eliminado de Google Drive.")