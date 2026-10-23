# Hands-on — Sesión 11: Backend mínimo y su DPIA

**Curso:** DS3031 — Ética y Seguridad de Datos
**Grupo / autor:** Joaquín Salazar
**Entrega:** 23/10/2026

## Quickstart (3 comandos)

```bash
pip install -r requirements.txt
FLASK_APP=app python3 -m flask run --port 5050
```

Abrir **http://localhost:5050/** — ahí está el formulario de registro y el botón para ver los registros guardados.

## Contenido de esta carpeta

| Ruta | Descripción |
|---|---|
| `app.py` | Backend mínimo (Flask + SQLite) descrito en el Paso 1 del laboratorio. Expone `POST /registro`, `GET /registros` y `GET /` (sirve el frontend). Construido deliberadamente sin protecciones de privacidad, tal como pide el enunciado. |
| `static/index.html` | Frontend mínimo: formulario de registro (nombres, apellidos, correo, teléfono) y botón para listar los registros existentes, consumiendo la misma API. |
| `requirements.txt` | Única dependencia: `flask`. |
| `docs/plantilla_DPIA.md` | Evaluación de Impacto en la Protección de Datos (DPIA) del backend, siguiendo la estructura del template oficial de DPIA (ICO): datos del responsable, Pasos 1-2 (necesidad y descripción del tratamiento), Paso 4 (necesidad y proporcionalidad), Paso 5 (riesgos), Paso 6 (medidas de mitigación) y Paso 7 (firmas y decisión). |
| `docs/checklist.md` | Checklist oficial del curso ("IntroPrivacy Checklist", 21 ítems en 6 categorías), evaluado contra el backend real, con referencias cruzadas a los riesgos (R1-R6) y restricciones (C-01-C06) de la DPIA. |
| `.gitignore` | Excluye `lab.db` del control de versiones — nunca se sube una base de datos con registros, ni siquiera de prueba. |

## Probar la API directamente (alternativa al formulario)

```bash
curl -X POST localhost:5050/registro -H "Content-Type: application/json" \
  -d '{"nombres":"Ana","apellidos":"Quispe","correo":"ana@correo.pe","telefono":"987654321"}'

curl localhost:5050/registros
```

## Resumen del ejercicio

1. Se construyó el backend mínimo y se verificó su comportamiento con 4 registros de prueba: `GET /registros` devuelve todos los datos personales (nombre, correo, teléfono) sin ningún control de acceso.
2. Se realizó la DPIA de ese mismo backend (`docs/plantilla_DPIA.md`), identificando 6 riesgos concretos (desde la falta de autenticación hasta la ausencia de registro de consentimiento) y una restricción de diseño verificable por cada uno.
3. El checklist oficial del curso (`docs/checklist.md`) confirma, ítem por ítem, que ninguna de las 21 medidas de privacidad está implementada — resultado esperado, ya que el Paso 1 pide construir el sistema sin protecciones para que la DPIA sea la que las identifique.
4. **Decisión de la DPIA:** el sistema no puede lanzarse en su estado actual; puede lanzarse con condiciones una vez implementadas las restricciones C-01 a C-06.
