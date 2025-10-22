# automatas.py
import numpy as np
import matplotlib.pyplot as plt

# --- AUTÓMATA 1D (Regla de Wolfram) ---
def automata_1d(regla=30, pasos=100, tamaño=201):
    """
    Muestra la evolución del autómata 1D (reglas de Wolfram).
    regla: entero 0-255 (ej: 110, 30, 90)
    """
    # inicial
    estado = np.zeros(tamaño, dtype=int)
    estado[tamaño // 2] = 1

    # regla en binario como string, MSB regla_bin[0]
    regla_bin = np.binary_repr(int(regla), width=8)
    matriz = np.zeros((pasos, tamaño), dtype=int)
    matriz[0] = estado

    for i in range(1, pasos):
        nuevo = np.zeros_like(estado)
        # bordes fijos a 0 (o podríamos usar periodic)
        for j in range(1, tamaño - 1):
            a, b, c = estado[j - 1], estado[j], estado[j + 1]
            bits = 4*a + 2*b + c   # valor entre 0 y 7
            # índice en regla_bin: MSB corresponde a configuración 111 (bits=7)
            nuevo[j] = int(regla_bin[7 - bits])
        estado = nuevo
        matriz[i] = estado

    plt.figure(figsize=(8,6))
    plt.imshow(matriz, cmap='binary', interpolation='nearest', aspect='auto')
    plt.title(f"Autómata 1D - Regla {regla}")
    plt.xlabel("Celda")
    plt.ylabel("Paso")
    plt.show()

# --- AUTÓMATA 2D (Juego de la Vida) ---
def automata_2d(tamaño=80, pasos=200, densidad=0.2, pausa=0.05):
    matriz = np.random.rand(tamaño, tamaño) < densidad
    plt.figure(figsize=(6,6))
    im = plt.imshow(matriz, cmap='binary', interpolation='nearest')
    plt.title("Juego de la Vida (2D)")
    for _ in range(pasos):
        vecinos = sum(np.roll(np.roll(matriz, i, 0), j, 1)
                      for i in (-1, 0, 1) for j in (-1, 0, 1)
                      if not (i == 0 and j == 0))
        nueva = (vecinos == 3) | (matriz & (vecinos == 2))
        matriz = nueva
        im.set_data(matriz)
        plt.pause(pausa)
    plt.show()

# --- SIMULACIÓN COVID SIMPLE (SIR en autómata celular 2D) ---
def simulacion_covid_2d(tamaño=80, pasos=200, densidad_inicial=0.02,
                        p_infeccion=0.3, p_recuperacion=0.05, pausa=0.05):
    """
    Estados:
      0: Susceptible (S)
      1: Infectado (I)
      2: Recuperado (R)
    p_infeccion: probabilidad por vecino infectado por paso
    p_recuperacion: probabilidad de recuperación por paso
    """
    # inicial: todos susceptibles excepto algunos infectados
    matriz = np.zeros((tamaño, tamaño), dtype=int)
    # poner infectados aleatorios según densidad_inicial
    infectados = np.random.rand(tamaño, tamaño) < densidad_inicial
    matriz[infectados] = 1

    plt.figure(figsize=(6,6))
    cmap = plt.get_cmap('viridis', 3)  # 3 colores discretos
    im = plt.imshow(matriz, cmap=cmap, vmin=0, vmax=2, interpolation='nearest')
    plt.title("Simulación COVID (SIR) - 0:S 1:I 2:R")

    for _ in range(pasos):
        vecinos_inf = sum(np.roll(np.roll(matriz == 1, i, 0), j, 1)
                          for i in (-1, 0, 1) for j in (-1, 0, 1)
                          if not (i == 0 and j == 0))
        nueva = matriz.copy()
        # susceptibles que se infectan si tienen vecinos infectados (probabilístico)
        susceptible = (matriz == 0)
        prob_contagio = 1 - (1 - p_infeccion) ** vecinos_inf  # prob se infecte por al menos uno
        rand = np.random.rand(tamaño, tamaño)
        nueva[np.logical_and(susceptible, rand < prob_contagio)] = 1

        # infectados que se recuperan
        rand2 = np.random.rand(tamaño, tamaño)
        nueva[np.logical_and(matriz == 1, rand2 < p_recuperacion)] = 2

        matriz = nueva
        im.set_data(matriz)
        plt.pause(pausa)

    plt.show()
