"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Estrategia incremental – Insertion sort instrumentado

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""

import time
import random


# ---------------------------------------------------------------------------
# Problema A – Insertion sort con métricas
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list) -> tuple:
    """
    Ordena 'arr' usando insertion sort e instrumenta la ejecución.

    Retorna:
        (arreglo_ordenado, comparaciones, movimientos, tiempo_seg)

    Pistas:
        El bucle externo recorre i de 1 a n-1.
        'llave' = arr[i] es el elemento a insertar.
        El bucle interno (while) desplaza elementos mayores que 'llave' hacia
        la derecha; cada desplazamiento es un movimiento.
        Cuenta también la última comparación del while (la que falla).
        La colocación final de llave es un movimiento.
    """
    arr          = arr.copy()
    n            = len(arr)
    comparaciones = 0
    movimientos   = 0
    inicio        = time.perf_counter()

    for i in range(1, n):
        llave = arr[i]
        j = i - 1

        # Mientras el elemento a la izquierda sea mayor que la llave
        while j >= 0:
            comparaciones += 1
            if arr[j] > llave:
                arr[j + 1] = arr[j] # Desplazamiento
                movimientos += 1
                j -= 1
            else:
                # Si arr[j] <= llave, el bucle termina, pero la comparación ya se contó
                break

        arr[j + 1] = llave
        movimientos += 1

    tiempo = time.perf_counter() - inicio
    return (arr, comparaciones, movimientos, tiempo)


# ---------------------------------------------------------------------------
# Problema B – Generación de escenarios
# ---------------------------------------------------------------------------

def generar_arreglo(n: int, escenario: str) -> list:
    if escenario == "mejor":
        return list(range(n))  # Arreglo ya ordenado
    elif escenario == "peor":
        return list(range(n, 0, -1))  # Arreglo ordenado en reversa
    elif escenario == "promedio":
        arr = list(range(n))
        random.shuffle(arr)  # Arreglo con elementos en orden aleatorio
        return arr
    else:
        raise ValueError(f"Escenario '{escenario}' no es valido.")


def medir_escenarios(tamanos: list) -> list:
    resultados = []
    for n in tamanos:
        for escenario in ("mejor", "promedio", "peor"):
            #Mensaje para indicar progreso
            print(f"Procesando: Tamaño {n}, Escenario: {escenario}...", end="\r")

            arr = generar_arreglo(n, escenario)
            _, comps, movs, t = insertion_sort_metricas(arr)

            resultados.append({
                "tamano": n,
                "escenario": escenario,
                "comparaciones": comps,
                "movimientos": movs,
                "tiempo": t
            })
    return resultados


# ---------------------------------------------------------------------------
# Problema D – Versión híbrida (insertion sort + merge sort)
# ---------------------------------------------------------------------------

def _merge(izq: list, der: list) -> list:
    resultado = []
    i = j = 0
    
    while i < len(izq) and j < len(der):
        if izq[i] < der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
            
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


def _merge_sort_hibrido(arr: list, umbral: int) -> list:
    """
    Divide 'arr' recursivamente.
    Si el subarreglo tiene tamaño <= umbral, usa insertion_sort_metricas.
    Si no, divide a la mitad y fusiona con _merge.
    """
    if len(arr) <= umbral:
        # Usamos la versión de insertion sort y tomamos solo el arreglo ordenado
        return insertion_sort_metricas(arr)[0]

    mid = len(arr) // 2
    izq = _merge_sort_hibrido(arr[:mid], umbral)
    der = _merge_sort_hibrido(arr[mid:], umbral)
    
    return _merge(izq, der)


def insertion_sort_hibrido(arr: list, umbral: int = 32) -> list:
    """
    Punto de entrada del ordenamiento híbrido.
    Retorna el arreglo ordenado.
    """
    return _merge_sort_hibrido(arr, umbral)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tamanos = [1000, 2000, 4000, 8000]
    print("Midiendo escenarios... (puede tardar unos segundos)\n")
    resultados = medir_escenarios(tamanos)

    if resultados:
        print(f"{'Tamaño':>8} {'Escenario':>10} {'Comps':>12} "
              f"{'Movs':>12} {'Tiempo (s)':>12}")
        print("-" * 60)
        for r in resultados:
            print(f"{r['tamano']:>8} {r['escenario']:>10} "
                  f"{r['comparaciones']:>12} {r['movimientos']:>12} "
                  f"{r['tiempo']:>12.4f}")
    else:
        print("medir_escenarios aún no implementada.")
