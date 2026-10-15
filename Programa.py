"""
Prototipo de mesa de partes digital
Curso: Fundamentos de Programación

El programa permite registrar, validar, consultar, ordenar y guardar
expedientes en un archivo CSV.
"""

import csv
import os
from datetime import datetime

ARCHIVO = "expedientes.csv"
CAMPOS = [
    "codigo",
    "dni",
    "ciudadano",
    "tipo_documento",
    "asunto",
    "descripcion",
    "fecha_recepcion",
    "area_responsable",
    "estado",
]


def limpiar_pantalla():
    """Limpia la consola para que el menú sea más ordenado."""
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("\nPresione ENTER para continuar...")


def cargar_expedientes():
    """Lee los expedientes almacenados en el archivo CSV."""
    expedientes = []

    if not os.path.exists(ARCHIVO):
        return expedientes

    try:
        with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                expedientes.append(fila)
    except (OSError, csv.Error) as error:
        print(f"No se pudo leer el archivo: {error}")

    return expedientes


def guardar_expedientes(expedientes):
    """Guarda todos los expedientes en el archivo CSV."""
    try:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(expedientes)
        return True
    except OSError as error:
        print(f"No se pudo guardar la información: {error}")
        return False


def solicitar_dato(mensaje):
    """Solicita un dato obligatorio y evita que quede vacío."""
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("El dato es obligatorio. Intente nuevamente.")


def validar_dni(dni):
    """Verifica que el DNI tenga exactamente ocho dígitos."""
    return dni.isdigit() and len(dni) == 8


def solicitar_dni():
    """Solicita un DNI válido al usuario."""
    while True:
        dni = input("DNI del ciudadano (8 dígitos): ").strip()
        if validar_dni(dni):
            return dni
        print("El DNI debe contener exactamente 8 dígitos numéricos.")


def generar_codigo(expedientes):
    """Genera un código correlativo con el formato EXP-0001."""
    mayor = 0
    for expediente in expedientes:
        codigo = expediente.get("codigo", "")
        try:
            numero = int(codigo.split("-")[-1])
            mayor = max(mayor, numero)
        except (ValueError, IndexError):
            continue
    return f"EXP-{mayor + 1:04d}"


def registrar_expediente(expedientes):
    """Solicita los datos, valida la información y registra un expediente."""
    print("\n--- REGISTRO DE EXPEDIENTE ---")
    dni = solicitar_dni()
    ciudadano = solicitar_dato("Nombres y apellidos: ")
    tipo_documento = solicitar_dato("Tipo de documento: ")
    asunto = solicitar_dato("Asunto: ")
    descripcion = solicitar_dato("Descripción breve: ")
    area = solicitar_dato("Área responsable: ")

    expediente = {
        "codigo": generar_codigo(expedientes),
        "dni": dni,
        "ciudadano": ciudadano,
        "tipo_documento": tipo_documento,
        "asunto": asunto,
        "descripcion": descripcion,
        "fecha_recepcion": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "area_responsable": area,
        "estado": "Recibido",
    }

    expedientes.append(expediente)
    if guardar_expedientes(expedientes):
        print("\nExpediente registrado correctamente.")
        print(f"Código asignado: {expediente['codigo']}")
        print(f"Fecha de recepción: {expediente['fecha_recepcion']}")
    else:
        expedientes.pop()
        print("El expediente no pudo ser guardado.")


def buscar_expediente(expedientes):
    """Busca un expediente mediante su código de identificación."""
    print("\n--- CONSULTA DE EXPEDIENTE ---")
    codigo_buscado = solicitar_dato("Ingrese el código (ejemplo EXP-0001): ").upper()

    for expediente in expedientes:
        if expediente["codigo"].upper() == codigo_buscado:
            mostrar_expediente(expediente)
            return

    print("No se encontró un expediente con ese código.")


def ordenar_expedientes(expedientes):
    """Ordena los expedientes por código usando el método burbuja."""
    ordenados = expedientes.copy()
    n = len(ordenados)

    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):
            if ordenados[j]["codigo"] > ordenados[j + 1]["codigo"]:
                ordenados[j], ordenados[j + 1] = ordenados[j + 1], ordenados[j]
                hubo_cambio = True
        if not hubo_cambio:
            break

    return ordenados


def mostrar_expediente(expediente):
    """Muestra los datos de un expediente con formato legible."""
    print("\n" + "=" * 55)
    print(f"Código:          {expediente['codigo']}")
    print(f"Ciudadano:       {expediente['ciudadano']}")
    print(f"DNI:             {expediente['dni']}")
    print(f"Tipo de doc.:    {expediente['tipo_documento']}")
    print(f"Asunto:          {expediente['asunto']}")
    print(f"Descripción:     {expediente['descripcion']}")
    print(f"Fecha recepción: {expediente['fecha_recepcion']}")
    print(f"Área responsable:{expediente['area_responsable']}")
    print(f"Estado:          {expediente['estado']}")
    print("=" * 55)


def mostrar_expedientes(expedientes):
    """Muestra todos los expedientes ordenados por código."""
    print("\n--- LISTA DE EXPEDIENTES ---")
    if not expedientes:
        print("Todavía no hay expedientes registrados.")
        return

    for expediente in ordenar_expedientes(expedientes):
        print(
            f"{expediente['codigo']} | {expediente['ciudadano']} | "
            f"{expediente['asunto']} | {expediente['estado']}"
        )


def mostrar_menu():
    """Muestra el menú principal y devuelve la opción seleccionada."""
    print("\n" + "=" * 55)
    print("       MESA DE PARTES DIGITAL - PROTOTIPO")
    print("=" * 55)
    print("1. Registrar expediente")
    print("2. Consultar expediente por código")
    print("3. Mostrar expedientes ordenados")
    print("4. Salir")
    print("=" * 55)
    return input("Seleccione una opción: ").strip()


def main():
    """Ejecuta el menú principal del sistema."""
    expedientes = cargar_expedientes()

    while True:
        limpiar_pantalla()
        opcion = mostrar_menu()

        if opcion == "1":
            registrar_expediente(expedientes)
            pausa()
        elif opcion == "2":
            buscar_expediente(expedientes)
            pausa()
        elif opcion == "3":
            mostrar_expedientes(expedientes)
            pausa()
        elif opcion == "4":
            print("\nGracias por utilizar la mesa de partes digital.")
            break
        else:
            print("Opción no válida. Seleccione una opción del 1 al 4.")
            pausa()


if __name__ == "__main__":
    main()
