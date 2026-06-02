import streamlit as st
import json
import pandas as pd
import random
from pathlib import Path

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Manual Comercial de Objeciones - AFP Capital",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- RUTAS DE ARCHIVOS ---
BASE_DIR = Path(__file__).parent
DATA_OBJECIONES_PATH = BASE_DIR / "objeciones_base_streamlit.json"
DATA_PARAMETROS_PATH = BASE_DIR / "parametros_app_manual_objeciones.json"

# --- FUNCIONES DE CARGA Y GUARDADO DE DATOS ---
@st.cache_data
def load_base_objeciones():
    try:
        with open(DATA_OBJECIONES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error al cargar las objeciones base: {e}")
        return []

def load_parametros():
    try:
        with open(DATA_PARAMETROS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error al cargar los parámetros de configuración: {e}")
        return {}

def save_parametros(data):
    try:
        with open(DATA_PARAMETROS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error al guardar los parámetros: {e}")
        return False

# --- INICIALIZACIÓN DE ESTADO ---
if "objeciones" not in st.session_state:
    st.session_state.objeciones = load_base_objeciones()

if "parametros" not in st.session_state:
    st.session_state.parametros = load_parametros()

# Variables para Role Play
if "role_play_obj" not in st.session_state:
    st.session_state.role_play_obj = None
if "role_play_user_answer" not in st.session_state:
    st.session_state.role_play_user_answer = ""
if "role_play_evaluated" not in st.session_state:
    st.session_state.role_play_evaluated = False

# --- DISEÑO Y ESTILOS CSS (AESTHETICS) ---
def apply_custom_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Fuente global */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Configuración de colores primarios */
    :root {
        --primary: #FF8200;
        --secondary: #0F2C59;
        --bg-soft: #F8F9FA;
        --text: #2D3748;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F2C59 !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Tarjetas de Objeción */
    .objection-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .objection-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }
    
    /* Bordes de sensibilidad */
    .border-verde { border-left: 6px solid #137333; }
    .border-amarillo { border-left: 6px solid #FFC107; }
    .border-rojo { border-left: 6px solid #D93025; }
    
    /* Badges de estado */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 6px;
        letter-spacing: 0.5px;
    }
    .badge-verde { background-color: #E6F4EA; color: #137333; }
    .badge-amarillo { background-color: #FEF7E0; color: #B06000; }
    .badge-rojo { background-color: #FCE8E6; color: #C5221F; }
    .badge-secondary { background-color: #E8EAED; color: #3C4043; }
    
    /* Estructuras de Contenido */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0F2C59;
        margin-top: 15px;
        margin-bottom: 5px;
    }
    .content-box {
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 12px 16px;
        border-left: 3px solid #0F2C59;
        font-size: 0.95rem;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .error-box {
        background-color: #FCE8E6;
        border-radius: 8px;
        padding: 12px 16px;
        border-left: 3px solid #C5221F;
        font-size: 0.95rem;
        color: #C5221F;
        margin-bottom: 12px;
    }
    
    /* Títulos principales */
    .app-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #0F2C59;
        margin-bottom: 2px;
    }
    .app-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        color: #FF8200;
        margin-bottom: 25px;
    }
    
    /* Links interactivos */
    .tool-link {
        color: #FF8200;
        text-decoration: none;
        font-weight: 500;
    }
    .tool-link:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# --- FUNCIONES DE ADAPTACIÓN DE TEXTO ---
def generate_whatsapp_message(objection, tone, client_name=""):
    name_str = f" {client_name}" if client_name.strip() else ""
    body = objection.get("whatsapp", "")
    
    if tone == "Cercano":
        greeting = f"¡Hola{name_str}! 😊 Espero que estés muy bien."
    elif tone == "Ejecutivo":
        greeting = f"Estimado/a{name_str}, espero que se encuentre muy bien."
        # Reemplazar términos informales a formales
        replacements = {
            " tu ": " su ",
            " tus ": " sus ",
            " te ": " le ",
            " decidas ": " decida ",
            " decides ": " decida ",
            " tomas ": " tome ",
            " contigo ": " con usted ",
            " eres ": " es "
        }
        for k, v in replacements.items():
            body = body.replace(k, v)
            body = body.replace(k.capitalize(), v.capitalize())
    elif tone == "Directo":
        greeting = f"Hola{name_str}."
    elif tone == "Educativo":
        greeting = f"Hola{name_str}. Te comparto un punto importante para tu planificación previsional:"
        
    return f"{greeting}\n\n{body}"

# --- FUNCIONES DE EXPORTACIÓN ---
def export_objection_markdown(obj):
    md = f"# Objeción: {obj['objecion_cliente']}\n\n"
    md += f"**ID**: {obj['id']} | **Categoría**: {obj['categoria']} | **Dificultad**: {obj['nivel']}\n\n"
    md += f"## Qué hay detrás\n{obj['fondo_real']}\n\n"
    md += f"## Preguntas de Diagnóstico\n"
    for q in obj['preguntas_diagnostico']:
        md += f"- {q}\n"
    md += f"\n## Respuesta Comercial Recomendada\n{obj['respuesta_comercial']}\n\n"
    md += f"## Argumentos de Apoyo\n"
    for arg in obj['argumentos']:
        md += f"- {arg}\n"
    md += f"\n## Herramientas / Evidencia\n"
    for tool in obj['herramientas']:
        md += f"- {tool}\n"
    md += f"\n## Cierre Sugerido\n{obj['cierre']}\n\n"
    md += f"## Versiones por Canal\n"
    md += f"- **WhatsApp**: {obj.get('whatsapp', '')}\n"
    md += f"- **Llamada**: {obj.get('llamada', '')}\n\n"
    md += f"## Errores a Evitar\n"
    for err in obj['errores_evitar']:
        md += f"- {err}\n"
    return md

def export_study_sheet_markdown(obj):
    md = f"# Ficha de Estudio: {obj['objecion_cliente']}\n\n"
    md += f"**ID**: {obj['id']} | **Categoría**: {obj['categoria']} | **Nivel**: {obj['nivel']}\n\n"
    md += f"## 1. Análisis del Comportamiento del Cliente\n"
    md += f"**Fondo Real**: {obj['fondo_real']}\n\n"
    md += f"## 2. Preguntas de Diagnóstico Clínico Comercial\n"
    for q in obj['preguntas_diagnostico']:
        md += f"- {q}\n"
    md += f"\n## 3. Respuesta Sugerida y Argumentación\n"
    md += f"**Respuesta**: {obj['respuesta_comercial']}\n\n"
    md += f"**Argumentos Clave**:\n"
    for arg in obj['argumentos']:
        md += f"- {arg}\n"
    md += f"\n## 4. Guía de Práctica y Role Play\n"
    md += f"- **Contexto de Práctica**: Practica esta objeción con un colega simulando una reunión de {obj.get('producto', ['AFP'])[0]}.\n"
    md += f"- **Pregunta de Autoevaluación**: ¿Lograste empatizar antes de dar la respuesta?\n\n"
    md += f"## 5. Checklist de Dominio Comercial\n"
    md += f"- [ ] Puedo parafrasear la respuesta comercial de forma natural.\n"
    md += f"- [ ] Comprendo la motivación real detrás del cliente.\n"
    md += f"- [ ] Sé cómo guiar la conversación al cierre diagnóstico.\n"
    return md

# --- MENU LATERAL (SIDEBAR) ---
st.sidebar.markdown("<div class='sidebar-brand'>🛡️ AFP Capital<br><small>Manual de Objeciones</small></div>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Inicio",
        "🔍 Buscar Objeción",
        "🤝 Modo Reunión",
        "📖 Modo Estudio",
        "🎭 Role Play",
        "💬 WhatsApp",
        "⚙️ Configuración",
        "🛡️ Buenas Prácticas"
    ]
)

# --- PANEL DE PARÁMETROS DILUIDOS ---
parametros = st.session_state.parametros
comisiones = parametros.get("comisiones", {})
topes_tributarios = parametros.get("topes_tributarios", {})
links_herramientas = parametros.get("links_herramientas", {})
disclaimers = parametros.get("disclaimers", [])

# Mapeador de enlaces a herramientas interactivo
def render_tool_link(tool_name):
    lower_name = tool_name.lower()
    if "comparador" in lower_name and links_herramientas.get("comparador_costos"):
        return f"<a href='{links_herramientas['comparador_costos']}' target='_blank' class='tool-link'>🛠️ {tool_name} (Acceder)</a>"
    elif "simulador apv" in lower_name and links_herramientas.get("simulador_apv"):
        return f"<a href='{links_herramientas['simulador_apv']}' target='_blank' class='tool-link'>🛠️ {tool_name} (Acceder)</a>"
    elif "perfil" in lower_name and links_herramientas.get("perfil_riesgo"):
        return f"<a href='{links_herramientas['perfil_riesgo']}' target='_blank' class='tool-link'>🛠️ {tool_name} (Acceder)</a>"
    elif "crm" in lower_name and links_herramientas.get("crm"):
        return f"<a href='{links_herramientas['crm']}' target='_blank' class='tool-link'>💼 {tool_name} (Registrar)</a>"
    return f"📌 {tool_name}"

# --- MÓDULOS DE APLICACIÓN ---

# 1. MÓDULO INICIO
if menu == "🏠 Inicio":
    st.markdown("<h1 class='app-title'>Manual Comercial de Objeciones AFP Capital</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Convierte dudas en conversaciones y conversaciones en cierres</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Objeciones", len(st.session_state.objeciones))
    with col2:
        verdes = len([o for o in st.session_state.objeciones if o.get("sensibilidad") == "Verde"])
        st.metric("Objeciones Simples (Verde)", verdes)
    with col3:
        amarillos = len([o for o in st.session_state.objeciones if o.get("sensibilidad") == "Amarillo"])
        st.metric("De Diagnóstico (Amarillo)", amarillos)
    with col4:
        rojos = len([o for o in st.session_state.objeciones if o.get("sensibilidad") == "Rojo"])
        st.metric("Sensibles (Rojo)", rojos)
        
    st.markdown("---")
    
    st.markdown("### ¿Cómo utilizar esta herramienta?")
    st.markdown("""
    Esta herramienta está diseñada para acompañarte en tu día a día comercial. Puedes usarla en diversos momentos:
    
    *   **En vivo con el cliente (Modo Reunión):** Obtén respuestas de 30 segundos y preguntas clave en medio de una llamada o reunión.
    *   **Autoestudio (Modo Estudio y Role Play):** Domina los argumentos comerciales, practica tus respuestas y autoevalúate con escenarios interactivos.
    *   **Seguimiento digital (WhatsApp):** Envía textos adaptados y listos con diferentes tonos profesionales.
    *   **Actualización normativa (Configuración):** Ajusta comisiones, topes y links de herramientas para que la app se actualice dinámicamente.
    """)
    
    st.markdown("### Disclaimers y Reglas Generales de Uso")
    for d in disclaimers:
        st.info(d)

# 2. MÓDULO BUSCAR OBJECIÓN
elif menu == "🔍 Buscar Objeción":
    st.markdown("<h1 class='app-title'>Buscador General de Objeciones</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Filtra y encuentra argumentos específicos al instante</p>", unsafe_allow_html=True)
    
    # Buscador por palabra clave
    query = st.text_input("Buscador general", placeholder="Ej: caro, rentabilidad, no tengo tiempo...")
    
    # Filtros
    categorias = list(set([o["categoria"] for o in st.session_state.objeciones]))
    productos = list(set([p for o in st.session_state.objeciones for p in o["producto"]]))
    canales = list(set([c for o in st.session_state.objeciones for c in o["canal"]]))
    niveles = list(set([o["nivel"] for o in st.session_state.objeciones]))
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        f_cat = st.selectbox("Categoría", ["Todas"] + categorias)
    with col2:
        f_prod = st.selectbox("Producto", ["Todos"] + productos)
    with col3:
        f_canal = st.selectbox("Canal de uso", ["Todos"] + canales)
    with col4:
        f_nivel = st.selectbox("Nivel de dificultad", ["Todos"] + niveles)
        
    # Filtrar
    filtered = st.session_state.objeciones
    if query:
        filtered = [
            o for o in filtered
            if query.lower() in o["objecion_cliente"].lower()
            or query.lower() in o["fondo_real"].lower()
            or query.lower() in o["respuesta_comercial"].lower()
        ]
    if f_cat != "Todas":
        filtered = [o for o in filtered if o["categoria"] == f_cat]
    if f_prod != "Todos":
        filtered = [o for o in filtered if f_prod in o["producto"]]
    if f_canal != "Todos":
        filtered = [o for o in filtered if f_canal in o["canal"]]
    if f_nivel != "Todos":
        filtered = [o for o in filtered if o["nivel"] == f_nivel]
        
    st.write(f"Mostrando **{len(filtered)}** objeciones encontradas.")
    
    # Botón para exportar listado completo a CSV
    df = pd.DataFrame(st.session_state.objeciones)
    for col in ['producto', 'canal', 'preguntas_diagnostico', 'argumentos', 'herramientas', 'errores_evitar']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    csv_data = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Exportar Todo el Manual a CSV",
        data=csv_data,
        file_name="manual_objeciones_completo.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # Vista de Tarjetas
    for obj in filtered:
        sens = obj.get("sensibilidad", "Verde")
        border_class = f"border-{sens.lower()}"
        badge_class = f"badge-{sens.lower()}"
        
        # Estructura de tarjeta en HTML
        st.markdown(f"""
        <div class='objection-card {border_class}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <strong style='font-size:1.15rem; color:#0F2C59;'>{obj['objecion_cliente']}</strong>
                <div>
                    <span class='badge {badge_class}'>Sensibilidad: {sens}</span>
                    <span class='badge badge-secondary'>{obj['nivel']}</span>
                </div>
            </div>
            <div style='margin-top:10px;'>
                <small style='color:#718096;'>ID: {obj['id']} | Categoría: {obj['categoria']} | Productos: {", ".join(obj['producto'])}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Expander para ver los detalles
        with st.expander("Ver Plan de Acción Comercial Completo", expanded=False):
            st.markdown("<div class='section-title'>🔍 ¿Qué hay detrás? (Fondo Real)</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='content-box'>{obj['fondo_real']}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='section-title'>💬 Preguntas de Diagnóstico Recomendadas</div>", unsafe_allow_html=True)
            for q in obj["preguntas_diagnostico"]:
                st.markdown(f"- {q}")
                
            st.markdown("<div class='section-title'>🎯 Respuesta Comercial Recomendada</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='content-box'>{obj['respuesta_comercial']}</div>", unsafe_allow_html=True)
            st.code(obj['respuesta_comercial'], language="text")
            
            st.markdown("<div class='section-title'>💡 Argumentos de Apoyo</div>", unsafe_allow_html=True)
            for arg in obj["argumentos"]:
                st.markdown(f"- {arg}")
                
            st.markdown("<div class='section-title'>🛠️ Herramientas / Evidencia Sugerida</div>", unsafe_allow_html=True)
            for tool in obj["herramientas"]:
                link_html = render_tool_link(tool)
                st.markdown(f"- {link_html}", unsafe_allow_html=True)
                
            st.markdown("<div class='section-title'>🏁 Cierre Sugerido</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='content-box'>{obj['cierre']}</div>", unsafe_allow_html=True)
            st.code(obj['cierre'], language="text")
            
            st.markdown("<div class='section-title'>⚠️ Errores Frecuentes a Evitar</div>", unsafe_allow_html=True)
            for err in obj["errores_evitar"]:
                st.markdown(f"<div class='error-box'>✘ {err}</div>", unsafe_allow_html=True)
                
            # Exportaciones individuales
            obj_md = export_objection_markdown(obj)
            study_md = export_study_sheet_markdown(obj)
            
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                st.download_button(
                    label="📄 Descargar Ficha en Markdown",
                    data=obj_md,
                    file_name=f"ficha_{obj['id']}.md",
                    mime="text/markdown",
                    key=f"dl_md_{obj['id']}"
                )
            with col_exp2:
                st.download_button(
                    label="📖 Descargar Ficha de Estudio",
                    data=study_md,
                    file_name=f"estudio_{obj['id']}.md",
                    mime="text/markdown",
                    key=f"dl_std_{obj['id']}"
                )

# 3. MÓDULO MODO REUNIÓN
elif menu == "🤝 Modo Reunión":
    st.markdown("<h1 class='app-title'>Modo Reunión (En Vivo con Cliente)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Esquema de acción ultrarrápido y de alto impacto para uso durante la llamada o reunión</p>", unsafe_allow_html=True)
    
    # Selector de objeción rápido
    obj_options = {o["objecion_cliente"]: o for o in st.session_state.objeciones}
    selected_text = st.selectbox("Selecciona la objeción del cliente", list(obj_options.keys()))
    
    if selected_text:
        obj = obj_options[selected_text]
        sens = obj.get("sensibilidad", "Verde")
        badge_class = f"badge-{sens.lower()}"
        
        st.markdown(f"""
        <div style='background-color:#0F2C59; color:#FFFFFF; padding:20px; border-radius:10px; margin-bottom:20px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:1.3rem; font-weight:600;'>{obj['objecion_cliente']}</span>
                <span class='badge {badge_class}' style='color:#FFFFFF; border:1px solid #FFFFFF;'>Sensibilidad: {sens}</span>
            </div>
            <p style='margin-top:10px; font-size:0.95rem; opacity:0.85;'>detrás de la duda: {obj['fondo_real']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❓ 3 Preguntas Clave de Diagnóstico")
            for i, q in enumerate(obj["preguntas_diagnostico"][:3]):
                st.markdown(f"""
                <div style='background-color:#FFFFFF; border-left:4px solid #FF8200; padding:12px; margin-bottom:10px; border-radius:4px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>
                    <strong>{i+1}.</strong> {q}
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("### 🏁 Cierre Recomendado")
            st.markdown(f"<div class='content-box' style='border-left-color:#FF8200;'>{obj['cierre']}</div>", unsafe_allow_html=True)
            st.code(obj['cierre'], language="text")
            
        with col2:
            st.markdown("### ⏱️ Respuesta en 30 Segundos")
            st.markdown(f"""
            <div style='background-color:#FFF7EF; border-left:4px solid #0F2C59; padding:15px; border-radius:6px; font-size:1.05rem; line-height:1.6; color:#0F2C59;'>
                "{obj['respuesta_comercial']}"
            </div>
            """, unsafe_allow_html=True)
            st.code(obj['respuesta_comercial'], language="text")
            
            # Recordatorio de cumplimiento dinámico
            st.warning("⚠️ Recuerda registrar la objeción e intenciones en el CRM corporativo una vez finalizada la interacción.")

# 4. MÓDULO MODO ESTUDIO
elif menu == "📖 Modo Estudio":
    st.markdown("<h1 class='app-title'>Modo Estudio Individual</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Profundiza en la argumentación técnica y metodologías comerciales</p>", unsafe_allow_html=True)
    
    obj_options = {o["objecion_cliente"]: o for o in st.session_state.objeciones}
    selected_text = st.selectbox("Elige la objeción a estudiar", list(obj_options.keys()))
    
    if selected_text:
        obj = obj_options[selected_text]
        
        st.markdown(f"## {obj['objecion_cliente']}")
        
        # Tabs de estudio
        tab1, tab2, tab3 = st.tabs(["📚 Fundamentación y Respuesta", "🎭 Guía de Role Play", "✅ Autoevaluación"])
        
        with tab1:
            st.markdown("### ¿Cuál es la motivación real del cliente?")
            st.info(obj["fondo_real"])
            
            st.markdown("### Estructura de la Respuesta Recomendada")
            st.write(obj["respuesta_comercial"])
            
            st.markdown("### Argumentos Técnicos a Considerar")
            for arg in obj["argumentos"]:
                st.markdown(f"- {arg}")
                
            st.markdown("### Herramientas y Simuladores de Apoyo")
            for tool in obj["herramientas"]:
                link_html = render_tool_link(tool)
                st.markdown(f"- {link_html}", unsafe_allow_html=True)
                
        with tab2:
            st.markdown("### Guión del Juego de Roles")
            st.markdown(f"""
            *   **Contexto del cliente:** Un prospecto en etapa de evaluación de su {", ".join(obj['producto'])}. Nivel de dificultad: **{obj['nivel']}**.
            *   **Rol Ejecutivo:** Debe usar el **Método R.E.A.C.C.I.O.N.**:
                1.  **Recibir y Empatizar:** Validar la preocupación del cliente (ej. por costos o rentabilidad) sin debatir.
                2.  **Diagnosticar:** Hacer al menos 2 preguntas para indagar sobre las experiencias y objetivos del cliente.
                3.  **Contestar y Evidenciar:** Entregar el argumento comercial y referenciar las herramientas correspondientes.
                4.  **Cierre:** Proponer el siguiente paso (ej. simulación o próxima cita).
            """)
            
            st.markdown("### Preguntas de práctica individual")
            st.write("Ensaya responder estas preguntas de diagnóstico en voz alta:")
            for q in obj["preguntas_diagnostico"]:
                st.markdown(f"*   *\"{q}\"*")
                
        with tab3:
            st.markdown("### Checklist de Dominio Comercial")
            st.write("Marca los elementos a medida que los domines en tus llamadas de prueba:")
            
            # Usar claves únicas basadas en la objeción
            st.checkbox("Comprendo el motivo real y temores detrás de la objeción.", key=f"chk_fnd_{obj['id']}")
            st.checkbox("Soy capaz de realizar al menos 2 preguntas de diagnóstico de forma fluida.", key=f"chk_diag_{obj['id']}")
            st.checkbox("Sé estructurar la respuesta sin titubear y con tono consultivo.", key=f"chk_resp_{obj['id']}")
            st.checkbox("Identifico qué simuladores/herramientas debo invocar.", key=f"chk_tool_{obj['id']}")
            st.checkbox("Logro proponer un cierre de bajo compromiso y orientar el paso al CRM.", key=f"chk_crm_{obj['id']}")
            
            # Descargar ficha de estudio
            study_md = export_study_sheet_markdown(obj)
            st.download_button(
                label="📥 Descargar esta Guía de Estudio (Markdown)",
                data=study_md,
                file_name=f"ficha_estudio_{obj['id']}.md",
                mime="text/markdown"
            )

# 5. MÓDULO ROLE PLAY
elif menu == "🎭 Role Play":
    st.markdown("<h1 class='app-title'>Simulador de Role Play</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Pon a prueba tus habilidades comerciales ante objeciones aleatorias</p>", unsafe_allow_html=True)
    
    # Botón para nueva objeción aleatoria
    if st.button("🔄 Generar Nueva Objeción Aleatoria") or st.session_state.role_play_obj is None:
        st.session_state.role_play_obj = random.choice(st.session_state.objeciones)
        st.session_state.role_play_user_answer = ""
        st.session_state.role_play_evaluated = False
        st.rerun()
        
    obj = st.session_state.role_play_obj
    
    if obj:
        sens = obj.get("sensibilidad", "Verde")
        badge_class = f"badge-{sens.lower()}"
        
        # Tarjeta de simulación
        st.markdown(f"""
        <div style='background-color:#F8F9FA; padding:25px; border-radius:10px; border-left:6px solid #FF8200; margin-bottom:20px; box-shadow:0 3px 10px rgba(0,0,0,0.05);'>
            <h3>🎭 Escenario de Simulación</h3>
            <p style='font-size:1.25rem; color:#0F2C59; font-weight:600; margin-top:15px;'>El cliente dice: "{obj['objecion_cliente']}"</p>
            <div style='margin-top:15px;'>
                <span class='badge {badge_class}'>Sensibilidad: {sens}</span>
                <span class='badge badge-secondary'>Dificultad: {obj['nivel']}</span>
                <span class='badge badge-secondary'>Productos: {", ".join(obj['producto'])}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Entrada de usuario
        st.session_state.role_play_user_answer = st.text_area(
            "Escribe tu respuesta comercial aquí:",
            value=st.session_state.role_play_user_answer,
            placeholder="Introduce cómo reaccionarías ante la objeción..."
        )
        
        if st.button("🚀 Evaluar Respuesta"):
            if not st.session_state.role_play_user_answer.strip():
                st.warning("Por favor, escribe una respuesta antes de evaluar.")
            else:
                st.session_state.role_play_evaluated = True
                
        if st.session_state.role_play_evaluated:
            st.markdown("---")
            st.markdown("### 🎯 Respuesta Sugerida AFP Capital")
            st.markdown(f"<div class='content-box'>{obj['respuesta_comercial']}</div>", unsafe_allow_html=True)
            
            st.markdown("### 🏁 Cierre Sugerido")
            st.write(obj["cierre"])
            
            st.markdown("### ✅ Checklist de Autoevaluación")
            st.write("Revisa tu respuesta escrita y califica sinceramente si cumpliste los siguientes puntos:")
            
            c1 = st.checkbox("¿Escuché y validé la objeción con empatía? (Sin ponerse a la defensiva)", key="eval_1")
            c2 = st.checkbox("¿Hice preguntas de diagnóstico antes de entregar la respuesta?", key="eval_2")
            c3 = st.checkbox("¿Conecté mi argumento con el objetivo real del cliente?", key="eval_3")
            c4 = st.checkbox("¿Hice referencia a alguna evidencia o herramienta interna (simuladores, comparadores)?", key="eval_4")
            c5 = st.checkbox("¿Cerré proponiendo un siguiente paso concreto (diagnóstico, cotización, etc.)?", key="eval_5")
            c6 = st.checkbox("¿Evité prometer rentabilidades futuras de manera absoluta (cumplimiento)?", key="eval_6")
            
            score = sum([c1, c2, c3, c4, c5, c6])
            
            if score == 6:
                st.success("🏆 ¡Excelente! Cumpliste con todo el protocolo del Método R.E.A.C.C.I.O.N. y normativas.")
            elif score >= 4:
                st.info(f"👍 Buen trabajo. Lograste un puntaje de {score}/6. Pon atención a las áreas que faltaron marcar.")
            else:
                st.warning(f"⚠️ Rendimiento en desarrollo ({score}/6). Repasa la ficha en el Modo Estudio e inténtalo de nuevo.")

# 6. MÓDULO WHATSAPP
elif menu == "💬 WhatsApp":
    st.markdown("<h1 class='app-title'>Generador de Mensajes para WhatsApp</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Adapta la respuesta a un formato digital rápido y copia al portapapeles</p>", unsafe_allow_html=True)
    
    obj_options = {o["objecion_cliente"]: o for o in st.session_state.objeciones}
    selected_text = st.selectbox("Selecciona la objeción", list(obj_options.keys()))
    
    if selected_text:
        obj = obj_options[selected_text]
        
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Nombre del cliente (Opcional)", placeholder="Ej: Marcela")
            tone = st.selectbox(
                "Selecciona el tono del mensaje",
                ["Cercano", "Ejecutivo", "Directo", "Educativo"]
            )
            
            st.markdown("""
            **Guía de tonos:**
            *   **Cercano:** Conversacional, usa emojis y tuteo amable.
            *   **Ejecutivo:** Formal, ideal para clientes corporativos de alto patrimonio.
            *   **Directo:** Conciso, directo al grano para clientes muy ocupados.
            *   **Educativo:** Enfocado en la asesoría, el análisis y la toma de decisiones informadas.
            """)
            
        with col2:
            st.markdown("### 📱 Mensaje Generado")
            msg = generate_whatsapp_message(obj, tone, client_name)
            
            st.markdown("""
            <div style='background-color:#DCF8C6; color:#303030; padding:15px; border-radius:8px; font-family:sans-serif; white-space: pre-wrap; font-size:0.95rem; box-shadow:0 2px 5px rgba(0,0,0,0.05); margin-bottom:15px;'>
            """ + msg.replace("\n", "<br>") + """
            </div>
            """, unsafe_allow_html=True)
            
            st.code(msg, language="text")

# 7. MÓDULO CONFIGURACIÓN
elif menu == "⚙️ Configuración":
    st.markdown("<h1 class='app-title'>Parámetros y Configuración Comercial</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Modifica los datos normativos, comisiones y enlaces internos. Estos cambios se guardarán de forma persistente.</p>", unsafe_allow_html=True)
    
    # Formulario de edición de parámetros
    with st.form("config_form"):
        st.markdown("### 💼 Comisiones AFP Capital")
        c_obligatoria = st.text_input("Comisión Cuenta Obligatoria", value=comisiones.get("cuenta_obligatoria", ""))
        c_apv = st.text_input("Comisión APV", value=comisiones.get("apv", ""))
        c_cuenta2 = st.text_input("Comisión Cuenta 2", value=comisiones.get("cuenta_2", ""))
        c_deposito = st.text_input("Comisión Depósito Convenido", value=comisiones.get("deposito_convenido", ""))
        
        st.markdown("### 📈 Topes Tributarios Vigentes")
        t_reg_a = st.text_input("Tope APV Régimen A", value=topes_tributarios.get("apv_regimen_a", ""))
        t_reg_b = st.text_input("Tope APV Régimen B", value=topes_tributarios.get("apv_regimen_b", ""))
        t_cuenta2 = st.text_input("Tope Cuenta 2", value=topes_tributarios.get("cuenta_2", ""))
        
        st.markdown("### 🔗 Enlaces a Herramientas Internas")
        link_apv = st.text_input("Link a Simulador APV", value=links_herramientas.get("simulador_apv", ""))
        link_costos = st.text_input("Link a Comparador de Costos", value=links_herramientas.get("comparador_costos", ""))
        link_rent = st.text_input("Link a Rentabilidad de Multifondos", value=links_herramientas.get("rentabilidad_multifondos", ""))
        link_perfil = st.text_input("Link a Test de Perfil de Riesgo", value=links_herramientas.get("perfil_riesgo", ""))
        link_crm = st.text_input("Link a Registro CRM", value=links_herramientas.get("crm", ""))
        
        st.markdown("### 🛡️ Disclaimers y Notas de Cumplimiento")
        disc_text = st.text_area(
            "Disclaimers (Uno por línea)",
            value="\n".join(disclaimers),
            help="Ingresa cada advertencia en una línea diferente."
        )
        
        submitted = st.form_submit_button("💾 Guardar Configuración")
        
        if submitted:
            # Reestructurar los datos editados
            nuevos_parametros = {
                "empresa": parametros.get("empresa", "AFP Capital"),
                "version": parametros.get("version", "MVP-1"),
                "fecha_actualizacion": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "comisiones": {
                    "cuenta_obligatoria": c_obligatoria,
                    "apv": c_apv,
                    "cuenta_2": c_cuenta2,
                    "deposito_convenido": c_deposito
                },
                "topes_tributarios": {
                    "apv_regimen_a": t_reg_a,
                    "apv_regimen_b": t_reg_b,
                    "cuenta_2": t_cuenta2
                },
                "links_herramientas": {
                    "simulador_apv": link_apv,
                    "comparador_costos": link_costos,
                    "rentabilidad_multifondos": link_rent,
                    "perfil_riesgo": link_perfil,
                    "crm": link_crm
                },
                "disclaimers": [d.strip() for d in disc_text.split("\n") if d.strip()]
            }
            
            # Guardar y actualizar sesión
            if save_parametros(nuevos_parametros):
                st.session_state.parametros = nuevos_parametros
                st.success("✅ ¡Configuración guardada correctamente de manera persistente!")
                st.rerun()

# 8. MÓDULO BUENAS PRÁCTICAS Y CUMPLIMIENTO
elif menu == "🛡️ Buenas Prácticas":
    st.markdown("<h1 class='app-title'>Buenas Prácticas y Cumplimiento Normativo</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Directrices obligatorias de la Superintendencia de Pensiones y políticas internas de AFP Capital</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color:#FEEFC3; border-left:6px solid #F2994A; padding:20px; border-radius:8px; margin-bottom:25px;'>
        <h4 style='color:#B06000; margin:0 0 10px 0;'>⚠️ Regla de Cumplimiento Crítica</h4>
        <p style='color:#B06000; margin:0; line-height:1.5;'>
            La venta previsional y la asesoría de inversiones están estrictamente reguladas en Chile. El uso de datos erróneos o promesas infundadas puede acarrear severas multas institucionales y la desvinculación o sanción del ejecutivo comercial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚫 Prohibiciones Absolutas")
        st.markdown("""
        *   **No asegurar rentabilidades futuras:** Toda rentabilidad previsional es por definición variable. Utiliza siempre la frase: *"La rentabilidad pasada no garantiza la rentabilidad futura"*.
        *   **No desacreditar a la competencia:** No utilices descalificaciones contra otras administradoras de fondos. En su lugar, resalta el valor de nuestro servicio de asesoría y planificación.
        *   **No ofrecer incentivos indebidos:** Está estrictamente prohibido ofrecer pagos, regalos o compensaciones económicas para concretar un traspaso.
        *   **No usar datos desactualizados:** Siempre corrobora comisiones y topes tributarios antes de asesorar formalmente a un cliente.
        """)
        
    with col2:
        st.markdown("### ✅ Buenas Prácticas de Asesoría")
        st.markdown("""
        *   **Diagnóstico Primero:** Nunca entregues una recomendación sin antes realizar preguntas sobre el perfil de riesgo, la edad y el horizonte de inversión.
        *   **Registro CRM Obligatorio:** Registra sistemáticamente en el CRM la objeción principal del cliente y el acuerdo alcanzado para mantener la trazabilidad de la relación.
        *   **Transparencia de Costos:** Explica la estructura de comisiones con claridad. Los clientes aprecian la honestidad respecto a lo que pagan y el valor que reciben a cambio.
        *   **Uso de Herramientas Oficiales:** Apóyate en los simuladores internos aprobados para proyectar pensiones y calcular los beneficios tributarios (APV Régimen A y B).
        """)
        
    st.markdown("---")
    st.markdown("### Resumen Normativo de Comisiones y Topes Vigentes")
    
    # Mostrar tabla estructurada con las variables diluidas de configuración
    data_resumen = {
        "Variable": [
            "Comisión Cuenta Obligatoria",
            "Comisión APV",
            "Comisión Cuenta 2",
            "Tope APV Régimen A",
            "Tope APV Régimen B",
            "Tope Cuenta 2"
        ],
        "Valor Vigente (Configurado)": [
            comisiones.get("cuenta_obligatoria", "No configurado"),
            comisiones.get("apv", "No configurado"),
            comisiones.get("cuenta_2", "No configurado"),
            topes_tributarios.get("apv_regimen_a", "No configurado"),
            topes_tributarios.get("apv_regimen_b", "No configurado"),
            topes_tributarios.get("cuenta_2", "No configurado")
        ]
    }
    st.table(pd.DataFrame(data_resumen))
