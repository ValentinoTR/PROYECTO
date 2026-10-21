"""Interfaz de consola del prototipo académico; no conecta con SUNAT."""
import argparse
from pathlib import Path
from almacenamiento import cargar, guardar
from dominio import crear_expediente, buscar, ordenar


def mostrar(registro):
    print(" | ".join(f"{k}: {v}" for k, v in registro.items()))


def registrar(registros, ruta):
    nuevo = crear_expediente(
        registros, input("DNI: "), input("Nombres: "),
        input("Asunto: "), input("Área o tipo de trámite (referencia académica): "))
    candidatos = registros + [nuevo]
    guardar(ruta, candidatos)  # Confirmar en memoria solo si persiste en disco.
    registros.append(nuevo)
    print(f"Registrado y guardado: {nuevo['codigo']}")


def ejecutar(ruta):
    print("MESA DE PARTES - PROTOTIPO ACADÉMICO / CASO SUNAT")
    print("Simulación local: no presenta trámites ante SUNAT.")
    try:
        registros = cargar(ruta)
    except (OSError, ValueError, UnicodeError) as error:
        print(f"No se puede cargar el archivo: {error}")
        print("El archivo original no se modificó. Revíselo antes de continuar.")
        return 1
    print(f"Registros cargados: {len(registros)}")
    try:
        while True:
            print("\n1. Registrar  2. Buscar  3. Listar ordenados  4. Salir")
            opcion = input("Opción: ").strip()
            try:
                if opcion == "1":
                    registrar(registros, ruta)
                elif opcion == "2":
                    encontrado = buscar(registros, input("Código: "))
                    if encontrado is None:
                        print("No se encontró el expediente.")
                    else:
                        mostrar(encontrado)
                elif opcion == "3":
                    if not registros:
                        print("No hay expedientes registrados.")
                    for registro in ordenar(registros):
                        mostrar(registro)
                elif opcion == "4":
                    print("Fin. Los registros confirmados ya están guardados.")
                    return 0
                else:
                    print("Opción inválida. Seleccione del 1 al 4.")
            except (OSError, ValueError, UnicodeError) as error:
                print(f"Operación no completada: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada interrumpida. Se conservan los registros confirmados.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archivo", type=Path,
                        default=Path(__file__).resolve().parent / "datos" / "expedientes.json")
    raise SystemExit(ejecutar(parser.parse_args().archivo))
