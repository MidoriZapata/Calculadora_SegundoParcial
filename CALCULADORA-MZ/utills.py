# utils.py
import pandas as pd
import matplotlib
# For embedding matplotlib into Tkinter in Spyder it's safe to use TkAgg
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import csv
import os

# --- Exportación ---
def export_csv(numeros):
    ruta = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV files", "*.csv")])
    if ruta:
        with open(ruta, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Índice", "Número"])
            for i, num in enumerate(numeros):
                writer.writerow([i+1, float(num)])
        print(f"Archivo guardado en {ruta}")

def exportar_a_excel(datos, nombre="datos.xlsx"):
    df = pd.DataFrame(datos, columns=["Valores"])
    df.to_excel(nombre, index=False)
    print(f"Archivo guardado como {os.path.abspath(nombre)}")

# --- Histogramas (embebidos en un frame de Tkinter) ---
def mostrar_histograma(frame, numeros, titulo):
    # destruir todos los widgets hijos del frame (para refrescar)
    for widget in frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6,3))
    ax.hist(numeros, bins=30, edgecolor="black")
    ax.set_title(f"Histograma - {titulo}")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
