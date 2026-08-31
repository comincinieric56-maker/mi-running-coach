import streamlit as st
from datetime import date
import random

st.set_page_config(
    page_title="Mi Running Coach",
    page_icon="🏃",
    layout="centered",
)

# -----------------------------
# Helpers
# -----------------------------
GOAL_LABELS = {
    "5K": "5K",
    "10K": "10K",
    "21K": "Media maratón (21K)",
    "42K": "Maratón (42K)",
    "fitness": "Mejorar condición física",
}

LEVEL_MULTIPLIER = {
    "Principiante": 0.80,
    "Intermedio": 1.00,
    "Avanzado": 1.18,
}

GOAL_MULTIPLIER = {
    "5K": 0.90,
    "10K": 1.00,
    "21K": 1.12,
    "42K": 1.25,
    "fitness": 0.85,
}

RUN_DAY_MAP = {
    2: [1, 5],             # martes, sábado
    3: [1, 3, 6],          # martes, jueves, domingo
    4: [0, 2, 4, 6],       # lunes, miércoles, viernes, domingo
    5: [0, 1, 3, 4, 6],    # lunes, martes, jueves, viernes, domingo
    6: [0, 1, 2, 3, 4, 6], # descanso sábado
    7: [0, 1, 2, 3, 4, 5, 6],
}

DAY_NAMES = [
    "Lunes", "Martes", "Miércoles", "Jueves",
    "Viernes", "Sábado", "Domingo"
]


def clamp(value, low, high):
    return max(low, min(high, value))


def km_round(value):
    return round(value * 2) / 2


def today_seed(profile):
    p = f"{date.today().isoformat()}-{profile['goal']}-{profile['level']}-{profile['days']}-{profile['weekly_km']}"
    return sum(ord(ch) for ch in p)


def workout_type_for_today(profile):
    weekday = date.today().weekday()
    run_days = RUN_DAY_MAP[profile["days"]]

    if weekday not in run_days:
        return "Descanso"

    position = run_days.index(weekday)

    # El último día programado de la semana es la tirada larga.
    if position == len(run_days) - 1 and profile["days"] >= 3:
        return "Tirada larga"

    # Una sesión de calidad para 2-3 días; dos para 4+.
    if profile["days"] <= 3:
        quality_positions = {0}
    else:
        quality_positions = {1, max(0, len(run_days) - 3)}

    if position in quality_positions:
        return "Calidad"

    return "Suave"


def build_workout(profile, feedback="normal"):
    seed = today_seed(profile) + {"fácil": 7, "difícil": -7}.get(feedback, 0)
    rng = random.Random(seed)

    wtype = workout_type_for_today(profile)
    weekly_km = float(profile["weekly_km"])
    level_mult = LEVEL_MULTIPLIER[profile["level"]]
    goal_mult = GOAL_MULTIPLIER[profile["goal"]]

    adjustment = 1.0
    if feedback == "fácil":
        adjustment = 1.05
    elif feedback == "difícil":
        adjustment = 0.90

    base_daily = weekly_km / max(profile["days"], 1)
    target = clamp(base_daily * level_mult * goal_mult * adjustment, 3.0, 24.0)

    if wtype == "Descanso":
        return {
            "title": "Descanso / recuperación",
            "badge": "RECUPERACIÓN",
            "summary": "Hoy no tienes carrera programada.",
            "distance": "0 km",
            "duration": "20–35 min opcionales",
            "effort": "Muy suave · RPE 1–2/10",
            "steps": [
                "Caminata suave de 20–30 min si te apetece.",
                "5–10 min de movilidad de tobillos, cadera y espalda.",
                "Hidrátate y prioriza el sueño.",
            ],
            "note": "Si tienes dolor agudo, mareos o síntomas fuera de lo normal, no entrenes y busca orientación profesional.",
        }

    if wtype == "Suave":
        km = km_round(clamp(target * 0.90, 3.0, 16.0))
        return {
            "title": "Rodaje suave",
            "badge": "SUAVE",
            "summary": "Construye base aeróbica sin acumular demasiada fatiga.",
            "distance": f"{km:g} km",
            "duration": "Ritmo conversacional",
            "effort": "RPE 3–4/10",
            "steps": [
                "5–8 min caminando o trotando muy suave.",
                f"Corre {km:g} km a un ritmo en el que puedas hablar en frases completas.",
                "Termina con 5 min muy suaves y movilidad ligera.",
            ],
            "note": "No conviertas el rodaje suave en una carrera. Debe sentirse controlado.",
        }

    if wtype == "Tirada larga":
        long_km = km_round(clamp(weekly_km * 0.28 * adjustment, 5.0, 30.0))
        if profile["goal"] == "42K":
            long_km = km_round(clamp(weekly_km * 0.30 * adjustment, 7.0, 32.0))
        return {
            "title": "Tirada larga",
            "badge": "RESISTENCIA",
            "summary": "El entrenamiento principal para mejorar resistencia.",
            "distance": f"{long_km:g} km",
            "duration": "Ritmo cómodo y estable",
            "effort": "RPE 3–5/10",
            "steps": [
                "10 min muy suaves para entrar en calor.",
                f"Completa {long_km:g} km a ritmo cómodo.",
                "Los últimos 10 min pueden ser un poco más alegres solo si te sientes bien.",
                "Camina 5 min al terminar.",
            ],
            "note": "Para tiradas largas, aumenta distancia gradualmente de una semana a otra.",
        }

    # Calidad
    options = ["Intervalos", "Tempo", "Fartlek"]
    quality = rng.choice(options)

    if profile["level"] == "Principiante":
        quality = rng.choice(["Fartlek", "Tempo"])

    if quality == "Intervalos":
        reps = {"Principiante": 4, "Intermedio": 6, "Avanzado": 8}[profile["level"]]
        rep_m = 400 if profile["goal"] in ("5K", "10K", "fitness") else 800
        total_km = km_round(clamp(target, 4.5, 14.0))
        return {
            "title": f"Intervalos · {reps} × {rep_m} m",
            "badge": "CALIDAD",
            "summary": "Trabaja velocidad y economía de carrera.",
            "distance": f"≈ {total_km:g} km total",
            "duration": "Incluye calentamiento y vuelta a la calma",
            "effort": "Repeticiones: RPE 7–8/10",
            "steps": [
                "12–15 min de trote suave + movilidad dinámica.",
                f"{reps} × {rep_m} m a esfuerzo fuerte pero controlado.",
                "Recupera 90–120 s trotando o caminando entre repeticiones.",
                "10 min de trote muy suave para terminar.",
            ],
            "note": "La última repetición debería sentirse exigente, pero no como un sprint máximo.",
        }

    if quality == "Tempo":
        tempo_min = {"Principiante": 12, "Intermedio": 20, "Avanzado": 28}[profile["level"]]
        if profile["goal"] in ("21K", "42K"):
            tempo_min += 5
        total_km = km_round(clamp(target, 4.0, 15.0))
        return {
            "title": f"Tempo · {tempo_min} min",
            "badge": "UMBRAL",
            "summary": "Mejora tu capacidad de sostener un ritmo exigente.",
            "distance": f"≈ {total_km:g} km total",
            "duration": f"{tempo_min} min de bloque tempo",
            "effort": "Tempo: RPE 6–7/10",
            "steps": [
                "12 min de trote suave.",
                f"{tempo_min} min a esfuerzo sostenido: fuerte, pero sin ir al límite.",
                "10 min muy suaves para terminar.",
            ],
            "note": "Durante el tempo deberías poder decir frases muy cortas, no mantener una conversación.",
        }

    # Fartlek
    reps = {"Principiante": 6, "Intermedio": 8, "Avanzado": 10}[profile["level"]]
    total_km = km_round(clamp(target, 4.0, 14.0))
    return {
        "title": f"Fartlek · {reps} cambios",
        "badge": "CALIDAD",
        "summary": "Un entrenamiento flexible para trabajar cambios de ritmo.",
        "distance": f"≈ {total_km:g} km total",
        "duration": "Cambios de 1 min",
        "effort": "Cambios: RPE 7/10",
        "steps": [
            "12 min de trote suave.",
            f"{reps} × (1 min rápido + 2 min suave).",
            "Corre rápido con buena técnica, sin sprintar.",
            "10 min muy suaves para terminar.",
        ],
        "note": "Si pierdes la técnica o no recuperas en los tramos suaves, reduce la intensidad.",
    }


# -----------------------------
# UI
# -----------------------------
st.title("🏃 Mi Running Coach")
st.caption("Tu entrenamiento del día, ajustado a tu objetivo y carga semanal.")

with st.sidebar:
    st.header("Tu perfil")
    with st.form("profile_form"):
        goal = st.selectbox(
            "Objetivo",
            options=list(GOAL_LABELS.keys()),
            format_func=lambda x: GOAL_LABELS[x],
            index=1,
        )
        level = st.selectbox(
            "Nivel",
            ["Principiante", "Intermedio", "Avanzado"],
            index=0,
        )
        days = st.slider("Días que corres por semana", 2, 7, 3)
        weekly_km = st.number_input(
            "Kilómetros actuales por semana",
            min_value=5.0,
            max_value=160.0,
            value=20.0,
            step=1.0,
        )
        save = st.form_submit_button("Guardar perfil", use_container_width=True)

    if save or "profile" not in st.session_state:
        st.session_state.profile = {
            "goal": goal,
            "level": level,
            "days": days,
            "weekly_km": weekly_km,
        }

profile = st.session_state.profile

st.subheader(f"{DAY_NAMES[date.today().weekday()]} · {date.today().strftime('%d/%m/%Y')}")

c1, c2, c3 = st.columns(3)
c1.metric("Objetivo", GOAL_LABELS[profile["goal"]])
c2.metric("Nivel", profile["level"])
c3.metric("Carga", f"{profile['weekly_km']:g} km/sem")

if "feedback" not in st.session_state:
    st.session_state.feedback = "normal"

workout = build_workout(profile, st.session_state.feedback)

st.markdown(f"### {workout['title']}")
st.markdown(f"**{workout['badge']}** · {workout['summary']}")

m1, m2, m3 = st.columns(3)
m1.metric("Distancia", workout["distance"])
m2.metric("Duración", workout["duration"])
m3.metric("Esfuerzo", workout["effort"])

st.markdown("#### Sesión")
for i, step in enumerate(workout["steps"], start=1):
    st.write(f"**{i}.** {step}")

st.info(workout["note"])

st.markdown("#### ¿Cómo se siente la carga?")
b1, b2, b3 = st.columns(3)

with b1:
    if st.button("😌 Muy fácil", use_container_width=True):
        st.session_state.feedback = "fácil"
        st.rerun()

with b2:
    if st.button("👍 Bien", use_container_width=True):
        st.session_state.feedback = "normal"
        st.rerun()

with b3:
    if st.button("🥵 Muy difícil", use_container_width=True):
        st.session_state.feedback = "difícil"
        st.rerun()

st.divider()

if st.button("✅ Marcar entrenamiento como completado", use_container_width=True):
    st.session_state.completed = date.today().isoformat()
    st.success("¡Entrenamiento marcado como completado! 🙌")

if st.session_state.get("completed") == date.today().isoformat():
    st.success("Hoy ya completaste tu sesión ✅")

st.caption(
    "Esta versión genera recomendaciones generales de entrenamiento. "
    "Si tienes una lesión, una condición médica o síntomas durante el ejercicio, "
    "consulta a un profesional de salud o entrenamiento."
)
