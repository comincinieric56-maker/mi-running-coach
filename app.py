import streamlit as st
from datetime import date, datetime, timedelta

st.set_page_config(
    page_title="RunningCoachPro",
    page_icon="🏃",
    layout="wide",
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR '
           'LADO | HIP THRUST 3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 '
            '| CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES '
           'DE ESA SEMANA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR '
           'LADO | HIP THRUST 3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 '
            '| CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES '
           'DE ESA SEMANA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR '
           'LADO | HIP THRUST 3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 '
            '| CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES '
           'DE ESA SEMANA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR '
           'LADO | HIP THRUST 3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 '
            '| CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES '
           'DE ESA SEMANA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR '
           'LADO | HIP THRUST 3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR '
           'LADO | HIP THRUST 3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 '
            '| CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES '
           'DE ESA SEMANA.'},
 {'fecha': '2026-11-15',
  'semana': 11,
  'tipo': 'LARGA',
  'entrenamiento': 'TIRADA LARGA 18 KM',
  'descripcion': '18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 5 KM CERCA DE RITMO MM OBJETIVO (5:05 '
                 'MIN/KM) SOLO SI LAS SENSACIONES SON BUENAS.',
  'km': 18.0,
  'ritmo': '5:52-6:08 min/km',
  'duracion': '1:45:36',
  'intensidad': 'MEDIA',
  'objetivo': 'RESISTENCIA AERÓBICA, DURABILIDAD Y ESPECIFICIDAD PARA MEDIA MARATÓN',
  'calentamiento': 'PRIMEROS 2 KM ESPECIALMENTE CONTROLADOS',
  'bloque': '18 km | RUTA APROX. 157 M D+ | ÚLTIMOS 5 KM CERCA DE RITMO MM OBJETIVO (5:05 MIN/KM) SOLO SI LAS '
            'SENSACIONES SON BUENAS',
  'recuperacion': 'NO APLICA',
  'enfriamiento': '5-10 min caminando + movilidad',
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'ESFUERZO CONTROLADO. NO CONVERTIR EL TEMPO EN UNA CARRERA. FUERZA B 20-25 MIN: ZANCADA/BÚLGARA 3x8 POR '
           'LADO | HIP THRUST 3x8-10 | SÓLEO 3x12-15 | ESTABILIDAD DE CADERA + CORE. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'notas': 'EL RITMO ES UNA REFERENCIA PARA LA RUTA HABITUAL. EN SUBIDAS PRIORIZAR ESFUERZO Y NO FORZAR EL RITMO. NO '
           'COMPENSAR DESCENSOS CORRIENDO EXCESIVAMENTE RÁPIDO.'},
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
  'notas': 'SERIES EXCLUSIVAMENTE EN TERRENO PLANO O CAMINADORA. NO COMPENSAR REPETICIONES PERDIDAS. FUERZA A 20-25 '
           'MIN: SENTADILLA 3x6-8 | PESO MUERTO RUMANO 3x8 | GEMELOS 3x12-15 | CORE 3 SERIES. RIR 2-3.'},
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
  'notas': 'POSTURNO. NO REALIZAR SI EL DESCANSO HA SIDO INSUFICIENTE, EXISTE FATIGA MARCADA, PESO EXCESIVO EN PIERNAS '
           'O RPE BASAL ELEVADO. OMITIR ESTA SESIÓN NO DEBE RECUPERARSE OTRO DÍA.'},
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
  'bloque': 'BÚLGARA 3x8/LADO | HIP THRUST 3x8-10 | PESO MUERTO UNILATERAL 3x8/LADO | SÓLEO 3x12-15 | GEMELOS 3x12-15 '
            '| CORE 3 SERIES',
  'recuperacion': '60-90 s entre series',
  'enfriamiento': 'MOVILIDAD DE TOBILLO, CADERA Y CADENA POSTERIOR',
  'notas': 'NO ENTRENAR AL FALLO. MANTENER 2-3 REPETICIONES EN RESERVA. ESTA SESIÓN SUSTITUYE LA FUERZA B DEL JUEVES '
           'DE ESA SEMANA.'},
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


def fmt_km(km):
    if abs(km - round(km)) < 1e-9:
        return f"{int(round(km))} km"
    return f"{km:.1f} km"


def session_for(day):
    return SESSION_BY_DATE.get(day.isoformat())


def plan_status(day):
    if day < PLAN_START:
        return "PRE"
    if day > PLAN_END:
        return "POST"
    return "ACTIVE"


def week_start(day):
    return day - timedelta(days=day.weekday())


def next_session_from(day):
    future = [s for s in PLAN if date.fromisoformat(s["fecha"]) >= day]
    return future[0] if future else None


def base_week_metrics(week_number):
    rows = [s for s in PLAN if s["semana"] == week_number]
    base = [s for s in rows if s["intensidad"] != "OPCIONAL"]
    optional = [s for s in rows if s["intensidad"] == "OPCIONAL"]
    return {
        "sesiones_base": len(base),
        "km_base": sum(s["km"] for s in base),
        "km_total_con_opcional": sum(s["km"] for s in rows),
        "opcional": optional,
    }


def completed_key(fecha):
    return f"completed_{fecha}"


def record_key(fecha):
    return f"record_{fecha}"


def is_completed(fecha):
    return st.session_state.get(completed_key(fecha), False)


def completed_count():
    return sum(1 for s in PLAN if is_completed(s["fecha"]))


def completed_km():
    total = 0.0
    for s in PLAN:
        rec = st.session_state.get(record_key(s["fecha"]), {})
        if is_completed(s["fecha"]):
            total += float(rec.get("km_real", s["km"]) or 0)
    return total


def show_session_details(s):
    icon = TYPE_ICONS.get(s["tipo"], "🏃")
    st.markdown(f"## {icon} {s['entrenamiento']}")
    st.caption(f"{s['tipo']} · Semana {s['semana']} · Intensidad {s['intensidad']}")

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

    if s["descripcion"]:
        with st.expander("Descripción completa"):
            st.write(s["descripcion"])

    if s["notas"]:
        st.info(s["notas"])

    if s["tipo"] == "RODAJE":
        st.warning(
            "Este rodaje es OPCIONAL. Si el descanso posturno fue insuficiente, hay fatiga marcada, "
            "piernas muy pesadas o RPE basal elevado, se omite. No se recupera otro día."
        )

    if s["tipo"] == "SERIES":
        st.caption(
            f"Series en terreno plano o caminadora al {TREADMILL_INCLINE:g}% de inclinación, tal como indica el plan."
        )


def show_rest(day):
    st.markdown("## 😴 Descanso / recuperación")
    if day.weekday() in (0, 2):
        st.write("Día de descanso estructural del plan. No hay carrera programada.")
    else:
        st.write("No hay una sesión programada para esta fecha.")

    nxt = next_session_from(day + timedelta(days=1))
    if nxt:
        nd = date.fromisoformat(nxt["fecha"])
        st.info(
            f"Próxima sesión: {DAY_NAMES[nd.weekday()]} {nd.strftime('%d/%m')} · "
            f"{nxt['entrenamiento']} · {fmt_km(nxt['km'])} · {nxt['ritmo']}"
        )


# ---------------- SIDEBAR ----------------
st.sidebar.title("🏃 RunningCoachPro")
st.sidebar.caption("Plan importado de tu RunningCoachPro Sep–Nov 2026")

today = date.today()
default_day = today
if today < PLAN_START:
    default_day = today
elif today > PLAN_END:
    default_day = PLAN_END

selected_day = st.sidebar.date_input(
    "Fecha a consultar",
    value=default_day,
    min_value=date(2026, 8, 25),
    max_value=date(2026, 12, 7),
)

st.sidebar.divider()
st.sidebar.markdown(f"**Corredor:** {NAME}")
st.sidebar.markdown(f"**Objetivo:** {GOAL.title()}")
st.sidebar.markdown(f"**MM actual:** {CURRENT_TIME} · {CURRENT_PACE}/km")
st.sidebar.markdown(f"**Objetivo:** {TARGET_TIME} · {TARGET_PACE}/km")
st.sidebar.markdown(f"**Carrera objetivo:** {RACE_DATE.strftime('%d/%m/%Y')}")

days_to_race = (RACE_DATE - selected_day).days
if days_to_race >= 0:
    st.sidebar.metric("Días para la carrera", days_to_race)
else:
    st.sidebar.metric("Días desde la carrera", abs(days_to_race))

st.sidebar.caption(
    "Los registros de completado/RPE de esta V2 se guardan solo durante la sesión actual de la app."
)

# ---------------- HEADER ----------------
st.title("🏃 RunningCoachPro")
st.caption("Tu plan real de media maratón · Septiembre a Noviembre 2026")

h1, h2, h3, h4 = st.columns(4)
h1.metric("Marca actual", CURRENT_TIME)
h2.metric("Ritmo actual", f"{CURRENT_PACE} min/km")
h3.metric("Meta", TARGET_TIME)
h4.metric("Ritmo meta", f"{TARGET_PACE} min/km")

total_days = (RACE_DATE - PLAN_START).days
elapsed = max(0, min(total_days, (selected_day - PLAN_START).days))
progress = elapsed / total_days if total_days else 0
st.progress(progress, text=f"Progreso hacia la media maratón objetivo · {progress*100:.0f}%")

tab_today, tab_week, tab_plan, tab_zones, tab_log = st.tabs(
    ["📍 Hoy / fecha", "📅 Semana", "🗓️ Plan completo", "🎯 Zonas", "✅ Registro"]
)

# ---------------- TAB: HOY ----------------
with tab_today:
    st.subheader(
        f"{DAY_NAMES[selected_day.weekday()]} · {selected_day.strftime('%d/%m/%Y')}"
    )

    status = plan_status(selected_day)
    if status == "PRE":
        st.markdown("## 🟦 Preparación previa al bloque")
        st.write(
            f"El bloque comienza el {PLAN_START.strftime('%d/%m/%Y')}. "
            "Hoy no hay una sesión del plan programada."
        )
        nxt = next_session_from(PLAN_START)
        if nxt:
            nd = date.fromisoformat(nxt["fecha"])
            st.success(
                f"Primera sesión: {DAY_NAMES[nd.weekday()]} {nd.strftime('%d/%m')} · "
                f"{nxt['entrenamiento']} · {fmt_km(nxt['km'])} · {nxt['ritmo']}"
            )
    elif status == "POST":
        st.markdown("## 🏁 Bloque finalizado")
        st.write("El bloque septiembre–noviembre 2026 ya terminó.")
    else:
        s = session_for(selected_day)
        if s:
            show_session_details(s)

            st.divider()
            done = is_completed(s["fecha"])
            if done:
                st.success("Sesión marcada como completada ✅")
            else:
                if st.button("✅ Marcar esta sesión como completada", use_container_width=True):
                    st.session_state[completed_key(s["fecha"])] = True
                    st.rerun()
        else:
            show_rest(selected_day)

# ---------------- TAB: SEMANA ----------------
with tab_week:
    monday = week_start(selected_day)
    sunday = monday + timedelta(days=6)

    week_rows = []
    week_no = None
    for i in range(7):
        d = monday + timedelta(days=i)
        s = session_for(d)
        if s:
            week_no = s["semana"]
            week_rows.append((d, s))
        else:
            week_rows.append((d, None))

    title_suffix = f" · Semana {week_no}" if week_no else ""
    st.subheader(
        f"{monday.strftime('%d/%m')} – {sunday.strftime('%d/%m/%Y')}{title_suffix}"
    )

    if week_no:
        met = base_week_metrics(week_no)
        x1, x2, x3 = st.columns(3)
        x1.metric("Sesiones base", met["sesiones_base"])
        x2.metric("KM base", f"{met['km_base']:.1f}")
        x3.metric("KM con rodaje opcional", f"{met['km_total_con_opcional']:.1f}")

    for d, s in week_rows:
        with st.container(border=True):
            c1, c2, c3 = st.columns([1.1, 2.6, 1.2])
            c1.markdown(f"**{DAY_NAMES[d.weekday()]}**")
            c1.caption(d.strftime("%d/%m"))

            if s:
                icon = TYPE_ICONS.get(s["tipo"], "🏃")
                c2.markdown(f"**{icon} {s['entrenamiento']}**")
                c2.caption(f"{s['tipo']} · {s['ritmo']}")
                c3.markdown(f"**{fmt_km(s['km'])}**")
                if is_completed(s["fecha"]):
                    c3.success("Completado")
                elif s["intensidad"] == "OPCIONAL":
                    c3.warning("Opcional")
                else:
                    c3.caption(s["intensidad"])
            elif PLAN_START <= d <= PLAN_END:
                c2.markdown("**😴 Descanso**")
                c2.caption("Sin sesión programada")
                c3.caption("Recuperación")
            else:
                c2.caption("Fuera del bloque")

# ---------------- TAB: PLAN COMPLETO ----------------
with tab_plan:
    st.subheader("Plan completo · 13 semanas")

    filt1, filt2 = st.columns(2)
    types = ["TODOS"] + sorted({s["tipo"] for s in PLAN})
    selected_type = filt1.selectbox("Filtrar por tipo", types)
    selected_week = filt2.selectbox("Filtrar por semana", ["TODAS"] + list(range(1, 14)))

    table = []
    for s in PLAN:
        if selected_type != "TODOS" and s["tipo"] != selected_type:
            continue
        if selected_week != "TODAS" and s["semana"] != selected_week:
            continue

        d = date.fromisoformat(s["fecha"])
        table.append({
            "Fecha": d.strftime("%d/%m/%Y"),
            "Día": DAY_NAMES[d.weekday()],
            "Semana": s["semana"],
            "Tipo": s["tipo"],
            "Entrenamiento": s["entrenamiento"],
            "KM": round(s["km"], 1),
            "Ritmo": s["ritmo"],
            "Intensidad": s["intensidad"],
            "Estado": "✅ Completado" if is_completed(s["fecha"]) else "Pendiente",
        })

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "KM": st.column_config.NumberColumn("KM", format="%.1f"),
        },
    )

    base = [s for s in PLAN if s["intensidad"] != "OPCIONAL"]
    optional = [s for s in PLAN if s["intensidad"] == "OPCIONAL"]
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Sesiones plan", len(PLAN))
    p2.metric("KM totales", f"{sum(s['km'] for s in PLAN):.1f}")
    p3.metric("Sesiones base", len(base))
    p4.metric("KM base", f"{sum(s['km'] for s in base):.1f}")

# ---------------- TAB: ZONAS ----------------
with tab_zones:
    st.subheader("Zonas de ritmo del documento")
    for name, pace, note in ZONES:
        with st.container(border=True):
            z1, z2 = st.columns([1.2, 2])
            z1.markdown(f"**{name}**")
            z2.markdown(f"**{pace}**")
            z2.caption(note)

    st.info(
        f"La tirada larga está referenciada a tu ruta habitual de aproximadamente "
        f"{LONG_ROUTE_ELEVATION} m D+. En subidas, el plan prioriza el esfuerzo sobre el ritmo."
    )

# ---------------- TAB: REGISTRO ----------------
with tab_log:
    st.subheader("Registrar ejecución")

    s = session_for(selected_day)
    if not s:
        st.info("Selecciona una fecha que tenga una sesión programada para registrar datos.")
    else:
        existing = st.session_state.get(record_key(s["fecha"]), {})

        with st.form(f"log_{s['fecha']}"):
            r1, r2, r3 = st.columns(3)
            km_real = r1.number_input(
                "Distancia real (km)",
                min_value=0.0,
                max_value=60.0,
                value=float(existing.get("km_real", s["km"])),
                step=0.1,
            )
            dur_min = r2.number_input(
                "Duración real (min)",
                min_value=0,
                max_value=600,
                value=int(existing.get("dur_min", 0)),
                step=1,
            )
            rpe = r3.slider(
                "RPE",
                1, 10,
                value=int(existing.get("rpe", 5)),
            )

            f1, f2 = st.columns(2)
            fc_media = f1.number_input(
                "FC media (opcional)",
                min_value=0,
                max_value=230,
                value=int(existing.get("fc_media", 0)),
                step=1,
            )
            fc_max = f2.number_input(
                "FC máxima (opcional)",
                min_value=0,
                max_value=240,
                value=int(existing.get("fc_max", 0)),
                step=1,
            )

            obs = st.text_area(
                "Observaciones",
                value=str(existing.get("obs", "")),
                placeholder="Sensaciones, sueño, molestias, clima, etc.",
            )

            save = st.form_submit_button("Guardar registro", use_container_width=True)

        if save:
            st.session_state[record_key(s["fecha"])] = {
                "km_real": km_real,
                "dur_min": dur_min,
                "rpe": rpe,
                "fc_media": fc_media,
                "fc_max": fc_max,
                "obs": obs,
            }
            st.session_state[completed_key(s["fecha"])] = True
            st.success("Registro guardado y sesión marcada como completada ✅")
            st.rerun()

        if is_completed(s["fecha"]):
            st.success("Esta sesión está completada.")
            if st.button("↩️ Desmarcar completado"):
                st.session_state[completed_key(s["fecha"])] = False
                st.rerun()

    st.divider()
    q1, q2 = st.columns(2)
    q1.metric("Sesiones completadas (esta sesión de app)", completed_count())
    q2.metric("KM registrados/completados", f"{completed_km():.1f}")

st.divider()
st.caption(
    "Plan basado en el archivo RunningCoachPro_Sep_Nov_2026. "
    "El rodaje opcional no debe compensarse si se omite. "
    "Ante dolor agudo, mareos, síntomas anormales o lesión, suspende el entrenamiento y consulta a un profesional."
)
