# Prompt para Antigravity: Herramienta Streamlit Manual Comercial de Objeciones

Quiero construir una aplicación en **Streamlit** para uso interno de ejecutivos comerciales de AFP Capital. La herramienta debe funcionar como un **manual interactivo de objeciones comerciales**, útil en reuniones con clientes, capacitaciones, role play y estudio individual.

## Objetivo de la app
Crear una herramienta simple, rápida y práctica que permita a un ejecutivo buscar una objeción de cliente y recibir inmediatamente:

1. Interpretación comercial de la objeción.
2. Preguntas de diagnóstico.
3. Respuesta comercial sugerida.
4. Argumentos de apoyo.
5. Herramientas o evidencias recomendadas.
6. Cierre sugerido.
7. Errores a evitar.
8. Versión breve para WhatsApp.
9. Versión para llamada.
10. Versión para reunión presencial o Teams.

La herramienta debe tener una finalidad comercial, no académica. Debe ayudar a avanzar la conversación hacia un siguiente paso concreto.

---

## Requisitos funcionales

### 1. Página principal
Debe mostrar:
- Título: **Manual Comercial de Objeciones AFP Capital**.
- Subtítulo: **Convierte dudas en conversaciones y conversaciones en cierres**.
- Buscador general por palabra clave.
- Filtros por:
  - Categoría.
  - Producto.
  - Canal de uso.
  - Nivel de dificultad.

### 2. Categorías mínimas
La app debe incluir estas categorías:
- Costos.
- Cambio de AFP.
- Servicio.
- Rentabilidad.
- Fondos y riesgo.
- Sistema previsional.
- Incentivos indebidos.
- APV.
- Cuenta 2.
- Ahorro voluntario.
- Objeciones de tiempo.
- Objeciones de confianza.

### 3. Vista de tarjetas
Cada objeción debe verse como una tarjeta expandible con:
- Objeción textual del cliente.
- Qué hay detrás.
- Preguntas de diagnóstico.
- Respuesta recomendada.
- Argumentos.
- Evidencia o herramienta sugerida.
- Cierre.
- Errores a evitar.
- Botones para copiar:
  - Respuesta completa.
  - Respuesta WhatsApp.
  - Respuesta llamada.
  - Cierre sugerido.

### 4. Modo reunión
Crear un modo llamado **Modo Reunión**.
Debe mostrar una versión muy breve y accionable:
- Objeción.
- 3 preguntas clave.
- Respuesta de 30 segundos.
- Cierre recomendado.

Este modo debe ser útil para usar mientras el ejecutivo está con el cliente.

### 5. Modo estudio
Crear un modo llamado **Modo Estudio**.
Debe incluir:
- Explicación más desarrollada.
- Role play sugerido.
- Preguntas para practicar.
- Checklist de dominio.

### 6. Modo role play
Crear un modo en que la app muestre:
- Objeción aleatoria.
- Contexto del cliente.
- Producto involucrado.
- Nivel de dificultad.
- Campo para que el ejecutivo escriba su respuesta.
- Luego mostrar respuesta sugerida y checklist de evaluación.

Checklist de evaluación:
- ¿Escuchó y validó la objeción?
- ¿Hizo preguntas antes de responder?
- ¿Conectó con el objetivo del cliente?
- ¿Usó evidencia o herramienta?
- ¿Cerró con un siguiente paso?
- ¿Evitó prometer rentabilidad futura?

### 7. Modo WhatsApp
Crear un generador de mensaje breve por objeción.
Debe permitir seleccionar tono:
- Cercano.
- Ejecutivo.
- Directo.
- Educativo.

Debe generar un texto breve, listo para copiar y enviar.

### 8. Módulo de cumplimiento
Agregar una sección fija llamada **Buenas prácticas y cumplimiento** con advertencias:
- No prometer rentabilidades futuras.
- No desacreditar a la competencia.
- No ofrecer incentivos indebidos.
- Validar comisiones, topes, beneficios tributarios y normativa vigente antes de usar datos con clientes.
- Registrar la objeción y el siguiente paso en CRM.

### 9. Módulo editable de parámetros
Crear una página de configuración donde pueda actualizar manualmente variables comerciales como:
- Comisión APV AFP Capital.
- Comisión Cuenta 2 AFP Capital.
- Comisión Cuenta Obligatoria.
- Topes tributarios.
- Link a simuladores internos.
- Link a comparadores.
- Frases institucionales autorizadas.

Estas variables no deben quedar rígidas en el código. Deben guardarse en un archivo JSON o YAML editable.

### 10. Exportación
La app debe permitir exportar:
- Una objeción seleccionada a Markdown.
- Una ficha de estudio en PDF o Markdown.
- El listado completo de objeciones a CSV.

---

## Requisitos de diseño

Usar diseño limpio y ejecutivo.

### Estilo visual
- Fondo claro.
- Tarjetas con bordes suaves.
- Uso moderado de color.
- Semáforo para nivel de urgencia o sensibilidad:
  - Verde: objeción simple.
  - Amarillo: requiere diagnóstico.
  - Rojo: requiere cuidado normativo o reputacional.

### Navegación lateral
Incluir sidebar con:
- Inicio.
- Buscar objeción.
- Modo reunión.
- Modo estudio.
- Role play.
- WhatsApp.
- Configuración.
- Buenas prácticas.

---

## Estructura de datos sugerida

Crear un archivo `objeciones.json` con esta estructura:

```json
[
  {
    "id": "OBJ-001",
    "categoria": "Costos",
    "producto": ["Cuenta Obligatoria", "APV", "Cuenta 2"],
    "canal": ["Reunión", "Llamada", "WhatsApp"],
    "nivel": "Intermedio",
    "sensibilidad": "Amarillo",
    "objecion_cliente": "Ustedes son más caros",
    "fondo_real": "El cliente quiere saber si el mayor costo se justifica con valor real.",
    "preguntas_diagnostico": [
      "Cuando dice caro, ¿lo está mirando como monto mensual o como impacto sobre su pensión futura?",
      "¿Qué espera recibir a cambio de la comisión que paga?",
      "¿Hoy siente que su AFP actual lo asesora activamente?"
    ],
    "respuesta_comercial": "Entiendo perfectamente su preocupación. Nadie quiere pagar más sin una razón clara. Por eso mi propuesta no es que tome la decisión sólo mirando la comisión, sino mirando el valor completo: asesoría, elección de fondos, planificación de APV, beneficios tributarios, seguimiento y acompañamiento.",
    "argumentos": [
      "El costo es importante, pero no debe analizarse aislado.",
      "Una mala elección de fondo, régimen tributario o producto puede costar más que una diferencia de comisión.",
      "La asesoría permite transformar información en decisiones concretas."
    ],
    "herramientas": [
      "Comparador de costos",
      "Simulador APV A/B",
      "Diagnóstico de multifondo"
    ],
    "cierre": "Revisemos cuánto representa la diferencia de costo en pesos y contrastémosla con las oportunidades que podríamos capturar con una asesoría bien hecha. ¿Le parece?",
    "whatsapp": "Entiendo tu preocupación por el costo. La idea es revisarlo con datos: cuánto representa realmente y qué valor podríamos generar con asesoría, fondos, APV o beneficios tributarios. Lo vemos y decides informado.",
    "llamada": "Le propongo revisar el costo en pesos y compararlo contra el valor de la asesoría. Si no vemos una oportunidad concreta, se lo diré con claridad.",
    "errores_evitar": [
      "Decir simplemente que no somos caros.",
      "Defender la comisión sin mostrar valor.",
      "No cuantificar la diferencia."
    ]
  }
]
```

---

## Arquitectura de archivos sugerida

```text
manual_objeciones_app/
│
├── app.py
├── data/
│   ├── objeciones.json
│   └── parametros.json
│
├── pages/
│   ├── 1_Buscar_Objecion.py
│   ├── 2_Modo_Reunion.py
│   ├── 3_Modo_Estudio.py
│   ├── 4_Role_Play.py
│   ├── 5_WhatsApp.py
│   ├── 6_Configuracion.py
│   └── 7_Buenas_Practicas.py
│
├── utils/
│   ├── loaders.py
│   ├── search.py
│   ├── exporters.py
│   └── templates.py
│
├── requirements.txt
└── README.md
```

---

## Librerías sugeridas

Usar:
- streamlit
- pandas
- json
- pathlib
- rapidfuzz o difflib para búsqueda flexible
- pyyaml si se usa YAML
- markdown o fpdf si se exporta PDF

---

## Flujo de uso esperado

1. Ejecutivo abre la app.
2. Busca “caro”, “rentabilidad”, “no tengo tiempo”, “no tengo plata”, etc.
3. La app muestra objeciones relacionadas.
4. Ejecutivo abre una tarjeta.
5. Usa preguntas de diagnóstico.
6. Copia una respuesta o cierre.
7. Registra resultado en CRM.
8. En capacitación, usa el modo role play.

---

## Priorización MVP

Construir primero:
1. Carga de objeciones desde JSON.
2. Buscador y filtros.
3. Tarjetas expandibles.
4. Modo reunión.
5. Modo WhatsApp.
6. Página de buenas prácticas.

Luego agregar:
1. Role play.
2. Exportación.
3. Parámetros editables desde UI.
4. Métricas de uso.
5. Login o control de acceso, si corresponde.

---

## Instrucción importante

No hardcodear datos normativos o comisiones en el texto final de la aplicación. Deben venir desde `parametros.json` y ser fáciles de actualizar.

La herramienta debe estar redactada en español de Chile, con tono profesional, comercial, claro, simple y orientado a cierre consultivo.
