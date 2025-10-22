# main.py
import tkinter as tk
from tkinter import messagebox
import numpy as np

from generators import CuadradosMedios, ProductosMedios, MultiplicadorConstante
from generators import dist_uniforme_continua, dist_exponencial, dist_erlang, dist_gamma, dist_normal, dist_weibull
from generators import dist_uniforme_discreta, dist_bernoulli, dist_binomial, dist_poisson

from utills import mostrar_histograma, export_csv, exportar_a_excel
from tests import PruebaMedia, PruebaVarianza, PruebaChi2
from automatas import automata_1d, automata_2d, simulacion_covid_2d


class PRNGDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Aleatoria - Midori")
        self.geometry("1150x750")
        self.configure(bg="#B3E5FC")
        self.minsize(900, 600)
        self.numeros = []

        tk.Label(
            self,
            text="CALCULADORA DE NÚMEROS ALEATORIOS",
            font=("Helvetica", 22, "bold"),
            bg="#B3E5FC",
            fg="#0D47A1"
        ).pack(pady=12)

        # contenedor principal
        main_frame = tk.Frame(self, bg="#B3E5FC")
        main_frame.pack(fill="both", expand=True)

        # panel izquierdo
        self.frame_botones = tk.Frame(main_frame, bg="#B3E5FC")
        self.frame_botones.pack(side="left", fill="y", padx=10, pady=10)

        # panel derecho
        self.frame_resultados = tk.Frame(main_frame, bg="#B3E5FC")
        self.frame_resultados.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # output box
        self.output_text = tk.Text(
            self.frame_botones, height=16, width=45, font=("Helvetica", 10)
        )
        self.output_text.pack(padx=5, pady=5, fill="both", expand=True)

        # botones principales
        botones = [
            ("Cuadrados Medios", self.run_cuadrados),
            ("Productos Medios", self.run_productos),
            ("Multiplicador Constante", self.run_multiplicador),
            ("Prueba Media", self.test_media),
            ("Prueba Varianza", self.test_varianza),
            ("Prueba Chi²", self.test_chi2),
            ("Distribuciones", self.ver_distribuciones),
            ("Autómatas", self.ver_automatas),
            ("Exportar CSV", self.exportar),
            ("Limpiar", self.limpiar)
        ]

        for txt, cmd in botones:
            b = tk.Button(
                self.frame_botones,
                text=txt,
                width=25,
                bg="#03A9F4",
                fg="white",
                font=("Helvetica", 11, "bold"),
                command=cmd
            )
            b.pack(pady=4, fill="x")

    # ---------------------- PARAMETROS DINÁMICOS ----------------------
    def pedir_parametros(self, campos):
        """Ventana para pedir parámetros de forma dinámica"""
        win = tk.Toplevel(self)
        win.title("Parámetros del generador")
        win.geometry("400x400")
        win.configure(bg="#E1F5FE")
        win.grab_set()

        entradas = {}
        tk.Label(
            win, text="Ingrese los parámetros:",
            bg="#E1F5FE", font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        for campo in campos:
            tk.Label(win, text=campo + ":", bg="#E1F5FE",
                     font=("Helvetica", 12)).pack()
            entrada = tk.Entry(win, font=("Helvetica", 12))
            entrada.pack(pady=5)
            entradas[campo] = entrada

        valores = {}

        def confirmar():
            nonlocal valores
            valores = {campo: entradas[campo].get() for campo in campos}
            win.destroy()

        tk.Button(
            win, text="Aceptar", bg="#0288D1", fg="white",
            font=("Helvetica", 12, "bold"), command=confirmar
        ).pack(pady=15)

        win.wait_window()
        return valores

    # ---------------------- GENERADORES ----------------------
    def run_cuadrados(self):
        params = self.pedir_parametros(["Semilla (seed)", "Cantidad (n)"])
        try:
            seed = int(params["Semilla (seed)"])
            n = int(params["Cantidad (n)"])
            gen = CuadradosMedios(seed=seed, n=n)
            self.numeros = gen.generar()
            self.mostrar_resultados("Cuadrados Medios")
        except Exception as e:
            messagebox.showerror("Error", f"Parámetros inválidos: {e}")

    def run_productos(self):
        params = self.pedir_parametros(["Semilla 1", "Semilla 2", "Cantidad (n)"])
        try:
            s1 = int(params["Semilla 1"])
            s2 = int(params["Semilla 2"])
            n = int(params["Cantidad (n)"])
            gen = ProductosMedios(seed1=s1, seed2=s2, n=n)
            self.numeros = gen.generar()
            self.mostrar_resultados("Productos Medios")
        except Exception as e:
            messagebox.showerror("Error", f"Parámetros inválidos: {e}")

    def run_multiplicador(self):
        params = self.pedir_parametros(["Semilla (seed)", "Cantidad (n)", "Constante (a)"])
        try:
            seed = int(params["Semilla (seed)"])
            n = int(params["Cantidad (n)"])
            a = int(params["Constante (a)"])
            gen = MultiplicadorConstante(seed=seed, n=n, a=a)
            self.numeros = gen.generar()
            self.mostrar_resultados("Multiplicador Constante")
        except Exception as e:
            messagebox.showerror("Error", f"Parámetros inválidos: {e}")

    # ---------------------- PRUEBAS ----------------------
    def test_media(self):
        if not self.numeros:
            messagebox.showwarning("Aviso", "Genere números primero.")
            return
        test = PruebaMedia(self.numeros)
        self.output_text.insert(tk.END, test.calcular() + "\n")

    def test_varianza(self):
        if not self.numeros:
            messagebox.showwarning("Aviso", "Genere números primero.")
            return
        test = PruebaVarianza(self.numeros)
        self.output_text.insert(tk.END, test.calcular() + "\n")

    def test_chi2(self):
        if not self.numeros:
            messagebox.showwarning("Aviso", "Genere números primero.")
            return
        test = PruebaChi2(self.numeros, k=10)
        self.output_text.insert(tk.END, test.calcular() + "\n")

    # ---------------------- RESULTADOS ----------------------
    def mostrar_resultados(self, metodo):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(
            tk.END, f"{metodo}:\n{self.numeros[:50]}...\nTotal: {len(self.numeros)}\n"
        )
        for w in self.frame_resultados.winfo_children():
            w.destroy()
        mostrar_histograma(self.frame_resultados, self.numeros, metodo)

    def exportar(self):
        if self.numeros:
            export_csv(self.numeros)
        else:
            messagebox.showwarning("Aviso", "No hay números generados para exportar.")

    def limpiar(self):
        self.numeros = []
        self.output_text.delete("1.0", tk.END)
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

    # ---------------------- DISTRIBUCIONES ----------------------
    def ver_distribuciones(self):
        win = tk.Toplevel(self)
        win.title("Distribuciones estadísticas")
        win.geometry("420x520")
        win.configure(bg="#E1F5FE")

        opciones = [
            ("Uniforme continua", dist_uniforme_continua),
            ("Exponencial", dist_exponencial),
            ("Erlang", dist_erlang),
            ("Gamma", dist_gamma),
            ("Normal", dist_normal),
            ("Weibull", dist_weibull),
            ("Uniforme discreta", dist_uniforme_discreta),
            ("Bernoulli", dist_bernoulli),
            ("Binomial", dist_binomial),
            ("Poisson", dist_poisson)
        ]

        tk.Label(
            win, text="Seleccione una distribución:",
            bg="#E1F5FE", font=("Helvetica", 12, "bold")
        ).pack(pady=10)

        for nombre, func in opciones:
            tk.Button(
                win, text=nombre, bg="#4FC3F7", fg="white",
                font=("Helvetica", 11), width=28,
                command=lambda f=func, n=nombre: self.mostrar_distribucion(f, n, win)
            ).pack(pady=4)

        framep = tk.Frame(win, bg="#E1F5FE")
        framep.pack(pady=8)
        tk.Label(framep, text="n:", bg="#E1F5FE").grid(row=0, column=0)
        self.entry_n_dist = tk.Entry(framep, width=8)
        self.entry_n_dist.insert(0, "1000")
        self.entry_n_dist.grid(row=0, column=1, padx=6)

    def mostrar_distribucion(self, funcion, nombre, ventana):
        n = int(self.entry_n_dist.get() or 1000)
        datos = funcion(n=n)
        datos = np.asarray(datos).flatten()
        mostrar_histograma(self.frame_resultados, datos, nombre)
        exportar_a_excel(datos, f"{nombre.replace(' ', '_')}.xlsx")
        messagebox.showinfo("Éxito", f"{nombre} generada y exportada correctamente.")

    # ---------------------- AUTOMATAS ----------------------
    def ver_automatas(self):
        win = tk.Toplevel(self)
        win.title("Autómatas Celulares")
        win.geometry("380x340")
        win.configure(bg="#E1F5FE")

        tk.Label(
            win, text="Simulación de autómatas celulares",
            bg="#E1F5FE", font=("Helvetica", 12, "bold")
        ).pack(pady=8)

        opciones = [
            ("Autómata 1D (Regla 110)", lambda: automata_1d(regla=110, pasos=150, tamaño=301)),
            ("Autómata 1D (Regla 30)", lambda: automata_1d(regla=30, pasos=150, tamaño=301)),
            ("Autómata 2D (Juego de la Vida)", lambda: automata_2d(tamaño=80, pasos=200, densidad=0.2)),
            ("Simulación COVID 2D (SIR)", lambda: simulacion_covid_2d(
                tamaño=80, pasos=200, densidad_inicial=0.02, p_infeccion=0.25, p_recuperacion=0.03))
        ]

        for nombre, func in opciones:
            tk.Button(
                win, text=nombre,
                bg="#1976D2" if "1D" in nombre else "#E64A19",
                fg="white", font=("Helvetica", 11, "bold"),
                width=30, command=func
            ).pack(pady=6)


if __name__ == "__main__":
    app = PRNGDashboard()
    app.mainloop()
