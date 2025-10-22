# tests.py
import numpy as np
from scipy import stats

class PruebaMedia:
    def __init__(self, numeros):
        self.numeros = np.array(numeros, dtype=float)

    def calcular(self):
        n = len(self.numeros)
        if n == 0:
            return "No hay datos para la prueba de media."
        media = self.numeros.mean()
        # para U(0,1) media esperada 0.5, var = 1/12
        z = (media - 0.5) / np.sqrt(1.0/(12.0*n))
        # p-valor dos colas
        pval = 2 * (1 - stats.norm.cdf(abs(z)))
        return f"Media = {media:.4f}, Z = {z:.4f}, p-valor = {pval:.4f}"

class PruebaVarianza:
    def __init__(self, numeros):
        self.numeros = np.array(numeros, dtype=float)

    def calcular(self):
        n = len(self.numeros)
        if n < 2:
            return "No hay suficientes datos para la prueba de varianza."
        varianza = self.numeros.var(ddof=1)  # muestra
        # para U(0,1) var esperada = 1/12
        chi2 = (n-1) * varianza / (1.0/12.0)
        # p-valor (two-tail) no siempre útil pero lo calculamos
        p_lower = stats.chi2.cdf(chi2, df=n-1)
        pval = 2 * min(p_lower, 1-p_lower)
        return f"Varianza (muestral) = {varianza:.6f}, Chi2 = {chi2:.4f}, p-valor ~ {pval:.4f}"

class PruebaChi2:
    def __init__(self, numeros, k=10):
        self.numeros = np.array(numeros, dtype=float)
        self.k = int(k)

    def calcular(self):
        n = len(self.numeros)
        if n == 0:
            return "No hay datos para Chi²."
        frec, _ = np.histogram(self.numeros, bins=self.k, range=(0,1))
        esperada = n / self.k
        chi2 = ((frec - esperada)**2 / esperada).sum()
        # p-valor:
        from scipy import stats
        pval = 1 - stats.chi2.cdf(chi2, df=self.k - 1)
        return f"Chi² = {chi2:.4f} con {self.k-1} gl, p-valor = {pval:.4f}"
