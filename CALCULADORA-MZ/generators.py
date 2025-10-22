# generators.py
import numpy as np
from scipy.stats import uniform, expon, erlang, gamma, norm, weibull_min, bernoulli, binom, poisson

# ====== GENERADORES CLÁSICOS ======

class CuadradosMedios:
    """
    Método de los cuadrados medios.
    seed: entero (se recomienda 4 dígitos)
    n: cantidad de números a generar
    """
    def __init__(self, seed: int, n: int):
        self.seed = int(seed)
        self.n = int(n)

    def generar(self):
        nums = []
        x = self.seed
        for _ in range(self.n):
            sq = x**2
            s = str(sq).zfill(8)  # asegurar 8 caracteres
            mid = int(s[2:6])     # 4 cifras centrales
            nums.append(mid / 10000.0)
            x = mid
        return nums

class ProductosMedios:
    """
    Producto de semillas (medios).
    seed1, seed2: enteros (recomendado 4 dígitos)
    """
    def __init__(self, seed1: int, seed2: int, n: int):
        self.x = int(seed1)
        self.y = int(seed2)
        self.n = int(n)

    def generar(self):
        nums = []
        for _ in range(self.n):
            p = self.x * self.y
            s = str(p).zfill(8)
            mid = int(s[2:6])
            nums.append(mid / 10000.0)
            # rotación de semillas (estilo clásico)
            self.x, self.y = self.y, mid
        return nums

class MultiplicadorConstante:
    """
    Generador congruencial multiplicativo simple (mod 10000)
    seed: entero
    a: multiplicador
    """
    def __init__(self, seed: int, n: int, a: int = 5):
        self.x = int(seed)
        self.n = int(n)
        self.a = int(a)
        self.m = 10000

    def generar(self):
        nums = []
        x = self.x
        for _ in range(self.n):
            x = (self.a * x) % self.m
            nums.append(x / float(self.m))
        return nums

# ====== DISTRIBUCIONES CONTINUAS ======
def dist_uniforme_continua(a=0.0, b=1.0, n=1000):
    return uniform.rvs(loc=a, scale=b-a, size=n)

def dist_exponencial(lam=1.0, n=1000):
    return expon.rvs(scale=1.0/lam, size=n)

def dist_erlang(k=2, lam=1.0, n=1000):
    return erlang.rvs(k, scale=1.0/lam, size=n)

def dist_gamma(alpha=2.0, lam=1.0, n=1000):
    return gamma.rvs(alpha, scale=1.0/lam, size=n)

def dist_normal(mu=0.0, sigma=1.0, n=1000):
    return norm.rvs(loc=mu, scale=sigma, size=n)

def dist_weibull(k=1.5, lam=1.0, n=1000):
    return weibull_min.rvs(c=k, scale=lam, size=n)

# ====== DISTRIBUCIONES DISCRETAS ======
def dist_uniforme_discreta(a=1, b=6, n=1000):
    return np.random.randint(a, b + 1, size=n)

def dist_bernoulli(p=0.5, n=1000):
    return bernoulli.rvs(p, size=n)

def dist_binomial(n_ensayos=10, p=0.5, n=1000):
    return binom.rvs(n_ensayos, p, size=n)

def dist_poisson(lam=3.0, n=1000):
    return poisson.rvs(mu=lam, size=n)

