
import streamlit as st
from datetime import date, datetime, timedelta, timezone
from io import StringIO
import csv
import hmac
import re
import requests

st.set_page_config(
    page_title="RunningCoachPro V5",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------------
# V5 · Optimización para celular
# ------------------------------
st.markdown(
    """
    <style>
    /* Contenido general */
    .block-container {
        max-width: 1180px;
        padding-top: 1.15rem;
        padding-bottom: 4rem;
    }

    /* Botones táctiles */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {
        min-height: 48px;
        border-radius: 12px;
        font-weight: 600;
    }

    /* Inputs más cómodos */
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] > div,
    textarea {
        min-height: 44px;
        font-size: 16px !important;
    }

    /* Tarjetas y avisos */
    [data-testid="stMetric"] {
        padding: 0.6rem 0;
    }

    /* Tabs desplazables con dedo */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
        overflow-x: auto;
        scrollbar-width: thin;
        white-space: nowrap;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 44px;
        flex: 0 0 auto;
    }

    /* Tablas: permitir scroll horizontal local */
    [data-testid="stDataFrame"] {
        overflow-x: auto;
    }

    @media (max-width: 768px) {
        /* Márgenes compactos en móvil */
        .block-container {
            padding-left: 0.85rem;
            padding-right: 0.85rem;
            padding-top: 0.75rem;
            padding-bottom: 5rem;
        }

        h1 {
            font-size: 1.9rem !important;
            line-height: 1.15 !important;
        }

        h2 {
            font-size: 1.45rem !important;
        }

        h3 {
            font-size: 1.15rem !important;
        }

        /* En móvil, las columnas se apilan */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.55rem !important;
        }

        [data-testid="column"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
        }

        /* Métricas como tarjetas legibles */
        [data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 14px;
            padding: 0.75rem 0.85rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.65rem !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.82rem !important;
        }

        /* Botones full-width cómodos */
        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stFormSubmitButton"] > button {
            width: 100% !important;
            min-height: 50px;
        }

        /* Tabs más compactas */
        .stTabs [data-baseweb="tab"] {
            padding-left: 0.65rem;
            padding-right: 0.65rem;
        }

        /* Gráficos aprovechan todo el ancho */
        [data-testid="stVegaLiteChart"] {
            width: 100% !important;
        }

        /* Menos aire en separadores */
        hr {
            margin-top: 0.8rem !important;
            margin-bottom: 0.8rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PLAN = [{'fecha': '2026-09-01',
  'semana': 1,
  'tipo': 'SERIES',
  'entrenamiento': '6 x 600 m',
  'descripcion': 'CALENTAMIENTO + 6 x 600 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 8.0,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '44:00',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '6 x 600 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '90 s trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-09-03',
  'semana': 1,
  'tipo': 'TEMPO',
  'entrenamiento': 'TEMPO 5 KM',
  'descripcion': '5 km tempo controlado + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 8.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '43:20',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '5 km tempo controlado',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR LADO | HIP THRUST '
           '3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
 {'fecha': '2026-09-04',
  'semana': 1,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 6 KM',
  'descripcion': '6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 6.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '37:12',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '6 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-09-06',
  'semana': 1,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 14 KM',
  'descripcion': '14 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',
  'km': 14.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:22:08',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '14 km | RUTA APROX. 157 M D+ | TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-09-08',
  'semana': 2,
  'tipo': 'SERIES',
  'entrenamiento': '5 x 800 m',
  'descripcion': 'CALENTAMIENTO + 5 x 800 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 8.5,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '46:45',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '5 x 800 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:00 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-09-10',
  'semana': 2,
  'tipo': 'TEMPO',
  'entrenamiento': 'TEMPO 6 KM',
  'descripcion': '6 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 9.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '48:45',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '6 km tempo continuo',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B PROGRAMADA EL SÁBADO DE ESTA SEMANA.'},
 {'fecha': '2026-09-11',
  'semana': 2,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 6 KM',
  'descripcion': '6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 6.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '37:12',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '6 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-09-12',
  'semana': 2,
  'tipo': 'FUERZA',
  'entrenamiento': 'FUERZA B + MOVILIDAD',
  'descripcion': 'SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',
  'km': 0.0,
  'ritmo': 'NO APLICA',
  'duracion': '40-50 MIN',
  'intensidad': 'MEDIA',
  'objetivo': 'FUERZA ESPECÍFICA, ESTABILIDAD, ECONOMÍA DE CARRERA Y PREVENCIÓN DE LESIONES',
  'calentamiento': '8-10 min movilidad dinámica',
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 | CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES DE ESA SEMANA.'},
 {'fecha': '2026-09-13',
  'semana': 2,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 16 KM',
  'descripcion': '16 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',
  'km': 16.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:33:52',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '16 km | RUTA APROX. 157 M D+ | TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-09-15',
  'semana': 3,
  'tipo': 'SERIES',
  'entrenamiento': '6 x 800 m',
  'descripcion': 'CALENTAMIENTO + 6 x 800 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 9.5,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '52:15',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '6 x 800 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:00 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-09-17',
  'semana': 3,
  'tipo': 'TEMPO',
  'entrenamiento': '2 x 4 KM UMBRAL',
  'descripcion': '2 x 4 km + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 11.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '59:35',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '2 x 4 km',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR LADO | HIP THRUST '
           '3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
 {'fecha': '2026-09-18',
  'semana': 3,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 6 KM',
  'descripcion': '6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 6.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '37:12',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '6 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-09-20',
  'semana': 3,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 18 KM',
  'descripcion': '18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 3 KM PROGRESIVOS SIN SUPERAR RPE 7.',
  'km': 18.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:45:36',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '18 km | RUTA APROX. 157 M D+ | ÚLTIMOS 3 KM PROGRESIVOS SIN SUPERAR RPE 7',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-09-22',
  'semana': 4,
  'tipo': 'SERIES',
  'entrenamiento': '10 x 400 m',
  'descripcion': 'CALENTAMIENTO + 10 x 400 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 8.0,
  'ritmo': '4:29-4:37 min/km',
  'duracion': '44:00',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '10 x 400 m a 4:29-4:37 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '200 m trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-09-24',
  'semana': 4,
  'tipo': 'TEMPO',
  'entrenamiento': 'TEMPO 5 KM',
  'descripcion': '5 km tempo controlado + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 8.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '43:20',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '5 km tempo controlado',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B PROGRAMADA EL SÁBADO DE ESTA SEMANA.'},
 {'fecha': '2026-09-25',
  'semana': 4,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 6 KM',
  'descripcion': '6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 6.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '37:12',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '6 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-09-26',
  'semana': 4,
  'tipo': 'FUERZA',
  'entrenamiento': 'FUERZA B + MOVILIDAD',
  'descripcion': 'SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',
  'km': 0.0,
  'ritmo': 'NO APLICA',
  'duracion': '40-50 MIN',
  'intensidad': 'MEDIA',
  'objetivo': 'FUERZA ESPECÍFICA, ESTABILIDAD, ECONOMÍA DE CARRERA Y PREVENCIÓN DE LESIONES',
  'calentamiento': '8-10 min movilidad dinámica',
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 | CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES DE ESA SEMANA.'},
 {'fecha': '2026-09-27',
  'semana': 4,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 15 KM',
  'descripcion': '15 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',
  'km': 15.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:28:00',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '15 km | RUTA APROX. 157 M D+ | TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-09-29',
  'semana': 5,
  'tipo': 'SERIES',
  'entrenamiento': '5 x 1000 m',
  'descripcion': 'CALENTAMIENTO + 5 x 1000 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 9.5,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '52:15',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '5 x 1000 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:00 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-10-01',
  'semana': 5,
  'tipo': 'TEMPO',
  'entrenamiento': 'TEMPO 7 KM',
  'descripcion': '7 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 10.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '54:10',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '7 km tempo continuo',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR LADO | HIP THRUST '
           '3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
 {'fecha': '2026-10-02',
  'semana': 5,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 7 KM',
  'descripcion': '7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 7.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '43:24',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '7 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-10-04',
  'semana': 5,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 18 KM',
  'descripcion': '18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',
  'km': 18.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:45:36',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '18 km | RUTA APROX. 157 M D+ | TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-10-06',
  'semana': 6,
  'tipo': 'SERIES',
  'entrenamiento': '6 x 1000 m',
  'descripcion': 'CALENTAMIENTO + 6 x 1000 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 10.5,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '57:45',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '6 x 1000 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:00 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-10-08',
  'semana': 6,
  'tipo': 'TEMPO',
  'entrenamiento': '2 x 4 KM UMBRAL',
  'descripcion': '2 x 4 km + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 11.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '59:35',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '2 x 4 km',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B PROGRAMADA EL SÁBADO DE ESTA SEMANA.'},
 {'fecha': '2026-10-09',
  'semana': 6,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 7 KM',
  'descripcion': '7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 7.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '43:24',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '7 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-10-10',
  'semana': 6,
  'tipo': 'FUERZA',
  'entrenamiento': 'FUERZA B + MOVILIDAD',
  'descripcion': 'SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',
  'km': 0.0,
  'ritmo': 'NO APLICA',
  'duracion': '40-50 MIN',
  'intensidad': 'MEDIA',
  'objetivo': 'FUERZA ESPECÍFICA, ESTABILIDAD, ECONOMÍA DE CARRERA Y PREVENCIÓN DE LESIONES',
  'calentamiento': '8-10 min movilidad dinámica',
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 | CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES DE ESA SEMANA.'},
 {'fecha': '2026-10-11',
  'semana': 6,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 20 KM',
  'descripcion': '20 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 4 KM PROGRESIVOS HASTA RITMO MODERADO.',
  'km': 20.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:57:20',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '20 km | RUTA APROX. 157 M D+ | ÚLTIMOS 4 KM PROGRESIVOS HASTA RITMO MODERADO',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-10-13',
  'semana': 7,
  'tipo': 'SERIES',
  'entrenamiento': '4 x 1200 m',
  'descripcion': 'CALENTAMIENTO + 4 x 1200 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 9.5,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '52:15',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '4 x 1200 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:30 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-10-15',
  'semana': 7,
  'tipo': 'TEMPO',
  'entrenamiento': 'TEMPO 8 KM',
  'descripcion': '8 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 11.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '59:35',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '8 km tempo continuo',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR LADO | HIP THRUST '
           '3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
 {'fecha': '2026-10-16',
  'semana': 7,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 7 KM',
  'descripcion': '7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 7.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '43:24',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '7 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-10-18',
  'semana': 7,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 16 KM',
  'descripcion': '16 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',
  'km': 16.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:33:52',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '16 km | RUTA APROX. 157 M D+ | TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-10-20',
  'semana': 8,
  'tipo': 'SERIES',
  'entrenamiento': '5 x 1200 m',
  'descripcion': 'CALENTAMIENTO + 5 x 1200 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 10.5,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '57:45',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '5 x 1200 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:30 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-10-22',
  'semana': 8,
  'tipo': 'TEMPO',
  'entrenamiento': '3 x 3 KM UMBRAL',
  'descripcion': '3 x 3 km + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 12.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '1:05:00',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '3 x 3 km',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B PROGRAMADA EL SÁBADO DE ESTA SEMANA.'},
 {'fecha': '2026-10-23',
  'semana': 8,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 7 KM',
  'descripcion': '7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 7.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '43:24',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '7 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-10-24',
  'semana': 8,
  'tipo': 'FUERZA',
  'entrenamiento': 'FUERZA B + MOVILIDAD',
  'descripcion': 'SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',
  'km': 0.0,
  'ritmo': 'NO APLICA',
  'duracion': '40-50 MIN',
  'intensidad': 'MEDIA',
  'objetivo': 'FUERZA ESPECÍFICA, ESTABILIDAD, ECONOMÍA DE CARRERA Y PREVENCIÓN DE LESIONES',
  'calentamiento': '8-10 min movilidad dinámica',
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 | CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES DE ESA SEMANA.'},
 {'fecha': '2026-10-25',
  'semana': 8,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 21 KM',
  'descripcion': '21 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 5 KM PROGRESIVOS SIN ENTRAR EN UMBRAL.',
  'km': 21.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '2:03:12',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '21 km | RUTA APROX. 157 M D+ | ÚLTIMOS 5 KM PROGRESIVOS SIN ENTRAR EN UMBRAL',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-10-27',
  'semana': 9,
  'tipo': 'SERIES',
  'entrenamiento': '8 x 600 m',
  'descripcion': 'CALENTAMIENTO + 8 x 600 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 9.0,
  'ritmo': '4:29-4:37 min/km',
  'duracion': '49:30',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '8 x 600 m a 4:29-4:37 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '90 s trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-10-29',
  'semana': 9,
  'tipo': 'TEMPO',
  'entrenamiento': 'TEMPO 9 KM',
  'descripcion': '9 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 12.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '1:05:00',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '9 km tempo continuo',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR LADO | HIP THRUST '
           '3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
 {'fecha': '2026-10-30',
  'semana': 9,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 7 KM',
  'descripcion': '7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 7.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '43:24',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '7 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-11-01',
  'semana': 9,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 18 KM',
  'descripcion': '18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',
  'km': 18.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:45:36',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '18 km | RUTA APROX. 157 M D+ | TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-11-03',
  'semana': 10,
  'tipo': 'SERIES',
  'entrenamiento': '6 x 1000 m',
  'descripcion': 'CALENTAMIENTO + 6 x 1000 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 10.5,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '57:45',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '6 x 1000 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:00 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-11-05',
  'semana': 10,
  'tipo': 'TEMPO',
  'entrenamiento': '2 x 5 KM UMBRAL',
  'descripcion': '2 x 5 km + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 13.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '1:10:25',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '2 x 5 km',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR LADO | HIP THRUST '
           '3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
 {'fecha': '2026-11-06',
  'semana': 10,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 7 KM',
  'descripcion': '7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 7.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '43:24',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '7 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-11-08',
  'semana': 10,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 22 KM',
  'descripcion': '22 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 4 KM A ESFUERZO STEADY CONTROLADO.',
  'km': 22.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '2:09:04',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '22 km | RUTA APROX. 157 M D+ | ÚLTIMOS 4 KM A ESFUERZO STEADY CONTROLADO',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-11-10',
  'semana': 11,
  'tipo': 'SERIES',
  'entrenamiento': '3 x 1600 m',
  'descripcion': 'CALENTAMIENTO + 3 x 1600 m a ritmo controlado de 10K + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 10.0,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '55:00',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '3 x 1600 m a ritmo controlado de 10K a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '3:00 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-11-12',
  'semana': 11,
  'tipo': 'TEMPO',
  'entrenamiento': 'BLOQUE ESPECÍFICO MM',
  'descripcion': '3 km suaves + 6 km ritmo MM objetivo + 2 km suaves + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 11.0,
  'ritmo': '5:05 min/km',
  'duracion': '59:35',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '3 km suaves + 6 km ritmo MM objetivo + 2 km suaves',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B PROGRAMADA EL SÁBADO DE ESTA SEMANA.'},
 {'fecha': '2026-11-13',
  'semana': 11,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 7 KM',
  'descripcion': '7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 7.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '43:24',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '7 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-11-14',
  'semana': 11,
  'tipo': 'FUERZA',
  'entrenamiento': 'FUERZA B + MOVILIDAD',
  'descripcion': 'SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',
  'km': 0.0,
  'ritmo': 'NO APLICA',
  'duracion': '40-50 MIN',
  'intensidad': 'MEDIA',
  'objetivo': 'FUERZA ESPECÍFICA, ESTABILIDAD, ECONOMÍA DE CARRERA Y PREVENCIÓN DE LESIONES',
  'calentamiento': '8-10 min movilidad dinámica',
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 | CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES DE ESA SEMANA.'},
 {'fecha': '2026-11-15',
  'semana': 11,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 18 KM',
  'descripcion': '18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 5 KM CERCA DE RITMO MM OBJETIVO (5:05 MIN/KM) SOLO SI LAS '
                 'SENSACIONES SON BUENAS.',
  'km': 18.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:45:36',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '18 km | RUTA APROX. 157 M D+ | ÚLTIMOS 5 KM CERCA DE RITMO MM OBJETIVO (5:05 MIN/KM) SOLO SI LAS SENSACIONES SON BUENAS',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-11-17',
  'semana': 12,
  'tipo': 'SERIES',
  'entrenamiento': '5 x 800 m',
  'descripcion': 'CALENTAMIENTO + 5 x 800 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 8.0,
  'ritmo': '4:42-4:49 min/km',
  'duracion': '44:00',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '5 x 800 m a 4:42-4:49 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '2:00 min trote suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-11-19',
  'semana': 12,
  'tipo': 'TEMPO',
  'entrenamiento': 'TEMPO 5 KM',
  'descripcion': '5 km umbral controlado + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 8.0,
  'ritmo': '4:55-5:00 min/km',
  'duracion': '43:20',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '5 km umbral controlado',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR LADO | HIP THRUST '
           '3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
 {'fecha': '2026-11-20',
  'semana': 12,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 5 KM',
  'descripcion': '5 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 5.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '31:00',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '5 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-11-22',
  'semana': 12,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 14 KM',
  'descripcion': '14 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',
  'km': 14.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:22:08',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '14 km | RUTA APROX. 157 M D+ | TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO COMPENSAR DESCENSOS '
           'CORRIENDO EXCESIVAMENTE RÁPIDO.'},
 {'fecha': '2026-11-24',
  'semana': 13,
  'tipo': 'SERIES',
  'entrenamiento': '6 x 400 m',
  'descripcion': 'CALENTAMIENTO + 6 x 400 m ágiles sin máximo esfuerzo + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',
  'km': 6.5,
  'ritmo': '4:29-4:37 min/km',
  'duracion': '35:45',
  'intensidad': 'ALTA',
  'objetivo': 'ECONOMÍA DE CARRERA, POTENCIA AERÓBICA Y VELOCIDAD',
  'calentamiento': '2 km suaves + movilidad + 4 progresivos de 80-100 m',
  'bloque': '6 x 400 m ágiles sin máximo esfuerzo a 4:29-4:37 min/km | TERRENO PLANO O CAMINADORA 1%',
  'recuperacion': '200 m trote muy suave',
  'enfriamiento': '1.5-2 km suaves',
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 MIN: SENTADILLA 3x6-8 '
           '| PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
 {'fecha': '2026-11-26',
  'semana': 13,
  'tipo': 'TEMPO',
  'entrenamiento': 'ACTIVACIÓN MM',
  'descripcion': '2 km suaves + 3 km ritmo MM + 1 km suave + TRABAJO COMPLEMENTARIO DE FUERZA',
  'km': 6.0,
  'ritmo': '5:05 min/km',
  'duracion': '32:30',
  'intensidad': 'MEDIA-ALTA',
  'objetivo': 'ELEVAR UMBRAL, MEJORAR RESISTENCIA A RITMOS ALTOS Y ESPECIFICIDAD MM',
  'calentamiento': '2 km suaves + movilidad dinámica',
  'bloque': '2 km suaves + 3 km ritmo MM + 1 km suave',
  'recuperacion': 'EN BLOQUES FRACCIONADOS: 2-3 MIN DE TROTE SUAVE',
  'enfriamiento': '1-2 km suaves',
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B PROGRAMADA EL SÁBADO DE ESTA SEMANA.'},
 {'fecha': '2026-11-27',
  'semana': 13,
  'tipo': 'RODAJE',
  'entrenamiento': 'RODAJE OPCIONAL POSTURNO 5 KM',
  'descripcion': '5 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',
  'km': 5.0,
  'ritmo': '6:12-6:31 min/km',
  'duracion': '31:00',
  'intensidad': 'OPCIONAL',
  'objetivo': 'RECUPERACIÓN ACTIVA Y VOLUMEN AERÓBICO SIN AÑADIR FATIGA',
  'calentamiento': '5-10 min extremadamente suaves',
  'bloque': '5 km conversacionales',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5 min caminando + movilidad',
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS O RPE BASAL '
           'ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
 {'fecha': '2026-11-28',
  'semana': 13,
  'tipo': 'FUERZA',
  'entrenamiento': 'FUERZA B + MOVILIDAD',
  'descripcion': 'SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',
  'km': 0.0,
  'ritmo': 'NO APLICA',
  'duracion': '40-50 MIN',
  'intensidad': 'MEDIA',
  'objetivo': 'FUERZA ESPECÍFICA, ESTABILIDAD, ECONOMÍA DE CARRERA Y PREVENCIÓN DE LESIONES',
  'calentamiento': '8-10 min movilidad dinámica',
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 | CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES DE ESA SEMANA.'},
 {'fecha': '2026-11-29',
  'semana': 13,
  'tipo': 'LARGA',
  'entrenamiento': 'MEDIA MARATÓN OBJETIVO 21.1 KM',
  'descripcion': 'MEDIA MARATÓN OBJETIVO. SALIDA CONTROLADA Y PROGRESIÓN POR ESFUERZO.',
  'km': 21.0975,
  'ritmo': '5:05 min/km',
  'duracion': '1:47:12',
  'intensidad': 'COMPETENCIA',
  'objetivo': 'MEJORAR MARCA OFICIAL 1:49:53',
  'calentamiento': '10-15 min muy suaves + movilidad + 4 progresivos cortos',
  'bloque': 'KM 1-5 CONTROLADOS | KM 6-16 RITMO OBJETIVO | KM 17-21.1 PROGRESAR SEGÚN SENSACIONES',
  'recuperacion': 'NO APLICA',
  'enfriamiento': 'CAMINATA SUAVE + HIDRATACIÓN',
  'notas': 'REFERENCIA ACTUAL: 1:49:53. OBJETIVO INICIAL DEL BLOQUE: 1:47:12 (5:05 MIN/KM).'}]
ZONES = [('Recuperación', '6:12-6:31 min/km', 'Muy suave'),
 ('Rodaje', '5:51-6:08 min/km', 'Aeróbico'),
 ('Tirada larga', '5:52-6:08 min/km', 'Ruta habitual ~157 m D+'),
 ('Umbral', '4:55-5:00 min/km', 'Tempo / umbral'),
 ('Series 1000 m', '4:42-4:49 min/km', 'Series medias/largas'),
 ('Series 400 m', '4:29-4:37 min/km', 'Series cortas'),
 ('Ritmo MM objetivo', '5:05 min/km', 'Competencia')]

NAME = 'ERIC'
GOAL = 'MEJORAR MARCA MEDIA MARATÓN'
CURRENT_TIME = '1:49:53'
CURRENT_PACE = '5:13'
TARGET_TIME = '1:47:12'
TARGET_PACE = '5:05'
LONG_ROUTE_ELEVATION = 157
TREADMILL_INCLINE = 1.0

PLAN_START = date(2026, 9, 1)
PLAN_END = date(2026, 11, 30)
RACE_DATE = date(2026, 11, 29)

DAY_NAMES = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo"
]

TYPE_ICONS = {
    "SERIES": "⚡",
    "TEMPO": "🔥",
    "RODAJE": "🌿",
    "FUERZA": "🏋️",
    "LARGA": "🏃",
}

SESSION_BY_DATE = {s["fecha"]: s for s in PLAN}


# ------------------------------
# Utilidades generales
# ------------------------------
def secret_value(name, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


SUPABASE_URL = str(secret_value("SUPABASE_URL", "") or "").rstrip("/")
SUPABASE_SECRET_KEY = str(secret_value("SUPABASE_SECRET_KEY", "") or "")
APP_PIN = str(secret_value("APP_PIN", "") or "")
DB_READY = bool(SUPABASE_URL and SUPABASE_SECRET_KEY)


def fmt_km(km):
    km = float(km or 0)
    if abs(km - round(km)) < 1e-9:
        return f"{int(round(km))} km"
    return f"{km:.1f} km"


def fmt_num(value, decimals=1):
    if value is None:
        return "—"
    return f"{float(value):.{decimals}f}"


def session_for(day):
    return SESSION_BY_DATE.get(day.isoformat())


def week_start(day):
    return day - timedelta(days=day.weekday())


def next_session_from(day):
    future = [s for s in PLAN if date.fromisoformat(s["fecha"]) >= day]
    return future[0] if future else None


def is_optional(s):
    return s and s["intensidad"] == "OPCIONAL"


def is_running(s):
    return s and s["tipo"] != "FUERZA"


def planned_duration_default(s):
    raw = str(s.get("duracion", "")).strip()
    if re.fullmatch(r"\d+:\d{2}:\d{2}", raw):
        return raw
    if re.fullmatch(r"\d+:\d{2}", raw):
        mm, ss = raw.split(":")
        return f"00:{int(mm):02d}:{int(ss):02d}"
    m = re.search(r"(\d+)\s*-\s*(\d+)\s*MIN", raw.upper())
    if m:
        avg = round((int(m.group(1)) + int(m.group(2))) / 2)
        return f"00:{avg:02d}:00"
    m = re.search(r"(\d+)\s*MIN", raw.upper())
    if m:
        return f"00:{int(m.group(1)):02d}:00"
    return "00:00:00"


def parse_duration(text):
    text = str(text or "").strip()
    if not text:
        return 0, None

    if re.fullmatch(r"\d+(?:[.,]\d+)?", text):
        minutes = float(text.replace(",", "."))
        if minutes < 0:
            return None, "La duración no puede ser negativa."
        return int(round(minutes * 60)), None

    parts = text.split(":")
    try:
        nums = [int(x) for x in parts]
    except ValueError:
        return None, "Usa HH:MM:SS, MM:SS o minutos."

    if len(nums) == 2:
        mm, ss = nums
        if not (0 <= ss < 60) or mm < 0:
            return None, "Duración inválida."
        return mm * 60 + ss, None

    if len(nums) == 3:
        hh, mm, ss = nums
        if hh < 0 or not (0 <= mm < 60) or not (0 <= ss < 60):
            return None, "Duración inválida."
        return hh * 3600 + mm * 60 + ss, None

    return None, "Usa HH:MM:SS, MM:SS o minutos."


def fmt_duration(seconds):
    if seconds is None:
        return "—"
    seconds = int(seconds)
    hh, rem = divmod(seconds, 3600)
    mm, ss = divmod(rem, 60)
    if hh:
        return f"{hh}:{mm:02d}:{ss:02d}"
    return f"{mm}:{ss:02d}"


def fmt_pace(seconds, km):
    if not seconds or not km or float(km) <= 0:
        return "—"
    sec_per_km = int(round(float(seconds) / float(km)))
    mm, ss = divmod(sec_per_km, 60)
    return f"{mm}:{ss:02d} min/km"


def today_or_nearest():
    t = date.today()
    if t < PLAN_START:
        return t
    if t > PLAN_END:
        return PLAN_END
    return t


# ------------------------------
# PIN de acceso
# ------------------------------
if DB_READY and not APP_PIN:
    st.error(
        "La base de datos está configurada, pero falta APP_PIN en los Secrets de Streamlit. "
        "Añádelo antes de usar el guardado permanente."
    )
    st.stop()

if APP_PIN:
    if not st.session_state.get("_authenticated", False):
        st.title("🏃 RunningCoachPro")
        st.caption("Acceso privado")
        entered = st.text_input("PIN", type="password")
        if st.button("Entrar", use_container_width=True):
            if hmac.compare_digest(str(entered), APP_PIN):
                st.session_state["_authenticated"] = True
                st.rerun()
            else:
                st.error("PIN incorrecto.")
        st.stop()


# ------------------------------
# Persistencia Supabase / fallback
# ------------------------------
REST_TABLE = f"{SUPABASE_URL}/rest/v1/runningcoach_logs" if DB_READY else ""


def db_headers(extra=None):
    headers = {
        "apikey": SUPABASE_SECRET_KEY,
        "Content-Type": "application/json",
    }
    if extra:
        headers.update(extra)
    return headers


def load_logs():
    if not DB_READY:
        return list(st.session_state.get("_local_logs", {}).values())

    try:
        r = requests.get(
            REST_TABLE,
            params={
                "select": "*",
                "runner": f"eq.{NAME}",
                "order": "session_date.asc",
            },
            headers=db_headers(),
            timeout=12,
        )
        r.raise_for_status()
        return r.json()
    except Exception as exc:
        st.error(f"No pude leer la base de datos: {exc}")
        return []


def save_log(record):
    if not DB_READY:
        store = st.session_state.setdefault("_local_logs", {})
        store[record["session_date"]] = record
        return True, None

    try:
        r = requests.post(
            REST_TABLE,
            params={"on_conflict": "runner,session_date"},
            headers=db_headers({
                "Prefer": "resolution=merge-duplicates,return=representation",
            }),
            json=record,
            timeout=12,
        )
        r.raise_for_status()
        return True, None
    except Exception as exc:
        return False, str(exc)


def logs_by_date(logs):
    return {str(x.get("session_date")): x for x in logs}


LOGS = load_logs()
LOG_BY_DATE = logs_by_date(LOGS)


# ------------------------------
# Métricas
# ------------------------------
def log_for(day):
    key = day.isoformat() if isinstance(day, date) else str(day)
    return LOG_BY_DATE.get(key)


def status_label(log):
    if not log:
        return "PENDIENTE"
    return str(log.get("status") or "COMPLETADO").upper()


def session_completed(s):
    log = LOG_BY_DATE.get(s["fecha"])
    return bool(log and status_label(log) in ("COMPLETADO", "MODIFICADO"))


def week_metrics(week_no):
    rows = [s for s in PLAN if s["semana"] == week_no]
    base = [s for s in rows if not is_optional(s)]
    optional = [s for s in rows if is_optional(s)]
    actual_km = sum(
        float(LOG_BY_DATE.get(s["fecha"], {}).get("actual_km") or 0)
        for s in rows
        if status_label(LOG_BY_DATE.get(s["fecha"])) in ("COMPLETADO", "MODIFICADO")
    )
    return {
        "base_sessions": len(base),
        "base_km": sum(s["km"] for s in base),
        "optional_km": sum(s["km"] for s in optional),
        "actual_km": actual_km,
    }


def dashboard_metrics(as_of):
    due_base = [
        s for s in PLAN
        if date.fromisoformat(s["fecha"]) <= as_of and not is_optional(s)
    ]
    completed_base = [s for s in due_base if session_completed(s)]

    due_running_base = [s for s in due_base if is_running(s)]
    plan_km_due = sum(s["km"] for s in due_running_base)

    actual_km = 0.0
    rpes = []
    for s in PLAN:
        if date.fromisoformat(s["fecha"]) > as_of:
            continue
        log = LOG_BY_DATE.get(s["fecha"])
        if not log:
            continue
        if status_label(log) in ("COMPLETADO", "MODIFICADO"):
            actual_km += float(log.get("actual_km") or 0)
            if log.get("rpe") is not None:
                try:
                    rpes.append(float(log.get("rpe")))
                except Exception:
                    pass

    compliance = (len(completed_base) / len(due_base) * 100) if due_base else 0
    avg_rpe = sum(rpes) / len(rpes) if rpes else None

    return {
        "due_base": len(due_base),
        "completed_base": len(completed_base),
        "compliance": compliance,
        "plan_km_due": plan_km_due,
        "actual_km": actual_km,
        "avg_rpe": avg_rpe,
    }


def readiness(as_of):
    recent_cutoff = as_of - timedelta(days=14)
    recent = []
    missed_base = 0

    for s in PLAN:
        d = date.fromisoformat(s["fecha"])
        if not (recent_cutoff <= d <= as_of):
            continue

        log = LOG_BY_DATE.get(s["fecha"])
        if log:
            recent.append((s, log))
            if not is_optional(s) and status_label(log) == "OMITIDO":
                missed_base += 1

    rpes = []
    for _, log in recent:
        if status_label(log) in ("COMPLETADO", "MODIFICADO") and log.get("rpe") is not None:
            try:
                rpes.append(float(log["rpe"]))
            except Exception:
                pass

    last_rpes = rpes[-3:]
    avg3 = sum(last_rpes) / len(last_rpes) if last_rpes else None
    very_high = sum(1 for x in last_rpes if x >= 9)

    if missed_base >= 2 or very_high >= 2 or (avg3 is not None and avg3 >= 8.5):
        return (
            "ROJO",
            avg3,
            "No añadas volumen ni intensidad extra. Omite el rodaje opcional del viernes. "
            "Si la fatiga alta persiste o aparece dolor/síntomas anormales, suspende y busca orientación profesional.",
        )
    if missed_base >= 1 or (avg3 is not None and avg3 >= 7.5):
        return (
            "AMARILLO",
            avg3,
            "Mantén el plan sin extras. El viernes opcional solo si has recuperado bien. "
            "No aceleres los ritmos prescritos aunque te sientas mejor al inicio.",
        )
    if avg3 is None:
        return (
            "SIN DATOS",
            None,
            "Registra al menos algunas sesiones y su RPE para que el semáforo pueda estimar la carga reciente.",
        )
    return (
        "VERDE",
        avg3,
        "La carga reciente parece tolerable según tus registros. Mantén las zonas y la progresión del plan; no añadas trabajo no programado.",
    )



def hms_to_seconds(text):
    parts = [int(x) for x in str(text).split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return 0


def pace_text_to_seconds(text):
    m = re.match(r"^\s*(\d+):(\d{2})", str(text))
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def pace_decimal(seconds_per_km):
    if seconds_per_km is None:
        return None
    return round(float(seconds_per_km) / 60.0, 3)


def logged_running_sessions(as_of):
    rows = []
    for s in PLAN:
        d = date.fromisoformat(s["fecha"])
        if d > as_of or not is_running(s):
            continue

        log = LOG_BY_DATE.get(s["fecha"])
        if not log or status_label(log) not in ("COMPLETADO", "MODIFICADO"):
            continue

        km = float(log.get("actual_km") or 0)
        sec = int(log.get("actual_duration_sec") or 0)
        if km <= 0:
            continue

        pace_sec = (sec / km) if sec > 0 else None
        rows.append({
            "date": d,
            "session": s,
            "log": log,
            "km": km,
            "seconds": sec,
            "pace_sec": pace_sec,
        })
    return rows


def weekly_dashboard_data(as_of):
    data = []
    for w in range(1, 14):
        sessions = [s for s in PLAN if s["semana"] == w]
        plan_base_km = sum(
            s["km"] for s in sessions
            if not is_optional(s) and is_running(s)
        )

        real_km = 0.0
        load_proxy = 0.0
        rpes = []
        completed = 0
        due_base = 0

        for s in sessions:
            d = date.fromisoformat(s["fecha"])
            if d <= as_of and not is_optional(s):
                due_base += 1

            log = LOG_BY_DATE.get(s["fecha"])
            if not log or d > as_of:
                continue

            if status_label(log) in ("COMPLETADO", "MODIFICADO"):
                if not is_optional(s) and d <= as_of:
                    completed += 1

                km = float(log.get("actual_km") or 0)
                real_km += km

                try:
                    rpe = float(log.get("rpe")) if log.get("rpe") is not None else None
                except Exception:
                    rpe = None

                if rpe is not None:
                    rpes.append(rpe)
                    if is_running(s):
                        load_proxy += km * rpe

        data.append({
            "week": w,
            "plan_km": round(plan_base_km, 2),
            "real_km": round(real_km, 2),
            "load": round(load_proxy, 2),
            "avg_rpe": round(sum(rpes) / len(rpes), 2) if rpes else None,
            "completed": completed,
            "due_base": due_base,
        })
    return data


def milestone_metrics(as_of):
    runs = logged_running_sessions(as_of)
    if not runs:
        return {
            "longest": None,
            "fastest_easy": None,
            "best_week_km": None,
            "long_runs_completed": 0,
        }

    longest = max(runs, key=lambda x: x["km"])

    comparable = [
        x for x in runs
        if x["session"]["tipo"] in ("RODAJE", "LARGA") and x["pace_sec"] is not None
    ]
    fastest_easy = min(comparable, key=lambda x: x["pace_sec"]) if comparable else None

    weekly = weekly_dashboard_data(as_of)
    best_week = max(weekly, key=lambda x: x["real_km"]) if weekly else None

    long_runs_completed = sum(
        1 for x in runs if x["session"]["tipo"] == "LARGA"
    )

    return {
        "longest": longest,
        "fastest_easy": fastest_easy,
        "best_week_km": best_week,
        "long_runs_completed": long_runs_completed,
    }


def recent_training_alerts(as_of):
    messages = []
    recent = []
    cutoff = as_of - timedelta(days=14)

    for s in PLAN:
        d = date.fromisoformat(s["fecha"])
        if not (cutoff <= d <= as_of):
            continue

        log = LOG_BY_DATE.get(s["fecha"])
        if not log:
            continue

        recent.append((s, log))

        if (
            status_label(log) in ("COMPLETADO", "MODIFICADO")
            and is_running(s)
            and float(s["km"] or 0) > 0
        ):
            real_km = float(log.get("actual_km") or 0)
            if real_km > float(s["km"]) * 1.15:
                messages.append(
                    f"{d.strftime('%d/%m')}: corriste {real_km:.1f} km frente a "
                    f"{float(s['km']):.1f} km planificados (+15% o más)."
                )

    high_rpe = []
    for s, log in recent:
        if status_label(log) in ("COMPLETADO", "MODIFICADO"):
            try:
                rpe = float(log.get("rpe"))
            except Exception:
                continue
            if rpe >= 8:
                high_rpe.append((s, rpe))

    if len(high_rpe) >= 2:
        messages.append(
            f"Hay {len(high_rpe)} sesiones con RPE ≥8 en los últimos 14 días."
        )

    missed_base = [
        s for s, log in recent
        if not is_optional(s) and status_label(log) == "OMITIDO"
    ]
    if missed_base:
        messages.append(
            f"Hay {len(missed_base)} sesión(es) base omitida(s) en los últimos 14 días."
        )

    return messages[:5]

def csv_export():
    out = StringIO()
    cols = [
        "session_date", "week_plan", "workout_type", "workout_name",
        "planned_km", "actual_km", "actual_duration_sec", "real_pace",
        "rpe", "avg_hr", "max_hr", "status", "notes"
    ]
    writer = csv.DictWriter(out, fieldnames=cols)
    writer.writeheader()
    for s in PLAN:
        log = LOG_BY_DATE.get(s["fecha"], {})
        duration = log.get("actual_duration_sec")
        actual_km = log.get("actual_km")
        writer.writerow({
            "session_date": s["fecha"],
            "week_plan": s["semana"],
            "workout_type": s["tipo"],
            "workout_name": s["entrenamiento"],
            "planned_km": s["km"],
            "actual_km": actual_km if actual_km is not None else "",
            "actual_duration_sec": duration if duration is not None else "",
            "real_pace": fmt_pace(duration, actual_km) if duration and actual_km else "",
            "rpe": log.get("rpe", ""),
            "avg_hr": log.get("avg_hr", ""),
            "max_hr": log.get("max_hr", ""),
            "status": log.get("status", "PENDIENTE") if log else "PENDIENTE",
            "notes": log.get("notes", ""),
        })
    return out.getvalue()


# ------------------------------
# SIDEBAR
# ------------------------------
st.sidebar.title("🏃 RunningCoachPro V5")
st.sidebar.caption("Plan importado de RunningCoachPro Sep–Nov 2026")

st.sidebar.caption("📱 V5 optimizada para celular")
with st.sidebar.expander("📲 Añadir a pantalla de inicio"):
    st.markdown(
        "**iPhone (Safari):** Compartir → Añadir a pantalla de inicio.\n\n"
        "**Android (Chrome):** menú ⋮ → Añadir a pantalla principal / Instalar app."
    )

selected_day = st.sidebar.date_input(
    "Fecha a consultar",
    value=today_or_nearest(),
    min_value=date(2026, 8, 25),
    max_value=date(2026, 12, 7),
)

st.sidebar.divider()
st.sidebar.markdown(f"**Corredor:** {NAME}")
st.sidebar.markdown(f"**Objetivo:** {GOAL.title()}")
st.sidebar.markdown(f"**MM actual:** {CURRENT_TIME} · {CURRENT_PACE}/km")
st.sidebar.markdown(f"**Meta:** {TARGET_TIME} · {TARGET_PACE}/km")
st.sidebar.markdown(f"**Carrera:** {RACE_DATE.strftime('%d/%m/%Y')}")

days_to_race = (RACE_DATE - selected_day).days
st.sidebar.metric(
    "Días para la carrera" if days_to_race >= 0 else "Días desde la carrera",
    abs(days_to_race),
)

if DB_READY:
    st.sidebar.success("🟢 Guardado permanente activo")
else:
    st.sidebar.warning("🟠 Modo temporal: falta Supabase")

st.sidebar.download_button(
    "⬇️ Descargar respaldo CSV",
    data=csv_export(),
    file_name=f"runningcoachpro_{NAME.lower()}_registros.csv",
    mime="text/csv",
    use_container_width=True,
)

if APP_PIN and st.sidebar.button("Cerrar sesión", use_container_width=True):
    st.session_state["_authenticated"] = False
    st.rerun()


# ------------------------------
# HEADER
# ------------------------------
st.title("🏃 RunningCoachPro")
st.caption("Plan real de media maratón · Septiembre a Noviembre 2026 · V5 · Mobile")

h1, h2, h3, h4 = st.columns(4)
h1.metric("Marca actual", CURRENT_TIME)
h2.metric("Ritmo actual", f"{CURRENT_PACE} min/km")
h3.metric("Meta", TARGET_TIME)
h4.metric("Ritmo meta", f"{TARGET_PACE} min/km")

total_days = max(1, (RACE_DATE - PLAN_START).days)
elapsed = max(0, min(total_days, (selected_day - PLAN_START).days))
progress = elapsed / total_days
st.progress(progress, text=f"Progreso hacia la media maratón objetivo · {progress*100:.0f}%")


tab_dashboard, tab_today, tab_week, tab_progress, tab_plan, tab_zones, tab_log = st.tabs(
    ["🏠 Dashboard", "📍 Hoy / fecha", "📅 Semana", "📊 Progreso", "🗓️ Plan completo", "🎯 Zonas", "✅ Registro"]
)


# ------------------------------
# DASHBOARD V4
# ------------------------------
with tab_dashboard:
    st.subheader("Panel de rendimiento")

    dm = dashboard_metrics(selected_day)
    level, avg3, recommendation = readiness(selected_day)
    weekly = weekly_dashboard_data(selected_day)
    milestones = milestone_metrics(selected_day)
    alerts = recent_training_alerts(selected_day)

    current_sec = hms_to_seconds(CURRENT_TIME)
    target_sec = hms_to_seconds(TARGET_TIME)
    time_gap = max(0, current_sec - target_sec)
    current_pace_sec = pace_text_to_seconds(CURRENT_PACE)
    target_pace_sec = pace_text_to_seconds(TARGET_PACE)
    pace_gap = (
        current_pace_sec - target_pace_sec
        if current_pace_sec is not None and target_pace_sec is not None
        else None
    )

    days_left = (RACE_DATE - selected_day).days

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        "Cumplimiento base",
        f"{dm['compliance']:.0f}%",
        f"{dm['completed_base']} de {dm['due_base']} sesiones",
    )
    k2.metric(
        "KM reales acumulados",
        f"{dm['actual_km']:.1f}",
        f"Plan vencido: {dm['plan_km_due']:.1f} km",
    )
    k3.metric(
        "RPE promedio",
        "—" if dm["avg_rpe"] is None else f"{dm['avg_rpe']:.1f}/10",
    )
    k4.metric(
        "Días para carrera" if days_left >= 0 else "Días desde carrera",
        abs(days_left),
    )

    st.markdown("### 🎯 Objetivo 1:47:12")
    g1, g2, g3 = st.columns(3)
    g1.metric("Marca de referencia", CURRENT_TIME)
    g2.metric("Meta", TARGET_TIME, f"-{time_gap // 60}:{time_gap % 60:02d}")
    g3.metric(
        "Cambio de ritmo objetivo",
        f"{TARGET_PACE} min/km",
        None if pace_gap is None else f"-{pace_gap} s/km",
    )

    if dm["due_base"] > 0:
        st.progress(
            min(1.0, dm["compliance"] / 100.0),
            text=f"Cumplimiento de sesiones base vencidas · {dm['compliance']:.0f}%",
        )
    else:
        st.info("Aún no hay sesiones base vencidas en la fecha seleccionada.")

    st.markdown("### 📊 PLAN vs REAL por semana")
    km_chart = []
    for row in weekly:
        km_chart.append({"Semana": str(row["week"]), "Serie": "Plan base", "KM": row["plan_km"]})
        km_chart.append({"Semana": str(row["week"]), "Serie": "Real", "KM": row["real_km"]})

    st.vega_lite_chart(
        {
            "data": {"values": km_chart},
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "x": {"field": "Semana", "type": "ordinal", "title": "Semana"},
                "xOffset": {"field": "Serie"},
                "y": {"field": "KM", "type": "quantitative", "title": "Kilómetros"},
                "color": {"field": "Serie", "type": "nominal"},
                "tooltip": [
                    {"field": "Semana", "type": "ordinal"},
                    {"field": "Serie", "type": "nominal"},
                    {"field": "KM", "type": "quantitative", "format": ".1f"},
                ],
            },
        },
        use_container_width=True,
    )

    chart_left, chart_right = st.columns(2)

    with chart_left:
        st.markdown("### 🏃 Evolución de ritmo real")
        run_rows = logged_running_sessions(selected_day)
        pace_types = ["RODAJE", "LARGA", "TEMPO", "SERIES"]
        selected_pace_types = st.multiselect(
            "Tipos incluidos",
            pace_types,
            default=["RODAJE", "LARGA", "TEMPO"],
            key="dashboard_pace_types",
        )

        pace_data = []
        for x in run_rows:
            if x["session"]["tipo"] not in selected_pace_types or x["pace_sec"] is None:
                continue
            pace_data.append({
                "Fecha": x["date"].isoformat(),
                "Ritmo": pace_decimal(x["pace_sec"]),
                "RitmoTexto": fmt_pace(x["seconds"], x["km"]),
                "Tipo": x["session"]["tipo"],
                "Entrenamiento": x["session"]["entrenamiento"],
            })

        if pace_data:
            st.vega_lite_chart(
                {
                    "data": {"values": pace_data},
                    "mark": {"type": "line", "point": True, "tooltip": True},
                    "encoding": {
                        "x": {"field": "Fecha", "type": "temporal", "title": "Fecha"},
                        "y": {
                            "field": "Ritmo",
                            "type": "quantitative",
                            "title": "Ritmo promedio total (min/km)",
                            "scale": {"reverse": True, "zero": False},
                        },
                        "color": {"field": "Tipo", "type": "nominal"},
                        "tooltip": [
                            {"field": "Fecha", "type": "temporal"},
                            {"field": "Entrenamiento", "type": "nominal"},
                            {"field": "RitmoTexto", "type": "nominal", "title": "Ritmo"},
                        ],
                    },
                },
                use_container_width=True,
            )
            st.caption(
                "Es el ritmo promedio de toda la sesión registrada; en series/tempo incluye calentamiento y recuperaciones."
            )
        else:
            st.info("Todavía no hay suficientes sesiones con distancia y duración para graficar ritmo.")

    with chart_right:
        st.markdown("### 🔋 Carga semanal")
        load_data = [
            {"Semana": str(x["week"]), "Carga": x["load"]}
            for x in weekly if x["load"] > 0
        ]
        if load_data:
            st.vega_lite_chart(
                {
                    "data": {"values": load_data},
                    "mark": {"type": "bar", "tooltip": True},
                    "encoding": {
                        "x": {"field": "Semana", "type": "ordinal"},
                        "y": {"field": "Carga", "type": "quantitative", "title": "Índice km × RPE"},
                        "tooltip": [
                            {"field": "Semana", "type": "ordinal"},
                            {"field": "Carga", "type": "quantitative", "format": ".1f"},
                        ],
                    },
                },
                use_container_width=True,
            )
            st.caption(
                "Indicador simple de seguimiento: kilómetros reales × RPE. No es una medición fisiológica ni sustituye evaluación profesional."
            )
        else:
            st.info("Registra sesiones con km y RPE para construir la carga semanal.")

    st.markdown("### 🚦 Estado de carga reciente")
    if level == "VERDE":
        st.success(f"VERDE · RPE reciente {avg3:.1f}" if avg3 is not None else "VERDE")
    elif level == "AMARILLO":
        st.warning(f"AMARILLO · RPE reciente {avg3:.1f}" if avg3 is not None else "AMARILLO")
    elif level == "ROJO":
        st.error(f"ROJO · RPE reciente {avg3:.1f}" if avg3 is not None else "ROJO")
    else:
        st.info("SIN DATOS")
    st.write(recommendation)

    if alerts:
        st.markdown("#### Alertas de seguimiento")
        for msg in alerts:
            st.warning(msg)

    st.markdown("### 🏆 Hitos registrados")
    m1, m2, m3, m4 = st.columns(4)

    longest = milestones["longest"]
    m1.metric(
        "Tirada/sesión más larga",
        "—" if longest is None else f"{longest['km']:.1f} km",
        None if longest is None else longest["date"].strftime("%d/%m"),
    )

    fastest = milestones["fastest_easy"]
    m2.metric(
        "Mejor ritmo rodaje/larga",
        "—" if fastest is None else fmt_pace(fastest["seconds"], fastest["km"]),
        None if fastest is None else fastest["date"].strftime("%d/%m"),
    )

    best_week = milestones["best_week_km"]
    m3.metric(
        "Semana con más KM reales",
        "—" if not best_week or best_week["real_km"] <= 0 else f"{best_week['real_km']:.1f} km",
        None if not best_week or best_week["real_km"] <= 0 else f"Semana {best_week['week']}",
    )

    m4.metric(
        "Tiradas largas completadas",
        milestones["long_runs_completed"],
    )

    st.markdown("### 🧾 Últimos registros")
    recent_records = []
    for s in reversed(PLAN):
        d = date.fromisoformat(s["fecha"])
        if d > selected_day:
            continue
        log = LOG_BY_DATE.get(s["fecha"])
        if not log:
            continue

        recent_records.append({
            "Fecha": d.strftime("%d/%m/%Y"),
            "Tipo": s["tipo"],
            "Sesión": s["entrenamiento"],
            "Plan km": round(float(s["km"]), 1),
            "Real km": round(float(log.get("actual_km") or 0), 1),
            "Ritmo real": fmt_pace(log.get("actual_duration_sec"), log.get("actual_km")),
            "RPE": log.get("rpe"),
            "Estado": status_label(log),
        })
        if len(recent_records) >= 6:
            break

    if recent_records:
        st.dataframe(recent_records, use_container_width=True, hide_index=True)
    else:
        st.caption("Aún no hay registros para mostrar.")


# ------------------------------
# HOY
# ------------------------------
with tab_today:
    st.subheader(f"{DAY_NAMES[selected_day.weekday()]} · {selected_day.strftime('%d/%m/%Y')}")

    s = session_for(selected_day)
    if selected_day < PLAN_START:
        st.info(f"El bloque comienza el {PLAN_START.strftime('%d/%m/%Y')}.")
        nxt = next_session_from(PLAN_START)
        if nxt:
            st.success(
                f"Primera sesión: {date.fromisoformat(nxt['fecha']).strftime('%d/%m')} · "
                f"{nxt['entrenamiento']} · {fmt_km(nxt['km'])}"
            )

    elif selected_day > PLAN_END:
        st.info("El bloque septiembre–noviembre 2026 ya terminó.")

    elif not s:
        st.markdown("## 😴 Descanso / recuperación")
        st.write("No hay sesión programada para esta fecha.")
        nxt = next_session_from(selected_day + timedelta(days=1))
        if nxt:
            nd = date.fromisoformat(nxt["fecha"])
            st.info(
                f"Próxima sesión: {DAY_NAMES[nd.weekday()]} {nd.strftime('%d/%m')} · "
                f"{nxt['entrenamiento']} · {fmt_km(nxt['km'])} · {nxt['ritmo']}"
            )

    else:
        icon = TYPE_ICONS.get(s["tipo"], "🏃")
        st.markdown(f"## {icon} {s['entrenamiento']}")
        st.caption(f"{s['tipo']} · Semana {s['semana']} · {s['intensidad']}")

        a, b, c, d = st.columns(4)
        a.metric("Distancia plan", fmt_km(s["km"]))
        b.metric("Ritmo objetivo", s["ritmo"])
        c.metric("Duración estimada", s["duracion"])
        d.metric("Intensidad", s["intensidad"])

        st.markdown("### 🎯 Objetivo")
        st.write(s["objetivo"])

        st.markdown("### 📋 Sesión")
        st.markdown(f"**Calentamiento:** {s['calentamiento']}")
        st.markdown(f"**Bloque principal:** {s['bloque']}")
        st.markdown(f"**Recuperación:** {s['recuperacion']}")
        st.markdown(f"**Enfriamiento:** {s['enfriamiento']}")

        if s["notas"]:
            st.info(s["notas"])

        existing = LOG_BY_DATE.get(s["fecha"])
        if existing:
            estado = status_label(existing)
            if estado in ("COMPLETADO", "MODIFICADO"):
                st.success(
                    f"{estado} ✅ · Real: {fmt_km(existing.get('actual_km') or 0)} · "
                    f"{fmt_pace(existing.get('actual_duration_sec'), existing.get('actual_km'))} · "
                    f"RPE {existing.get('rpe') or '—'}"
                )
            elif estado == "OMITIDO":
                if is_optional(s):
                    st.warning("Sesión opcional omitida. No debe recuperarse otro día.")
                else:
                    st.warning("Sesión marcada como omitida.")
        else:
            st.caption("Aún no has registrado esta sesión.")


# ------------------------------
# SEMANA
# ------------------------------
with tab_week:
    monday = week_start(selected_day)
    sunday = monday + timedelta(days=6)
    week_no = None
    week_rows = []

    for i in range(7):
        d = monday + timedelta(days=i)
        s = session_for(d)
        if s:
            week_no = s["semana"]
        week_rows.append((d, s))

    suffix = f" · Semana {week_no}" if week_no else ""
    st.subheader(f"{monday.strftime('%d/%m')} – {sunday.strftime('%d/%m/%Y')}{suffix}")

    if week_no:
        wm = week_metrics(week_no)
        x1, x2, x3, x4 = st.columns(4)
        x1.metric("Sesiones base", wm["base_sessions"])
        x2.metric("KM base", f"{wm['base_km']:.1f}")
        x3.metric("KM opcionales", f"{wm['optional_km']:.1f}")
        x4.metric("KM reales", f"{wm['actual_km']:.1f}")

    for d, s in week_rows:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1.0, 2.8, 1.2, 1.2])
            c1.markdown(f"**{DAY_NAMES[d.weekday()]}**")
            c1.caption(d.strftime("%d/%m"))

            if s:
                icon = TYPE_ICONS.get(s["tipo"], "🏃")
                c2.markdown(f"**{icon} {s['entrenamiento']}**")
                c2.caption(f"{s['tipo']} · {s['ritmo']}")
                c3.markdown(f"**{fmt_km(s['km'])}**")
                c3.caption(s["intensidad"])

                log = LOG_BY_DATE.get(s["fecha"])
                estado = status_label(log)
                if estado == "COMPLETADO":
                    c4.success("Completado")
                elif estado == "MODIFICADO":
                    c4.warning("Modificado")
                elif estado == "OMITIDO":
                    c4.warning("Omitido")
                elif is_optional(s):
                    c4.caption("Opcional")
                else:
                    c4.caption("Pendiente")
            elif PLAN_START <= d <= PLAN_END:
                c2.markdown("**😴 Descanso**")
                c2.caption("Sin sesión programada")
                c4.caption("Recuperación")


# ------------------------------
# PROGRESO
# ------------------------------
with tab_progress:
    st.subheader("Progreso PLAN vs REAL")

    dm = dashboard_metrics(selected_day)
    p1, p2, p3, p4 = st.columns(4)
    p1.metric(
        "Sesiones base cumplidas",
        f"{dm['completed_base']} / {dm['due_base']}",
    )
    p2.metric("Cumplimiento", f"{dm['compliance']:.0f}%")
    p3.metric("KM reales acumulados", f"{dm['actual_km']:.1f}")
    p4.metric("RPE promedio", "—" if dm["avg_rpe"] is None else f"{dm['avg_rpe']:.1f}")

    st.markdown("### KM por semana")
    weekly_data = []
    for w in range(1, 14):
        wm = week_metrics(w)
        weekly_data.append({"Semana": str(w), "Serie": "Plan base", "KM": round(wm["base_km"], 2)})
        weekly_data.append({"Semana": str(w), "Serie": "Real", "KM": round(wm["actual_km"], 2)})

    st.vega_lite_chart(
        {
            "data": {"values": weekly_data},
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "x": {"field": "Semana", "type": "ordinal", "title": "Semana"},
                "xOffset": {"field": "Serie"},
                "y": {"field": "KM", "type": "quantitative", "title": "Kilómetros"},
                "color": {"field": "Serie", "type": "nominal"},
                "tooltip": [
                    {"field": "Semana", "type": "ordinal"},
                    {"field": "Serie", "type": "nominal"},
                    {"field": "KM", "type": "quantitative", "format": ".1f"},
                ],
            },
        },
        use_container_width=True,
    )

    rpe_week = []
    for w in range(1, 14):
        vals = []
        for s in PLAN:
            if s["semana"] != w:
                continue
            log = LOG_BY_DATE.get(s["fecha"])
            if log and status_label(log) in ("COMPLETADO", "MODIFICADO") and log.get("rpe") is not None:
                try:
                    vals.append(float(log["rpe"]))
                except Exception:
                    pass
        if vals:
            rpe_week.append({"Semana": w, "RPE": round(sum(vals) / len(vals), 2)})

    st.markdown("### RPE promedio semanal")
    if rpe_week:
        st.vega_lite_chart(
            {
                "data": {"values": rpe_week},
                "mark": {"type": "line", "point": True, "tooltip": True},
                "encoding": {
                    "x": {"field": "Semana", "type": "ordinal"},
                    "y": {"field": "RPE", "type": "quantitative", "scale": {"domain": [1, 10]}},
                    "tooltip": [
                        {"field": "Semana", "type": "ordinal"},
                        {"field": "RPE", "type": "quantitative", "format": ".1f"},
                    ],
                },
            },
            use_container_width=True,
        )
    else:
        st.caption("Aún no hay RPE registrados.")

    st.markdown("### 🚦 Semáforo de carga")
    level, avg3, recommendation = readiness(selected_day)
    if level == "VERDE":
        st.success(f"VERDE · RPE reciente: {avg3:.1f}")
    elif level == "AMARILLO":
        st.warning(f"AMARILLO · RPE reciente: {avg3:.1f}" if avg3 is not None else "AMARILLO")
    elif level == "ROJO":
        st.error(f"ROJO · RPE reciente: {avg3:.1f}" if avg3 is not None else "ROJO")
    else:
        st.info("SIN DATOS")
    st.write(recommendation)

    st.caption(
        "El semáforo no cambia automáticamente el plan del Excel; solo resume tus registros recientes "
        "para ayudarte a decidir si conviene mantener, omitir extras o revisar la carga."
    )


# ------------------------------
# PLAN COMPLETO
# ------------------------------
with tab_plan:
    st.subheader("Plan completo · 13 semanas")

    f1, f2 = st.columns(2)
    types = ["TODOS"] + sorted({s["tipo"] for s in PLAN})
    selected_type = f1.selectbox("Filtrar por tipo", types)
    selected_week = f2.selectbox("Filtrar por semana", ["TODAS"] + list(range(1, 14)))

    rows = []
    for s in PLAN:
        if selected_type != "TODOS" and s["tipo"] != selected_type:
            continue
        if selected_week != "TODAS" and s["semana"] != selected_week:
            continue

        log = LOG_BY_DATE.get(s["fecha"])
        rows.append({
            "Fecha": date.fromisoformat(s["fecha"]).strftime("%d/%m/%Y"),
            "Semana": s["semana"],
            "Tipo": s["tipo"],
            "Entrenamiento": s["entrenamiento"],
            "KM plan": round(s["km"], 1),
            "Ritmo": s["ritmo"],
            "KM real": log.get("actual_km") if log else None,
            "RPE": log.get("rpe") if log else None,
            "Estado": status_label(log),
        })

    st.dataframe(rows, use_container_width=True, hide_index=True)


# ------------------------------
# ZONAS
# ------------------------------
with tab_zones:
    st.subheader("Zonas de ritmo del documento")
    for zone_name, pace, note in ZONES:
        with st.container(border=True):
            z1, z2 = st.columns([1.2, 2])
            z1.markdown(f"**{zone_name}**")
            z2.markdown(f"**{pace}**")
            z2.caption(note)

    st.info(
        f"La tirada larga usa como referencia tu ruta habitual de aproximadamente "
        f"{LONG_ROUTE_ELEVATION} m D+. En subidas, el documento prioriza esfuerzo sobre ritmo."
    )
    st.caption(f"Series: terreno plano o caminadora al {TREADMILL_INCLINE:g}%.")


# ------------------------------
# REGISTRO
# ------------------------------
with tab_log:
    st.subheader("Registrar ejecución")

    s = session_for(selected_day)
    if not s:
        st.info("Selecciona una fecha con sesión programada.")
    else:
        existing = LOG_BY_DATE.get(s["fecha"], {})
        default_status = str(existing.get("status") or "COMPLETADO").upper()
        if default_status not in ("COMPLETADO", "MODIFICADO", "OMITIDO"):
            default_status = "COMPLETADO"

        st.caption(
            f"Plan: {s['entrenamiento']} · {fmt_km(s['km'])} · {s['ritmo']} · {s['duracion']}"
        )

        with st.form(f"record_{s['fecha']}"):
            r1, r2, r3 = st.columns(3)

            km_default = float(existing.get("actual_km") if existing.get("actual_km") is not None else s["km"])
            actual_km = r1.number_input(
                "Distancia real (km)",
                min_value=0.0,
                max_value=60.0,
                value=km_default,
                step=0.1,
            )

            duration_default = (
                fmt_duration(existing.get("actual_duration_sec"))
                if existing.get("actual_duration_sec") is not None
                else planned_duration_default(s)
            )
            duration_text = r2.text_input(
                "Duración real (HH:MM:SS)",
                value=duration_default,
                help="También acepta MM:SS o un número de minutos.",
            )

            rpe = r3.slider(
                "RPE",
                min_value=1,
                max_value=10,
                value=int(existing.get("rpe") or 5),
            )

            q1, q2, q3 = st.columns(3)
            avg_hr = q1.number_input(
                "FC media (opcional)",
                min_value=0,
                max_value=230,
                value=int(existing.get("avg_hr") or 0),
                step=1,
            )
            max_hr = q2.number_input(
                "FC máxima (opcional)",
                min_value=0,
                max_value=240,
                value=int(existing.get("max_hr") or 0),
                step=1,
            )
            status = q3.selectbox(
                "Estado",
                ["COMPLETADO", "MODIFICADO", "OMITIDO"],
                index=["COMPLETADO", "MODIFICADO", "OMITIDO"].index(default_status),
            )

            notes = st.text_area(
                "Observaciones",
                value=str(existing.get("notes") or ""),
                placeholder="Sensaciones, sueño, clima, molestias, cambios realizados, etc.",
            )

            save = st.form_submit_button("💾 Guardar registro", use_container_width=True)

        if save:
            seconds, error = parse_duration(duration_text)
            if error:
                st.error(error)
            else:
                if status == "OMITIDO":
                    actual_km_to_save = 0.0
                    seconds_to_save = 0
                else:
                    actual_km_to_save = float(actual_km)
                    seconds_to_save = int(seconds or 0)

                record = {
                    "runner": NAME,
                    "session_date": s["fecha"],
                    "week_plan": s["semana"],
                    "workout_type": s["tipo"],
                    "workout_name": s["entrenamiento"],
                    "planned_km": float(s["km"]),
                    "actual_km": actual_km_to_save,
                    "actual_duration_sec": seconds_to_save,
                    "rpe": int(rpe),
                    "avg_hr": int(avg_hr) if avg_hr else None,
                    "max_hr": int(max_hr) if max_hr else None,
                    "status": status,
                    "notes": notes.strip(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }

                ok, err = save_log(record)
                if ok:
                    st.success("Registro guardado correctamente ✅")
                    st.rerun()
                else:
                    st.error(f"No se pudo guardar: {err}")

        current = LOG_BY_DATE.get(s["fecha"])
        if current:
            st.divider()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Estado", status_label(current))
            c2.metric("Real", fmt_km(current.get("actual_km") or 0))
            c3.metric(
                "Ritmo real",
                fmt_pace(current.get("actual_duration_sec"), current.get("actual_km")),
            )
            plan_diff = float(current.get("actual_km") or 0) - float(s["km"] or 0)
            c4.metric("Diferencia vs plan", f"{plan_diff:+.1f} km")

            if is_optional(s) and status_label(current) == "OMITIDO":
                st.info("Correcto según el documento: un viernes opcional omitido no se recupera otro día.")


if not DB_READY:
    st.warning(
        "La V5 está funcionando en modo temporal. Para que los registros sobrevivan a reinicios de Streamlit, "
        "configura Supabase con los archivos incluidos en el paquete V3."
    )

st.divider()
st.caption(
    "Plan basado directamente en RunningCoachPro_Sep_Nov_2026.xlsx. "
    "El semáforo es una ayuda de seguimiento y no sustituye evaluación profesional. "
    "Ante dolor agudo, mareos, lesión o síntomas anormales, suspende el entrenamiento y busca orientación profesional."
)
