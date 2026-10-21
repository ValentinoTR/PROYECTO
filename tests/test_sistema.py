"""Pruebas reproducibles con identidades ficticias, nunca expedientes reales."""
import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from dominio import crear_expediente, buscar, ordenar, validar_datos, siguiente_codigo
from almacenamiento import cargar, guardar
from main import registrar, ejecutar


def ejemplo(registros=None):
    return crear_expediente(registros or [], "00000001", "Persona Prueba Uno",
                            "Solicitud ficticia de demostración", "Administrativos")


class PruebasSistema(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ruta = Path(self.temp.name) / "expedientes.json"

    def test_01_archivo_inexistente(self):
        self.assertEqual(cargar(self.ruta), [])

    def test_02_registro_valido_y_normalizacion(self):
        r = crear_expediente([], " 00000001 ", " Persona   Prueba ", "Solicitud ficticia", "Tributos internos")
        self.assertEqual(r["codigo"], "EXP-000001")
        self.assertEqual(r["nombres"], "Persona Prueba")
        self.assertEqual(r["dni"], "00000001")

    def test_03_dni_invalido(self):
        for dni in ["", "123", "123456789", "1234567A", "１２３４５６７８", 12345678]:
            with self.subTest(dni=dni), self.assertRaises(ValueError):
                validar_datos(dni, "Persona Prueba", "Solicitud ficticia", "Administrativos")

    def test_04_campos_vacios_y_limites(self):
        for nombres, asunto, area in [(" ", "Solicitud", "Área"), ("Persona", " ", "Área"),
                                      ("Persona", "Solicitud", ""), ("X" * 101, "Solicitud", "Área"),
                                      ("Persona", "X" * 201, "Área"), ("Persona", "Solicitud", "X" * 81),
                                      ("Persona\nPrueba", "Solicitud", "Área")]:
            with self.subTest(nombres=nombres, asunto=asunto, area=area), self.assertRaises(ValueError):
                validar_datos("00000001", nombres, asunto, area)

    def test_05_busqueda_existente_ausente_y_formato(self):
        r = ejemplo()
        self.assertEqual(buscar([r], " exp-000001 "), r)
        self.assertIsNone(buscar([r], "EXP-000002"))
        with self.assertRaises(ValueError):
            buscar([r], "EXP-1")

    def test_06_ordenamiento_y_no_mutacion(self):
        registros = [dict(ejemplo(), codigo=f"EXP-{n:06d}") for n in [10, 2, 1, 20]]
        copia = copy.deepcopy(registros)
        self.assertEqual([r["codigo"] for r in ordenar(registros)],
                         ["EXP-000001", "EXP-000002", "EXP-000010", "EXP-000020"])
        self.assertEqual(registros, copia)
        self.assertEqual(ordenar([]), [])
        self.assertEqual(ordenar([registros[0]]), [registros[0]])

    def test_07_persistencia_y_siguiente_codigo(self):
        guardar(self.ruta, [ejemplo()])
        recuperados = cargar(self.ruta)
        self.assertEqual(recuperados[0]["asunto"], "Solicitud ficticia de demostración")
        self.assertEqual(ejemplo(recuperados)["codigo"], "EXP-000002")

    def test_08_codigo_usa_maximo_y_detecta_agotamiento(self):
        self.assertEqual(siguiente_codigo([dict(ejemplo(), codigo="EXP-000009"), ejemplo()]), "EXP-000010")
        with self.assertRaises(ValueError):
            siguiente_codigo([dict(ejemplo(), codigo="EXP-999999")])

    def test_09_archivo_corrupto_no_se_sobrescribe(self):
        self.ruta.write_text("{mal json", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ejecutar(self.ruta), 1)
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), "{mal json")

    def test_10_esquema_fecha_y_duplicados(self):
        casos = [{}, [{}], [dict(ejemplo(), fecha="2026-02-30")],
                 [ejemplo(), ejemplo()], [dict(ejemplo(), estado="INVALIDO")]]
        for registros in casos:
            with self.subTest(registros=registros):
                self.ruta.write_text(json.dumps(registros), encoding="utf-8")
                with self.assertRaises(ValueError):
                    cargar(self.ruta)

    def test_11_fallo_reemplazo_preserva_archivo(self):
        guardar(self.ruta, [ejemplo()])
        previo = self.ruta.read_bytes()
        with patch("almacenamiento.os.replace", side_effect=PermissionError("Simulado")):
            with self.assertRaises(PermissionError):
                guardar(self.ruta, [ejemplo(), ejemplo([ejemplo()])])
        self.assertEqual(self.ruta.read_bytes(), previo)
        self.assertEqual(list(self.ruta.parent.glob("*.tmp")), [])

    def test_12_fallo_guardado_no_confirma_alta(self):
        registros = []
        with patch("builtins.input", side_effect=["00000001", "Persona Prueba", "Solicitud ficticia", "Administrativos"]), \
             patch("main.guardar", side_effect=OSError("Simulado")):
            with self.assertRaises(OSError):
                registrar(registros, self.ruta)
        self.assertEqual(registros, [])

    def test_13_menu_flujo_completo_y_reinicio(self):
        salida = io.StringIO()
        entradas = ["9", "3", "1", "00000001", "Persona Prueba", "Solicitud ficticia", "Administrativos",
                    "2", "EXP-000001", "2", "EXP-000002", "3", "4"]
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(salida):
            self.assertEqual(ejecutar(self.ruta), 0)
        self.assertEqual(len(cargar(self.ruta)), 1)
        for mensaje in ["Opción inválida", "No hay expedientes", "Registrado y guardado: EXP-000001", "No se encontró"]:
            self.assertIn(mensaje, salida.getvalue())
        with patch("builtins.input", return_value="4"), contextlib.redirect_stdout(salida):
            self.assertEqual(ejecutar(self.ruta), 0)
        self.assertIn("Registros cargados: 1", salida.getvalue())

    def test_14_interrupcion_y_utf8_invalido(self):
        with patch("builtins.input", side_effect=EOFError), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ejecutar(self.ruta), 0)
        self.ruta.write_bytes(b"\xff\xfe")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ejecutar(self.ruta), 1)
        self.assertEqual(self.ruta.read_bytes(), b"\xff\xfe")


if __name__ == "__main__":
    unittest.main(verbosity=2)
