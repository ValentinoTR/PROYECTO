# Decisiones de diseño

Se elige Python, una lista de diccionarios y un archivo JSON UTF-8. Cada expediente tiene código EXP-000001, DNI como cadena, nombres, asunto, área, fecha ISO y estado RECIBIDO. Se genera el siguiente código a partir del mayor existente, nunca de la posición del registro.

Búsqueda lineal O(n); ordenamiento por inserción O(n²) en el peor caso. La lista conserva sus registros originales cuando se presenta una vista ordenada. La persistencia requiere O(n) por guardado porque serializa la colección completa.

Se rechazan campos vacíos, controles de texto, DNI de formato incorrecto, códigos duplicados, esquema de archivo inválido y fechas imposibles. El archivo inexistente inicia una lista vacía; un archivo corrupto bloquea el inicio para evitar sobrescribirlo. El alta solo se confirma tras guardar correctamente. El reemplazo de un archivo temporal en la misma carpeta reduce el riesgo de escritura parcial, pero no sustituye respaldos ni permite concurrencia.
