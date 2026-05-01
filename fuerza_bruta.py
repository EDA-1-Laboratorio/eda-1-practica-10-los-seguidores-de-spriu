"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Fuerza bruta

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""

import itertools
import string
import time

# ---------------------------------------------------------------------------
# Alfabetos predefinidos
# ---------------------------------------------------------------------------
DIGITOS    = string.digits                      # '0123456789'
MINUSCULAS = string.ascii_lowercase             # 'abcdefghijklmnopqrstuvwxyz'
ALNUM      = string.ascii_letters + string.digits


# ---------------------------------------------------------------------------
# Problema A – Generación y búsqueda exhaustiva
# ---------------------------------------------------------------------------

def generar_candidatos(alfabeto: str, longitud: int):
    for combinacion in itertools.product(alfabeto, repeat=longitud):
        yield "".join(combinacion)

def buscar_cadena_objetivo(objetivo: str, alfabeto: str, min_len: int = 1) -> tuple:
    intentos = 0
    inicio = time.perf_counter()

    for longitud in range(min_len, len(objetivo) + 1):
        for candidato in generar_candidatos(alfabeto, longitud):
            intentos += 1
            if candidato == objetivo:
                tiempo = time.perf_counter() - inicio
                return (True, intentos, tiempo)

    tiempo = time.perf_counter() - inicio
    return (False, intentos, tiempo)


# ---------------------------------------------------------------------------
# Problema B – Análisis de crecimiento
# ---------------------------------------------------------------------------

def combinar_teoricas(alfabeto: str, min_len: int, max_len: int) -> int:
    return sum(len(alfabeto)**k for k in range(min_len, max_len + 1))


# ---------------------------------------------------------------------------
# Problema C – Optimización con poda por prefijo
# ---------------------------------------------------------------------------

def buscar_con_poda(objetivo: str, alfabeto: str,
                    prefijos_validos: set) -> tuple:
    """
    Variante con poda: antes de contar un candidato, verifica que cada uno
    de sus prefijos propios esté en 'prefijos_validos'.  Si algún prefijo
    falta, descarta la rama completa (usa continue).

    Retorna:
        (encontrada: bool, intentos: int, tiempo_seg: float)

    Pistas:
        El prefijo de longitud k de 'cadena' es candidato[:k].
        Prueba prefijos para k en range(1, len(candidato)).
    """
    intentos = 0
    inicio   = time.perf_counter()

    for longitud in range(1, len(objetivo) + 1):
        for partes in itertools.product(alfabeto, repeat=longitud):
            candidato = "".join(partes)
            
            es_valido = True
            for k in range(1, len(candidato)):
                if candidato[:k] not in prefijos_validos:
                    es_valido = False
                    break
            
            if not es_valido:
                continue

            intentos += 1
            if candidato == objetivo:
                tiempo = time.perf_counter() - inicio
                return (True, intentos, tiempo)

    tiempo = time.perf_counter() - inicio
    return (False, intentos, tiempo)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    objetivo = "abc"
    print("=== Búsqueda por fuerza bruta ===")
    encontrada, intentos, t = buscar_cadena_objetivo(objetivo, MINUSCULAS)
    if encontrada:
        print(f"  Objetivo : '{objetivo}'")
        print(f"  Intentos : {intentos}")
        print(f"  Tiempo   : {t:.4f} s")
        print(f"  Tasa     : {intentos / t:.0f} candidatos/s")
    else:
        print("  generar_candidatos aún no implementada (o target no encontrado)")

    print("\n=== Combinaciones teóricas ===")

    for max_len in [3, 4, 5]:
        n = combinar_teoricas(DIGITOS, 1, max_len)
        print(f"  Dígitos hasta longitud {max_len}: {n:,} candidatos")
        
    print("-" * 30)
    
    for max_len in [3, 4, 5]:
        n = combinar_teoricas(MINUSCULAS, 1, max_len)
        print(f"  Letras hasta longitud {max_len}: {n:,} candidatos")

    print("\n=== Optimización con poda por prefijo ===")
    objetivo_poda = "xyz"
    prefijos_permitidos = {"x", "xy"}
    
    print("Buscando 'xyz' SIN poda...")
    _, intentos_sin, t_sin = buscar_cadena_objetivo(objetivo_poda, MINUSCULAS)
    print(f"  Intentos : {intentos_sin}")
    print(f"  Tiempo   : {t_sin:.4f} s")
    
    print("\nBuscando 'xyz' CON poda...")
    _, intentos_con, t_con = buscar_con_poda(objetivo_poda, MINUSCULAS, prefijos_permitidos)
    print(f"  Intentos : {intentos_con}")
    print(f"  Tiempo   : {t_con:.4f} s")

    # ---------------------------------------------------------------------------
    # Problema D.1 – Razón T(n)/T(n-1)
    # ---------------------------------------------------------------------------
    print("\n=== Problema D.1: Razón T(n) / T(n-1) ===")
    tiempos_d1 = {}
    print(f"{'n':<4} | {'Objetivo':<10} | {'T(n) medido (s)':<18} | {'Razón T(n)/T(n-1)'}")
    print("-" * 60)
    
    for n in range(1, 6):
        objetivo_d1 = "9" * n 
        
        # Reutilizamos la función del Problema A
        _, _, tiempo_medido = buscar_cadena_objetivo(objetivo_d1, DIGITOS)
        tiempos_d1[n] = tiempo_medido
        
        if n == 1:
            razon = "—"
        else:
            if tiempos_d1[n-1] > 0:
                razon_calculada = tiempos_d1[n] / tiempos_d1[n-1]
                razon = f"{razon_calculada:.2f}"
            else:
                razon = "N/A"
            
        print(f"{n:<4} | {objetivo_d1:<10} | {tiempo_medido:<18.6f} | {razon}")
