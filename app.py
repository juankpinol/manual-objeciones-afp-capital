import streamlit as st
import json
import pandas as pd
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
    
    /* Tarjeta de Objeción */
    .objection-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        border-left: 6px solid #FF8200;
    }
    
    /* Semáforos de Sensibilidad */
    .border-verde { border-left-color: #137333; }
    .border-amarillo { border-left-color: #FFC107; }
    .border-rojo { border-left-color: #D93025; }
    
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
    
    /* Secciones del Manual */
    .manual-h3 {
        font-size: 1.15rem;
        font-weight: 600;
        color: #0F2C59;
        margin-top: 25px;
        margin-bottom: 10px;
        border-bottom: 1px solid #E8EAED;
        padding-bottom: 5px;
    }
    .manual-box {
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 15px;
        border-left: 3px solid #0F2C59;
        font-size: 0.98rem;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    .manual-box-accent {
        background-color: #FFF7EF;
        border-radius: 8px;
        padding: 18px;
        border-left: 4px solid #FF8200;
        font-size: 1.05rem;
        color: #0F2C59;
        line-height: 1.6;
        margin-bottom: 15px;
    }
    .manual-box-error {
        background-color: #FCE8E6;
        border-radius: 8px;
        padding: 12px 16px;
        border-left: 3px solid #C5221F;
        font-size: 0.95rem;
        color: #C5221F;
        margin-bottom: 12px;
    }
    
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
        "📖 Manual de Objeciones",
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
    
    st.markdown("### Guía de Uso del Manual")
    st.markdown("""
    Esta herramienta simplifica el acceso a la argumentación comercial y técnica del manual de objeciones.
    
    *   **Navegación Intuitiva:** Dirígete a la sección **📖 Manual de Objeciones** en la barra lateral.
    *   **Selección Directa:** Selecciona la Categoría y luego la Objeción del cliente para abrir inmediatamente el texto completo del manual en una sola vista.
    *   **Uso Híbrido:**
        *   **En Reunión:** Accede rápidamente al argumento comercial recomendado, cierre y preguntas de diagnóstico.
        *   **En Estudio:** Estudia el fundamento técnico de fondo, el role play conversacional y descarga la guía de autoestudio.
    """)
    
    st.markdown("### Disclaimers y Notas de Cumplimiento")
    for d in disclaimers:
        st.info(d)

# 2. MÓDULO MANUAL DE OBJECIONES (ESTRUCTURA DE FLUJO SIMPLIFICADA)
elif menu == "📖 Manual de Objeciones":
    st.markdown("<h1 class='app-title'>Manual de Objeciones</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Identifica la categoría de la objeción, la duda específica y utiliza el texto oficial del manual</p>", unsafe_allow_html=True)
    
    # 1. Identificar la Categoría
    categorias = sorted(list(set([o["categoria"] for o in st.session_state.objeciones])))
    selected_cat = st.selectbox("📁 1. Selecciona la Categoría de la Objeción", categorias)
    
    # 2. Identificar la Objeción dentro de la categoría
    filtered_objeciones = [o for o in st.session_state.objeciones if o["categoria"] == selected_cat]
    obj_options = {o["objecion_cliente"]: o for o in filtered_objeciones}
    selected_obj_text = st.selectbox("💬 2. Selecciona la Objeción del Cliente", list(obj_options.keys()))
    
    st.markdown("---")
    
    if selected_obj_text:
        obj = obj_options[selected_obj_text]
        sens = obj.get("sensibilidad", "Verde")
        border_class = f"border-{sens.lower()}"
        badge_class = f"badge-{sens.lower()}"
        
        # Cabecera de la Ficha
        st.markdown(f"""
        <div class='objection-card {border_class}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:1.4rem; font-weight:700; color:#0F2C59;'>"{obj['objecion_cliente']}"</span>
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
        
        # TEXTO COMPLETO DEL MANUAL EN UN SOLO FLUJO VERTICAL CONTINUO
        
        # A. Análisis Psicológico / Fondo Real
        st.markdown("<div class='manual-h3'>🧠 ¿Qué hay detrás de la objeción? (Fondo Real)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='manual-box'>{obj['fondo_real']}</div>", unsafe_allow_html=True)
        
        # B. Concepto Técnico
        st.markdown("<div class='manual-h3'>🔬 Concepto Técnico que debe entender el Ejecutivo</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='manual-box' style='background-color:#F0F4F8;'>{obj.get('concepto_tecnico', 'No especificado.')}</div>", unsafe_allow_html=True)
        
        # C. Explicación Simple para el Cliente
        st.markdown("<div class='manual-h3'>📢 Explicación Simple para el Cliente (Sin Tecnicismos)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='manual-box'>{obj.get('explicacion_simple', 'No especificada.')}</div>", unsafe_allow_html=True)
        
        # D. Argumento Comercial Recomendado
        st.markdown("<div class='manual-h3'>🎯 Argumento Comercial Recomendado</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='manual-box-accent'>\"{obj['respuesta_comercial']}\"</div>", unsafe_allow_html=True)
        st.code(obj['respuesta_comercial'], language="text")
        
        # E. Preguntas de Diagnóstico
        st.markdown("<div class='manual-h3'>❓ Preguntas de Diagnóstico para Calificar</div>", unsafe_allow_html=True)
        st.write("Realiza estas preguntas antes de dar la respuesta definitiva para indagar la meta del cliente:")
        for q in obj["preguntas_diagnostico"]:
            st.markdown(f"*   *\"{q}\"*")
            
        # F. Ejemplo Práctico
        st.markdown("<div class='manual-h3'>💡 Ejemplo Práctico Aplicado</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='manual-box'>{obj.get('ejemplo_practico', 'No especificado.')}</div>", unsafe_allow_html=True)
        
        # G. Cierre Recomendado
        st.markdown("<div class='manual-h3'>🏁 Cierre Recomendado (Siguiente Paso Comercial)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='manual-box'>\"{obj['cierre']}\"</div>", unsafe_allow_html=True)
        st.code(obj['cierre'], language="text")
        
        # H. Role Play
        st.markdown("<div class='manual-h3'>🎭 Role Play de Simulación Dialéctica</div>", unsafe_allow_html=True)
        rp = obj.get("role_play", {})
        st.markdown(f"""
        <div style='background-color:#FFFFFF; border:1px solid #E8EAED; border-radius:8px; padding:15px; margin-bottom:15px;'>
            <p><strong>1. Cliente plantea la objeción:</strong><br><span style='color:#555;'>"{rp.get('cliente_plantea', '')}"</span></p>
            <p><strong>2. Ejecutivo responde (Empatía + Diagnóstico):</strong><br><span style='color:#0F2C59; font-weight:500;'>"{rp.get('ejecutivo_responde', '')}"</span></p>
            <p><strong>3. Cliente repregunta:</strong><br><span style='color:#555;'>"{rp.get('cliente_repregunta', '')}"</span></p>
            <p><strong>4. Ejecutivo profundiza y cierra:</strong><br><span style='color:#FF8200; font-weight:500;'>"{rp.get('ejecutivo_profundiza_cierra', '')}"</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # I. Versión breve para WhatsApp
        st.markdown("<div class='manual-h3'>💬 Generador de Mensaje Breve para WhatsApp</div>", unsafe_allow_html=True)
        col_wa1, col_wa2 = st.columns(2)
        with col_wa1:
            wa_client_name = st.text_input("Nombre del cliente", placeholder="Ej: Francisco", key=f"wa_name_simp_{obj['id']}")
            wa_tone = st.selectbox("Tono del mensaje", ["Cercano", "Ejecutivo", "Directo", "Educativo"], key=f"wa_tone_simp_{obj['id']}")
        with col_wa2:
            wa_msg = generate_whatsapp_message(obj, wa_tone, wa_client_name)
            st.write("**Texto para copiar:**")
            st.code(wa_msg, language="text")
            
        # J. Versión Llamada Telefónica
        if obj.get("llamada"):
            st.markdown("<div class='manual-h3'>📞 Versión Rápida para Llamada Telefónica</div>", unsafe_allow_html=True)
            st.code(obj["llamada"], language="text")
            
        # K. Errores a Evitar
        st.markdown("<div class='manual-h3'>⚠️ Errores Típicos a Evitar</div>", unsafe_allow_html=True)
        for err in obj["errores_evitar"]:
            st.markdown(f"<div class='manual-box-error'>✘ {err}</div>", unsafe_allow_html=True)
            
        # L. Descargas de Fichas
        st.markdown("---")
        st.markdown("### 📥 Descargar Ficha Técnica")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            obj_md = export_objection_markdown(obj)
            st.download_button(
                label="📄 Descargar Ficha en Markdown",
                data=obj_md,
                file_name=f"ficha_{obj['id']}.md",
                mime="text/markdown",
                key=f"dl_md_simp_{obj['id']}"
            )
        with col_dl2:
            study_md = export_study_sheet_markdown(obj)
            st.download_button(
                label="📖 Descargar Ficha de Estudio",
                data=study_md,
                file_name=f"estudio_{obj['id']}.md",
                mime="text/markdown",
                key=f"dl_std_simp_{obj['id']}"
            )

# 3. MÓDULO CONFIGURACIÓN
elif menu == "⚙️ Configuración":
    st.markdown("<h1 class='app-title'>Parámetros y Configuración Comercial</h1>", unsafe_allow_html=True)
    st.markdown("<p class='app-subtitle'>Modifica los datos normativos, comisiones y enlaces internos de forma persistente.</p>", unsafe_allow_html=True)
    
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
            
            if save_parametros(nuevos_parametros):
                st.session_state.parametros = nuevos_parametros
                st.success("✅ ¡Configuración guardada correctamente de manera persistente!")
                st.rerun()

# 4. MÓDULO BUENAS PRÁCTICAS Y CUMPLIMIENTO
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
