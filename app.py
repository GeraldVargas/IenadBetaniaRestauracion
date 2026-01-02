import streamlit as st
from PIL import Image
import datetime
import pytz
import json
import pandas as pd
import streamlit.components.v1 as components
import json
import os
import urllib.parse

def scroll_to_top():
    components.html(
        """
        <script>
        const waitForApp = () => {
            const app = window.parent.document.querySelector(
                'div[data-testid="stAppViewContainer"]'
            );

            if (!app) {
                setTimeout(waitForApp, 50);
                return;
            }

            const observer = new MutationObserver(() => {
                app.scrollTop = 0;
            });

            observer.observe(app, {
                childList: true,
                subtree: true
            });

            // primer intento inmediato
            app.scrollTop = 0;

            // refuerzo
            setTimeout(() => {
                app.scrollTop = 0;
            }, 100);
        };

        waitForApp();
        </script>
        """,
        height=0,
    )


# ============================================================================
# 1. CONFIGURACIÓN DE PÁGINA 
# ============================================================================

st.set_page_config(
    page_title="IENAD-RESTAURACION",
    page_icon=  "LogoIglesia.jpeg" if os.path.exists("LogoIglesia.jpeg") else "✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

# ============================================================================
# 2. SISTEMA DE ESTILOS AVANZADO (CSS) - MANTENIDO
# ============================================================================

st.markdown("""
    <style>
    /* 1. IMPORTACIÓN DE FUENTES */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Montserrat:wght@300;400;600&display=swap');

    /* 2. VARIABLES Y CONFIGURACIÓN GLOBAL */
    :root {
        --primary: #1E3A8A;
        --secondary: #D4AF37;
        --dark: #071840;
        --light: #ffffff;
    }

    section.main > div {
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    div[data-testid="stAppViewContainer"] {
        overflow-x: hidden;
    }

    .stApp {
        background-color: var(--light);
    }

    /* 3. TIPOGRAFÍAS (CORREGIDO PARA NO ROMPER ICONOS) */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 900 !important;
    }
    
    /* Aplicamos Montserrat solo a textos reales, no a contenedores de iconos */
    .stApp p, .stApp label, .stApp li, .stApp .stButton button, .stApp span:not([data-testid="stIconMaterial"]) {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* 4. HEADER (AZUL DARK Y BORDE DORADO) */
    header[data-testid="stHeader"] {
        background-color: var(--dark) !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.3) !important;
        height: 3.5rem !important;
        z-index: 999 !important;
    }

    /* 5. SIDEBAR PREMIUM */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark) 0%, #1e293b 100%) !important;
        border-right: 1px solid var(--secondary);
    }
    
    /* Texto normal en el sidebar */
    .stSidebar [data-testid="stMarkdownContainer"] p {
        color: #cbd5e1;
        font-family: 'Montserrat', sans-serif;
    }

    /* EFECTO DORADO EN NOMBRES DE PÁGINAS (HOVER) */
    [data-testid="stSidebarNav"] li:hover span {
        color: var(--secondary) !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebarNav"] span {
        color: #cbd5e1 !important;
        transition: all 0.3s ease !important;
    }

    /* 6. ELIMINAR TEXTO "KEYBOARD DOUBLE..." Y PONER FLECHA DORADA */
    button[data-testid="collapsedControl"] {
        position: relative !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--secondary) !important;
        width: 40px !important;
        height: 40px !important;
        overflow: hidden !important;
        color: transparent !important;
        text-indent: -9999px !important; /* Manda el texto al infinito */
        margin-top: 8px !important;
        margin-left: 10px !important;
    }

    button[data-testid="collapsedControl"] * {
        display: none !important; /* Oculta cualquier span o svg interno */
    }

    button[data-testid="collapsedControl"]::after {
        content: "〉" !important; /* Flecha simple */
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        font-size: 20px !important;
        color: var(--secondary) !important;
        font-family: Arial, sans-serif !important;
        text-indent: 0 !important; /* Trae la flecha al centro */
        visibility: visible !important;
        font-weight: bold !important;
    }

    /* 7. COMPONENTES DE DISEÑO (CARDS, HERO, BUTTONS) */
    .hero-section {
        background: linear-gradient(rgba(15, 23, 42, 0.7), rgba(15, 23, 42, 0.7)), 
                    url('https://images.unsplash.com/photo-1438232992991-995b7058bbb3?q=80&w=2000');
        background-size: cover;
        background-position: center;
        padding: 100px 40px;
        border-radius: 30px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }

    .glass-card {
        background: white;
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border-top: 5px solid var(--secondary);
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
    }

    .stButton > button {
        width: 100%;
        background-color: transparent !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        border-color: var(--secondary) !important;
        color: var(--secondary) !important;
        background: rgba(212, 175, 55, 0.1) !important;
    }

    /* 8. FOOTER Y OTROS */
    .custom-footer {
        background: var(--dark);
        color: white;
        padding: 60px 40px;
        border-radius: 30px 30px 0 0;
        text-align: center;
        margin-top: 50px;
    }

    .whatsapp-button {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;
        color: white !important;
        border: none !important;
    }
            /* ======================================
    HEADER CAMUFLADO (PLOMO OSCURO)
    ====================================== */

    /* Header principal */
    header[data-testid="stHeader"] {
        background: #071840 !important;   /* plomo oscuro */
        box-shadow: none !important;
        border-bottom: 1px solid #334155 !important;
    }

    /* Ocultar SOLO el texto/icono roto */
    header [data-testid="collapsedControl"] span,
    header [data-testid="collapsedControl"] i {
        display: none !important;
    }

    /* Evita que el texto fallback se muestre */
    header [data-testid="collapsedControl"] {
        font-size: 0 !important;
        width: 36px;
    }

    /* Ajustar botones del header (Deploy, ⋮) */
    header button {
        color: #CBD5E1 !important;
    }

    /* Hover sutil */
    header button:hover {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 8px;
    }

    </style>
    
""", unsafe_allow_html=True)

# ============================================================================
# 3. FUNCIONES DE UTILIDAD PROFESIONALES
# ============================================================================

def get_bolivia_time():
    """Obtiene la hora actual en Bolivia"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.datetime.now(bolivia_tz)

def calculate_time_until_next_service():
    """Calcula el tiempo hasta el próximo CULTO (solo sábados y domingos)"""
    now = get_bolivia_time()
    current_weekday = now.weekday()
    current_time = now.time()
    
    # SOLO cultos (sábado y domingo según lo solicitado)
    # Los ensayos (martes, jueves, viernes) NO aparecen aquí
    services = {
        5: [  # Sábado (weekday 5) - SOLO CULTO
            {'name': 'Culto de Restauración', 'time': datetime.time(18, 30), 'icon': '🕊️'}
        ],
        6: [  # Domingo (weekday 6) - SOLO CULTO
            {'name': 'Culto Dominical', 'time': datetime.time(10, 30), 'icon': '✝️'}
        ]
        # NOTA: Ya NO incluimos miércoles (culto de oración)
    }
    
    # Buscar el próximo servicio en los próximos 7 días
    for days_ahead in range(8):  # Buscar en la semana actual + 1 día
        check_date = now + datetime.timedelta(days=days_ahead)
        check_weekday = check_date.weekday()
        
        if check_weekday in services:
            for service in services[check_weekday]:
                # Crear datetime con la misma zona horaria que 'now'
                service_datetime = datetime.datetime.combine(
                    check_date.date(), 
                    service['time'],
                    tzinfo=now.tzinfo  # Agregar la misma zona horaria
                )
                
                if days_ahead == 0 and service['time'] <= current_time:
                    continue  # Este servicio ya pasó hoy
                
                time_until = service_datetime - now
                return {
                    'name': service['name'],
                    'datetime': service_datetime,
                    'icon': service['icon'],
                    'time_until': time_until,
                    'is_today': days_ahead == 0
                }
    
    # Si no encuentra ningún culto en los próximos 7 días (caso raro)
    return None
def save_prayer_request(data):
    """Guarda la petición de oración (en producción usaría una base de datos)"""
    try:
        with open('prayer_requests.json', 'a') as f:
            json.dump({**data, 'timestamp': str(datetime.datetime.now())}, f)
            f.write('\n')
        return True
    except:
        return False

def load_verse_of_day():
    """Carga el versículo del día (podría conectarse a una API bíblica)"""
    verses = [
        {"text": "De modo que si alguno está en Cristo, nueva criatura es; las cosas viejas pasaron; he aquí todas son hechas nuevas.", "reference": "2 Corintios 5:17"},
        {"text": "Todo lo puedo en Cristo que me fortalece.", "reference": "Filipenses 4:13"},
        {"text": "Jehová es mi pastor; nada me faltará.", "reference": "Salmos 23:1"},
        {"text": "Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito.", "reference": "Juan 3:16"},
        {"text": "Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.", "reference": "1 Pedro 5:7"}
    ]
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return verses[day_of_year % len(verses)]

# ============================================================================
# 4. GESTIÓN DE NAVEGACIÓN Y ESTADO DE LA APLICACIÓN
# ============================================================================

if 'page' not in st.session_state:
    st.session_state.page = 'Inicio'

if 'prayer_count' not in st.session_state:
    st.session_state.prayer_count = 0

def set_page(name):
    st.session_state.page = name

# ============================================================================
# 5. SIDEBAR REDISEÑADO
# ============================================================================

with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Logo de la iglesia
    try:
        st.image("LogoIglesia.jpeg", use_container_width=True)
    except:
        st.markdown("<h1 style='color:var(--secondary); text-align:center;'>✝️</h1>", unsafe_allow_html=True)
    
    # Título y ubicación
    st.markdown("<h2 style='color:white; text-align:center; font-size:1.5rem;'>RESTAURACIÓN</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.8rem; margin-top:-15px;'>Cochabamba - Bolivia</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
    
    # Contador de próxima reunión
       # Contador de próxima reunión
    next_service = calculate_time_until_next_service()
    if next_service:
        days_word = "Hoy" if next_service['is_today'] else "Próximo"
        
        # Traducir el día y mes al español
        dias_semana_es = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        meses_es = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        
        # Obtener fecha en formato inglés
        fecha_ingles = next_service['datetime'].strftime('%A %d, %H:%M')
        
        # Traducir a español
        fecha_espanol = fecha_ingles
        for eng, esp in dias_semana_es.items():
            fecha_espanol = fecha_espanol.replace(eng, esp)
        
        # Si necesitas traducir meses también (por si acaso)
        # for eng, esp in meses_es.items():
        #     fecha_espanol = fecha_espanol.replace(eng, esp)
        
        st.markdown(f"""
            <div style="background: rgba(30, 58, 138, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <p style="color: #D4AF37; font-size: 0.9rem; margin: 0; font-weight: bold;">
                    {next_service['icon']} {days_word}: {next_service['name']}
                </p>
                <p style="color: white; font-size: 0.8rem; margin: 5px 0 0 0;">
                    {fecha_espanol}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Navegación principal
    st.button(" Inicio", on_click=set_page, args=('Inicio',))
    st.button(" Horarios de Culto", on_click=set_page, args=('Horarios',))
    st.button(" Anuncios", on_click=set_page, args=('Anuncios',))  # NUEVO
    st.button(" Nuestra Ubicación", on_click=set_page, args=('Ubicacion',))
    st.button(" Redes Sociales", on_click=set_page, args=('Redes',))
    st.button(" Petición de Oración", on_click=set_page, args=('Oracion',))
    st.button(" Contactos Directos", on_click=set_page, args=('Contactos',))
    
    # Información adicional en sidebar
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    
    
    st.info("¡Te esperamos con los brazos abiertos!")

# ============================================================================
# 6. LÓGICA DE CONTENIDO POR PÁGINA
# ============================================================================
# PÁGINA: INICIO
# ============================================================================

if st.session_state.page == 'Inicio':
    scroll_to_top()
    import base64
    import os
    
    # Función para convertir imagen a base64
    def get_base64_image(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    
    # Cargar las TRES imágenes para el hero
    imagen1_base64 = None  # f1.jpeg
    imagen2_base64 = None  # f3.jpeg  
    imagen3_base64 = None  # f5.jpeg
    
    # Buscar imágenes para el hero
    for img_name, var in [('f1.jpeg', 'imagen1_base64'), ('f3.jpeg', 'imagen2_base64'), ('f5.jpeg', 'imagen3_base64')]:
        for ruta in [img_name, f'./{img_name}', f'images/{img_name}', f'static/{img_name}', f'assets/{img_name}']:
            if os.path.exists(ruta):
                if var == 'imagen1_base64':
                    imagen1_base64 = get_base64_image(ruta)
                elif var == 'imagen2_base64':
                    imagen2_base64 = get_base64_image(ruta)
                else:
                    imagen3_base64 = get_base64_image(ruta)
                break
    
    # Cargar imágenes para los cuadros
    fini_base64 = None
    f9_base64 = None
    otras_imagenes = {}
    
    # Buscar fini.jpeg
    for ruta in ['fini.jpeg', './fini.jpeg', 'images/fini.jpeg', 'static/fini.jpeg', 'assets/fini.jpeg']:
        if os.path.exists(ruta):
            fini_base64 = get_base64_image(ruta)
            break
    
    # Buscar f9.jpeg
    for ruta in ['f9.jpeg', './f9.jpeg', 'images/f9.jpeg', 'static/f9.jpeg', 'assets/f9.jpeg']:
        if os.path.exists(ruta):
            f9_base64 = get_base64_image(ruta)
            break
    
    # Cargar otras imágenes para "Conoce más a la iglesia"
    otras_imgs_nombres = ['f6.jpeg', 'f11.jpeg', 'f10.jpeg', 'f7.jpeg']
    for img_nombre in otras_imgs_nombres:
        for ruta in [img_nombre, f'./{img_nombre}', f'images/{img_nombre}', f'static/{img_nombre}', f'assets/{img_nombre}']:
            if os.path.exists(ruta):
                otras_imagenes[img_nombre] = get_base64_image(ruta)
                break
    
    # Hero section (igual que antes)
    hero_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        body, html {{
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }}
        .hero-slideshow-wrapper {{
            position: relative;
            width: 100vw !important;
            margin-left: -50vw !important;
            left: 50% !important;
            right: 50% !important;
            margin-right: -50vw !important;
            overflow: hidden !important;
            background: transparent !important;
        }}
        
        .hero-slideshow {{
            position: relative;
            width: 100vw !important;
            height: 500px;
            overflow: hidden;
            border-radius: 0px !important;
            margin-bottom: 40px;
            background: transparent !important;
        }}    
        
        .slide {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            transition: opacity 1s ease-in-out;
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        
        .slide.active {{
            opacity: 1;
        }}
        
        .hero-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.6);
            z-index: 1;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 20px 20px;
            color: white;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            padding-top: 5px;
        }}
        </style>
    </head>
    <body>
        <div class="hero-slideshow">
            <!-- Imagen 1 -->
            <div class="slide active" id="slide1" style="background-image: url('data:image/jpeg;base64,{imagen1_base64 if imagen1_base64 else ''}');"></div>
            
            <!-- Imagen 2 -->
            <div class="slide" id="slide2" style="background-image: url('data:image/jpeg;base64,{imagen2_base64 if imagen2_base64 else ''}');"></div>
            
            <!-- Imagen 3 -->
            <div class="slide" id="slide3" style="background-image: url('data:image/jpeg;base64,{imagen3_base64 if imagen3_base64 else ''}');"></div>
            
            <!-- Overlay para oscurecer -->
            <div class="hero-overlay"></div>
            
            <!-- Contenido de texto -->
            <div class="hero-content">
                <h1 style="font-size: 3.8rem; color: white; margin-bottom: 1px; text-shadow: 2px 2px 6px rgba(0,0,0,0.8); line-height: 1.1;">
                    IENAD BETANIA<br>
                    <span style="font-size: 2.5rem; color: #D4AF37; text-shadow: 1px 1px 4px rgba(0,0,0,0.7);">
                        - RESTAURACIÓN -
                    </span>
                </h1>
                
                <div style="max-width: 900px; margin: 150px auto 0; padding: 18px; background: rgba(0,0,0,0.4); border-radius: 12px; backdrop-filter: blur(5px);">
                    <p style="font-size: 1.2rem; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); line-height: 1.6; margin: 0;">
                        Somos una comunidad apasionada por la presencia de Dios.
                    </p>
                </div>
            </div>
        </div>
        
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            let currentSlide = 0;
            const slides = document.querySelectorAll('.slide');
            const totalSlides = slides.length;
            
            function showNextSlide() {{
                // Ocultar slide actual
                slides[currentSlide].classList.remove('active');
                
                // Calcular siguiente slide
                currentSlide = (currentSlide + 1) % totalSlides;
                
                // Mostrar siguiente slide
                slides[currentSlide].classList.add('active');
            }}
            
            // Cambiar slide cada 3 segundos (3000 milisegundos)
            setInterval(showNextSlide, 3000);
            
            // Inicializar primera transición después de 3 segundos
            setTimeout(showNextSlide, 3000);
        }});
        </script>
    </body>
    </html>
    """
    
    # Mostrar el hero section
    st.components.v1.html(hero_html, height=500)
    
    # 2. TARJETAS DE INFORMACIÓN (Misión, Visión, Valores)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class="glass-card">
            <h3 style="color:#1E3A8A">Misión</h3>
            <div style="height: 4px; width: 50px; background: #D4AF37; margin: 10px 0 20px 0;"></div>
            <p style="color:#64748b">Predicar el evangelio de Jesucristo a toda persona, restaurando la dignidad y propósito del ser humano.</p>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="glass-card">
            <h3 style="color:#1E3A8A">Visión</h3>
            <div style="height: 4px; width: 50px; background: #D4AF37; margin: 10px 0 20px 0;"></div>
            <p style="color:#64748b">Ser una iglesia de impacto transformador en Cochabamba, basada en el amor bíblico y el servicio real.</p>
        </div>""", unsafe_allow_html=True)
        
    with col3:
        st.markdown("""<div class="glass-card">
            <h3 style="color:#1E3A8A">Valores</h3>
            <div style="height: 4px; width: 50px; background: #D4AF37; margin: 10px 0 20px 0;"></div>
            <p style="color:#64748b">Fe, Integridad, Familia y Restauración espiritual constante a través de la Palabra de Dios.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 3. VERSÍCULO DEL DÍA
    verse = load_verse_of_day()
    
    # Formatear la fecha en español
    meses_es = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
        'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
        'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    
    fecha_ingles = get_bolivia_time().strftime('%d de %B, %Y')
    for eng, esp in meses_es.items():
        fecha_ingles = fecha_ingles.replace(eng, esp)
    
    c_vers, c_img = st.columns([2, 1])
    with c_vers:
        st.markdown(f"""
        <div style="background: white; padding: 50px; border-radius: 20px; border-left: 8px solid #D4AF37; box-shadow: 0 15px 35px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h2 style="color: #1E3A8A; margin-top: 0;">La Palabra de Hoy</h2>
                <span style="color: #64748b; font-size: 0.9rem;">{fecha_ingles}</span>
            </div>
            <p style="font-size: 1.8rem; font-style: italic; color: #1e293b; line-height: 1.4;">
                "{verse['text']}"
            </p>
            <p style="color: #D4AF37; font-weight: bold; font-size: 1.2rem; margin-top: 20px;">— {verse['reference']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c_img:
        try:
            st.image("LogoIglesia.jpeg", use_container_width=True)
        except:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E3A8A 0%, #D4AF37 100%); 
                    padding: 30px; border-radius: 20px; text-align: center; height: 100%; display: flex; 
                    flex-direction: column; justify-content: center;">
                <h3 style="color: white; margin-bottom: 10px;">Restauración</h3>
                <p style="color: rgba(255,255,255,0.9);">En Cristo somos nuevas criaturas</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 4. DOS CUADROS GRANDES: "¿Qué creemos?" y "Acerca de nosotros"
    st.markdown("""
        <div style="text-align:center; padding: 20px 0 40px 0;">
            <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>Conoce nuestra fe e historia</h1>
            <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
            
        </div>
    """, unsafe_allow_html=True)
    
    col_creemos, col_acerca = st.columns(2)
    
    # 1. CSS ESPECÍFICO (Solo para botones en el área principal, NO toca el sidebar)
    st.markdown("""
        <style>
        /* Este selector asegura que SOLO los botones del área central cambien */
        section[data-testid="stMain"] div.stButton > button {
            background-color: var(--dark) !important; /* Tu azul --dark */
            color: primary !important;           /* Letras Doradas */
            border: 2px solid #D4AF37 !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            height: 50px !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase;
        }
        
        section[data-testid="stMain"] div.stButton > button:hover {
            background-color: #D4AF37  !important;
            color: #1E3A8A !important;
            transform: scale(1.02);
        }
        </style>
    """, unsafe_allow_html=True)

    col_creemos, col_acerca = st.columns(2)

    with col_creemos:
        # Cuadro "¿Qué creemos?"
        if fini_base64:
            cuadro_creemos_html = f"""
            <div style="position: relative; height: 280px; border-radius: 15px; overflow: hidden; margin-bottom: 10px;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                            background-image: url('data:image/jpeg;base64,{fini_base64}');
                            background-size: cover; background-position: center;"></div>
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.6);"></div>
                
            </div>
            """
        else:
            cuadro_creemos_html = """
            <div style="background: #D4AF37; height: 280px; border-radius: 15px; padding: 30px; display: flex; align-items: flex-end; margin-bottom: 10px;">
                <h3 style="font-size: 2.2rem; color: white; margin: 0;">¿Qué creemos?</h3>
            </div>
            """
        st.markdown(cuadro_creemos_html, unsafe_allow_html=True)
        
        # BOTÓN: Texto actualizado a "¿Qué creemos?"
        if st.button("¿Qué creemos?", key="btn_creemos", use_container_width=True):
            st.session_state.page = 'pagina_creemos'
            st.rerun()

    with col_acerca:
        # Cuadro "Acerca de nosotros"
        if f9_base64:
            cuadro_acerca_html = f"""
            <div style="position: relative; height: 280px; border-radius: 15px; overflow: hidden; margin-bottom: 10px;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                            background-image: url('data:image/jpeg;base64,{f9_base64}');
                            background-size: cover; background-position: center;"></div>
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.6);"></div>
               
            </div>
            """
        else:
            cuadro_acerca_html = """
            <div style="background: #0F172A; height: 280px; border-radius: 15px; padding: 30px; display: flex; align-items: flex-end; margin-bottom: 10px;">
                <h3 style="font-size: 2.2rem; color: white; margin: 0;">Acerca de nosotros</h3>
            </div>
            """
        st.markdown(cuadro_acerca_html, unsafe_allow_html=True)
        
        # BOTÓN: Texto actualizado a "Acerca de nosotros"
        if st.button("Acerca de nosotros", key="btn_acerca", use_container_width=True):
            st.session_state.page = 'pagina_acerca'
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
            <div style="text-align:center; padding: 20px 0 40px 0;">
                <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>Conoce más a la iglesia</h1>
                <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
                
            </div>
        """, unsafe_allow_html=True)    
    # Mostrar las otras imágenes en 2 filas de 2 columnas SIN SOMBRAS
    if otras_imagenes:
        # Primera fila
        col_img1, col_img2 = st.columns(2)
        
        with col_img1:
            if 'f6.jpeg' in otras_imagenes:
                st.markdown(f"""
                <div style="border-radius: 15px; overflow: hidden; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{otras_imagenes['f6.jpeg']}" 
                         style="width: 100%; height: 250px; object-fit: cover; display: block;">
                </div>
                """, unsafe_allow_html=True)
        
        with col_img2:
            if 'f11.jpeg' in otras_imagenes:
                st.markdown(f"""
                <div style="border-radius: 15px; overflow: hidden; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{otras_imagenes['f11.jpeg']}" 
                         style="width: 100%; height: 250px; object-fit: cover; display: block;">
                </div>
                """, unsafe_allow_html=True)
        
        # Segunda fila
        col_img3, col_img4 = st.columns(2)
        
        with col_img3:
            if 'f10.jpeg' in otras_imagenes:
                st.markdown(f"""
                <div style="border-radius: 15px; overflow: hidden; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{otras_imagenes['f10.jpeg']}" 
                         style="width: 100%; height: 250px; object-fit: cover; display: block;">
                </div>
                """, unsafe_allow_html=True)
        
        with col_img4:
            if 'f7.jpeg' in otras_imagenes:
                st.markdown(f"""
                <div style="border-radius: 15px; overflow: hidden; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{otras_imagenes['f7.jpeg']}" 
                         style="width: 100%; height: 250px; object-fit: cover; display: block;">
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Las imágenes de 'Conoce más a la iglesia' no se encontraron.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
       # 6. PRÓXIMA ACTIVIDAD - SOLO CULTOS (actualizado)
    st.markdown("""
            <div style="text-align:center; padding: 20px 0 40px 0;">
                <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>Próxima Actividad</h1>
                <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
                
            </div>
        """, unsafe_allow_html=True)    
    next_service = calculate_time_until_next_service()
    if next_service:
        days = next_service['time_until'].days
        hours = next_service['time_until'].seconds // 3600
        minutes = (next_service['time_until'].seconds % 3600) // 60
        
        # Formatear fecha en español
        dias_semana_es = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        meses_es = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        
        # Determinar qué día es para mostrar el mensaje correcto
        if next_service['name'] == 'Culto de Restauración':
            fecha_servicio = next_service['datetime'].strftime('%A %d de %B, %H:%M')
            actividad_desc = "Sábado 6:30 PM - Culto principal de restauración y palabra"
        elif next_service['name'] == 'Culto Dominical':
            fecha_servicio = next_service['datetime'].strftime('%A %d de %B, %H:%M')
            actividad_desc = "Domingo 10:30 AM - Celebración dominical para toda la familia"
        else:
            fecha_servicio = next_service['datetime'].strftime('%A %d de %B, %H:%M')
            actividad_desc = next_service['name']
        
        for eng, esp in dias_semana_es.items():
            fecha_servicio = fecha_servicio.replace(eng, esp)
        
        for eng, esp in meses_es.items():
            fecha_servicio = fecha_servicio.replace(eng, esp)
        
        # Contenedor principal
        st.markdown(f"""
        <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); max-width: 800px; margin: 0 auto; border-top: 5px solid #D4AF37;">
            <div style="text-align: center;">
                <span style="background: #1E3A8A; color: white; padding: 8px 20px; border-radius: 20px; font-size: 0.9rem; font-weight: bold;">
                    {next_service['icon']} PRÓXIMO CULTO
                </span>
                <h3 style="color: #1E3A8A; margin-top: 15px; margin-bottom: 5px;">{next_service['name']}</h3>
                <p style="color: #64748b; margin-bottom: 10px; font-size: 1.1rem;">
                    {fecha_servicio}
                </p>
                <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 30px;">
                    {actividad_desc}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #1E3A8A; text-align: center; margin-bottom: 30px;'>Comienza en:</h4>", unsafe_allow_html=True)
        
        # Contador
        col_dias, col_horas, col_minutos = st.columns(3)
        
        with col_dias:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #1E3A8A;">{days}</div>
                <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Días</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_horas:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #1E3A8A;">{hours}</div>
                <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Horas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_minutos:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #1E3A8A;">{minutes}</div>
                <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Minutos</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Botón para ver todos los horarios
        
        
        # Cerrar el div principal
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Si no hay próximo culto (ejemplo: es domingo por la tarde)
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); max-width: 800px; margin: 0 auto; border-top: 5px solid #D4AF37; text-align: center;">
            <h3 style="color: #1E3A8A; margin-top: 0;">🎉 ¡Hoy hemos adorado juntos!</h3>
            <p style="color: #64748b; margin: 15px 0 25px 0;">
                El próximo culto será el próximo sábado a las 6:30 PM.
            </p>
            <p style="color: #D4AF37; font-weight: bold;">
                "No dejando de congregarnos, como algunos tienen por costumbre"<br>
                — Hebreos 10:25
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Cerrar el div principal
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# PÁGINA: HORARIOS (CON FOTOS Y ESTILO PREMIUM)
# ============================================================================

elif st.session_state.page == 'Horarios':
    scroll_to_top()
    # Encabezado con estilo de revista premium
    st.markdown(f"""
        <div style="text-align:center; padding: 20px 0 40px 0;">
            <h1 style='font-size:3.8rem; color:var(--primary); margin-bottom: 5px;'>Nuestros Horarios</h1>
            <div style="width: 80px; height: 4px; background: var(--secondary); margin: 0 auto 20px auto; border-radius: 2px;"></div>
            <p style='color:#64748b; font-size: 1.2rem; font-family: "Montserrat", sans-serif;'>
                Te esperamos con los brazos abiertos para compartir la palabra de Dios
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Datos de horarios actualizados con imágenes
    horarios = [
        {
            "dia": "Sábado",
            "subtitle": "Preparación y Restauración",
            "eventos": [
                {
                    "nombre": "Ayuno Congregacional", 
                    "hora": "08:00 AM", 
                    "img": "https://images.unsplash.com/photo-1544427920-c49ccfb85579?q=80&w=400&h=400&auto=format&fit=crop", 
                    "descripcion": "Un tiempo de intimidad y búsqueda profunda del Espíritu Santo."
                },
                {
                    "nombre": "Culto de Restauración", 
                    "hora": "06:30 PM", 
                    "icon": "🕊️", # Mantenemos la palomita
                    "descripcion": "Ven a recibir sanidad y una palabra fresca para tu vida."
                }
            ]
        },
        {
            "dia": "Domingo",
            "subtitle": "Día de Celebración",
            "eventos": [
                {
                    "nombre": "Gran Culto Dominical", 
                    "hora": "10:30 AM", 
                    "img": "data:image/jpeg;base64,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", # Imagen solicitada
                    "descripcion": "Nuestra mayor celebración semanal para toda la familia unida."
                }
            ]
        }
    ]
    
    # Columnas principales
    col1, col2 = st.columns(2, gap="large")
    
    for i, dia_info in enumerate(horarios):
        with [col1, col2][i]:
            eventos_html = ""
            for evento in dia_info["eventos"]:
                # Lógica para mostrar imagen o icono (palomita)
                if "img" in evento:
                    media_html = f'<img src="{evento["img"]}" style="width: 70px; height: 70px; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">'
                else:
                    media_html = f'<div style="width: 70px; height: 70px; background: rgba(212, 175, 55, 0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 2rem;">{evento["icon"]}</div>'

                eventos_html += f"""
                <div class="event-box" style="
                    background: #ffffff; 
                    padding: 20px; 
                    border-radius: 18px; 
                    margin-bottom: 20px; 
                    border: 1px solid #f1f5f9;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
                    display: flex;
                    gap: 15px;
                    align-items: center;
                    transition: transform 0.3s ease;
                ">
                    {media_html}
                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="color: var(--dark); margin: 0; font-family: 'Playfair Display'; font-size: 1.2rem;">{evento['nombre']}</h4>
                            <span style="background: var(--primary); color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; font-family: 'Montserrat';">
                                {evento['hora']}
                            </span>
                        </div>
                        <p style="color: #64748b; font-size: 0.85rem; line-height: 1.4; margin: 5px 0 0 0; font-family: 'Montserrat';">
                            {evento['descripcion']}
                        </p>
                    </div>
                </div>
                """
            
            st.markdown(f"""
                <div class="glass-card" style="padding: 30px; border-radius: 25px; background: #fdfdfd; height: 100%;">
                    <h2 style="color: var(--secondary); margin-bottom:5px; font-family: 'Playfair Display';">{dia_info['dia']}</h2>
                    <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">{dia_info['subtitle']}</p>
                    {eventos_html}
                </div>
            """, unsafe_allow_html=True)
    
    # CTA - BIENVENIDA ABIERTA
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, var(--dark) 0%, #1e293b 100%);
            padding: 50px 30px;
            border-radius: 30px;
            text-align: center;
            margin-top: 40px;
            border: 1px solid rgba(212, 175, 55, 0.4);
        ">
            <h2 style="color: white; font-family: 'Playfair Display'; margin-bottom: 15px;">¡Estás invitado a casa!</h2>
            <p style="color: #cbd5e1; font-size: 1.1rem; max-width: 600px; margin: 0 auto 30px auto; font-family: 'Montserrat';">
                En esta comunidad, nuestras puertas están siempre abiertas para ti. No importa dónde te encuentres en tu camino espiritual, aquí encontrarás una familia lista para recibirte.
            </p>
            <div style="display: flex; justify-content: center;">
               
        </div>
    """, unsafe_allow_html=True)

    # Nota de aviso (Footer de horarios)
    st.info("💡 **Aviso:** Durante días feriados, los horarios pueden variar. Te recomendamos seguir nuestras redes sociales para anuncios de último minuto.")

# ============================================================================
# PÁGINA: ANUNCIOS - DISEÑO PREMIUM (MANTENIENDO TODA LA FUNCIONALIDAD)
# ============================================================================

elif st.session_state.page == 'Anuncios':
    scroll_to_top()
    
    # Encabezado con el estilo del sistema
    st.markdown(f"""
        <div style="text-align:center; padding: 20px 0 40px 0;">
            <h1 style='font-size:3.8rem; color:var(--primary); margin-bottom: 5px;'> Anuncios Semanales</h1>
            <div style="width: 80px; height: 4px; background: var(--secondary); margin: 0 auto 20px auto; border-radius: 2px;"></div>
            <p style='color:#64748b; font-size: 1.2rem; font-family: "Montserrat", sans-serif;'>
                Mantente informado sobre nuestras actividades y eventos especiales.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # SECCIÓN: ANUNCIOS RECIENTES
    # ============================================
    st.markdown(f"""
    <div style="
        background: white; 
        padding: 40px; 
        border-radius: 25px; 
        border-top: 5px solid var(--secondary);
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        margin-bottom: 50px;
        text-align: center;
    ">
        <h3 style="color:var(--primary); font-family: 'Playfair Display'; font-size: 2rem; margin-bottom: 20px;">
             Noticias de la Semana
        </h3>
        <div style="padding: 30px; background: #f8fafc; border-radius: 20px; border: 1px dashed #cbd5e1;">
            <p style="color: #64748b; font-size: 1.1rem; margin: 0; font-family: 'Montserrat';">
                Esta semana no hay anuncios especiales.<br>
                <span style="color: var(--secondary); font-weight: bold; letter-spacing: 1px;">¡MANTENTE ATENTO PARA PRÓXIMOS ANUNCIOS!</span>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # LÓGICA DE IMÁGENES (FUNCIONALIDAD INTACTA)
    # ============================================
    try:
        import base64
        import os
        import urllib.parse
        from PIL import Image
        
        # Función para convertir imagen a base64 (Mantenida exactamente igual)
        def image_to_base64(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            except:
                return None
        
        # Cargar imágenes buscando en múltiples rutas (Mantenida exactamente igual)
        img_musica_base64 = None
        img_danza_base64 = None
        
        # Buscar imagen de música (f15.jpeg)
        for ruta in ['f15.jpeg', './f15.jpeg', 'images/f15.jpeg', 'static/f15.jpeg', 'assets/f15.jpeg']:
            if os.path.exists(ruta):
                img_musica_base64 = image_to_base64(ruta)
                break
        
        # Buscar imagen de danza (f16.jpeg)  
        for ruta in ['f16.jpeg', './f16.jpeg', 'images/f16.jpeg', 'static/f16.jpeg', 'assets/f16.jpeg']:

            if os.path.exists(ruta):

                img_danza_base64 = image_to_base64(ruta)

                break
                
    except Exception as e:
        img_musica_base64 = None
        img_danza_base64 = None

    # ============================================
    # ACTIVIDADES REGULARES: MÚSICA
    # ============================================
    
    st.markdown(f"<h2 style='color:var(--primary); font-family: \"Playfair Display\"; margin-bottom: 25px;'> Ministerio de Música</h2>", unsafe_allow_html=True)
    
    # Mostrar imagen de música si existe
    if img_musica_base64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/jpeg;base64,{img_musica_base64}" 
                 style="width: 100%; max-height: 450px; border-radius: 25px; object-fit: cover; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px; background: #f1f5f9; padding: 60px; border-radius: 25px; border: 2px dashed #cbd5e1;">
            <p style="color: #94a3b8; font-size: 1.2rem;">Capturando la esencia de la adoración...</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detalles Música en Columnas
    col_musica1, col_musica2, col_musica3 = st.columns(3)
    
    with col_musica1:
        st.markdown(f"""
        <div style="background: white; text-align: center; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 4px solid var(--primary);">
            <h4 style="color: var(--primary); margin: 0 0 10px 0; font-family: 'Playfair Display';">📅 Días</h4>
            <p style="color: #64748b; margin: 0; font-weight: bold; font-family: 'Montserrat';">Martes y Jueves</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_musica2:
        st.markdown(f"""
        <div style="background: white; text-align: center; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 4px solid var(--primary);">
            <h4 style="color: var(--primary); margin: 0 0 10px 0; font-family: 'Playfair Display';">⏰ Hora</h4>
            <p style="color: #64748b; margin: 0; font-weight: bold; font-family: 'Montserrat';">6:30 PM</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_musica3:
        st.markdown(f"""
        <div style="background: white; text-align: center; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 4px solid var(--primary);">
            <h4 style="color: var(--primary); margin: 0 0 10px 0; font-family: 'Playfair Display';">📞 Contacto</h4>
            <p style="color: #64748b; margin: 0; font-weight: bold; font-family: 'Montserrat';">68460049</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Info Adicional Música
    st.markdown("""
    <div style="background: rgba(30, 58, 138, 0.03); padding: 30px; border-radius: 20px; margin-top: 25px; border-left: 5px solid var(--primary);">
        <p style="color: #334155; margin: 0; line-height: 1.8; font-family: 'Montserrat'; font-size: 1rem;">
            <strong style="color:var(--primary);">¿Qué hacemos?</strong> Ensayamos canciones para los cultos, preparamos 
            alabanza especial y desarrollamos talentos musicales para servir a Dios.
        </p>
        <p style="color: #334155; margin: 15px 0 0 0; line-height: 1.8; font-family: 'Montserrat'; font-size: 1rem;">
            <strong style="color:var(--primary);">Dirigido a:</strong> Miembros del equipo de alabanza y personas con 
            talento musical que quieran servir.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    # ============================================
    # ACTIVIDADES REGULARES: DANZA
    # ============================================
    
    st.markdown(f"<h2 style='color:var(--secondary); font-family: \"Playfair Display\"; margin-bottom: 25px;'> Panderos y Danza</h2>", unsafe_allow_html=True)
    
    if img_danza_base64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/jpeg;base64,{img_danza_base64}" 
                 style="width: 100%; max-height: 450px; border-radius: 25px; object-fit: cover; box-shadow: 0 10px 30px rgba(0,0,0,0.15);">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px; background: #fdfaf1; padding: 60px; border-radius: 25px; border: 2px dashed #f5e6b3;">
            <p style="color: #d4af37; font-size: 1.2rem;">Arte en movimiento para Su gloria...</p>
        </div>
        """, unsafe_allow_html=True)
    
    col_danza1, col_danza2, col_danza3 = st.columns(3)
    
    with col_danza1:
        st.markdown(f"""
        <div style="background: white; text-align: center; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 4px solid var(--secondary);">
            <h4 style="color: var(--primary); margin: 0 0 10px 0; font-family: 'Playfair Display';">📅 Día</h4>
            <p style="color: #64748b; margin: 0; font-weight: bold; font-family: 'Montserrat';">Viernes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_danza2:
        st.markdown(f"""
        <div style="background: white; text-align: center; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 4px solid var(--secondary);">
            <h4 style="color: var(--primary); margin: 0 0 10px 0; font-family: 'Playfair Display';">⏰ Hora</h4>
            <p style="color: #64748b; margin: 0; font-weight: bold; font-family: 'Montserrat';">6:30 PM</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_danza3:
        st.markdown(f"""
        <div style="background: white; text-align: center; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 4px solid var(--secondary);">
            <h4 style="color: var(--primary); margin: 0 0 10px 0; font-family: 'Playfair Display';">📞 Contacto</h4>
            <p style="color: #64748b; margin: 0; font-weight: bold; font-family: 'Montserrat';">67553113</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(212, 175, 55, 0.05); padding: 30px; border-radius: 20px; margin-top: 25px; border-left: 5px solid var(--secondary);">
        <p style="color: #334155; margin: 0; line-height: 1.8; font-family: 'Montserrat'; font-size: 1rem;">
            <strong style="color:var(--secondary);">¿Qué hacemos?</strong> Aprendemos a usar el pandero para la alabanza y 
            desarrollamos danzas litúrgicas para adorar a Dios con todo nuestro ser.
        </p>
        <p style="color: #334155; margin: 15px 0 0 0; line-height: 1.8; font-family: 'Montserrat'; font-size: 1rem;">
            <strong style="color:var(--secondary);">Dirigido a:</strong> Jóvenes y adultos interesados en la alabanza con 
            panderos y danza. No se necesita experiencia previa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # SECCIÓN: CONTACTOS DIRECTOS (WHATSAPP)
    # ============================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:var(--primary); font-family: \"Playfair Display\"; text-align: center; margin-bottom: 30px;'>📲 Escríbenos directamente</h3>", unsafe_allow_html=True)
    
    col_wp1, col_wp2 = st.columns(2)
    
    with col_wp1:
        mensaje_musica = "Hola, me interesa el ensayo de música. ¿Me podrían dar más información?"
        mensaje_musica_cod = urllib.parse.quote(mensaje_musica)
        whatsapp_musica = f"https://wa.me/59168460049?text={mensaje_musica_cod}"
        
        st.markdown(f"""
        <div style="background: var(--dark); padding: 35px; border-radius: 25px; text-align: center; border: 1px solid var(--primary);">
            <h4 style="color: white; font-family: 'Playfair Display'; margin-bottom: 10px;">Líder de Música</h4>
            <p style="color: #94a3b8; margin-bottom: 20px; font-family: 'Montserrat'; font-size: 0.9rem;">Para ensayos y audiciones</p>
            <a href="{whatsapp_musica}" target="_blank" style="text-decoration: none;">
                <div style="background: #25D366; color: white; padding: 15px; border-radius: 15px; font-weight: bold; font-family: 'Montserrat'; transition: 0.3s;">
                    HABLAR POR WHATSAPP
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col_wp2:
        mensaje_danza = "Hola, me interesa la clase de panderos y danza. ¿Me podrían dar más información?"
        mensaje_danza_cod = urllib.parse.quote(mensaje_danza)
        whatsapp_danza = f"https://wa.me/59167553113?text={mensaje_danza_cod}"
        
        st.markdown(f"""
        <div style="background: var(--dark); padding: 35px; border-radius: 25px; text-align: center; border: 1px solid var(--secondary);">
            <h4 style="color: white; font-family: 'Playfair Display'; margin-bottom: 10px;">Líder de Danza</h4>
            <p style="color: #94a3b8; margin-bottom: 20px; font-family: 'Montserrat'; font-size: 0.9rem;">Para clases y panderos</p>
            <a href="{whatsapp_danza}" target="_blank" style="text-decoration: none;">
                <div style="background: #25D366; color: white; padding: 15px; border-radius: 15px; font-weight: bold; font-family: 'Montserrat'; transition: 0.3s;">
                    HABLAR POR WHATSAPP
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # RESUMEN Y VERSÍCULO FINAL
    # ============================================
    st.markdown("<br><hr style='border-color: #e2e8f0;'><br>", unsafe_allow_html=True)
    
    col_resumen1, col_resumen2 = st.columns(2)
    with col_resumen1:
        st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; border-right: 4px solid var(--primary); text-align: right;">
                <strong style="color: var(--primary);">Ensayo de Música</strong><br>
                <span style="color: #64748b;">Mar y Jue 6:30 PM</span>
            </div>
        """, unsafe_allow_html=True)
    with col_resumen2:
        st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 15px; border-left: 4px solid var(--secondary); text-align: left;">
                <strong style="color: var(--secondary);">Panderos y Danza</strong><br>
                <span style="color: #64748b;">Vie 6:30 PM</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 40px; background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%); border-radius: 30px; border: 1px solid #e2e8f0;">
        <p style="color: #64748b; font-size: 1.1rem; font-style: italic; font-family: 'Playfair Display'; margin: 0;">
            "Canten a Dios con gratitud en el corazón."
        </p>
        <p style="color: var(--secondary); font-weight: bold; margin-top: 10px; font-family: 'Montserrat';">
            — COLOSENSES 3:16 —
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Aviso:** Durante días feriados, los horarios pueden variar. Te recomendamos seguir nuestras redes sociales para anuncios de último minuto.")


# ============================================================================
# PÁGINA: UBICACIÓN - DISEÑO FINAL CON IMAGEN BAJO EL BOTÓN
# ============================================================================

elif st.session_state.page == 'Ubicacion':
    scroll_to_top()
    # 1. Procesamiento de imagen f17.jpeg para la tarjeta
    import base64
    import os

    def get_base64_img(path):
        try:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return None
        except:
            return None

    img_f17_base64 = get_base64_img("f17.jpeg")
    
    # 2. Encabezado Premium
    st.markdown(f"""
        <div style="text-align:center; padding: 20px 0 20px 0;">
            <h1 style='font-size:3.8rem; color:#1E3A8A; margin-bottom: 5px; font-family: "Playfair Display";'>¿Dónde estamos ubicados?</h1>
            <div style="width: 80px; height: 4px; background: #D4AF37; margin: 0 auto 20px auto; border-radius: 2px;"></div>
            <p style='color:#64748b; font-size: 1.2rem; font-family: "Montserrat", sans-serif;'>
                Te esperamos en nuestra casa de oración
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 3. IMAGEN PRINCIPAL (Lugar.jpeg) - TODO EL ANCHO
    try:
        st.image("Lugar.jpeg", use_container_width=True)
    except:
        st.info("Imagen de la fachada no disponible.")

    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # 4. FILA DE DETALLES: DIRECCIÓN Y NUESTRO INTERIOR
    col_info, col_interior = st.columns([1, 1], gap="large")
    
    with col_info:
        # Generamos el HTML de la imagen f17.jpeg si existe
        f17_html = f"""
        <div style="margin-top: 25px; text-align: center;">
            <img src="data:image/jpeg;base64,{img_f17_base64}" 
                 style="width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); object-fit: cover;">
        </div>
        """ if img_f17_base64 else ""

        # Bloque de Dirección Exacta: Título -> Dirección -> Botón -> Imagen f17
        info_html = f"""
        <div class="glass-card" style="padding: 30px; border-left: 5px solid #D4AF37; background: #ffffff; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
            <h3 style="color:#D4AF37; margin-top: 0; font-family: 'Playfair Display'; font-size: 1.5rem;">📍 Dirección Exacta</h3>
            
            <div style="margin: 20px 0;">
                <p style="font-size: 1.3rem; color: #1E3A8A; font-weight: bold; line-height: 1.4; font-family: 'Montserrat';">
                    Calle Fortín Vanguardia #740<br>
                    <span style="color: #64748b; font-size: 1.1rem; font-weight: normal;">Cochabamba, Bolivia</span>
                </p>
            </div>
            
            <div style="margin-top: 30px;">
                <a href="http://googleusercontent.com/maps.google.com/4" target="_blank" style="text-decoration: none;">
                    <button style="background: #1E3A8A; color: white; border: none; padding: 18px 32px; 
                            border-radius: 12px; width: 100%; cursor: pointer; font-weight: bold; 
                            font-size: 1.1rem; transition: all 0.3s; font-family: 'Montserrat';
                            box-shadow: 0 5px 15px rgba(30, 58, 138, 0.25); text-transform: uppercase; letter-spacing: 1px;">
                        ABRIR EN GOOGLE MAPS
                    </button>
                </a>
            </div>

            {f17_html}
        </div>
        """
        # Ajustamos height a 650 para que el botón e imagen quepan sin scroll
        st.components.v1.html(info_html, height=650)

    with col_interior:
        
        try:
            st.image("Lugar1.jpeg", use_container_width=True, caption="Auditorio Principal")
        except:
            st.warning("Foto del interior no disponible.")

    # 5. Footer
    st.markdown("<hr style='margin: 40px 0; border-color: #e2e8f0; opacity: 0.6;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-family: 'Montserrat'; padding-bottom: 40px;">
        <p style="font-size: 1.1rem; color: #1E3A8A;"><strong>Horario de atención:</strong> Lunes a Domingo</p>
        <p style="font-size: 0.9rem; margin-top: 5px;">¡Las puertas están abiertas para ti y tu familia!</p>
    </div>
    """, unsafe_allow_html=True)
# ============================================================================
# PÁGINA: REDES SOCIALES - ACTUALIZADA CON INSTAGRAM Y FACEBOOK
# ============================================================================

elif st.session_state.page == 'Redes':
    scroll_to_top()    
    # Título principal de la página
    st.markdown("""
        <div style="text-align:center; padding: 20px 0 40px 0;">
            <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>Nuestra Comunidad Digital</h1>
            <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
            <p style='color:#64748b; font-size: 1.2rem; font-family: "Montserrat"; max-width: 800px; margin: 0 auto;'>
                Conéctate con nosotros y mantente al día con lo que Dios está haciendo en nuestra iglesia.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 3. SECCIÓN 1: YOUTUBE (Videos con estilo de galería)
    st.markdown("<h2 style='color:#1E3A8A; font-family: \"Playfair Display\"; margin-bottom: 30px; border-left: 5px solid #CC0000; padding-left: 15px;'>Videos de YouTube</h2>", unsafe_allow_html=True)
    

    
    # Crear 2 columnas para los videos de YouTube
    col_yt1, col_yt2 = st.columns(2)
    
    with col_yt1:
        # Primer video de YouTube
        video1_html = """
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 20px;">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px;">
                <iframe src="https://www.youtube.com/embed/Btp8NR7CVPg" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                </iframe>
            </div>
            <div style="margin-top: 15px;">
                <h4 style="color: #1E3A8A; margin-bottom: 5px;">Cuál eliges? A Dios o el mundo</h4>
                <p style="color: #64748b; font-size: 0.9rem;">Un mensaje poderoso sobre la decisión más importante de tu vida</p>
            </div>
            <div style="text-align: center; margin-top: 15px;">
                <a href="https://youtu.be/Btp8NR7CVPg?si=JktqQAGPuFgFlGi-" target="_blank" style="text-decoration: none;">
                    <button style="background: #CC0000; color: white; border: none; padding: 10px 25px; 
                            border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 0.95rem; width: 100%;">
                        Ver este video
                    </button>
                </a>
            </div>
        </div>
        """
        st.markdown(video1_html, unsafe_allow_html=True)
    
    with col_yt2:
        # Segundo video de YouTube
        video2_html = """
        <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 20px;">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px;">
                <iframe src="https://www.youtube.com/embed/56rP9fAy7Wo" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                </iframe>
            </div>
            <div style="margin-top: 15px;">
                <h4 style="color: #1E3A8A; margin-bottom: 5px;">Video de la Iglesia</h4>
                <p style="color: #64748b; font-size: 0.9rem;">Contenido especial de nuestra comunidad de fe</p>
            </div>
            <div style="text-align: center; margin-top: 15px;">
                <a href="https://youtu.be/56rP9fAy7Wo?si=sRF6rXMgY9kWukUN" target="_blank" style="text-decoration: none;">
                    <button style="background: #CC0000; color: white; border: none; padding: 10px 25px; 
                            border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 0.95rem; width: 100%;">
                        Ver este video
                    </button>
                </a>
            </div>
        </div>
        """
        st.markdown(video2_html, unsafe_allow_html=True)
    
    # Línea divisoria
    st.markdown("<hr style='margin: 30px 0; border-color: #e0e0e0;'>", unsafe_allow_html=True)
    
    # SECCIÓN 2: NUESTRAS REDES SOCIALES (AHORA 4 REDES)
    st.markdown("<h2 style='color: var(--primary); font-family: #D4AF37; margin-bottom: 30px; border-left: 5px solid #D4AF37; padding-left: 15px;'>Nuestras Redes Sociales</h2>", unsafe_allow_html=True)
    
    # Función para cargar imágenes como base64
    def cargar_logo_base64(nombre_archivo):
        """Carga una imagen y la convierte a base64"""
        try:
            # Buscar el archivo en diferentes ubicaciones
            posibles_rutas = [
                nombre_archivo,
                f'./{nombre_archivo}',
                f'images/{nombre_archivo}',
                f'static/{nombre_archivo}',
                f'assets/{nombre_archivo}'
            ]
            
            for ruta in posibles_rutas:
                if os.path.exists(ruta):
                    with open(ruta, "rb") as img_file:
                        import base64
                        return base64.b64encode(img_file.read()).decode()
            return None
        except:
            return None
    
    # Cargar logos
    logo_youtube = cargar_logo_base64("youtube.jpeg")
    logo_tiktok = cargar_logo_base64("tiktok.jpeg")
    logo_instagram = cargar_logo_base64("insta.jpeg")
    logo_facebook = cargar_logo_base64("face.jpeg")
    
    # Tarjetas de redes sociales en 4 columnas (2 filas de 2)
    # Primera fila: YouTube y TikTok
    col_fila1_1, col_fila1_2 = st.columns(2)
    
    with col_fila1_1:
        # Tarjeta de YouTube ACTUALIZADA
        youtube_html = """
        <div class="glass-card" style="text-align: center; margin-bottom: 20px; border-top: 5px solid #CC0000; height: 320px; display: flex; flex-direction: column;">
            <div style="margin-bottom: 15px; flex: 0 0 auto;">
        """
        
        if logo_youtube:
            youtube_html += f'<img src="data:image/jpeg;base64,{logo_youtube}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 50%; margin-bottom: 10px;">'
        else:
            youtube_html += """
            <div style="width: 80px; height: 80px; background: #CC0000; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto;">
                <span style="color: white; font-size: 2rem; font-weight: bold;">YT</span>
            </div>
            """
        
        youtube_html += """
                <h3 style="color: #CC0000; margin-bottom: 5px;">YouTube</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 5px;">@IENADRestauracion</p>
            </div>
            <div style="flex: 1 1 auto; margin-bottom: 15px;">
                <p style="color: #555; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                    Mira nuestras prédicas en vivo, conferencias y testimonios completos.
                </p>
            </div>
            <div style="flex: 0 0 auto;">
                <a href="https://www.youtube.com/@IENADRestauracion" target="_blank" style="text-decoration: none;">
                    <button style="background: #CC0000; color: white; border: none; padding: 10px 25px; 
                            border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 0.9rem; width: 100%;">
                        Seguir en YouTube
                    </button>
                </a>
            </div>
        </div>
        """
        st.markdown(youtube_html, unsafe_allow_html=True)
    
    with col_fila1_2:
        # Tarjeta de TikTok
        tiktok_html = """
        <div class="glass-card" style="text-align: center; margin-bottom: 20px; border-top: 5px solid #000000; height: 320px; display: flex; flex-direction: column;">
            <div style="margin-bottom: 15px; flex: 0 0 auto;">
        """
        
        if logo_tiktok:
            tiktok_html += f'<img src="data:image/jpeg;base64,{logo_tiktok}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 50%; margin-bottom: 10px;">'
        else:
            tiktok_html += """
            <div style="width: 80px; height: 80px; background: #000000; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto;">
                <span style="color: white; font-size: 2rem; font-weight: bold;">TT</span>
            </div>
            """
        
        tiktok_html += """
                <h3 style="color: #000000; margin-bottom: 5px;">TikTok</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 5px;">@lglesia_restauracion</p>
            </div>
            <div style="flex: 1 1 auto; margin-bottom: 15px;">
                <p style="color: #555; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                    Mensajes cortos de fe y momentos inspiradores de nuestra comunidad.
                </p>
            </div>
            <div style="flex: 0 0 auto;">
                <a href="https://www.tiktok.com/@lglesia_restauracion" target="_blank" style="text-decoration: none;">
                    <button style="background: #000000; color: white; border: none; padding: 10px 25px; 
                            border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 0.9rem; width: 100%;">
                        Seguir en TikTok
                    </button>
                </a>
            </div>
        </div>
        """
        st.markdown(tiktok_html, unsafe_allow_html=True)
    
    # Segunda fila: Instagram y Facebook
    col_fila2_1, col_fila2_2 = st.columns(2)
    
    with col_fila2_1:
        # Tarjeta de Instagram NUEVA
        instagram_html = """
        <div class="glass-card" style="text-align: center; margin-bottom: 20px; border-top: 5px solid #E4405F; height: 320px; display: flex; flex-direction: column;">
            <div style="margin-bottom: 15px; flex: 0 0 auto;">
        """
        
        if logo_instagram:
            instagram_html += f'<img src="data:image/jpeg;base64,{logo_instagram}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 50%; margin-bottom: 10px;">'
        else:
            instagram_html += """
            <div style="width: 80px; height: 80px; background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto;">
                <span style="color: white; font-size: 2rem; font-weight: bold;">IG</span>
            </div>
            """
        
        instagram_html += """
                <h3 style="color: #E4405F; margin-bottom: 5px;">Instagram</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 5px;">@iglesia.restauracion.one</p>
            </div>
            <div style="flex: 1 1 auto; margin-bottom: 15px;">
                <p style="color: #555; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                    Fotos, historias y momentos especiales de nuestra comunidad de fe.
                </p>
            </div>
            <div style="flex: 0 0 auto;">
                <a href="https://www.instagram.com/iglesia.restauracion.one?utm_source=qr&igsh=MXhseTU3M2g4NGs1dQ==" target="_blank" style="text-decoration: none;">
                    <button style="background: linear-gradient(45deg, #405DE6, #833AB4, #E1306C); color: white; border: none; padding: 10px 25px; 
                            border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 0.9rem; width: 100%;">
                        Seguir en Instagram
                    </button>
                </a>
            </div>
        </div>
        """
        st.markdown(instagram_html, unsafe_allow_html=True)
    
    with col_fila2_2:
        # Tarjeta de Facebook NUEVA
        facebook_html = """
        <div class="glass-card" style="text-align: center; margin-bottom: 20px; border-top: 5px solid #1877F2; height: 320px; display: flex; flex-direction: column;">
            <div style="margin-bottom: 15px; flex: 0 0 auto;">
        """
        
        if logo_facebook:
            facebook_html += f'<img src="data:image/jpeg;base64,{logo_facebook}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 50%; margin-bottom: 10px;">'
        else:
            facebook_html += """
            <div style="width: 80px; height: 80px; background: #1877F2; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto;">
                <span style="color: white; font-size: 2rem; font-weight: bold;">FB</span>
            </div>
            """
        
        facebook_html += """
                <h3 style="color: #1877F2; margin-bottom: 5px;">Facebook</h3>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 5px;">Iglesia Restauración</p>
            </div>
            <div style="flex: 1 1 auto; margin-bottom: 15px;">
                <p style="color: #555; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                    Eventos, noticias y comunidad en la red social más grande del mundo.
                </p>
            </div>
            <div style="flex: 0 0 auto;">
                <a href="https://www.facebook.com/profile.php?id=61585513010853" target="_blank" style="text-decoration: none;">
                    <button style="background: #1877F2; color: white; border: none; padding: 10px 25px; 
                            border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 0.9rem; width: 100%;">
                        Seguir en Facebook
                    </button>
                </a>
            </div>
        </div>
        """
        st.markdown(facebook_html, unsafe_allow_html=True)
    
    # Línea divisoria
    st.markdown("<hr style='margin: 40px 0; border-color: #e0e0e0;'>", unsafe_allow_html=True)
    
    # SECCIÓN 3: VIDEOS DE TIKTOK
    st.markdown("<h2 style='color: var(--primary); font-family: #D4AF37; margin-bottom: 30px; border-left: 5px solid var(--dark); padding-left: 15px;'>Videos de Tik Tok</h2>", unsafe_allow_html=True)
    
    # Videos de TikTok
    videos_tiktok = [
        {
            "titulo": "Mensaje de Fe",
            "descripcion": "Reflexión poderosa para tu caminar diario",
            "link": "https://www.tiktok.com/@lglesia_restauracion/video/7459193845733952773",
            "archivos": ["t1.jpeg", "T1.jpeg", "t1.jpg", "T1.jpg", "video1.jpeg", "tiktok1.jpeg"]
        },
        {
            "titulo": "Palabra de Vida", 
            "descripcion": "Versículo bíblico con aplicación práctica",
            "link": "https://www.tiktok.com/@lglesia_restauracion/video/7442934341178641719",
            "archivos": ["t2.jpeg", "T2.jpeg", "t2.jpg", "T2.jpg", "video2.jpeg", "tiktok2.jpeg"]
        },
        {
            "titulo": "Momento de Alabanza",
            "descripcion": "Adoración en comunidad",
            "link": "https://www.tiktok.com/@lglesia_restauracion/video/7445472009431026950",
            "archivos": ["t3.jpeg", "T3.jpeg", "t3.jpg", "T3.jpg", "video3.jpeg", "tiktok3.jpeg"]
        }
    ]
    
    # Mostrar videos en 3 columnas
    col_vid1, col_vid2, col_vid3 = st.columns(3)
    
    for i, video in enumerate(videos_tiktok):
        with [col_vid1, col_vid2, col_vid3][i]:
            with st.container():
                imagen_encontrada = False
                
                # Intentar cargar diferentes nombres de archivo
                for archivo in video["archivos"]:
                    try:
                        # Intentar cargar la imagen con PIL
                        img = Image.open(archivo)
                        # Redimensionar para consistencia
                        img = img.resize((300, 200), Image.Resampling.LANCZOS)
                        
                        # Mostrar la imagen
                        st.image(img, width=300, caption="", use_container_width="auto")
                        imagen_encontrada = True
                        break
                    except:
                        continue
                
                # Si no se encontró ninguna imagen
                if not imagen_encontrada:
                    placeholder_html = f"""
                    <div style="height: 200px; background: linear-gradient(135deg, #1E3A8A 0%, #000000 100%); 
                         border-radius: 10px; display: flex; align-items: center; justify-content: center; 
                         margin-bottom: 15px; flex-direction: column;">
                        <span style="color: white; font-size: 2.5rem; margin-bottom: 10px;">▶️</span>
                        <span style="color: rgba(255,255,255,0.8); font-size: 0.8rem;">{video['titulo']}</span>
                    </div>
                    """
                    st.markdown(placeholder_html, unsafe_allow_html=True)
                
                # Título y descripción
                st.markdown(f"<h4 style='color: #1E3A8A; margin-bottom: 8px; margin-top: 10px;'>{video['titulo']}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #64748b; font-size: 0.9rem; margin-bottom: 15px;'>{video['descripcion']}</p>", unsafe_allow_html=True)
                
                # Botón usando st.link_button
                st.link_button("▶ Ver en TikTok", video['link'], type="secondary", use_container_width=True)
    
    # Nota informativa sobre TikTok
    st.markdown("""
    <div style="background: #f8fafc; padding: 15px; border-radius: 10px; margin-top: 30px; text-align: center;">
        <p style="color: #64748b; font-size: 0.9rem; margin: 0;">
            Haz clic en "Ver en TikTok" para ver nuestros videos completos. Necesitarás tener la aplicación de TikTok instalada.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para ver más en TikTok
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <a href="https://www.tiktok.com/@lglesia_restauracion" target="_blank" style="text-decoration: none;">
            <button style="background: linear-gradient(to right, #000, #333); color: white; border: none; 
                    padding: 14px 40px; border-radius: 25px; cursor: pointer; font-weight: bold; font-size: 1.1rem;">
                Visitar Perfil Completo de TikTok
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # SECCIÓN ADICIONAL: Enlaces a todas las redes
    st.markdown("<hr style='margin: 40px 0; border-color: #e0e0e0;'>", unsafe_allow_html=True)
    
    # SECCIÓN ADICIONAL: Enlaces a todas las redes (VERSIÓN CORREGIDA)
    st.markdown("<hr style='margin: 40px 0; border-color: #e0e0e0;'>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: linear-gradient(135deg, var(--dark) 0%, #0f2461 100%); padding: 40px; border-radius: 25px; text-align: center; color: white;">
            <h3 style="font-family: 'Playfair Display'; margin-bottom: 10px;">🌐 Nuestra Red de Enlaces</h3>
            <p style="font-family: 'Montserrat'; opacity: 0.8; margin-bottom: 30px;">Todo nuestro contenido en un solo lugar</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; max-width: 900px; margin: 0 auto;">
                <a href="https://www.youtube.com/@IENADRestauracion" target="_blank" style="text-decoration: none; color: white; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; font-weight: bold; border: 1px solid rgba(255,255,255,0.2);" class="btn-hover">YOUTUBE</a>
                <a href="https://www.tiktok.com/@lglesia_restauracion" target="_blank" style="text-decoration: none; color: white; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; font-weight: bold; border: 1px solid rgba(255,255,255,0.2);" class="btn-hover">TIKTOK</a>
                <a href="https://www.instagram.com/iglesia.restauracion.one" target="_blank" style="text-decoration: none; color: white; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; font-weight: bold; border: 1px solid rgba(255,255,255,0.2);" class="btn-hover">INSTAGRAM</a>
                <a href="https://www.facebook.com/profile.php?id=61585513010853" target="_blank" style="text-decoration: none; color: white; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 12px; font-weight: bold; border: 1px solid rgba(255,255,255,0.2);" class="btn-hover">FACEBOOK</a>
            </div>
            
        </div>
        <br><br>
    """, unsafe_allow_html=True)

    # Mensaje final
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="color: #64748b; font-size: 0.9rem; margin: 0;">
            ¡Síguenos en todas nuestras redes para no perderte nada!
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PÁGINA: ORACIÓN - DISEÑO PREMIUM DARK (CORREGIDO)
# ============================================================================

elif st.session_state.page == 'Oracion':
    scroll_to_top()
    # 1. Título de la Página (Tu diseño actual centrado)
    st.markdown("""
        <div style="text-align:center; padding: 20px 0 40px 0;">
            <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>Petición de Oración</h1>
            <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
            <p style='color:#64748b; font-size: 1.2rem; font-family: "Montserrat"; max-width: 800px; margin: 0 auto;'>
                Comparte tus necesidades espirituales. La Iglesia orará personalmente por ti.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Contenedor de instrucciones
    st.markdown("""
        <div style="background: var(--dark, #0e1117); 
                    padding: 25px; 
                    border-radius: 15px; 
                    border: 1px solid #333;
                    margin-bottom: 30px;">
            <h4 style="color: #D4AF37; margin-top: 0; margin-bottom: 15px;">¿Cómo funciona?</h4>
            <p style="color: #bbb; margin-bottom: 8px;">1. <b>Completa el formulario</b> con tus datos y necesidad.</p>
            <p style="color: #bbb; margin-bottom: 8px;">2. <b>Genera el mensaje</b> haciendo clic en el botón inferior.</p>
            <p style="color: #bbb; margin-bottom: 8px;">3. <b>Envía por WhatsApp</b> el texto que hemos preparado para ti.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 3. Formulario
    with st.form("peticion_oracion_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<label style='color: var(--dark, #1E3A8A); font-weight: bold;'>Tu nombre completo</label>", unsafe_allow_html=True)
            nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Ej: María González")
        
        with col2:
            st.markdown("<label style='color: var(--dark, #1E3A8A); font-weight: bold;'>Tu número de WhatsApp</label>", unsafe_allow_html=True)
            telefono = st.text_input("Teléfono", label_visibility="collapsed", placeholder="Ej: 59171234567")
    
        st.markdown("<br><label style='color: var(--dark, #1E3A8A); font-weight: bold;'>Tu petición de oración</label>", unsafe_allow_html=True)
        peticion = st.text_area("Petición", label_visibility="collapsed", placeholder="Describe tu necesidad específica...", height=120)
        
        # Estilo CSS para el botón (Dark con letras doradas)
        st.markdown("""
            <style>
            div[data-testid="stForm"] button[kind="primary"] {
                background-color: var(--dark, #1E3A8A) !important;
                color: #D4AF37 !important;
                border: 2px solid #D4AF37 !important;
                border-radius: 10px !important;
                padding: 0.5rem 1rem !important;
                transition: all 0.3s ease !important;
                font-weight: bold !important;
            }
            div[data-testid="stForm"] button[kind="primary"]:hover {
                background-color: #D4AF37 !important;
                color: var(--dark, #1E3A8A) !important;
            }
            </style>
        """, unsafe_allow_html=True)

        submit = st.form_submit_button("ENVIAR PETICIÓN", use_container_width=True, type="primary")

        # ============================================================
        # LÓGICA DE PROCESAMIENTO Y GUARDADO (CORREGIDA)
        # ============================================================
        if submit:
            if nombre and telefono and peticion:
                try:
                    import datetime, urllib.parse, json, os
                    now = datetime.datetime.now()
                    fecha_f = now.strftime("%d/%m/%Y %H:%M")
                    
                    # 1. Preparar el diccionario de datos
                    prayer_data = {
                        "id": now.strftime("%Y%m%d%H%M%S"),
                        "nombre": nombre,
                        "telefono": telefono,
                        "peticion": peticion,
                        "fecha": fecha_f
                    }
                    
                    # 2. Lógica de guardado en JSON
                    json_file = 'peticiones_oracion.json'
                    peticiones_list = []

                    # Si el archivo ya existe, leemos lo que tiene
                    if os.path.exists(json_file):
                        with open(json_file, 'r', encoding='utf-8') as f:
                            try:
                                peticiones_list = json.load(f)
                            except json.JSONDecodeError:
                                peticiones_list = [] # Por si el archivo está vacío o corrupto

                    # Añadimos la nueva petición a la lista
                    peticiones_list.append(prayer_data)

                    # Guardamos la lista actualizada
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(peticiones_list, f, indent=4, ensure_ascii=False)
                    
                    # 3. Crear mensaje y enlace de WhatsApp
                    msg = f"*NUEVA PETICIÓN DE ORACIÓN*\n\n*Nombre:* {nombre}\n*WhatsApp:* {telefono}\n*Fecha:* {fecha_f}\n\n*Petición:*\n{peticion}"
                    whatsapp_url = f"https://wa.me/59167435065?text={urllib.parse.quote(msg)}"
                    
                    # 4. Mostrar confirmación profesional (Texto corregido para visibilidad)
                    st.markdown(f"""
                        <div style="background: rgba(37, 211, 102, 0.1); 
                                    border: 1px solid #25D366; 
                                    padding: 25px; 
                                    border-radius: 15px; 
                                    text-align: center; 
                                    margin-top: 20px;">
                            <h4 style="color: #25D366; margin-bottom: 10px;">¡Petición Registrada !</h4>
                            <p style="color: var(--dark); margin-bottom: 20px; font-style: italic;">
                                "Prioriza tu solicitud: Conexión directa con nuestro equipo de oración."
                            </p>
                            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                                <div style="background: #25D366; 
                                            color: white; 
                                            padding: 15px 30px; 
                                            border-radius: 10px; 
                                            font-weight: bold; 
                                            display: inline-block;
                                            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);">
                                    🟢 ENVIAR AHORA POR WHATSAPP
                                </div>
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    
                except Exception as e:
                    st.markdown(f"""
                        <div style="background-color: #fee2e2; 
                                    color: var(--dark, #1E3A8A); 
                                    padding: 15px; 
                                    border-radius: 10px; 
                                    border: 1px solid #ef4444; 
                                    font-weight: bold;
                                    text-align: center;
                                    margin-top: 15px;">
                            ❌ Hubo un error al procesar: {e}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background-color: #fef3c7; 
                                color: var(--dark, #1E3A8A); 
                                padding: 15px; 
                                border-radius: 10px; 
                                border: 1px solid #f59e0b; 
                                font-weight: bold;
                                text-align: center;
                                margin-bottom: 20px;">
                        ⚠️ Por favor, completa todos los campos del formulario.
                    </div>
                """, unsafe_allow_html=True)

    # 4. Sección informativa final
    st.markdown("""
        <div style="margin-top: 40px; background: var(--dark); padding: 30px; border-radius: 15px; border: 1px solid #333;">
            <h5 style="color: #D4AF37; text-align: center; margin-bottom: 25px; font-family: 'Playfair Display', serif;">
                Tu petición es importante
            </h5>
            <div style="display: flex; flex-wrap: wrap; justify-content: space-around; gap: 20px; text-align: center;">
                <div style="flex: 1; min-width: 150px;">
                    <div style="font-size: 25px; margin-bottom: 10px;">🙏</div>
                    <p style="color: white; font-weight: bold; margin-bottom: 5px;">Oración Personal</p>
                    <p style="color: #888; font-size: 0.85rem;">Atención individual y ruego específico.</p>
                </div>
                <div style="flex: 1; min-width: 150px;">
                    <div style="font-size: 25px; margin-bottom: 10px;">🔒</div>
                    <p style="color: white; font-weight: bold; margin-bottom: 5px;">Confidencialidad</p>
                    <p style="color: #888; font-size: 0.85rem;">Información tratada con total respeto.</p>
                </div>
                <div style="flex: 1; min-width: 150px;">
                    <div style="font-size: 25px; margin-bottom: 10px;">⚡</div>
                    <p style="color: white; font-weight: bold; margin-bottom: 5px;">Contacto Directo</p>
                    <p style="color: #888; font-size: 0.85rem;">Comunicación inmediata con la Pastora.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    
# ============================================================================
# PÁGINA: CONTACTOS - VERSIÓN ACTUALIZADA
# ============================================================================

elif st.session_state.page == 'Contactos':
    scroll_to_top()
    st.markdown("""
        <div style="text-align:center; padding: 20px 0 40px 0;">
            <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>Contactos Directos</h1>
            <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
            <p style='color:#64748b; font-size: 1.2rem; font-family: "Montserrat"; max-width: 800px; margin: 0 auto;'>
                Estamos aquí para servirte. No dudes en contactarnos.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Importar components para HTML
    import streamlit.components.v1 as components
    
    # Contactos principales simplificados
    contactos = [
        {
            "nombre": "Pastora Paula",
            "telefono": "+591 67435065",
            "whatsapp": "https://wa.me/59167435065"
        },
        {
            "nombre": "Pastor Boris",
            "telefono": "+591 77462108", 
            "whatsapp": "https://wa.me/59177462108"
        }
    ]
    
    # Mostrar contactos en columnas
    col1, col2 = st.columns(2)
    
    for i, contacto in enumerate(contactos):
        with [col1, col2][i]:
            # HTML completo para cada contacto
            contacto_html = f"""
            <div class="glass-card">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h3 style="color: #1E3A8A; margin: 0 0 15px 0;">{contacto['nombre']}</h3>
                </div>
                
                <div style="margin: 20px 0; text-align: center;">
                    <p style="color: #555; margin: 15px 0; font-size: 1.1rem;">
                        {contacto['telefono']}
                    </p>
                </div>
                
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <a href="{contacto['whatsapp']}" target="_blank" style="text-decoration: none; flex: 1;">
                        <button style="background: #25D366; color: white; border: none; padding: 12px; 
                                border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold;">
                            WhatsApp Directo
                        </button>
                    </a>
                </div>
            </div>
            """
            components.html(contacto_html, height=200)
    
    # Espacio entre secciones
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Grupo de WhatsApp con logo
    st.markdown("<h3 style='color:#1E3A8A; text-align: center;'>Grupo de WhatsApp de la Iglesia</h3>", unsafe_allow_html=True)
    
    # Mostrar logo de la iglesia
    try:
        col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
        with col_l2:
            st.image("LogoIglesia.jpeg", use_container_width=True)
    except:
        pass
    
    # HTML del grupo usando components.html
    # SECCIÓN DEL GRUPO DE WHATSAPP CORREGIDA
    grupo_html = """
    <div class="glass-card" style="max-width: 1000px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 20px;">
            <p style="color: #555; margin: 0;">
                Únete a nuestro grupo principal de WhatsApp para estar al día con anuncios, 
                devocionales y compartir en comunidad.
            </p>
        </div>
        
        <!-- Título "Enlace del Grupo:" CORREGIDO -->
        <div style="text-align: center; margin-bottom: 10px;">
            <h3 style="color: #1E3A8A; margin: 0 0 15px 0;">Enlace del Grupo:</h3>
        </div>
        
        <!-- Enlace en cuadro gris -->
        <div style="margin: 15px 0; text-align: center;">
            <div style="background: #f8fafc; padding: 15px; border-radius: 10px; margin: 0 0 20px 0; border: 1px solid #e0e0e0;">
                <p style="color: #555; margin: 0; word-break: break-all; font-size: 0.9rem;">
                    https://chat.whatsapp.com/KR6Av3mLAIW1JaSuZrOWvn
                </p>
            </div>
        </div>
        
        <!-- Botón para unirse -->
        <div style="display: flex; gap: 10px; margin-top: 10px;">
            <a href="https://chat.whatsapp.com/KR6Av3mLAIW1JaSuZrOWvn" target="_blank" style="text-decoration: none; flex: 1;">
                <button style="background: #25D366; color: white; border: none; padding: 15px; 
                        border-radius: 10px; width: 100%; cursor: pointer; font-weight: bold; font-size: 1rem;">
                    Unirse al Grupo
                </button>
            </a>
        </div>
    </div>
    """
    components.html(grupo_html, height=200)
    
    # Contacto de emergencia
    st.markdown("<br><br>", unsafe_allow_html=True)
    
# ============================================================================
# PÁGINA: ¿QUÉ CREEMOS? - VERSIÓN FINAL CORREGIDA
# ============================================================================

elif st.session_state.page == 'pagina_creemos':
    scroll_to_top()
    # 1. Estilo para el botón Volver (Fondo Dark / Letras Doradas)
    st.markdown("""
        <style>
        section[data-testid="stMain"] div.stButton > button {
            background-color: var(--dark, #1E3A8A) !important;
            color: #D4AF37 !important;
            border: 1px solid #D4AF37 !important;
            border-radius: 10px !important;
            font-weight: bold !important;
        }
        section[data-testid="stMain"] div.stButton > button:hover {
            background-color: #D4AF37 !important;
            color: var(--dark, #1E3A8A) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; padding: 20px 0 40px 0;">
            <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>¿Qué creemos?</h1>
            <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
            
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Botón Volver
    col_v, _ = st.columns([1, 3])
    with col_v:
        if st.button("← VOLVER AL INICIO", use_container_width=True):
            st.session_state.page = 'Inicio'
            st.rerun()

    # 3. CONTENIDO (IMPORTANTE: El HTML debe estar pegado a la izquierda del editor)
    col_izq, col_der = st.columns([2, 1])

    
        # IMPORTANTE: No dejes NINGÚN espacio antes de <div. Debe estar pegado al margen.
    with col_izq:
            # Fíjate que <div está pegado al borde izquierdo del código
            html_contenido = f"""
    <div style="background-color: var(--dark, #1E3A8A); 
                padding: 30px; 
                border-radius: 20px; 
                border: 1px solid #D4AF37;
                color: white;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
        <h3 style="color:#D4AF37; margin-top: 0; font-family: 'Playfair Display', serif; margin-bottom: 5px;">Nuestra Declaración de Fe</h3>
        <div style="height: 0.6px; background-color: #D4AF37; width: 100%; margin-bottom: 25px;"></div>
        <div style="line-height: 1.6; font-size: 1.05rem;">
            <p><b>1.</b> Creemos en un solo Dios, eterno creador del universo, subsistente en tres persona: Padre, Hijo y Espíritu Santo.</p>
            <p><b>2.</b> La palabra inspirada de Dios que es la biblia.</p>
            <p><b>3.</b> En jesucristo Dios verdadero y su encarnacion como hombre a travez de la obra del espiritu santo nacido de Maria. Jesucristo vivio sin pecado y murio en la cruz por nuestros pecados recusito corporalmente ascendio a los cielos y regresara en su segunda venida.</p>
            <p><b>4.</b> La salvacion se recibe a travez del arrepentimiento y fe en la obra de redencion de cristo; la salvacion es por gracia de Dios y no por obras.</p>
            <p><b>5.</b> El nuevo nacimiento es por obra del espiritu santo y da una nueva vida espiritual al creyente.</p>
            <p><b>6.</b> El bautismo en agua por imersion en el nombre padre hijo espiritu santo, que identifica al creyente con cristo en su muerte y nueva vida.</p>
            <p><b>7.</b> Bautismo del espiritu santo que capacita a los creyentes para una vida y servicio dotando de dones espirituales para edificacin de la iglesia.</p>
        </div>
    </div>
    """
            st.markdown(html_contenido, unsafe_allow_html=True)
        

    with col_der:
        try:
            st.image("logoIglesia.jpeg", use_container_width=True)
        except:
            st.info("IENAD Betania")

    st.markdown("<br><br>", unsafe_allow_html=True)


    
    
# ============================================================================
# PÁGINA: ACERCA DE NOSOTROS - VERSIÓN CORREGIDA (SIN CÓDIGO A LA VISTA)
# ============================================================================

# ============================================================================
# PÁGINA: ACERCA DE NOSOTROS - HISTORIA EXACTA
# ============================================================================

elif st.session_state.page == 'pagina_acerca':
    scroll_to_top()
    # 1. Estilos para botones del área principal
    st.markdown("""
        <style>
        section[data-testid="stMain"] div.stButton > button {
            background-color: var(--dark, #1E3A8A) !important;
            color: #D4AF37 !important;
            border: 1px solid #D4AF37 !important;
            border-radius: 10px !important;
            font-weight: bold !important;
        }
        section[data-testid="stMain"] div.stButton > button:hover {
            background-color: #D4AF37 !important;
            color: var(--dark, #1E3A8A) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
            <div style="text-align:center; padding: 20px 0 40px 0;">
                <h1 style='font-size:3.5rem; color:#1E3A8A; margin-bottom: 10px; font-family: "Playfair Display";'>¿Qué creemos?</h1>
                <div style="width: 100px; height: 4px; background: #D4AF37; margin: 0 auto 25px auto; border-radius: 2px;"></div>
                
            </div>
        """, unsafe_allow_html=True)    
    # 2. Botón Volver
    col_v, _ = st.columns([1, 3])
    with col_v:
        if st.button("← VOLVER AL INICIO", use_container_width=True):
            st.session_state.page = 'Inicio'
            st.rerun()

    # 3. CONTENIDO (HTML pegado al margen izquierdo para evitar errores)
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        html_acerca_fijo = f"""
<div style="background-color: var(--dark, #1E3A8A); 
            padding: 35px; 
            border-radius: 20px; 
            border: 1px solid #D4AF37;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
    <h3 style="color:#D4AF37; margin-top: 0; font-family: 'Playfair Display', serif; border-bottom: 1px solid rgba(212,175,55,0.3); padding-bottom: 10px;">
        Nuestra Historia
    </h3>
    <div style="line-height: 1.6; font-size: 0.95rem; margin-top: 20px; text-align: justify;">
        <p>Durante la pandemia del COVID 19, muchas iglesias restringieron la entrada a sus congregaciónes por el tema del contagio; el marzo del 2020. Se empezó con oraciones de intercesión por plataformas digitales como Skype, Google Meet y finalmente Zoom, estas reuniones se empezó con oración y lectura de pasajes bíblicos, posteriormente se empezó con pequeños devociónales.</p>
        <p style="margin-top: 10px;">Se llegó al año 2022, y luego de varios momentos de meditación de oración y lectura de la Biblia, se decidió tener cultos en el domicilio de la Familia Fernandez de esta manera para poder interactuar con las personas y predicar la palabra de Dios.</p>
        <p style="margin-top: 10px;">En una visita en Mayo de 2022 que se tuvo de Riberalta del pastor Demetrio Chipunavi, luego de la participación del encuentro de líderes y pastores que auspició la Fundación de educación y servicio FES. El manifestó la decisión que se pueda abrir una congregación con el respaldo de la IENAD BETANIA en Cochabamba.</p>
        <p style="margin-top: 10px;">Por esta razón se empezó con los cultos semanales en la casa. Se empezó el 3 de Julio 2022 con la participación de adolescentes que estaban en el nivel secundario de algunas unidades educativas. Pasaron los meses y poco a poco se estructuro de mejor manera las reuniones.</p>
        <p style="margin-top: 10px;">A finales del 2023 los pastores de la IENAD llegaron para colocar como obreros a los esposos Boris Fernández y Paula Joseff. En agosto de 2025 se los consagró como pastores y adscritos al concilio de la IENAD.</p>
    </div>
</div>
"""
        st.markdown(html_acerca_fijo, unsafe_allow_html=True)

    with col_der:
        try:
            st.image("logoIglesia.jpeg", use_container_width=True)
        except:
            st.info("IENAD Betania")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
   
# ============================================================================
# FOOTER 
# ============================================================================
footer_html = """
<style>
    /* ====== FIX STREAMLIT FULL WIDTH ====== */
    div[data-testid="stAppViewContainer"] {
        overflow-x: hidden;
    }

    section.main > div {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* ====== FOOTER ====== */
    .main-footer {
        background: linear-gradient(135deg, #071840 0%, #1E293B 100%);
        padding: 50px 20px;
        font-family: 'Segoe UI', sans-serif;
        color: #fff;
        border-top: 3px solid #D4AF37;
        margin-top: 60px;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.1);
        width: 100%;
        box-sizing: border-box;
    }

    .footer-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        max-width: 1200px;
        margin: 0 auto;
        gap: 30px;
    }

    .footer-section {
        margin: 20px;
        min-width: 250px;
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 12px;
    }

    .footer-title {
        font-weight: bold;
        color: #D4AF37;
        margin-bottom: 15px;
        text-transform: uppercase;
        font-size: 1rem;
    }

    .footer-content {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #f0f0f0;
    }

    .footer-bottom {
        text-align: center;
        margin-top: 40px;
        font-size: 0.8rem;
        opacity: 0.8;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 20px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }

    @media (max-width: 768px) {
        .footer-container {
            flex-direction: column;
            align-items: center;
        }

        .footer-section {
            min-width: 80%;
        }
    }
</style>

<div class="main-footer">
    <div class="footer-container">
        <div class="footer-section">
            <p class="footer-title">Ubicación</p>
            <p class="footer-content">Calle Fortín Vanguardia #740<br>Cochabamba, Bolivia</p>
        </div>
        <div class="footer-section">
            <p class="footer-title">Contactos</p>
            <p class="footer-content">
                Pastora Paula: <a href="https://wa.me/59167435065" target="_blank">+591 67435065</a><br>
                Pastor Boris: <a href="https://wa.me/59177462108" target="_blank">+591 77462108</a>
            </p>
        </div>
        <div class="footer-section">
            <p class="footer-title">Horarios</p>
            <p class="footer-content">Sábado: 6:30 PM<br>Domingo: 10:30 AM</p>
        </div>
    </div>
    <div class="footer-bottom">
        <p>© 2025 Iglesia Restauración. Desarrollado para la gloria de Dios.</p>
    </div>
</div>
"""

# Esta es la línea clave que renderiza el HTML
st.markdown(footer_html, unsafe_allow_html=True)
# ============================================================================
# FIN DEL ARCHIVO
# ============================================================================
