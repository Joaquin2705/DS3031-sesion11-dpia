# Evaluación de Impacto en la Protección de Datos (DPIA)

**Curso:** DS3031 — Ética y Seguridad de Datos · Sesión 11, Laboratorio
**Sistema evaluado:** `app.py` — backend Flask + SQLite con los endpoints `POST /registro` y `GET /registros` (código completo en `app.py`, en esta misma carpeta).
**Autor:** Joaquín Salazar · **Fecha:** 23/10/2026

*Estructura basada en el template oficial de DPIA (ICO — Information Commissioner's Office, Reino Unido), adaptada al caso del laboratorio.*

---

## Datos del responsable del tratamiento

| Campo | Valor |
|---|---|
| Nombre del responsable | Joaquín Salazar |
| Cargo / rol del DPO | Autor del ejercicio (rol asumido para este laboratorio) |
| Contacto del responsable / DPO | joaquin.salazar.p@utec.edu.pe |

---

## Paso 1 — Identificar la necesidad de la DPIA

El proyecto consiste en un backend mínimo que recolecta nombres, apellidos, correo y, opcionalmente, teléfono, a través de un endpoint `POST /registro`, y los expone mediante `GET /registros`. Se identificó la necesidad de esta DPIA porque el sistema, tal como fue construido en el Paso 1 del laboratorio, carece deliberadamente de controles básicos de privacidad: no implementa autenticación, no cifra los datos en reposo, no registra consentimiento y no define ningún plazo de retención. Aunque el volumen de datos es pequeño, el tratamiento afecta a información personal identificable y el endpoint de lectura está abierto a cualquiera que conozca la URL — un criterio suficiente para justificar una evaluación de impacto antes de procesar datos reales.

---

## Paso 2 — Descripción del tratamiento

### Naturaleza

Los datos se recolectan directamente del titular mediante una solicitud `POST` con cuerpo JSON (formulario, Postman o `curl`). Flask inserta el registro en una base de datos SQLite local (`lab.db`), sin cifrado. Cualquier cliente puede leer el contenido completo de la tabla mediante `GET /registros`, sin autenticación ni registro de quién realizó la consulta. No se declara ninguna cesión a terceros, pero tampoco existe ningún control técnico que la impida. El tratamiento de mayor riesgo identificado es la exposición sin control de acceso de datos personales en un único endpoint de lectura.

### Alcance

No se recolectan datos de categoría especial. El volumen actual es reducido (cuatro registros de prueba), pero el diseño no impone ningún límite: el sistema aceptaría cualquier cantidad de registros reales sin cambios. No existe límite geográfico declarado. La retención es indefinida: no hay ningún mecanismo de expiración ni borrado.

### Contexto

La relación entre el sistema y los titulares es la de un servicio que recolecta datos de registro a cambio de una funcionalidad (en este ejercicio, fines educativos). Los titulares no tienen ningún control sobre sus datos una vez enviados: no pueden consultarlos, corregirlos ni eliminarlos a través del sistema. No se advierte a los titulares, en ningún punto del flujo, qué se hace con su información ni por cuánto tiempo se conserva.

### Propósitos

El propósito declarado del sistema es registrar personas con fines de la actividad del laboratorio. No existe una finalidad declarada para el campo teléfono, que el backend acepta sin justificación. El beneficio esperado (para quien opera el sistema) es contar con un registro simple de contactos; el riesgo para el titular es que sus datos queden expuestos sin ningún control.

---

## Paso 4 — Evaluación de necesidad y proporcionalidad

- **¿El tratamiento logra su objetivo?** Sí, pero con más datos de los necesarios: el objetivo de "registrar a una persona" se cumple con nombres, apellidos y correo. El teléfono no tiene una finalidad declarada en el sistema.
- **¿Hay otra forma de lograr el mismo resultado con menos datos?** Sí: eliminar el campo teléfono mientras no se le asigne una finalidad concreta, o hacerlo condicional a un consentimiento específico separado.
- **Base legal:** relación directa con el servicio para nombres/apellidos/correo; el teléfono carece de base legal declarada, lo que debe corregirse antes de procesar datos reales.
- **Minimización y calidad del dato:** el sistema no valida el formato del correo ni impone restricciones sobre los campos de texto; no hay mecanismo de corrección por parte del titular.
- **Información y derechos del titular:** el sistema no informa nada al titular sobre el tratamiento ni ofrece manera de ejercer derechos de acceso, rectificación, cancelación u oposición.
- **Transferencias y terceros:** no se usan procesadores externos en esta versión del backend; si se agregara uno (por ejemplo, un proveedor de correo), debería mediar un contrato de encargo de tratamiento.

---

## Paso 5 — Identificación y evaluación de riesgos

| ID | Riesgo | Probabilidad | Severidad | Riesgo global |
|---|---|---|---|---|
| R1 | `GET /registros` devuelve nombre, correo y teléfono de todos los titulares a cualquiera que conozca la URL, sin autenticación | Probable | Severa | **Alto** |
| R2 | Correo y teléfono se almacenan en texto plano en `lab.db`; una copia del archivo, una subida accidental a un repositorio o un backup filtrado expondrían todos los registros | Posible | Severa | **Alto** |
| R3 | El teléfono se recolecta sin finalidad declarada ni base legal, lo que contraviene el principio de minimización | Probable | Mínima | Medio |
| R4 | No existe ningún registro de consentimiento (tabla, campo o versión de política); no hay forma de demostrar que el titular aceptó el tratamiento | Probable | Significativa | **Alto** |
| R5 | No existe plazo de retención ni mecanismo de borrado: los datos permanecen en `lab.db` de forma indefinida | Probable | Significativa | **Alto** |
| R6 | `lab.db` reside en el mismo directorio que el código fuente; si el repositorio se publica o se comparte, el archivo con datos reales se expone junto con él | Posible | Severa | Alto |

---

## Paso 6 — Medidas para reducir el riesgo

| ID | Riesgo (mitiga) | Opciones para reducir o eliminar el riesgo | Efecto | Riesgo residual | Medida aprobada |
|---|---|---|---|---|---|
| C-01 | R1 — Exposición de `GET /registros` sin autenticación | Exigir autenticación con rol de administrador; enmascarar correo y teléfono (`a***@correo.pe`) salvo que el solicitante sea el propio titular | Reducido | Bajo | Sí |
| C-02 | R2, R6 — Correo y teléfono en texto plano en `lab.db` | Cifrar correo y teléfono en reposo (Fernet/AES-256); mantener la llave de cifrado fuera del repositorio y de `lab.db` | Reducido | Medio — persiste si la llave y la base residen en el mismo servidor | Sí |
| C-03 | R3 — Teléfono sin finalidad declarada | Declarar la finalidad del teléfono en el aviso de privacidad antes de solicitarlo; eliminarlo si no se le asigna una finalidad real | Reducido | Bajo | Sí |
| C-04 | R4 — Ausencia de registro de consentimiento | Incorporar una tabla `consentimiento(titular_id, finalidad, version_politica, fecha, fecha_retiro)`, poblada en cada `POST /registro`; sin ese registro, la inserción no procede | Reducido | Bajo | Sí |
| C-05 | R5 — Ausencia de plazo de retención | Implementar un proceso programado (semanal) que elimine o anonimice registros con más de 12 meses sin actividad, documentado en la política de privacidad | Reducido | Bajo | Sí |
| C-06 | R6 — `lab.db` expuesto junto con el repositorio | Excluir `lab.db` y cualquier archivo con datos reales del control de versiones (`.gitignore`); no confirmar commits con datos de personas, ni siquiera de prueba con datos verosímiles | Reducido | Bajo | Sí |

---

## Paso 7 — Firmas y registro de resultados

| Ítem | Nombre / cargo / fecha | Notas |
|---|---|---|
| Medidas aprobadas por | Joaquín Salazar — 23/10/2026 | Integrar las medidas al plan del proyecto, con fecha y responsable de implementación |
| Riesgos residuales aprobados por | Joaquín Salazar — 23/10/2026 | El riesgo residual Medio (cifrado) se acepta documentado; no hay riesgo residual alto |
| Asesoría de privacidad brindada por | Joaquín Salazar — 23/10/2026 | El sistema no puede procesar datos reales hasta implementar las medidas del Paso 6 |
| Decisión final | **No se puede lanzar en su estado actual. Se puede lanzar con condiciones**, una vez implementadas todas las medidas del Paso 6 | Es la misma falla de diseño que presentaba el formulario de PromoMax analizado al inicio de la sesión: ausencia de finalidad declarada, de consentimiento verificable y de forma de revocarlo |
| Esta DPIA se revisará por | Por definir | — |
