"""Reglas del prototipo y algoritmos básicos, sin dependencias externas."""
import re
from datetime import date, datetime, timezone, timedelta

CAMPOS = {"codigo", "dni", "nombres", "asunto", "area", "fecha", "estado"}


def texto(valor, etiqueta, minimo, maximo):
    if not isinstance(valor, str) or any(ord(c) < 32 for c in valor):
        raise ValueError(f"{etiqueta}: ingrese texto sin caracteres de control.")
    limpio = " ".join(valor.split())
    if not minimo <= len(limpio) <= maximo:
        raise ValueError(f"{etiqueta}: use entre {minimo} y {maximo} caracteres.")
    return limpio


def validar_datos(dni, nombres, asunto, area):
    if not isinstance(dni, str) or not re.fullmatch(r"[0-9]{8}", dni.strip()):
        raise ValueError("DNI: se requieren exactamente 8 dígitos del 0 al 9.")
    return {
        "dni": dni.strip(),
        "nombres": texto(nombres, "Nombres", 2, 100),
        "asunto": texto(asunto, "Asunto", 5, 200),
        "area": texto(area, "Área", 2, 80),
    }


def normalizar_codigo(codigo):
    if not isinstance(codigo, str):
        raise ValueError("Código inválido; ejemplo: EXP-000001.")
    codigo = codigo.strip().upper()
    if not re.fullmatch(r"EXP-[0-9]{6}", codigo) or codigo == "EXP-000000":
        raise ValueError("Código inválido; ejemplo: EXP-000001.")
    return codigo


def validar_coleccion(registros):
    if not isinstance(registros, list):
        raise ValueError("El archivo debe contener una lista.")
    usados = set()
    for r in registros:
        if not isinstance(r, dict) or set(r) != CAMPOS:
            raise ValueError("Estructura de expediente inválida.")
        codigo = normalizar_codigo(r["codigo"])
        if codigo != r["codigo"] or codigo in usados:
            raise ValueError("Código duplicado o no normalizado.")
        usados.add(codigo)
        datos = validar_datos(r["dni"], r["nombres"], r["asunto"], r["area"])
        if any(r[k] != v for k, v in datos.items()):
            raise ValueError("Datos del archivo no normalizados.")
        if not isinstance(r["fecha"], str):
            raise ValueError("Fecha inválida.")
        fecha = date.fromisoformat(r["fecha"])
        if fecha.isoformat() != r["fecha"] or r["estado"] != "RECIBIDO":
            raise ValueError("Fecha o estado inválido.")


def siguiente_codigo(registros):
    mayor = max((int(r["codigo"][4:]) for r in registros), default=0)
    if mayor >= 999999:
        raise ValueError("Se alcanzó la capacidad del código de seis dígitos.")
    return f"EXP-{mayor + 1:06d}"


def crear_expediente(registros, dni, nombres, asunto, area):
    datos = validar_datos(dni, nombres, asunto, area)
    return dict(codigo=siguiente_codigo(registros), **datos,
                fecha=datetime.now(timezone(timedelta(hours=-5))).date().isoformat(),
                estado="RECIBIDO")


def buscar(registros, codigo):
    codigo = normalizar_codigo(codigo)
    for registro in registros:
        if registro["codigo"] == codigo:
            return registro
    return None


def ordenar(registros):
    """Inserción ascendente por código sobre una copia de la lista."""
    resultado = registros.copy()
    for i in range(1, len(resultado)):
        actual = resultado[i]
        j = i - 1
        while j >= 0 and resultado[j]["codigo"] > actual["codigo"]:
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = actual
    return resultado
