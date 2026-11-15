"""Verificación independiente de los valores numéricos de L1 c. 8 (LIBRO_DE_ESTILO.md, §17.3).

Cada aserción corresponde a un valor del texto, de un ejemplo o de una solución.
Uso: python3 verificacion/cap08.py   (sale con error si algún valor no coincide)
"""
import math
from fractions import Fraction


def cerca(x, y, tol):
    assert abs(x - y) <= tol, (x, y)


L = math.log10

# §8.1 ejemplos y errores frecuentes
assert 2**3 * 2**4 == 128 == 2**7 and (2**3)**2 == 64 == 2**6 and (2 * 5)**3 == 1000 == 2**3 * 5**3
assert (1 + 1)**2 == 4 and 1**2 + 1**2 == 2 and 2**2 + 2**3 == 12 and 2**5 == 32 and -2**2 == -4 and (-2)**2 == 4

# Ejemplo de descuento: 5000 / 1,08^3
assert abs(1.08**3 - 1.259712) < 1e-12
cerca(5000 / 1.08**3, 3969.16, 0.005)
cerca(3969.16 * 1.259712, 5000.00, 0.005)

# §8.3 raíces
assert 2**3 == 8 and abs(0.2**4 - 0.0016) < 1e-15 and math.isqrt(25) == 5

# Ejemplo de exponentes racionales
cerca(8 ** (2 / 3), 4, 1e-12); cerca(27 ** (-1 / 3), 1 / 3, 1e-12); cerca(16 ** 0.75, 8, 1e-12)
cerca(1.21 ** 0.5, 1.1, 1e-12)

# §8.6 comparaciones
assert 2**30 == 8**10 and 3**20 == 9**10 and 2**30 < 3**20 and 0.9**10 > 0.9**12
assert 0.5**2 == 0.25 and abs(0.25**0.5 - 0.5) < 1e-15

# §8.7 Bernoulli y comparación
assert (1 - 4)**3 == -27 and 1 + 3 * (-4) == -11
cerca(1000 * 1.1**10, 2593.74, 0.005); cerca(1000 * 1.1**30, 17449.40, 0.005)

# §8.8 tabla de 2^r: valores crecientes y menores que 2^1,5
valores = [2 ** float(e) for e in ["1.4", "1.41", "1.414", "1.4142", "1.41421"]]
assert all(a < b for a, b in zip(valores, valores[1:])) and valores[-1] < 2 ** 1.5

# §8.9 logaritmos
assert 2**10 == 1024 and Fraction(10)**-3 == Fraction(1, 1000) and 9**0.5 == 3
cerca(L(2), 0.30103, 5e-6); cerca(L(3), 0.47712, 5e-6); cerca(L(3) / L(2), 1.58496, 5e-6)
cerca(100 * L(2), 30.103, 5e-4)
assert str(2**100) == "1267650600228229401496703205376" and len(str(2**100)) == 31
cerca(L(20), 1.301, 5e-4)
assert round(L(100)**2, 12) == 4 and round(L(100**2), 12) == 4 and round(L(1000)**2, 12) == 9 and round(L(1000**2), 12) == 6

# §8.10 tasa mensual equivalente, plazo y regla del 72
cerca(1.12 ** (1 / 12) - 1, 0.009489, 5e-7); cerca(1.009489**12, 1.12000, 5e-6); cerca(1.01**12, 1.126825, 5e-7)
cerca(L(1.5), 0.176091, 5e-7); cerca(L(1.06), 0.025306, 5e-7); cerca(L(1.5) / L(1.06), 6.96, 0.005)
cerca(10000 * 1.06**6, 14185.19, 0.005); cerca(10000 * 1.06**7, 15036.30, 0.005)


def t_exacto(i):
    return L(2) / L(1 + i)


def error_rel(i, c=72):
    return (c / (100 * i) - t_exacto(i)) / t_exacto(i)


# RA-05: comprobación numérica en una malla fina de (0; 0,15]
assert max(abs(error_rel(k / 100000)) for k in range(1, 15001)) < 0.04
cerca(error_rel(1e-6), 0.72 / math.log(2) - 1, 1e-5)   # límite para i -> 0: 3,87 %
assert error_rel(0.30) < -0.08 and error_rel(0.07) > 0 > error_rel(0.08)

# §8.11 salidas de Python citadas en el texto
assert 1000 ** (1 / 3) == 9.999999999999998 and (1000 ** (1 / 3) == 10) is False
assert math.log(1000, 10) == 2.9999999999999996

# Ejercicios
assert 3**(4 - 2) == 9 and Fraction(2)**-3 == Fraction(1, 8) and 10**3 // 10**2 == 10
assert (2 + 3)**2 == 25 and 2**7 == 128 and 4**7 == 16384
cerca(20000 * 1.05**-6, 14924.31, 0.005); cerca(1.05**6, 1.340096, 5e-7)
cerca(1.1 * 0.9, 0.99, 1e-12); cerca(1 / 1.1, 0.909091, 5e-7)
cerca(81 ** 0.75, 27, 1e-9); cerca(0.25 ** -0.5, 2, 1e-12); cerca(1000 ** (-2 / 3), 0.01, 1e-12)
cerca(1.331 ** (1 / 3), 1.1, 1e-12)
izq, der = 2.0, 3.0
for _ in range(30):
    m = (izq + der) / 2
    izq, der = (izq, m) if m**3 > 10 else (m, der)
cerca(izq, 2.15443469, 1e-8); cerca(10 ** (1 / 3), 2.15443469, 5e-9)
assert 256**5 == 2**40 and 243**5 == 3**25 and 125**5 == 5**15 and 5**15 < 3**25 < 2**40
assert 0.7**0.5 < 0.7**(1 / 3) and 1.02**-5 < 1.02**-4 and 0.5**3 < 0.6**3
cerca(1.05**10, 1.628895, 5e-7); cerca(1.05**10 - 1.5, 0.128895, 5e-7)
assert 0.5**4 == 0.0625
cerca(1000 * 1.1**5, 1610.51, 0.005)
for n, r in [(5, 1.0737), (10, 1.2969), (30, 4.3624)]:
    cerca(1.1**n / (1 + 0.1 * n), r, 5e-5)
cerca(0.97**10, 0.737424, 5e-7)
assert math.isclose(math.log(81, 3), 4) and math.isclose(math.log(8, 0.5), -3) and math.isclose(math.log(8, 4), 1.5)
cerca(L(6), 0.77815, 5e-6); cerca(0.47712 - 0.30103, 0.17609, 1e-9)
cerca(3 * 0.30103 + 2 * 0.47712, 1.85733, 1e-9); cerca(L(72), 1.85733, 1e-5)
cerca(1 - 0.30103, 0.69897, 1e-9); cerca(0.30103 / 0.47712, 0.63093, 5e-6)
cerca(0.5 * L(7), 0.4225, 5e-5); cerca(L(1.6) / L(1.04), 11.9836, 5e-5)
cerca(50 * L(3), 23.856, 5e-4); assert len(str(3**50)) == 24
cerca(1000 * L(2), 301.03, 5e-3); assert len(str(2**1000)) == 302
cerca(L(1100), 3.0414, 5e-5)
cerca(1.1 ** 0.25 - 1, 0.024114, 5e-7); cerca(1.02**12 - 1, 0.268242, 5e-7)
cerca(L(3) / L(1.08), 14.27, 0.005); cerca(1.08**14, 2.9372, 5e-5); cerca(1.08**15, 3.1722, 5e-5)
cerca(1.5 ** 0.2 - 1, 0.084472, 5e-7); cerca(8000 * 1.084472**5, 12000, 0.1)
cerca(t_exacto(0.09), 8.04, 0.005); cerca(error_rel(0.09), -0.005, 5e-4)
for tasa, t_ref in [(0.02, 35.0028), (0.05, 14.2067), (0.10, 7.2725)]:
    cerca(t_exacto(tasa), t_ref, 5e-5)
for (c, tasa), valor in {(70, 0.02): -0.00008, (69, 0.02): -0.014, (70, 0.05): -0.015, (69, 0.05): -0.029,
                          (70, 0.10): -0.037, (69, 0.10): -0.051}.items():
    cerca(error_rel(tasa, c), valor, 5e-4)
assert all(abs(error_rel(t, 70)) < abs(error_rel(t, 69)) for t in (0.02, 0.05, 0.10))
cerca(error_rel(0.001, 69), -0.005, 5e-4); cerca(error_rel(0.001, 70), 0.009, 5e-4)
cerca(100 * math.log(2), 69.31, 0.005)
cerca(L(2) / L(1.04), 17.67, 0.005)
cerca(1.01**36, 1.430769, 5e-7); cerca(1.125**3, 1.423828, 5e-7)
assert 2 ** 0.5 * 2 ** 0.5 == 2.0000000000000004
assert isinstance((-8) ** (1 / 3), complex)
assert 10 ** math.log10(11) == 10.999999999999996
cerca(t_exacto(0.08), 9.01, 0.005); assert math.ceil(1 / 0.08) == 13
mejor = min((abs(72 / (100 * t) - t_exacto(t)), t) for t in [k / 1000 for k in range(10, 301)])
assert mejor[1] == 0.078, mejor
cerca(2 ** math.sqrt(2), 2.6651441, 5e-8)
assert (0.1 + 0.2 == 0.3) is False
print("cap08: todas las verificaciones superadas")
