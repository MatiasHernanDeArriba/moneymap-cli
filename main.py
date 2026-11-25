"""
Moneymap-CLI
Herramienta de línea de comandos para rastrear gastos personales.

Paso 1: guardar gastos y listarlos.
"""

import argparse
import csv
import json
import os
from datetime import date

# Archivo donde vamos a guardar todos los gastos.
# Es una lista de diccionarios, por ejemplo:
# [{"monto": 500, "categoria": "comida", "nota": "almuerzo", "fecha": "2026-07-24"}]
ARCHIVO_DATOS = "expenses.json"

# Categorías permitidas. Usamos un set (conjunto) en vez de una lista
# porque buscar "¿está esto adentro?" en un set es instantáneo,
# no importa si tenés 5 categorías o 5000. En una lista, Python
# tiene que recorrerla una por una.
CATEGORIAS_VALIDAS = {"comida", "transporte", "ocio", "servicios", "salud", "otros"}


def cargar_gastos():
    """Lee el archivo JSON y devuelve la lista de gastos.
    Si el archivo no existe todavía, devuelve una lista vacía."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []

    with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_gastos(gastos):
    """Escribe la lista de gastos en el archivo JSON.
    indent=2 es solo para que el archivo se vea prolijo si lo abrís."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(gastos, f, indent=2, ensure_ascii=False)


def agregar_gasto(monto, categoria, nota):
    """Crea un nuevo gasto y lo agrega a la lista existente."""
    gastos = cargar_gastos()

    nuevo_gasto = {
        "monto": monto,
        "categoria": categoria,
        "nota": nota or "",
        "fecha": date.today().isoformat(),  # ej: "2026-07-24"
    }

    gastos.append(nuevo_gasto)
    guardar_gastos(gastos)

    print(f"Gasto agregado: ${monto} en '{categoria}' ({nuevo_gasto['fecha']})")


def listar_gastos(categoria=None, desde=None, hasta=None):
    """Muestra los gastos guardados, con filtros opcionales.

    categoria: si se pasa, solo muestra gastos de esa categoría.
    desde / hasta: strings 'YYYY-MM-DD' para filtrar por rango de fechas.
    """
    gastos = cargar_gastos()

    # List comprehension: es una forma compacta de escribir
    #   resultado = []
    #   for g in gastos:
    #       if condición:
    #           resultado.append(g)
    # en una sola línea. Encadenamos varios filtros, uno por cada
    # argumento que el usuario haya pasado.
    if categoria:
        gastos = [g for g in gastos if g["categoria"] == categoria]
    if desde:
        gastos = [g for g in gastos if g["fecha"] >= desde]
    if hasta:
        gastos = [g for g in gastos if g["fecha"] <= hasta]
    # Nota: comparar fechas como texto (">=", "<=") funciona porque
    # están en formato ISO "YYYY-MM-DD" — ese formato ordena igual
    # como texto que como fecha real. Es un truco práctico, no magia.

    if not gastos:
        print("No hay gastos que coincidan con ese filtro.")
        return

    print(f"{'Fecha':<12} {'Categoría':<15} {'Monto':>10}  Nota")
    print("-" * 55)
    total = 0
    for g in gastos:
        print(f"{g['fecha']:<12} {g['categoria']:<15} ${g['monto']:>9}  {g['nota']}")
        total += g["monto"]

    print("-" * 55)
    print(f"Total: ${total}")


def exportar_csv(nombre_archivo="gastos_export.csv"):
    """Exporta todos los gastos a un archivo CSV."""
    gastos = cargar_gastos()

    if not gastos:
        print("No hay gastos para exportar.")
        return

    # csv.DictWriter escribe cada diccionario como una fila, usando
    # las keys como nombres de columna. Mucho más prolijo que armar
    # el texto del CSV a mano con comas y saltos de línea.
    campos = ["fecha", "categoria", "monto", "nota"]

    with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(gastos)

    print(f"Exportado a '{nombre_archivo}' ({len(gastos)} gastos).")


def resumen_por_categoria():
    """Agrupa los gastos por categoría y muestra un gráfico de barras
    hecho con caracteres, directo en la terminal."""
    gastos = cargar_gastos()

    if not gastos:
        print("Todavía no hay gastos registrados.")
        return

    # Patrón "group by": vamos acumulando un total por cada categoría
    # en un diccionario. dict.get(clave, 0) devuelve 0 si la clave
    # todavía no existe, así evitamos escribir un if para inicializarla.
    totales = {}
    for g in gastos:
        cat = g["categoria"]
        totales[cat] = totales.get(cat, 0) + g["monto"]

    # sorted() con key=... ordena por el valor (el gasto total),
    # de mayor a menor, para que la categoría más cara aparezca primero.
    categorias_ordenadas = sorted(totales.items(), key=lambda item: item[1], reverse=True)

    monto_maximo = categorias_ordenadas[0][1]
    ANCHO_MAXIMO_BARRA = 30  # caracteres que ocupa la barra más larga

    print("Resumen por categoría\n")
    for categoria, monto in categorias_ordenadas:
        # Regla de tres simple: cuántos caracteres le tocan a esta barra
        # en proporción al gasto máximo.
        largo_barra = round((monto / monto_maximo) * ANCHO_MAXIMO_BARRA)
        barra = "█" * largo_barra
        print(f"{categoria:<12} {barra:<{ANCHO_MAXIMO_BARRA}} ${monto:.2f}")

    print(f"\nTotal general: ${sum(totales.values()):.2f}")


def main():
    # argparse arma automáticamente el "--help" y valida los argumentos.
    parser = argparse.ArgumentParser(
        prog="moneymap",
        description="Rastreá tus gastos personales desde la terminal.",
    )

    # subparsers = subcomandos, como "add" y "list"
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando: add
    parser_add = subparsers.add_parser("add", help="Agregar un nuevo gasto")
    parser_add.add_argument("--monto", type=float, required=True, help="Monto del gasto")
    # choices= hace que argparse valide solo, sin que escribamos ningún if.
    # Si el usuario pone una categoría que no está en la lista, argparse
    # corta la ejecución y muestra las opciones válidas. Una línea
    # reemplaza todo un bloque de validación manual.
    parser_add.add_argument(
        "--categoria", type=str, required=True,
        choices=sorted(CATEGORIAS_VALIDAS), help="Categoría del gasto",
    )
    parser_add.add_argument("--nota", type=str, default="", help="Nota opcional")

    # Subcomando: list, ahora con filtros opcionales
    parser_list = subparsers.add_parser("list", help="Listar gastos")
    parser_list.add_argument("--categoria", type=str, choices=sorted(CATEGORIAS_VALIDAS), default=None)
    parser_list.add_argument("--desde", type=str, default=None, help="Fecha desde, formato YYYY-MM-DD")
    parser_list.add_argument("--hasta", type=str, default=None, help="Fecha hasta, formato YYYY-MM-DD")

    # Subcomando: export
    parser_export = subparsers.add_parser("export", help="Exportar gastos a CSV")
    parser_export.add_argument("--archivo", type=str, default="gastos_export.csv", help="Nombre del archivo CSV")

    # Subcomando: resumen
    subparsers.add_parser("resumen", help="Ver gastos totales por categoría")

    args = parser.parse_args()

    if args.comando == "add":
        agregar_gasto(args.monto, args.categoria, args.nota)
    elif args.comando == "list":
        listar_gastos(categoria=args.categoria, desde=args.desde, hasta=args.hasta)
    elif args.comando == "export":
        exportar_csv(args.archivo)
    elif args.comando == "resumen":
        resumen_por_categoria()


if __name__ == "__main__":
    main()