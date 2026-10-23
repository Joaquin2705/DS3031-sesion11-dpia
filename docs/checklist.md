# Checklist de validación de componentes — Hands-on Sesión 11

**Fuente:** checklist oficial del curso ("IntroPrivacy Checklist"), referenciado en la diapositiva 20 de L11.
**Evaluado contra:** `app.py`, backend mínimo descrito en el Paso 1, ejecutado y verificado.

Leyenda: ✅ implementado · ❌ no implementado (riesgo abierto, correlacionado con la DPIA en `plantilla_DPIA.md`) · N/A no aplica a este sistema.

## Consentimiento y recopilación de datos

- ❌ Mecanismo claro para obtener el consentimiento del usuario antes de recopilar datos (ver riesgo **R4** en la DPIA)
- ❌ Formularios que especifiquen para qué se utilizarán los datos (ver **R3**, **R4**)
- ❌ Evitar la recopilación de datos innecesarios; recopilar solo lo estrictamente necesario — el teléfono se recolecta sin finalidad declarada (**R3**)

## Acceso y control sobre los datos personales

- ❌ Interfaz que permita al usuario acceder a sus propios datos — no existe un endpoint de consulta individual con verificación de identidad
- ❌ Opciones para editar o corregir los datos — no hay endpoint `PUT`/`PATCH`
- ❌ Eliminación de la cuenta y los datos asociados — no hay endpoint `DELETE`
- ❌ Restricción del uso de los datos (máximo 2 datos) — no existe ningún mecanismo de restricción

## Seguridad de datos y protección

- ❌ Cifrado en la base de datos — correo y teléfono se almacenan en texto plano en `lab.db` (**R2**, mitigado por **C-02**)
- N/A Hashing de contraseñas — el sistema no maneja autenticación de usuarios
- N/A Autenticación de dos factores — no hay cuentas administrativas implementadas (la restricción **C-01** exige, como mínimo, autenticación simple para `GET /registros`)
- ❌ Firewalls o sistemas de protección contra intrusos — fuera del alcance de un backend de laboratorio en entorno local

## Transparencia y políticas de privacidad

- ❌ Apartado accesible en el front-end con la política de privacidad — el sistema no cuenta con front-end ni política
- N/A Política de privacidad clara y fácil de entender — no existe todavía
- ❌ Mecanismo para informar cambios en la política de privacidad — no implementado

## Integración de privacidad en el diseño

- ❌ Privacidad integrada desde la fase inicial del diseño de la base de datos y el front-end — el backend se construyó deliberadamente sin estas protecciones, conforme a lo solicitado en el Paso 1 del laboratorio
- ❌ Privacidad considerada en las decisiones de diseño y funcionalidad — ídem
- ❌ Revisiones periódicas de las prácticas de privacidad — no implementado
- ❌ Medidas para eliminar datos antiguos o innecesarios — no existe plazo de retención ni proceso de borrado (**R5**, mitigado por **C-05**)

## Extras

- ❌ Opción para que los usuarios descarguen sus datos en formato legible (portabilidad) — no implementado
- ❌ Protocolos claros ante brechas de seguridad o fuga de datos — abordado solo a nivel teórico (notificación a la ANPD en 48 horas, diapositiva 12), sin implementación en el sistema
- N/A Formación continua del equipo en privacidad y seguridad — no aplica a un entregable de código

---

**Interpretación:** de los 21 ítems del checklist, ninguno está implementado, de forma intencional. El backend se construyó sin protecciones de privacidad para que la DPIA (`plantilla_DPIA.md`) identificara cada vacío como un riesgo concreto y propusiera una restricción verificable. Los ítems marcados con ❌ corresponden exactamente a los riesgos R1–R6 y a las restricciones C-01–C-06 documentados en la DPIA.
