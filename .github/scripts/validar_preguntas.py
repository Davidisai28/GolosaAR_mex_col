import json
import re
import sys
from pathlib import Path

BASE = Path("Assets/Resources/Questions")

ARCHIVOS = {
    "preguntas_infantil.json": "infantil",
    "preguntas_avanzados.json": "avanzados",
}

CAMPOS = {
    "id", "categoria", "nivel", "pregunta",
    "opciones", "respuestaCorrecta", "fuente"
}

errores = []
ids_encontrados = {}


def error(archivo, mensaje):
    errores.append(f"{archivo}: {mensaje}")


for nombre, nivel_esperado in ARCHIVOS.items():
    ruta = BASE / nombre
    print(f"\nRevisando {ruta}...")

    if not ruta.is_file():
        print(
            f"::warning::{nombre} todavía no existe. "
            "Se permite durante los primeros incrementos."
        )
        continue

    try:
        datos = json.loads(ruta.read_text(encoding="utf-8-sig"))
    except (ValueError, UnicodeError) as exc:
        error(nombre, f"JSON inválido: {exc}")
        continue

    if not isinstance(datos, dict):
        error(nombre, "La raíz debe ser un objeto JSON.")
        continue

    preguntas = datos.get("preguntas")

    if not isinstance(preguntas, list):
        error(nombre, "'preguntas' debe ser un arreglo.")
        continue

    # Los bancos vacíos son válidos durante el desarrollo.
    if not preguntas:
        print("Banco vacío: válido por ahora.")
        continue

    for numero, pregunta in enumerate(preguntas, start=1):
        referencia = f"{nombre}, pregunta {numero}"

        if not isinstance(pregunta, dict):
            error(referencia, "Debe ser un objeto JSON.")
            continue

        faltantes = CAMPOS - pregunta.keys()
        if faltantes:
            error(referencia, f"Faltan campos: {sorted(faltantes)}")

        for campo in ("id", "categoria", "nivel", "pregunta", "fuente"):
            valor = pregunta.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                error(referencia, f"'{campo}' debe ser texto no vacío.")

        identificador = pregunta.get("id")
        if isinstance(identificador, str):
            if not re.fullmatch(r"GL-\d{3,}", identificador):
                error(referencia, "ID inválido. Ejemplo: GL-001.")

            if identificador in ids_encontrados:
                error(
                    referencia,
                    f"ID duplicado: {identificador}. "
                    f"Primera aparición: {ids_encontrados[identificador]}"
                )
            else:
                ids_encontrados[identificador] = referencia

        if pregunta.get("nivel") != nivel_esperado:
            error(
                referencia,
                f"El nivel debe ser '{nivel_esperado}'."
            )

        opciones = pregunta.get("opciones")
        if not isinstance(opciones, list) or len(opciones) != 4:
            error(referencia, "'opciones' debe tener exactamente 4 elementos.")
        else:
            if any(
                not isinstance(opcion, str) or not opcion.strip()
                for opcion in opciones
            ):
                error(referencia, "Las opciones deben ser textos no vacíos.")

            opciones_normalizadas = [
                opcion.strip().casefold()
                for opcion in opciones
                if isinstance(opcion, str)
            ]

            if len(set(opciones_normalizadas)) != len(opciones):
                error(referencia, "Hay opciones repetidas.")

        respuesta = pregunta.get("respuestaCorrecta")
        if type(respuesta) is not int or not 0 <= respuesta <= 3:
            error(referencia, "'respuestaCorrecta' debe estar entre 0 y 3.")

    print(f"Preguntas encontradas: {len(preguntas)}")


print("\n===== RESULTADO DEL VERIFICADOR =====")

if errores:
    for mensaje in errores:
        print(f"::error::{mensaje}")
    print(f"\nFalló la validación: {len(errores)} error(es).")
    sys.exit(1)

print("Todos los bancos de preguntas son válidos.")
sys.exit(0)
