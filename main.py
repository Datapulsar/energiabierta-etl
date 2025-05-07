import requests
import pandas as pd

# --- EXTRACCIÓN ---
short_url = "https://3b9x.short.gy/IlgSPa"
response = requests.get(short_url, allow_redirects=True)

if response.status_code == 200:
    content_type = response.headers.get('Content-Type', '')
    print("Redirección exitosa. Descargando el archivo.")
    print("Tipo de contenido:", content_type)

    if "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in content_type:
        file_path = 'C:/Users/datap/energiaabierta-etl/data.xlsx'

        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Archivo Excel guardado en: {file_path}")

        # --- TRANSFORMACIÓN ---
        try:
            df = pd.read_excel(file_path, engine="openpyxl")

            print("\nColumnas encontradas:")
            print(df.columns)

            # Mostrar primeras filas
            print("\nPrimeras filas:")
            print(df.head())

            # Limpieza básica
            df_clean = df.dropna(how='all')  # Elimina filas completamente vacías
            df_clean.columns = df_clean.columns.str.strip()  # Quita espacios en columnas
            df_clean = df_clean.loc[:, ~df_clean.columns.duplicated()]  # Quita columnas duplicadas

            # --- CARGA ---
            csv_path = 'C:/Users/datap/energiaabierta-etl/datos_limpios.csv'
            df_clean.to_csv(csv_path, index=False)
            print(f"\n✅ Datos limpios guardados en: {csv_path}")

        except Exception as e:
            print("❌ Error al procesar el archivo Excel:", e)
    else:
        print("⚠️ El contenido descargado no parece ser un archivo Excel.")
        print(response.content[:300])
else:
    print(f"❌ Error al seguir el enlace: Código {response.status_code}")
