import pandas as pd
import matplotlib.pyplot as plt

def graficar_datos(df, ruta_imagen):
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df = df.sort_values("Fecha")

    plt.figure(figsize=(10, 5))
    plt.plot(df["Fecha"], df["Emisiones CO2 toneladas métricas per capita"], marker='o')
    plt.title("Evolución de Emisiones de CO₂ per cápita")
    plt.xlabel("Año")
    plt.ylabel("Toneladas métricas per cápita")
    plt.grid(True)
    plt.tight_layout()

    # Guardar el gráfico como imagen
    plt.savefig(ruta_imagen, format='png')
    plt.close()  # Cerrar la figura para liberar memoria

    print(f"Gráfico guardado en: {ruta_imagen}")
    return ruta_imagen  # Devolver la ruta de la imagen guardada

if __name__ == "__main__":
    # Cargar el archivo CSV
    ruta_csv = "data/archivo.csv"
    df = pd.read_csv(ruta_csv)

    # Ruta para guardar la imagen
    ruta_imagen = "data/grafico_emisiones.png"
    
    # Generar gráfico
    graficar_datos(df, ruta_imagen)

