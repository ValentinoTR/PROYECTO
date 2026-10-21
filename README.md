# Mesa de partes: prototipo académico

Proyecto de Fundamentos de Programación. Caso de referencia: SUNAT. Desarrollo asistido por IA para los pasos 1 a 6 de la consigna. Los registros de demostración son ficticios. No se ha realizado una visita ni una entrevista institucional. SUNAT ya cuenta con una mesa de partes virtual: este programa local es una simplificación académica y no se conecta con ella.

## Ejecutar

Requiere Python 3.10 o posterior, sin paquetes adicionales.

```text
python main.py
python -m unittest discover -s tests -v
```

En Windows también puede usarse `py main.py`. El programa registra expedientes, valida datos, busca por código, ordena por código y conserva datos en `datos/expedientes.json`. Se ejecuta desde cualquier carpeta; el archivo queda junto al proyecto. Para elegir otro archivo: `python main.py --archivo ruta/expedientes.json`.

## Alcance

Un operador y una instancia del programa a la vez. Admite personas identificadas mediante DNI de ocho dígitos; esta regla valida el formato, no la identidad. No recibe archivos adjuntos ni envía notificaciones. No es un sistema institucional desplegable sin controles de acceso, copias de seguridad y validación adicional.

## Diseño

- `dominio.py`: validaciones, códigos, búsqueda lineal y ordenamiento por inserción.
- `almacenamiento.py`: lectura JSON validada y escritura temporal con reemplazo.
- `main.py`: menú, registro y consultas.
- `tests/test_sistema.py`: pruebas automatizadas con datos sintéticos y archivos temporales.

## Evidencia y pendientes

El historial Git registra avances reales de esta sesión, con autoría identificada como asistencia de IA; no representa trabajo previo del equipo. Repositorio de destino: https://github.com/ValentinoTR/PROYECTO. Completar sede de SUNAT, integrantes, fotografías fechadas, entrevista, tiempos y pruebas de campo antes de presentar como informe de trabajo real. Adjuntar el formato oficial de declaración de uso de IA del aula virtual.

## Repositorio y paquete

Repositorio: https://github.com/ValentinoTR/PROYECTO. Para continuar el trabajo publicado, clonar ese repositorio. El ZIP incluye el informe PDF, su versión editable Markdown, diagramas, evidencias y un archivo `historial.bundle` que conserva el historial local. El historial remoto y el local tienen identificadores distintos porque se publicaron por mecanismos diferentes; ambos corresponden a esta sesión.

```text
git clone https://github.com/ValentinoTR/PROYECTO.git
```

Para recuperar únicamente el historial local desde el paquete:

```text
git clone historial.bundle mesa_partes_restaurada
```

No se debe forzar una subida del historial local sobre el remoto. El ZIP no necesita incluir la carpeta oculta `.git`: el bundle permite reconstruirla.

## Informe y evidencias

- `documentacion/Informe_SUNAT_Pasos_1_al_6.pdf`: informe para leer.
- `documentacion/Informe_editable.md`: texto editable con tablas y pseudocódigo.
- `documentacion/diagrama.svg`: diagrama editable en formato vectorial.
- `evidencias/pruebas.txt`: salida íntegra de las pruebas ejecutadas.
- `evidencias/demo.txt`: salida de registro y consulta tras reiniciar.
- `evidencias/*.png`: renderizaciones del código y las salidas reales.

El informe contiene los formularios pendientes de campo; deben completarse con observaciones reales y autorizadas. Fuente de referencia de SUNAT: https://orientacion.sunat.gob.pe/mesa-de-partes-virtual.
