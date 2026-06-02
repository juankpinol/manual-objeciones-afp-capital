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

# --- DISEÑO Y ESTILOS CSS ---
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
    .accent-box {
        background-color: #FFF7EF;
        border-radius: 8px;
        padding: 15px 20px;
        border-left: 4px solid #FF8200;
        font-size: 1.05rem;
        color: #0F2C59;
        line-height: 1.6;
        margin-bottom: 15px;
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
    
    /* Burbujas de Chat / Role Play */
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        max-width: 80%;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    .chat-client {
        background-color: #F1F3F4;
        color: #2D3748;
        border-bottom-left-radius: 2px;
        align-self: flex-start;
    }
    .chat-executive {
        background-color: #FFF7EF;
        color: #0F2C59;
        border-bottom-right-radius: 2px;
        border-left: 4px solid #FF8200;
        align-self: flex-end;
        margin-left: auto;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        background-color: #FFFFFF;
        border: 1px solid #E8EAED;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
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
    md += f"## Concepto Técnico de Fondo\n{obj.get('concepto_tecnico', 'No especificado.')}\n\n"
    md += f"## Explicación Simple para el Cliente\n{obj.get('explicacion_simple', 'No especificada.')}\n\n"
    md += f"## Preguntas de Diagnóstico\n"
    for q in obj['preguntas_diagnostico']:
        md += f"- {q}\n"
    md += f"\n## Argumento Comercial Recomendado\n{obj['respuesta_comercial']}\n\n"
    md += f"## Ejemplo Práctico Aplicado\n{obj.get('ejemplo_practico', 'No especificado.')}\n\n"
    md += f"## Cierre Sugerido\n{obj['cierre']}\n\n"
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
    md += f"## 1. Análisis Psicológico y Comercial\n"
    md += f"**Fondo Real**: {obj['fondo_real']}\n\n"
    md += f"## 2. Concepto Técnico de Fondo\n"
    md += f"{obj.get('concepto_tecnico', 'No especificado.')}\n\n"
    md += f"## 3. Explicación Simple (Sin Tecnicismos)\n"
    md += f"{obj.get('explicacion_simple', 'No especificada.')}\n\n"
    md += f"## 4. Preguntas de Diagnóstico Clínico Comercial\n"
    for q in obj['preguntas_diagnostico']:
        md += f"- {q}\n"
    md += f"\n## 5. Argumentación Comercial y Respuestas\n"
    md += f"**Respuesta Comercial**: {obj['respuesta_comercial']}\n\n"
    md += f"**Ejemplo Práctico**: {obj.get('ejemplo_practico', 'No especificado.')}\n\n"
    md += f"## 6. Guía de Role Play Sugerida\n"
    rp = obj.get("role_play", {})
    md += f"- **Cliente plantea**: \"{rp.get('cliente_plantea', '')}\"\n"
    md += f"- **Ejecutivo responde**: \"{rp.get('ejecutivo_responde', '')}\"\n"
    md += f"- **Cliente repregunta**: \"{rp.get('cliente_repregunta', '')}\"\n"
    md += f"- **Ejecutivo profundiza y cierra**: \"{rp.get('ejecutivo_profundiza_cierra', '')}\"\n\n"
    md += f"## 7. Checklist de Dominio Técnico y Comercial\n"
    md += f"- [ ] Comprendo el concepto técnico de fondo de esta objeción.\n"
    md += f"- [ ] Puedo explicar este concepto en lenguaje simple y sin usar marcas externas.\n"
    md += f"- [ ] Sé guiar al cliente mediante al menos dos preguntas de diagnóstico.\n"
    md += f"- [ ] Puedo replicar la secuencia de cierre sin prometer rentabilidad.\n"
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
    
    *   **En vivo con el cliente (Modo Reunión / Pestaña Respuesta Rápida):** Obtén respuestas de 30 segundos y preguntas clave en medio de una llamada o reunión.
    *   **Autoestudio (Modo Estudio y Role Play):** Domina los argumentos comerciales, comprende el fundamento técnico de las objeciones y autoevalúate.
    *   **Seguimiento digital (WhatsApp):** Genera y copia mensajes adaptados según el perfil y tono del cliente.
    *   **Actualización normativa (Configuración):** Ajusta comisiones, topes y links de herramientas para que la app se mantenga al día de forma permanente.
    """)
    
    st.markdown("### Disclaimers y Reglas Generales de Uso")
    for d in disclaimers:
        st.info(d)

# 2. MÓDULO BUSCAR OBJECIÓN (CON LAS 7 PESTAÑAS)
elif menu == "🔍 Buscar Objeción":
    st.markdown("<h1 class='app-title'>Buscador General de Objeciones</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Busca por palabra clave o filtra por categorías para acceder a las fichas estructuradas</p>", unsafe_allow_html=True)
    
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
            or query.lower() in o.get("concepto_tecnico", "").lower()
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
    
    # Vista de Tarjetas con las 7 pestañas integradas
    for obj in filtered:
        sens = obj.get("sensibilidad", "Verde")
        border_class = f"border-{sens.lower()}"
        badge_class = f"badge-{sens.lower()}"
        
        # Tarjeta contenedor de cabecera
        st.markdown(f"""
        <div class='objection-card {border_class}' style='margin-bottom: 5px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <strong style='font-size:1.2rem; color:#0F2C59;'>{obj['objecion_cliente']}</strong>
                <div>
                    <span class='badge {badge_class}'>Sensibilidad: {sens}</span>
                    <span class='badge badge-secondary'>{obj['nivel']}</span>
                </div>
            </div>
            <div style='margin-top:8px;'>
                <small style='color:#718096;'>ID: {obj['id']} | Categoría: {obj['categoria']} | Productos: {", ".join(obj['producto'])}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Renderizado de pestañas de contenido dentro de un st.container para organizar la UI
        with st.container():
            t1, t2, t3, t4, t5, t6, t7 = st.tabs([
                "⚡ Respuesta Rápida",
                "📚 Fundamento Educativo",
                "❓ Diagnóstico",
                "💡 Ejemplo Práctico",
                "🎭 Role Play",
                "💬 WhatsApp",
                "⚠️ Errores a Evitar"
            ])
            
            # 1. Pestaña: Respuesta Rápida
            with t1:
                mr = obj.get("modo_reunion", {})
                st.markdown("### ❓ Pregunta Inicial de Calificación")
                p_reunion = mr.get("preguntas_clave", obj["preguntas_diagnostico"])[0]
                st.markdown(f"<div class='content-box' style='border-left-color:#FF8200;'><strong>Pregunta:</strong> \"{p_reunion}\"</div>", unsafe_allow_html=True)
                
                st.markdown("### 🎯 Respuesta de 30 Segundos")
                resp_reunion = mr.get("respuesta_30s", obj["respuesta_comercial"])
                st.markdown(f"<div class='accent-box'>\"{resp_reunion}\"</div>", unsafe_allow_html=True)
                st.code(resp_reunion, language="text")
                
                st.markdown("### 🏁 Cierre Recomendado")
                cierre_reunion = mr.get("cierre_recomendado", obj["cierre"])
                st.markdown(f"<div class='content-box'>\"{cierre_reunion}\"</div>", unsafe_allow_html=True)
                st.code(cierre_reunion, language="text")
                
            # 2. Pestaña: Fundamento Educativo
            with t2:
                st.markdown("### 🔬 Concepto Técnico de Fondo")
                st.markdown(f"<div class='content-box' style='background-color:#F0F4F8;'>{obj.get('concepto_tecnico', 'No especificado.')}</div>", unsafe_allow_html=True)
                
                st.markdown("### 📢 Explicación Simple para el Cliente")
                st.markdown(f"<div class='content-box'>{obj.get('explicacion_simple', 'No especificada.')}</div>", unsafe_allow_html=True)
                
                st.markdown("### 📖 Guía Formativa de Autoestudio")
                st.write(obj.get("modo_estudio", "No especificado."))
                
                # Botón de descarga de ficha
                study_md = export_study_sheet_markdown(obj)
                st.download_button(
                    label="📥 Descargar Ficha de Estudio en Markdown",
                    data=study_md,
                    file_name=f"estudio_{obj['id']}.md",
                    mime="text/markdown",
                    key=f"dl_std_btn_{obj['id']}"
                )
                
            # 3. Pestaña: Preguntas de Diagnóstico
            with t3:
                st.markdown("### 💬 Preguntas para Explorar la Objeción")
                st.write("Usa estas preguntas en tu reunión para indagar y evitar entrar en debates técnicos de entrada:")
                for q in obj["preguntas_diagnostico"]:
                    st.markdown(f"*   *\"{q}\"*")
                
                st.markdown("### 💡 Argumentos Clave Relacionados")
                for arg in obj["argumentos"]:
                    st.markdown(f"- {arg}")
                    
                st.markdown("### 🛠️ Herramientas Sugeridas para Respaldar")
                for tool in obj["herramientas"]:
                    link_html = render_tool_link(tool)
                    st.markdown(f"- {link_html}", unsafe_allow_html=True)
                    
            # 4. Pestaña: Ejemplo Práctico
            with t4:
                st.markdown("### 💡 Caso Aplicado de Demostración")
                st.write("Aterriza este concepto al cliente usando este escenario práctico simplificado:")
                st.markdown(f"<div class='content-box'>{obj.get('ejemplo_practico', 'No especificado.')}</div>", unsafe_allow_html=True)
                
            # 5. Pestaña: Role Play
            with t5:
                st.markdown("### 🎭 Flujo de Diálogo de Simulación")
                st.write("Estructura de conversación recomendada ante este escenario:")
                rp = obj.get("role_play", {})
                
                st.markdown(f"""
                <div class='chat-container'>
                    <div class='chat-bubble chat-client'>
                        <strong>Cliente plantea:</strong><br>"{rp.get('cliente_plantea', 'No especificado.')}"
                    </div>
                    <div class='chat-bubble chat-executive'>
                        <strong>Ejecutivo responde:</strong><br>"{rp.get('ejecutivo_responde', 'No especificado.')}"
                    </div>
                    <div class='chat-bubble chat-client'>
                        <strong>Cliente repregunta:</strong><br>"{rp.get('cliente_repregunta', 'No especificado.')}"
                    </div>
                    <div class='chat-bubble chat-executive'>
                        <strong>Ejecutivo profundiza y cierra:</strong><br>"{rp.get('ejecutivo_profundiza_cierra', 'No especificado.')}"
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # 6. Pestaña: WhatsApp
            with t6:
                st.markdown("### 💬 Generador de WhatsApp Personalizado")
                c_name = st.text_input("Nombre del cliente", placeholder="Ej: Carolina", key=f"wa_name_{obj['id']}")
                c_tone = st.selectbox("Selecciona el tono", ["Cercano", "Ejecutivo", "Directo", "Educativo"], key=f"wa_tone_{obj['id']}")
                
                wa_msg = generate_whatsapp_message(obj, c_tone, c_name)
                st.markdown("**Mensaje resultante (Copiar):**")
                st.code(wa_msg, language="text")
                
            # 7. Pestaña: Errores a Evitar
            with t7:
                st.markdown("### 🚫 Alertas y Errores Frecuentes")
                st.write("Evita decir o hacer lo siguiente frente a esta objeción:")
                for err in obj["errores_evitar"]:
                    st.markdown(f"<div class='error-box'>✘ {err}</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin-top:10px; margin-bottom:30px; border-color:#E8EAED;'>", unsafe_allow_html=True)

# 3. MÓDULO MODO REUNIÓN (ALINEADO A LA NUEVA ESTRUCTURA)
elif menu == "🤝 Modo Reunión":
    st.markdown("<h1 class='app-title'>Modo Reunión (Uso Rápido con Cliente)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Esquema de acción express y de alto impacto para uso durante la llamada o videoconferencia</p>", unsafe_allow_html=True)
    
    # Selector de objeción rápido
    obj_options = {o["objecion_cliente"]: o for o in st.session_state.objeciones}
    selected_text = st.selectbox("Selecciona la objeción del cliente", list(obj_options.keys()))
    
    if selected_text:
        obj = obj_options[selected_text]
        sens = obj.get("sensibilidad", "Verde")
        badge_class = f"badge-{sens.lower()}"
        mr = obj.get("modo_reunion", {})
        
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
            st.markdown("### ❓ Preguntas Clave de Diagnóstico")
            p_clave = mr.get("preguntas_clave", obj["preguntas_diagnostico"])
            for i, q in enumerate(p_clave[:3]):
                st.markdown(f"""
                <div style='background-color:#FFFFFF; border-left:4px solid #FF8200; padding:12px; margin-bottom:10px; border-radius:4px; box-shadow:0 2px 5px rgba(0,0,0,0.05);'>
                    <strong>{i+1}.</strong> {q}
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("### 🏁 Cierre Recomendado")
            cierre_rec = mr.get("cierre_recomendado", obj["cierre"])
            st.markdown(f"<div class='content-box' style='border-left-color:#FF8200;'>{cierre_rec}</div>", unsafe_allow_html=True)
            st.code(cierre_rec, language="text")
            
        with col2:
            st.markdown("### ⏱️ Respuesta Comercial en 30 Segundos")
            resp_30 = mr.get("respuesta_30s", obj["respuesta_comercial"])
            st.markdown(f"""
            <div style='background-color:#FFF7EF; border-left:4px solid #0F2C59; padding:15px; border-radius:6px; font-size:1.05rem; line-height:1.6; color:#0F2C59;'>
                "{resp_30}"
            </div>
            """, unsafe_allow_html=True)
            st.code(resp_30, language="text")
            
            st.warning("⚠️ Recuerda registrar la objeción en el CRM una vez finalizada la interacción.")

# 4. MÓDULO MODO ESTUDIO
elif menu == "📖 Modo Estudio":
    st.markdown("<h1 class='app-title'>Modo Estudio Individual</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Aprende la profundidad conceptual detrás de cada objeción para enriquecer tu dominio comercial</p>", unsafe_allow_html=True)
    
    obj_options = {o["objecion_cliente"]: o for o in st.session_state.objeciones}
    selected_text = st.selectbox("Elige la objeción a estudiar", list(obj_options.keys()))
    
    if selected_text:
        obj = obj_options[selected_text]
        
        st.markdown(f"## {obj['objecion_cliente']}")
        
        # Tabs de estudio
        tab1, tab2, tab3 = st.tabs(["📚 Fundamentación y Conceptos", "🎭 Guía de Role Play", "✅ Autoevaluación"])
        
        with tab1:
            st.markdown("### ¿Qué hay detrás de la objeción?")
            st.info(obj["fondo_real"])
            
            st.markdown("### 🔬 Concepto Técnico de Fondo")
            st.markdown(f"<div class='content-box' style='background-color:#F0F4F8; border-left-color:#FF8200;'>{obj.get('concepto_tecnico', 'No especificado.')}</div>", unsafe_allow_html=True)
            
            st.markdown("### 📢 Explicación Simple para el Cliente")
            st.markdown(f"<div class='content-box'>{obj.get('explicacion_simple', 'No especificada.')}</div>", unsafe_allow_html=True)
            
            st.markdown("### 📖 Guía Formativa")
            st.write(obj.get("modo_estudio", "No especificado."))
            
            st.markdown("### Argumentos Técnicos Clave")
            for arg in obj["argumentos"]:
                st.markdown(f"- {arg}")
                
            st.markdown("### Herramientas y Simuladores de Apoyo")
            for tool in obj["herramientas"]:
                link_html = render_tool_link(tool)
                st.markdown(f"- {link_html}", unsafe_allow_html=True)
                
        with tab2:
            st.markdown("### Guión del Juego de Roles")
            st.write("Estructura de conversación recomendada:")
            rp = obj.get("role_play", {})
            st.markdown(f"""
            <div class='chat-container'>
                <div class='chat-bubble chat-client'>
                    <strong>Cliente plantea:</strong><br>"{rp.get('cliente_plantea', 'No especificado.')}"
                </div>
                <div class='chat-bubble chat-executive'>
                    <strong>Ejecutivo responde:</strong><br>"{rp.get('ejecutivo_responde', 'No especificado.')}"
                </div>
                <div class='chat-bubble chat-client'>
                    <strong>Cliente repregunta:</strong><br>"{rp.get('cliente_repregunta', 'No especificado.')}"
                </div>
                <div class='chat-bubble chat-executive'>
                    <strong>Ejecutivo profundiza y cierra:</strong><br>"{rp.get('ejecutivo_profundiza_cierra', 'No especificado.')}"
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Preguntas de práctica individual")
            st.write("Ensaya responder estas preguntas de diagnóstico en voz alta:")
            for q in obj["preguntas_diagnostico"]:
                st.markdown(f"*   *\"{q}\"*")
                
        with tab3:
            st.markdown("### Checklist de Dominio Comercial")
            st.write("Marca los elementos a medida que los domines en tus llamadas de prueba:")
            
            st.checkbox("Comprendo el concepto técnico de fondo y la estructura de comisiones/impuestos implicada.", key=f"chk_fnd_{obj['id']}")
            st.checkbox("Soy capaz de traducir conceptos complejos a la explicación simple del cliente.", key=f"chk_diag_{obj['id']}")
            st.checkbox("Sé guiar la conversación mediante preguntas sin entrar a debatir de forma reactiva.", key=f"chk_resp_{obj['id']}")
            st.checkbox("Identifico qué simuladores/herramientas debo invocar y sé acceder a ellos.", key=f"chk_tool_{obj['id']}")
            st.checkbox("Logro proponer el cierre sin prometer rentabilidad futura.", key=f"chk_crm_{obj['id']}")
            
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
        rp = obj.get("role_play", {})
        
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
            placeholder="Escribe cómo iniciarías la argumentación, empatizando y haciendo preguntas de diagnóstico..."
        )
        
        if st.button("🚀 Evaluar Respuesta"):
            if not st.session_state.role_play_user_answer.strip():
                st.warning("Por favor, escribe una respuesta antes de evaluar.")
            else:
                st.session_state.role_play_evaluated = True
                
        if st.session_state.role_play_evaluated:
            st.markdown("---")
            
            # Mostrar diálogo de referencia
            st.markdown("### 🎭 Diálogo de Referencia Recomendado")
            st.markdown(f"""
            <div class='chat-container'>
                <div class='chat-bubble chat-client'>
                    <strong>Cliente plantea:</strong><br>"{rp.get('cliente_plantea', '')}"
                </div>
                <div class='chat-bubble chat-executive'>
                    <strong>Ejecutivo responde (Empatía + Diagnóstico):</strong><br>"{rp.get('ejecutivo_responde', '')}"
                </div>
                <div class='chat-bubble chat-client'>
                    <strong>Cliente repregunta:</strong><br>"{rp.get('cliente_repregunta', '')}"
                </div>
                <div class='chat-bubble chat-executive'>
                    <strong>Ejecutivo profundiza y cierra:</strong><br>"{rp.get('ejecutivo_profundiza_cierra', '')}"
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### ✅ Checklist de Autoevaluación")
            st.write("Revisa tu respuesta escrita y califica sinceramente si cumpliste los siguientes puntos:")
            
            c1 = st.checkbox("¿Escuché y validé la objeción con empatía? (Sin ponerse a la defensiva)", key="eval_1")
            c2 = st.checkbox("¿Hice preguntas de diagnóstico antes de entregar la respuesta?", key="eval_2")
            c3 = st.checkbox("¿Conecté mi argumento con el objetivo real del cliente?", key="eval_3")
            c4 = st.checkbox("¿Hice referencia a alguna evidencia o herramienta interna (simuladores, comparadores)?", key="eval_4")
            c5 = st.checkbox("¿Cerró con un siguiente paso concreto (diagnóstico, cotización, etc.)?", key="eval_5")
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
    st.markdown("<p class='app-subtitle'>Modifica los datos normativos, comisiones y enlaces internos. Estos cambios se guardarán de forma permanente.</p>", unsafe_allow_html=True)
    
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
