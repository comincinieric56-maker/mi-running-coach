
import streamlit as st
from datetime import date, datetime, timedelta, timezone
import math
import re
from supabase import create_client

st.set_page_config(
    page_title="RunningCoachPro",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# Diseño responsive web + celular
# ============================================================
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1180px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {
        min-height: 48px;
        border-radius: 12px;
        font-weight: 600;
    }
    div[data-baseweb="input"] input,
    textarea {
        min-height: 44px;
        font-size: 16px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: .25rem;
        overflow-x: auto;
        white-space: nowrap;
    }
    .stTabs [data-baseweb="tab"] {
        min-height: 44px;
        flex: 0 0 auto;
    }
    [data-testid="stDataFrame"] {
        overflow-x: auto;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-left: .85rem;
            padding-right: .85rem;
            padding-top: .65rem;
            padding-bottom: 5rem;
        }
        h1 { font-size: 1.9rem !important; line-height: 1.15 !important; }
        h2 { font-size: 1.45rem !important; }
        h3 { font-size: 1.15rem !important; }

        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: .55rem !important;
        }
        [data-testid="column"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
        }
        [data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,.20);
            border-radius: 14px;
            padding: .75rem .85rem;
        }
        [data-testid="stMetricValue"] { font-size: 1.6rem !important; }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stFormSubmitButton"] > button {
            width: 100% !important;
            min-height: 50px;
        }
        [data-testid="stVegaLiteChart"] { width: 100% !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Configuración
# ============================================================
def secret(name, default=""):
    try:
        return str(st.secrets.get(name, default) or "")
    except Exception:
        return default

SUPABASE_URL = secret("SUPABASE_URL").rstrip("/")
SUPABASE_PUBLISHABLE_KEY = secret("SUPABASE_PUBLISHABLE_KEY")
APP_URL = secret("APP_URL", "https://runningcoachpro.streamlit.app")
APP_VERSION = "6.2"

if not SUPABASE_URL or not SUPABASE_PUBLISHABLE_KEY:
    st.error(
        "Falta configurar SUPABASE_URL y SUPABASE_PUBLISHABLE_KEY "
        "en Streamlit → Manage app → Settings → Secrets."
    )
    st.stop()

GOAL_KM = {
    "5K": 5.0,
    "10K": 10.0,
    "21K": 21.1,
    "42K": 42.2,
    "Condición física": None,
}
LEVELS = ["Principiante", "Intermedio", "Avanzado"]
DAY_NAMES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

RUN_DAYS = {
    3: [1, 3, 6],          # Mar/Jue/Dom
    4: [1, 3, 5, 6],       # Mar/Jue/Sáb/Dom
    5: [0, 1, 3, 5, 6],    # Lun/Mar/Jue/Sáb/Dom
    6: [0, 1, 2, 3, 5, 6], # Lun/Mar/Mié/Jue/Sáb/Dom
}

ASSESSMENT_VERSION = "RCP-1.0"
RCP_LEVELS = ["INICIACIÓN", "PRINCIPIANTE", "INTERMEDIO", "AVANZADO"]
RCP_GOALS = [
    "Empezar a correr",
    "Correr 30 min continuos",
    "Condición física",
    "5K",
    "10K",
    "21K",
    "42K",
    "Mantener rendimiento",
    "Volver a correr tras una pausa",
]
EXPERIENCE_OPTIONS = [
    "Nunca",
    "<1 mes",
    "1–3 meses",
    "3–6 meses",
    "6–12 meses",
    "1–2 años",
    ">2 años",
]
CONTINUOUS_OPTIONS = {
    "<5 min": 3,
    "5–10 min": 8,
    "10–20 min": 15,
    "20–30 min": 25,
    "30–45 min": 38,
    "45–60 min": 52,
    "60–90 min": 75,
    ">90 min": 100,
}
TIME_AVAILABLE_OPTIONS = ["30 min", "45 min", "60 min", "75 min", "90+ min"]

# ============================================================
# Autenticación Supabase
# ============================================================
def new_client():
    return create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)


def store_session(session):
    st.session_state["access_token"] = session.access_token
    st.session_state["refresh_token"] = session.refresh_token


def clear_session():
    for key in ["access_token", "refresh_token", "user_id", "user_email"]:
        st.session_state.pop(key, None)


def authenticated_client():
    client = new_client()
    access = st.session_state.get("access_token")
    refresh = st.session_state.get("refresh_token")
    if not access or not refresh:
        return client, None

    try:
        session_result = client.auth.set_session(access, refresh)
        if getattr(session_result, "session", None):
            store_session(session_result.session)

        user_result = client.auth.get_user()
        user = user_result.user
        if user:
            st.session_state["user_id"] = str(user.id)
            st.session_state["user_email"] = str(user.email or "")
        return client, user
    except Exception:
        clear_session()
        return new_client(), None


def show_auth():
    st.title("🏃 RunningCoachPro")
    st.caption("Tu entrenador de running personal · Web + móvil")

    login_tab, signup_tab = st.tabs(["🔐 Entrar", "✨ Crear cuenta"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Correo electrónico", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_password")
            submit = st.form_submit_button("Entrar a RunningCoachPro", use_container_width=True)

        if submit:
            if not email.strip() or not password:
                st.error("Escribe tu correo y contraseña.")
            else:
                try:
                    client = new_client()
                    res = client.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password,
                    })
                    if res.session:
                        store_session(res.session)
                        st.success("Sesión iniciada.")
                        st.rerun()
                    else:
                        st.error("No pude iniciar sesión.")
                except Exception as exc:
                    st.error(f"No pude iniciar sesión: {exc}")

    with signup_tab:
        st.write("Cada corredor tendrá su propio perfil, plan y registros.")
        with st.form("signup_form"):
            name = st.text_input("Tu nombre")
            email = st.text_input("Correo electrónico", key="signup_email")
            password = st.text_input(
                "Contraseña",
                type="password",
                help="Usa al menos 8 caracteres.",
                key="signup_password",
            )
            password2 = st.text_input("Repite la contraseña", type="password")
            submit = st.form_submit_button("Crear mi cuenta", use_container_width=True)

        if submit:
            if not name.strip():
                st.error("Escribe tu nombre.")
            elif not email.strip():
                st.error("Escribe tu correo.")
            elif len(password) < 8:
                st.error("La contraseña debe tener al menos 8 caracteres.")
            elif password != password2:
                st.error("Las contraseñas no coinciden.")
            else:
                try:
                    client = new_client()
                    res = client.auth.sign_up({
                        "email": email.strip(),
                        "password": password,
                        "options": {
                            "data": {"display_name": name.strip()},
                            "email_redirect_to": APP_URL,
                        },
                    })

                    if res.session:
                        store_session(res.session)
                        st.success("Cuenta creada. Vamos a configurar tu plan.")
                        st.rerun()
                    else:
                        st.success(
                            "Cuenta creada. Revisa tu correo y confirma la cuenta. "
                            "Después vuelve aquí e inicia sesión."
                        )
                except Exception as exc:
                    st.error(f"No pude crear la cuenta: {exc}")

    st.info(
        "RunningCoachPro usa cuentas separadas. Los datos de cada usuario "
        "quedan protegidos por las reglas RLS de Supabase."
    )


client, user = authenticated_client()
if user is None:
    show_auth()
    st.stop()

USER_ID = str(user.id)
USER_EMAIL = str(user.email or "")

# ============================================================
# Datos con RLS
# ============================================================
def fetch_rows(table, **filters):
    q = client.table(table).select("*")
    for key, value in filters.items():
        q = q.eq(key, value)
    return q.execute().data or []


def get_profile():
    rows = fetch_rows("rc_profiles", user_id=USER_ID)
    return rows[0] if rows else None


def save_profile(payload):
    payload = dict(payload)
    payload["user_id"] = USER_ID
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    client.table("rc_profiles").upsert(payload, on_conflict="user_id").execute()


def get_plan():
    return (
        client.table("rc_plan_sessions")
        .select("*")
        .eq("user_id", USER_ID)
        .order("session_date")
        .execute()
        .data
        or []
    )


def replace_plan(rows):
    client.table("rc_workout_logs").delete().eq("user_id", USER_ID).execute()
    client.table("rc_plan_sessions").delete().eq("user_id", USER_ID).execute()
    if rows:
        client.table("rc_plan_sessions").insert(rows).execute()


def get_logs():
    return (
        client.table("rc_workout_logs")
        .select("*")
        .eq("user_id", USER_ID)
        .order("session_date")
        .execute()
        .data
        or []
    )


def save_log(payload):
    payload = dict(payload)
    payload["user_id"] = USER_ID
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    client.table("rc_workout_logs").upsert(
        payload, on_conflict="user_id,session_date"
    ).execute()


def delete_log(session_date):
    client.table("rc_workout_logs").delete().eq(
        "user_id", USER_ID
    ).eq("session_date", str(session_date)).execute()


def get_assessments(limit=20):
    """Historial de evaluaciones RCP. Si la migración V6.2 aún no existe, no rompe la app."""
    try:
        return (
            client.table("rc_assessments")
            .select("*")
            .eq("user_id", USER_ID)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
            .data
            or []
        )
    except Exception:
        return []


def get_latest_assessment():
    rows = get_assessments(limit=1)
    return rows[0] if rows else None


def save_assessment(payload):
    row = dict(payload)
    row["user_id"] = USER_ID
    row["assessment_version"] = ASSESSMENT_VERSION
    return client.table("rc_assessments").insert(row).execute()


def assessment_storage_ready():
    try:
        client.table("rc_assessments").select("id").eq("user_id", USER_ID).limit(1).execute()
        return True
    except Exception:
        return False


# ============================================================
# Helpers
# ============================================================
def session_is_optional(session):
    """Reconoce opcionales incluso en planes migrados con el flag antiguo incorrecto."""
    if bool(session.get("is_optional")):
        return True

    name = str(session.get("workout_name") or "").upper()
    intensity = str(session.get("intensity") or "").upper()
    return "OPCIONAL" in name or intensity == "OPCIONAL"


def parse_hms(text):
    text = str(text or "").strip()
    if not text:
        return None

    if re.fullmatch(r"\d+(?:[.,]\d+)?", text):
        return int(round(float(text.replace(",", ".")) * 60))

    parts = text.split(":")
    try:
        vals = [int(x) for x in parts]
    except ValueError:
        return None

    if len(vals) == 2:
        mm, ss = vals
        if mm < 0 or not 0 <= ss < 60:
            return None
        return mm * 60 + ss

    if len(vals) == 3:
        hh, mm, ss = vals
        if hh < 0 or not 0 <= mm < 60 or not 0 <= ss < 60:
            return None
        return hh * 3600 + mm * 60 + ss

    return None


def fmt_time(seconds):
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
    sec = int(round(float(seconds) / float(km)))
    mm, ss = divmod(sec, 60)
    return f"{mm}:{ss:02d} min/km"


def pace_from_target(target_seconds, distance):
    if not target_seconds or not distance:
        return None
    return target_seconds / distance


def pace_string(sec_per_km):
    if not sec_per_km:
        return "Por esfuerzo"
    sec = int(round(sec_per_km))
    mm, ss = divmod(sec, 60)
    return f"{mm}:{ss:02d} min/km"


def next_monday(day):
    delta = (7 - day.weekday()) % 7
    if delta == 0:
        return day
    return day + timedelta(days=delta)


def week_count(start, race_date, has_race):
    if not has_race or not race_date:
        return 12
    days = (race_date - start).days
    return max(6, min(20, math.ceil((days + 1) / 7)))


def volume_for_week(base_km, week_idx, total_weeks, has_race):
    # Build conservador con descarga cada 4 semanas y taper final.
    if has_race and week_idx == total_weeks - 1:
        return max(base_km * 0.55, 10)
    if has_race and week_idx == total_weeks - 2:
        return max(base_km * 0.72, 12)

    block_week = week_idx % 4
    build_index = week_idx - (week_idx // 4)
    growth = 1.0 + min(build_index * 0.04, 0.28)

    if block_week == 3:
        growth *= 0.88

    return base_km * growth


def _score_by_threshold(value, thresholds):
    score = 0
    for threshold, points in thresholds:
        if value >= threshold:
            score = points
    return score


def evaluate_safety(answers):
    """Cribado conservador. No diagnostica ni equivale a autorización médica."""
    concerning_symptoms = any([
        answers.get("chest_discomfort_exertion"),
        answers.get("unexplained_syncope"),
        answers.get("unreasonable_breathlessness"),
        answers.get("symptomatic_palpitations"),
    ])
    known_condition = bool(answers.get("known_condition"))
    professionally_cleared = bool(answers.get("professionally_cleared"))
    acute_issue = bool(answers.get("acute_illness")) or bool(answers.get("pain_changes_gait"))

    if concerning_symptoms:
        return (
            "REQUIERE VALORACIÓN",
            "Declaraste uno o más síntomas que justifican valoración profesional antes de iniciar o reanudar ejercicio intenso.",
        )
    if known_condition and not professionally_cleared:
        return (
            "VALORACIÓN ANTES DE INTENSIDAD",
            "Declaraste una condición cardiovascular, metabólica o renal conocida sin una indicación profesional vigente para ejercicio sin restricciones relevantes.",
        )
    if acute_issue:
        return (
            "PAUSA TEMPORAL",
            "Hay enfermedad aguda/fiebre o dolor que modifica la forma de correr. No conviene progresar la carga hasta resolverlo o reevaluarlo.",
        )
    return (
        "SIN ALERTAS DECLARADAS",
        "No se identificaron alertas en este cribado. Esto no equivale a una autorización médica ni descarta enfermedad.",
    )


def calculate_runner_score(answers):
    active_weeks = int(answers.get("active_weeks_8") or 0)
    running_days = int(answers.get("current_days") or 0)
    weekly_km = float(answers.get("weekly_km") or 0)
    long_km = float(answers.get("long_run_km") or 0)
    continuous_min = int(answers.get("continuous_min") or 0)
    experience = str(answers.get("experience") or "Nunca")
    quality_types = answers.get("quality_types") or []
    intense_sessions = int(answers.get("intense_sessions_per_week") or 0)
    race_experience = bool(answers.get("race_or_test_recent"))

    experience_score = {
        "Nunca": 0,
        "<1 mes": 2,
        "1–3 meses": 5,
        "3–6 meses": 8,
        "6–12 meses": 11,
        "1–2 años": 13,
        ">2 años": 15,
    }.get(experience, 0)

    consistency_score = round(min(active_weeks, 8) / 8 * 20)
    frequency_score = _score_by_threshold(running_days, [(0, 0), (1, 2), (2, 4), (3, 6), (4, 8), (5, 10)])
    volume_score = _score_by_threshold(weekly_km, [(0, 0), (5, 2), (10, 5), (20, 8), (30, 11), (40, 13), (55, 15)])
    continuous_score = _score_by_threshold(continuous_min, [(0, 0), (10, 3), (20, 6), (30, 9), (45, 11), (60, 13), (90, 15)])
    long_score = _score_by_threshold(long_km, [(0, 0), (3, 2), (5, 4), (8, 6), (12, 8), (16, 9), (20, 10)])

    structured_quality = len(set(quality_types))
    quality_score = 0
    if structured_quality >= 1 or intense_sessions >= 1:
        quality_score = 4
    if structured_quality >= 2 and intense_sessions >= 1:
        quality_score = 7
    if structured_quality >= 3 and intense_sessions >= 2:
        quality_score = 10

    race_score = 5 if race_experience else 0

    components = {
        "Consistencia": consistency_score,
        "Antigüedad": experience_score,
        "Frecuencia": frequency_score,
        "Volumen": volume_score,
        "Carrera continua": continuous_score,
        "Tirada larga": long_score,
        "Calidad estructurada": quality_score,
        "Experiencia en carrera/test": race_score,
    }
    score = int(max(0, min(100, sum(components.values()))))
    return score, components


def classify_runner(answers, score):
    experience = str(answers.get("experience") or "Nunca")
    active_weeks = int(answers.get("active_weeks_8") or 0)
    current_days = int(answers.get("current_days") or 0)
    weekly_km = float(answers.get("weekly_km") or 0)
    long_km = float(answers.get("long_run_km") or 0)
    continuous_min = int(answers.get("continuous_min") or 0)
    quality_types = len(set(answers.get("quality_types") or []))

    if score < 30:
        level = "INICIACIÓN"
    elif score < 50:
        level = "PRINCIPIANTE"
    elif score < 75:
        level = "INTERMEDIO"
    else:
        level = "AVANZADO"

    # Reglas de techo: la experiencia mínima importa más que un único valor alto.
    if active_weeks < 4 or continuous_min < 20 or experience in ("Nunca", "<1 mes"):
        level = "INICIACIÓN"
    elif experience == "1–3 meses" or active_weeks < 6 or current_days <= 2:
        level = "PRINCIPIANTE"

    # AVANZADO exige trayectoria y tolerancia estructurada, no solo velocidad.
    if level == "AVANZADO":
        advanced_experience = experience in ("1–2 años", ">2 años")
        if not (
            advanced_experience
            and current_days >= 5
            and weekly_km >= 40
            and long_km >= 14
            and quality_types >= 2
        ):
            level = "INTERMEDIO"

    return level


def goal_readiness(answers, safety_status):
    goal = str(answers.get("goal") or "Condición física")
    active_weeks = int(answers.get("active_weeks_8") or 0)
    weekly_km = float(answers.get("weekly_km") or 0)
    long_km = float(answers.get("long_run_km") or 0)
    continuous_min = int(answers.get("continuous_min") or 0)
    race_date_text = answers.get("goal_race_date")

    if safety_status != "SIN ALERTAS DECLARADAS":
        return "EVALUAR SEGURIDAD PRIMERO", ["El cribado de seguridad debe resolverse antes de progresar el entrenamiento."]

    if goal in ("Empezar a correr", "Correr 30 min continuos", "Condición física", "Volver a correr tras una pausa"):
        return "APTO PARA FASE ADAPTADA", ["El objetivo puede abordarse con una fase inicial ajustada a la capacidad actual."]

    if goal == "Mantener rendimiento":
        if active_weeks >= 4 and weekly_km > 0:
            return "BASE ACTUAL UTILIZABLE", ["Existe actividad reciente suficiente para plantear mantenimiento individualizado."]
        return "BASE PREVIA", ["Conviene reconstruir consistencia antes de un bloque de mantenimiento estructurado."]

    requirements = {
        "5K": (4, 8, 3, 20, 6),
        "10K": (4, 12, 5, 30, 8),
        "21K": (6, 18, 8, 45, 10),
        "42K": (8, 28, 14, 60, 16),
    }
    req = requirements.get(goal)
    if not req:
        return "REVISIÓN MANUAL", ["No hay reglas RCP definidas para este objetivo."]

    req_weeks, req_km, req_long, req_cont, min_calendar_weeks = req
    missing = []
    if active_weeks < req_weeks:
        missing.append(f"consistencia reciente ({active_weeks}/8 semanas)")
    if weekly_km < req_km:
        missing.append(f"volumen actual ({weekly_km:g} km/sem)")
    if long_km < req_long:
        missing.append(f"tirada larga actual ({long_km:g} km)")
    if continuous_min < req_cont:
        missing.append(f"carrera continua ({continuous_min} min)")

    calendar_short = False
    if race_date_text:
        try:
            race_day = date.fromisoformat(str(race_date_text))
            weeks_left = max(0, (race_day - date.today()).days / 7)
            if weeks_left < min_calendar_weeks:
                calendar_short = True
                missing.append(f"tiempo hasta la carrera ({weeks_left:.1f} semanas; referencia RCP ≥{min_calendar_weeks})")
        except Exception:
            pass

    if not missing:
        return "PREPARACIÓN ADECUADA", ["La base declarada cumple los umbrales internos RCP para iniciar este tipo de plan."]
    if len(missing) <= 2 and not calendar_short:
        return "NECESITA FASE DE BASE", missing
    return "OBJETIVO AGRESIVO PARA LA BASE ACTUAL", missing


def assessment_explanation(answers, components, level):
    positives = []
    developments = []

    if int(answers.get("active_weeks_8") or 0) >= 6:
        positives.append("buena consistencia en las últimas 8 semanas")
    else:
        developments.append("construir más semanas consecutivas de entrenamiento")

    if float(answers.get("weekly_km") or 0) >= 25:
        positives.append("base semanal consolidada")
    else:
        developments.append("aumentar la base aeróbica de forma progresiva")

    if int(answers.get("continuous_min") or 0) >= 60:
        positives.append("buena capacidad de carrera continua")
    elif int(answers.get("continuous_min") or 0) < 30:
        developments.append("mejorar tolerancia a carrera continua")

    if float(answers.get("long_run_km") or 0) >= 10:
        positives.append("experiencia con tiradas largas")
    else:
        developments.append("desarrollar progresivamente la tirada larga")

    if len(set(answers.get("quality_types") or [])) >= 2:
        positives.append("experiencia con entrenamiento estructurado")
    else:
        developments.append("introducir calidad estructurada solo cuando la base lo permita")

    reasons = []
    exp = str(answers.get("experience") or "Nunca")
    reasons.append(f"experiencia declarada: {exp}")
    reasons.append(f"frecuencia actual: {int(answers.get('current_days') or 0)} días/sem")
    reasons.append(f"volumen actual: {float(answers.get('weekly_km') or 0):g} km/sem")
    reasons.append(f"carrera continua: {int(answers.get('continuous_min') or 0)} min")
    reasons.append(f"tirada larga: {float(answers.get('long_run_km') or 0):g} km")

    return {
        "level": level,
        "reasons": reasons,
        "strengths": positives[:4],
        "development": developments[:4],
        "components": components,
    }


def quality_workout(level, week_no, target_pace):
    if level == "Principiante":
        reps = min(6 + (week_no // 3), 10)
        return {
            "name": f"Fartlek {reps} × 1 min",
            "target": "RPE 7/10",
            "description": (
                f"12 min suave + {reps} × (1 min rápido / 2 min suave) "
                "+ 10 min suave. Rápido, pero sin sprint máximo."
            ),
        }

    if week_no <= 4:
        reps, meters = 6, 400
    elif week_no <= 8:
        reps, meters = 5, 800
    else:
        reps, meters = 5, 1000

    target = "RPE 7–8/10"
    if target_pace:
        target = f"RPE 7–8/10 · controlado"

    return {
        "name": f"Series {reps} × {meters} m",
        "target": target,
        "description": (
            f"15 min suave + movilidad + {reps} × {meters} m a esfuerzo fuerte "
            "pero controlado; recuperar 90–120 s trotando + 10 min suave."
        ),
    }


def tempo_workout(level, week_no, target_pace):
    minutes = {
        "Principiante": min(12 + week_no, 20),
        "Intermedio": min(18 + week_no, 30),
        "Avanzado": min(22 + week_no, 35),
    }[level]

    target = "RPE 6–7/10"
    if target_pace:
        target = f"RPE 6–7/10 · cerca del ritmo específico, sin forzar"

    return {
        "name": f"Tempo {minutes} min",
        "target": target,
        "description": (
            f"12–15 min suave + {minutes} min sostenidos a RPE 6–7/10 "
            "+ 10 min suave."
        ),
    }


def generate_plan(profile):
    goal = profile["goal"]
    level = profile["level"]
    days = int(profile["days_per_week"])
    base_km = float(profile["weekly_km"])
    has_race = bool(profile.get("has_race"))
    race_date = (
        date.fromisoformat(profile["race_date"])
        if profile.get("race_date")
        else None
    )
    target_seconds = profile.get("target_time_sec")
    race_distance = GOAL_KM.get(goal)
    target_pace = pace_from_target(target_seconds, race_distance)

    start = next_monday(date.today())
    total_weeks = week_count(start, race_date, has_race)

    # Si la carrera está muy cerca, empezar mañana evita crear sesiones en el pasado.
    if has_race and race_date and (race_date - start).days < 35:
        start = date.today() + timedelta(days=1)
        total_weeks = max(4, math.ceil(((race_date - start).days + 1) / 7))

    run_days = RUN_DAYS[days]
    rows = []

    long_caps = {
        "5K": 12.0,
        "10K": 17.0,
        "21K": 25.0,
        "42K": 32.0,
        "Condición física": 16.0,
    }

    for w in range(total_weeks):
        week_no = w + 1
        monday = start + timedelta(days=7 * w)
        weekly_km = max(10.0, volume_for_week(base_km, w, total_weeks, has_race))
        long_km = min(long_caps[goal], max(5.0, weekly_km * (0.28 if days >= 4 else 0.32)))

        if has_race and w == total_weeks - 1:
            long_km = max(4.0, long_km * 0.55)

        # Distribuir el resto.
        remaining = max(0.0, weekly_km - long_km)
        non_long = len(run_days) - 1
        avg_km = remaining / max(1, non_long)

        for pos, weekday in enumerate(run_days):
            d = monday + timedelta(days=weekday)

            if has_race and race_date and d > race_date:
                continue

            # Carrera objetivo reemplaza cualquier sesión de ese día.
            if has_race and race_date and d == race_date and race_distance:
                rows.append({
                    "user_id": USER_ID,
                    "session_date": d.isoformat(),
                    "week_no": week_no,
                    "workout_type": "CARRERA",
                    "workout_name": f"{goal} objetivo",
                    "planned_km": float(race_distance),
                    "target": (
                        f"Ritmo objetivo {pace_string(target_pace)}"
                        if target_pace else "Ritmo de carrera controlado"
                    ),
                    "intensity": "COMPETENCIA",
                    "description": (
                        "Calentamiento habitual. Salir controlado, mantener el esfuerzo "
                        "objetivo y reservar margen para el tramo final."
                    ),
                    "is_optional": False,
                })
                continue

            is_last = pos == len(run_days) - 1
            if is_last:
                rows.append({
                    "user_id": USER_ID,
                    "session_date": d.isoformat(),
                    "week_no": week_no,
                    "workout_type": "LARGA",
                    "workout_name": f"Tirada larga {round(long_km, 1):g} km",
                    "planned_km": round(long_km, 1),
                    "target": "RPE 3–4/10 · conversacional",
                    "intensity": "BASE",
                    "description": (
                        "10 min muy suaves. Mantén un esfuerzo cómodo y estable. "
                        "En subidas prioriza esfuerzo sobre ritmo. Termina con 5 min suaves."
                    ),
                    "is_optional": False,
                })
                continue

            # Calidad principal
            quality_pos = 0 if days == 3 else 1
            if pos == quality_pos:
                q = quality_workout(level, week_no, target_pace)
                rows.append({
                    "user_id": USER_ID,
                    "session_date": d.isoformat(),
                    "week_no": week_no,
                    "workout_type": "SERIES",
                    "workout_name": q["name"],
                    "planned_km": round(max(4.0, avg_km), 1),
                    "target": q["target"],
                    "intensity": "CALIDAD",
                    "description": q["description"],
                    "is_optional": False,
                })
                continue

            # Segunda calidad para 4+ días.
            if days >= 4 and pos == len(run_days) - 3:
                q = tempo_workout(level, week_no, target_pace)
                rows.append({
                    "user_id": USER_ID,
                    "session_date": d.isoformat(),
                    "week_no": week_no,
                    "workout_type": "TEMPO",
                    "workout_name": q["name"],
                    "planned_km": round(max(4.0, avg_km), 1),
                    "target": q["target"],
                    "intensity": "CALIDAD",
                    "description": q["description"],
                    "is_optional": False,
                })
                continue

            # Resto suave / recuperación.
            recovery = days >= 6 and weekday == 2
            rows.append({
                "user_id": USER_ID,
                "session_date": d.isoformat(),
                "week_no": week_no,
                "workout_type": "RECUPERACION" if recovery else "RODAJE",
                "workout_name": (
                    f"Recuperación {round(max(3.0, avg_km * .75), 1):g} km"
                    if recovery
                    else f"Rodaje suave {round(max(3.5, avg_km), 1):g} km"
                ),
                "planned_km": round(
                    max(3.0, avg_km * .75) if recovery else max(3.5, avg_km), 1
                ),
                "target": "RPE 2–3/10" if recovery else "RPE 3–4/10 · conversacional",
                "intensity": "RECUPERACION" if recovery else "BASE",
                "description": (
                    "Muy suave. Debe dejarte mejor de lo que empezaste."
                    if recovery
                    else "Ritmo cómodo. Debes poder hablar en frases completas."
                ),
                "is_optional": False,
            })

    # Si la carrera no cae en un día RUN_DAYS, agregarla de todas formas.
    if has_race and race_date and race_distance:
        if not any(r["session_date"] == race_date.isoformat() for r in rows):
            rows = [r for r in rows if r["session_date"] != race_date.isoformat()]
            rows.append({
                "user_id": USER_ID,
                "session_date": race_date.isoformat(),
                "week_no": total_weeks,
                "workout_type": "CARRERA",
                "workout_name": f"{goal} objetivo",
                "planned_km": float(race_distance),
                "target": (
                    f"Ritmo objetivo {pace_string(target_pace)}"
                    if target_pace else "Ritmo de carrera controlado"
                ),
                "intensity": "COMPETENCIA",
                "description": (
                    "Calentamiento habitual. Salida controlada, ritmo estable y "
                    "progresión final solo si las sensaciones son buenas."
                ),
                "is_optional": False,
            })

    rows.sort(key=lambda x: x["session_date"])
    return rows


def _option_index(options, value, fallback=0):
    try:
        return options.index(value)
    except Exception:
        return fallback


def show_assessment_result(assessment):
    if not assessment:
        return

    score = int(assessment.get("runner_score") or 0)
    level = str(assessment.get("runner_level") or "—")
    safety = str(assessment.get("safety_status") or "—")
    readiness = str(assessment.get("goal_readiness") or "—")
    goal = str(assessment.get("goal") or "—")
    explanation = assessment.get("explanation") or {}

    st.markdown("### Tu perfil RCP")
    a, b, c, d = st.columns(4)
    a.metric("Nivel RCP", level.title())
    b.metric("Runner Score", f"{score}/100")
    c.metric("Objetivo evaluado", goal)
    d.metric("Preparación", readiness.title())

    if safety == "SIN ALERTAS DECLARADAS":
        st.success(f"**Cribado de seguridad:** {safety}. {assessment.get('safety_message') or ''}")
    elif safety == "PAUSA TEMPORAL":
        st.warning(f"**Cribado de seguridad:** {safety}. {assessment.get('safety_message') or ''}")
    else:
        st.error(f"**Cribado de seguridad:** {safety}. {assessment.get('safety_message') or ''}")

    reasons = explanation.get("reasons") or []
    strengths = explanation.get("strengths") or []
    development = explanation.get("development") or []
    components = explanation.get("components") or {}

    left, right = st.columns(2)
    with left:
        st.markdown("#### ¿Por qué este nivel?")
        for item in reasons:
            st.write(f"• {item}")
        if strengths:
            st.markdown("#### Fortalezas actuales")
            for item in strengths:
                st.write(f"• {item}")
    with right:
        if development:
            st.markdown("#### Áreas a desarrollar")
            for item in development:
                st.write(f"• {item}")
        readiness_reasons = assessment.get("readiness_reasons") or []
        if readiness_reasons:
            st.markdown("#### Preparación para el objetivo")
            for item in readiness_reasons:
                st.write(f"• {item}")

    if components:
        with st.expander("Ver composición del Runner Score"):
            score_rows = [{"Dimensión": k, "Puntos": v} for k, v in components.items()]
            st.dataframe(score_rows, use_container_width=True, hide_index=True)
            st.caption(
                "El Runner Score es un índice interno RCP de experiencia y tolerancia de entrenamiento; "
                "no es una escala médica ni una medida de talento o velocidad."
            )


def assessment_form(existing_assessment=None, onboarding=False):
    existing_answers = (existing_assessment or {}).get("answers") or {}

    st.subheader("🧭 Evaluación inicial RCP" if onboarding else "🧭 Reevaluación del corredor")
    st.caption(
        "Esta evaluación clasifica experiencia, base actual, disponibilidad y preparación para un objetivo. "
        "El apartado de seguridad es un cribado conservador y no sustituye valoración médica."
    )

    with st.form("rcp_assessment_form"):
        st.markdown("### 1 · Seguridad antes de aumentar la carga")
        st.caption("Marca solo lo que aplique actualmente o durante el ejercicio.")
        s1, s2 = st.columns(2)
        chest = s1.checkbox(
            "Molestia, presión u opresión en pecho/cuello/mandíbula/brazos asociada al esfuerzo",
            value=bool(existing_answers.get("chest_discomfort_exertion")),
        )
        breath = s1.checkbox(
            "Falta de aire claramente desproporcionada al esfuerzo habitual",
            value=bool(existing_answers.get("unreasonable_breathlessness")),
        )
        syncope = s1.checkbox(
            "Desmayo, pérdida de conocimiento o mareo intenso inexplicado",
            value=bool(existing_answers.get("unexplained_syncope")),
        )
        palpitations = s2.checkbox(
            "Palpitaciones rápidas/irregulares acompañadas de malestar, mareo o dolor",
            value=bool(existing_answers.get("symptomatic_palpitations")),
        )
        known_condition = s2.checkbox(
            "Condición cardiovascular, metabólica o renal conocida relevante para el ejercicio",
            value=bool(existing_answers.get("known_condition")),
        )
        professionally_cleared = s2.checkbox(
            "Tengo indicación profesional vigente para realizar ejercicio sin restricciones relevantes",
            value=bool(existing_answers.get("professionally_cleared")),
        )
        acute_illness = st.checkbox(
            "Actualmente tengo fiebre, enfermedad aguda o un cuadro que hace que entrenar no sea razonable",
            value=bool(existing_answers.get("acute_illness")),
        )

        st.markdown("### 2 · Experiencia corriendo")
        e1, e2, e3 = st.columns(3)
        running_status_options = [
            "No corro actualmente",
            "Estoy empezando",
            "Volviendo después de una pausa",
            "Corro regularmente",
        ]
        running_status = e1.selectbox(
            "Situación actual",
            running_status_options,
            index=_option_index(running_status_options, existing_answers.get("running_status"), 1),
        )
        experience = e2.selectbox(
            "Tiempo corriendo regularmente",
            EXPERIENCE_OPTIONS,
            index=_option_index(EXPERIENCE_OPTIONS, existing_answers.get("experience"), 0),
        )
        active_weeks = e3.slider(
            "Semanas corridas en las últimas 8",
            0, 8,
            int(existing_answers.get("active_weeks_8") or 0),
        )

        c1, c2, c3 = st.columns(3)
        current_days = c1.number_input(
            "Días que corres actualmente / semana",
            min_value=0, max_value=7,
            value=int(existing_answers.get("current_days") or 0),
            step=1,
        )
        weekly_km = c2.number_input(
            "KM promedio / semana (últimas 4 semanas)",
            min_value=0.0, max_value=250.0,
            value=float(existing_answers.get("weekly_km") or 0.0),
            step=1.0,
        )
        long_run_km = c3.number_input(
            "Tirada más larga de las últimas 4 semanas",
            min_value=0.0, max_value=100.0,
            value=float(existing_answers.get("long_run_km") or 0.0),
            step=0.5,
        )

        with st.expander("Opcional · Detallar las últimas 4 semanas"):
            wk = existing_answers.get("weekly_km_detail") or [0, 0, 0, 0]
            wk = list(wk) + [0, 0, 0, 0]
            w1, w2, w3, w4 = st.columns(4)
            week1 = w1.number_input("Semana -4", 0.0, 250.0, float(wk[0]), 1.0)
            week2 = w2.number_input("Semana -3", 0.0, 250.0, float(wk[1]), 1.0)
            week3 = w3.number_input("Semana -2", 0.0, 250.0, float(wk[2]), 1.0)
            week4 = w4.number_input("Semana -1", 0.0, 250.0, float(wk[3]), 1.0)

        continuous_label = st.selectbox(
            "Máximo tiempo que puedes correr de forma continua",
            list(CONTINUOUS_OPTIONS.keys()),
            index=_option_index(
                list(CONTINUOUS_OPTIONS.keys()),
                existing_answers.get("continuous_label"),
                0,
            ),
        )

        st.markdown("### 3 · Historial de entrenamiento")
        quality_options = [
            "Rodajes suaves",
            "Tirada larga",
            "Fartlek",
            "Series/intervalos",
            "Tempo/umbral",
            "Cuestas",
            "Strides/progresivos",
        ]
        quality_types = st.multiselect(
            "Sesiones que has realizado con cierta regularidad",
            quality_options,
            default=[x for x in (existing_answers.get("quality_types") or []) if x in quality_options],
        )
        h1, h2, h3 = st.columns(3)
        intense_sessions = h1.selectbox(
            "Sesiones intensas habituales / semana",
            [0, 1, 2, 3],
            index=min(3, int(existing_answers.get("intense_sessions_per_week") or 0)),
            format_func=lambda x: "3+" if x == 3 else str(x),
        )
        strength_options = ["No", "Ocasional", "1/sem", "2/sem", "3+/sem"]
        strength_frequency = h2.selectbox(
            "Trabajo de fuerza",
            strength_options,
            index=_option_index(strength_options, existing_answers.get("strength_frequency"), 0),
        )
        race_or_test = h3.checkbox(
            "Carrera o test reciente",
            value=bool(existing_answers.get("race_or_test_recent")),
            help="Una carrera o test reciente aporta evidencia de experiencia competitiva, pero no define por sí sola tu nivel.",
        )

        st.markdown("### 4 · Lesiones y tolerancia actual")
        i1, i2, i3 = st.columns(3)
        injury_last12m = i1.checkbox(
            "Lesión que impidió correr ≥7 días en los últimos 12 meses",
            value=bool(existing_answers.get("injury_last12m")),
        )
        current_pain = i2.slider(
            "Dolor actual al correr (0–10)",
            0, 10,
            int(existing_answers.get("current_pain") or 0),
        )
        pain_changes_gait = i3.checkbox(
            "El dolor cambia mi forma de caminar/correr",
            value=bool(existing_answers.get("pain_changes_gait")),
        )
        injury_areas = st.multiselect(
            "Zonas con lesión relevante reciente (opcional)",
            ["Pie/tobillo", "Aquiles", "Pantorrilla", "Tibia", "Rodilla", "Isquiotibiales", "Cadera", "Espalda", "Otra"],
            default=existing_answers.get("injury_areas") or [],
        )

        st.markdown("### 5 · Disponibilidad real")
        available_days = st.multiselect(
            "Días en los que realmente puedes entrenar",
            DAY_NAMES,
            default=existing_answers.get("available_days") or ["Martes", "Jueves", "Domingo"],
        )
        d1, d2 = st.columns(2)
        preferred_long_day = d1.selectbox(
            "Día preferido para tirada larga",
            DAY_NAMES,
            index=_option_index(DAY_NAMES, existing_answers.get("preferred_long_day"), 6),
        )
        no_intensity_days = d2.multiselect(
            "Días que prefieres evitar para calidad",
            DAY_NAMES,
            default=existing_answers.get("no_intensity_days") or [],
        )
        t1, t2 = st.columns(2)
        weekday_time = t1.selectbox(
            "Tiempo máximo entre semana",
            TIME_AVAILABLE_OPTIONS,
            index=_option_index(TIME_AVAILABLE_OPTIONS, existing_answers.get("weekday_time"), 2),
        )
        weekend_time = t2.selectbox(
            "Tiempo máximo fin de semana",
            TIME_AVAILABLE_OPTIONS,
            index=_option_index(TIME_AVAILABLE_OPTIONS, existing_answers.get("weekend_time"), 4),
        )

        st.markdown("### 6 · Objetivo")
        g1, g2 = st.columns(2)
        goal = g1.selectbox(
            "¿Qué quieres conseguir?",
            RCP_GOALS,
            index=_option_index(RCP_GOALS, existing_answers.get("goal"), 4),
        )
        goal_style_options = ["Terminar", "Terminar cómodo", "Mejorar mi marca", "Buscar una marca concreta"]
        goal_style = g2.selectbox(
            "Tipo de objetivo",
            goal_style_options,
            index=_option_index(goal_style_options, existing_answers.get("goal_style"), 0),
        )
        has_goal_race = st.checkbox(
            "Tengo una fecha de carrera/objetivo",
            value=bool(existing_answers.get("has_goal_race")),
        )
        default_goal_date = date.today() + timedelta(weeks=12)
        if existing_answers.get("goal_race_date"):
            try:
                default_goal_date = date.fromisoformat(str(existing_answers["goal_race_date"]))
            except Exception:
                pass
        goal_race_date = st.date_input(
            "Fecha objetivo (se ignora si no marcaste la casilla anterior)",
            value=default_goal_date,
            min_value=date.today() + timedelta(days=1),
            max_value=date.today() + timedelta(days=730),
        )

        accepted = st.checkbox(
            "Confirmo que respondí según mi situación actual y entiendo que esta evaluación no diagnostica ni reemplaza una valoración profesional.",
            value=False,
        )
        submit = st.form_submit_button(
            "Analizar mi perfil RCP",
            use_container_width=True,
        )

    if not submit:
        return False
    if not accepted:
        st.error("Confirma la casilla para guardar la evaluación.")
        return False
    if not available_days:
        st.error("Selecciona al menos un día disponible para entrenar.")
        return False

    weekly_detail = [float(week1), float(week2), float(week3), float(week4)]
    positive_weeks = [x for x in weekly_detail if x > 0]
    effective_weekly_km = float(weekly_km)
    if positive_weeks:
        effective_weekly_km = round(sum(positive_weeks) / len(positive_weeks), 2)

    answers = {
        "chest_discomfort_exertion": bool(chest),
        "unreasonable_breathlessness": bool(breath),
        "unexplained_syncope": bool(syncope),
        "symptomatic_palpitations": bool(palpitations),
        "known_condition": bool(known_condition),
        "professionally_cleared": bool(professionally_cleared),
        "acute_illness": bool(acute_illness),
        "running_status": running_status,
        "experience": experience,
        "active_weeks_8": int(active_weeks),
        "current_days": int(current_days),
        "weekly_km": effective_weekly_km,
        "weekly_km_declared": float(weekly_km),
        "weekly_km_detail": weekly_detail,
        "long_run_km": float(long_run_km),
        "continuous_label": continuous_label,
        "continuous_min": int(CONTINUOUS_OPTIONS[continuous_label]),
        "quality_types": quality_types,
        "intense_sessions_per_week": int(intense_sessions),
        "strength_frequency": strength_frequency,
        "race_or_test_recent": bool(race_or_test),
        "injury_last12m": bool(injury_last12m),
        "current_pain": int(current_pain),
        "pain_changes_gait": bool(pain_changes_gait),
        "injury_areas": injury_areas,
        "available_days": available_days,
        "preferred_long_day": preferred_long_day,
        "no_intensity_days": no_intensity_days,
        "weekday_time": weekday_time,
        "weekend_time": weekend_time,
        "goal": goal,
        "goal_style": goal_style,
        "has_goal_race": bool(has_goal_race),
        "goal_race_date": goal_race_date.isoformat() if has_goal_race else None,
    }

    safety_status, safety_message = evaluate_safety(answers)
    runner_score, components = calculate_runner_score(answers)
    runner_level = classify_runner(answers, runner_score)
    readiness, readiness_reasons = goal_readiness(answers, safety_status)
    explanation = assessment_explanation(answers, components, runner_level)

    payload = {
        "safety_status": safety_status,
        "safety_message": safety_message,
        "runner_score": int(runner_score),
        "runner_level": runner_level,
        "goal": goal,
        "goal_readiness": readiness,
        "weekly_km": effective_weekly_km,
        "days_running": int(current_days),
        "longest_run_km": float(long_run_km),
        "continuous_run_min": int(CONTINUOUS_OPTIONS[continuous_label]),
        "answers": answers,
        "explanation": explanation,
        "readiness_reasons": readiness_reasons,
    }

    try:
        save_assessment(payload)
    except Exception as exc:
        st.error(
            "No pude guardar la evaluación. Ejecuta primero supabase_v6_2_assessment.sql "
            f"en Supabase. Detalle: {exc}"
        )
        return False

    st.success(f"Evaluación guardada · Nivel RCP: {runner_level.title()} · {runner_score}/100")
    st.rerun()
    return True


def profile_form(existing=None, assessed_level=None):
    existing = existing or {}

    st.subheader("Configura tu RunningCoachPro")
    st.caption(
        "La app crea una planificación general basada en tu volumen actual, "
        "objetivo y días disponibles."
    )

    with st.form("profile_form"):
        name = st.text_input(
            "Nombre",
            value=str(existing.get("display_name") or ""),
        )

        c1, c2 = st.columns(2)
        goal_options = list(GOAL_KM.keys())
        current_goal = existing.get("goal", "10K")
        goal = c1.selectbox(
            "Objetivo",
            goal_options,
            index=goal_options.index(current_goal) if current_goal in goal_options else 1,
        )
        if assessed_level:
            legacy_level_map = {
                "INICIACIÓN": "Principiante",
                "PRINCIPIANTE": "Principiante",
                "INTERMEDIO": "Intermedio",
                "AVANZADO": "Avanzado",
            }
            level = legacy_level_map.get(str(assessed_level).upper(), "Principiante")
            c2.markdown("**Nivel RCP evaluado**")
            c2.info(str(assessed_level).title())
            c2.caption(
                f"El generador V6 usa temporalmente la plantilla {level}. "
                "El motor adaptativo V7 se conectará en la siguiente fase."
            )
        else:
            level = c2.selectbox(
                "Nivel (legacy · completa la Evaluación RCP para automatizarlo)",
                LEVELS,
                index=LEVELS.index(existing.get("level", "Principiante"))
                if existing.get("level") in LEVELS else 0,
            )

        c3, c4 = st.columns(2)
        days = c3.slider(
            "Días de carrera por semana",
            3, 6,
            int(existing.get("days_per_week") or 3),
        )
        weekly_km = c4.number_input(
            "KM actuales por semana",
            8.0, 180.0,
            float(existing.get("weekly_km") or 20.0),
            1.0,
        )

        has_race_default = bool(existing.get("has_race"))
        has_race = st.checkbox(
            "Tengo una carrera objetivo con fecha",
            value=has_race_default and goal != "Condición física",
            disabled=goal == "Condición física",
        )

        race_date = None
        target_time = ""
        if has_race and goal != "Condición física":
            r1, r2 = st.columns(2)
            default_race = (
                date.fromisoformat(existing["race_date"])
                if existing.get("race_date")
                else date.today() + timedelta(weeks=12)
            )
            race_date = r1.date_input(
                "Fecha de carrera",
                value=default_race,
                min_value=date.today() + timedelta(days=14),
                max_value=date.today() + timedelta(days=365),
            )
            existing_target = existing.get("target_time_sec")
            target_time = r2.text_input(
                "Tiempo objetivo (HH:MM:SS)",
                value=fmt_time(existing_target) if existing_target else "",
                placeholder="Ej.: 01:47:00",
            )

        st.markdown("**Marca reciente (opcional)**")
        m1, m2 = st.columns(2)
        current_distance = m1.selectbox(
            "Distancia de referencia",
            ["5K", "10K", "21K", "42K"],
            index=1,
        )
        current_time = m2.text_input(
            "Tiempo reciente (HH:MM:SS)",
            value=fmt_time(existing.get("current_time_sec"))
            if existing.get("current_time_sec") else "",
            placeholder="Ej.: 00:52:30",
        )

        accepted = st.checkbox(
            "Entiendo que es una planificación general y ajustaré/suspenderé "
            "el entrenamiento ante dolor, lesión o síntomas anormales.",
            value=False,
        )

        submit = st.form_submit_button(
            "🚀 Crear / actualizar mi plan",
            use_container_width=True,
        )

    if not submit:
        return False

    if not name.strip():
        st.error("Escribe tu nombre.")
        return False
    if not accepted:
        st.error("Confirma la casilla antes de crear el plan.")
        return False

    target_seconds = parse_hms(target_time) if target_time else None
    current_seconds = parse_hms(current_time) if current_time else None

    if target_time and target_seconds is None:
        st.error("Tiempo objetivo inválido. Usa HH:MM:SS.")
        return False
    if current_time and current_seconds is None:
        st.error("Marca reciente inválida. Usa HH:MM:SS.")
        return False

    profile = {
        "display_name": name.strip(),
        "goal": goal,
        "level": level,
        "days_per_week": int(days),
        "weekly_km": float(weekly_km),
        "has_race": bool(has_race and goal != "Condición física"),
        "race_date": race_date.isoformat() if race_date else None,
        "target_time_sec": target_seconds,
        "current_distance_km": GOAL_KM.get(current_distance),
        "current_time_sec": current_seconds,
    }

    save_profile(profile)
    generated = generate_plan(profile)
    replace_plan(generated)

    st.success(f"Plan creado: {len(generated)} sesiones.")
    st.rerun()
    return True


profile = get_profile()
ASSESSMENT_READY = assessment_storage_ready()
LATEST_ASSESSMENT = get_latest_assessment() if ASSESSMENT_READY else None

if not profile:
    st.title("🏃 Bienvenido a RunningCoachPro")
    st.write(f"Cuenta: **{USER_EMAIL}**")

    if ASSESSMENT_READY and not LATEST_ASSESSMENT:
        st.info(
            "Antes de crear tu primer plan, RunningCoachPro evaluará tu experiencia, "
            "base actual, disponibilidad y objetivo."
        )
        assessment_form(onboarding=True)
    elif ASSESSMENT_READY and LATEST_ASSESSMENT:
        show_assessment_result(LATEST_ASSESSMENT)
        st.divider()
        st.markdown("### Crear el plan actual")
        st.caption(
            "En V6.2 la evaluación ya determina tu nivel. El generador adaptativo completo "
            "se conectará en la siguiente fase; por ahora se conserva el generador V6 para no romper la app."
        )
        profile_form(assessed_level=LATEST_ASSESSMENT.get("runner_level"))
    else:
        st.warning(
            "El módulo de evaluación aún no está instalado en Supabase. "
            "Puedes usar temporalmente la configuración V6 o ejecutar supabase_v6_2_assessment.sql."
        )
        profile_form()
    st.stop()

PLAN = get_plan()
LOGS = get_logs()
PLAN_BY_DATE = {str(x["session_date"]): x for x in PLAN}

# Solo los registros asociados por fecha al plan vigente alimentan métricas y gráficos.
# Esto evita que registros de prueba o restos de una planificación anterior contaminen
# KM reales, RPE y PLAN vs REAL.
CURRENT_LOGS = [
    x for x in LOGS
    if str(x.get("session_date")) in PLAN_BY_DATE
]
ORPHAN_LOGS = [
    x for x in LOGS
    if str(x.get("session_date")) not in PLAN_BY_DATE
]
LOG_BY_DATE = {str(x["session_date"]): x for x in CURRENT_LOGS}

# ============================================================
# Navegación / Sidebar
# ============================================================
st.sidebar.title("🏃 RunningCoachPro")
st.sidebar.caption(f"V{APP_VERSION} Multiusuario · Web + móvil")
st.sidebar.markdown(f"**{profile['display_name']}**")
st.sidebar.caption(USER_EMAIL)
st.sidebar.markdown(f"🎯 **Objetivo:** {profile['goal']}")
st.sidebar.markdown(f"📅 **Días/sem:** {profile['days_per_week']}")
st.sidebar.markdown(f"📏 **Base:** {float(profile['weekly_km']):g} km/sem")
if LATEST_ASSESSMENT:
    st.sidebar.markdown(
        f"🧭 **Nivel RCP:** {str(LATEST_ASSESSMENT.get('runner_level') or '—').title()} "
        f"· {int(LATEST_ASSESSMENT.get('runner_score') or 0)}/100"
    )

selected_day = st.sidebar.date_input(
    "Fecha",
    value=date.today(),
)

with st.sidebar.expander("📲 Añadir al celular"):
    st.markdown(
        "**iPhone:** Safari → Compartir → Añadir a pantalla de inicio.\n\n"
        "**Android:** Chrome → ⋮ → Añadir a pantalla principal / Instalar app."
    )

if st.sidebar.button("Cerrar sesión", use_container_width=True):
    try:
        client.auth.sign_out()
    except Exception:
        pass
    clear_session()
    st.rerun()

# ============================================================
# Dashboard
# ============================================================
st.title("🏃 RunningCoachPro")
st.caption(f"Hola, {profile['display_name']} · Tu plan, tus datos, tu progreso")

completed = [
    l for l in CURRENT_LOGS
    if str(l.get("status", "")).upper() in ("COMPLETADO", "MODIFICADO")
]
actual_km_total = sum(float(x.get("actual_km") or 0) for x in completed)

dashboard_day = date.today()
due_sessions = [
    p for p in PLAN
    if date.fromisoformat(str(p["session_date"])) <= dashboard_day
    and not session_is_optional(p)
]
done_due = [
    p for p in due_sessions
    if str(LOG_BY_DATE.get(str(p["session_date"]), {}).get("status", "")).upper()
    in ("COMPLETADO", "MODIFICADO")
]
compliance = (len(done_due) / len(due_sessions) * 100) if due_sessions else 0

rpes = [
    float(x["rpe"]) for x in completed
    if x.get("rpe") is not None
]
avg_rpe = sum(rpes) / len(rpes) if rpes else None

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cumplimiento", "—" if not due_sessions else f"{compliance:.0f}%")
m2.metric("KM reales", f"{actual_km_total:.1f}")
m3.metric("RPE promedio", "—" if avg_rpe is None else f"{avg_rpe:.1f}/10")
m4.metric("Sesiones del plan", len(PLAN))

tabs = st.tabs([
    "📍 Hoy",
    "📅 Semana",
    "📊 Progreso",
    "🗓️ Plan",
    "✅ Registro",
    "🧭 Evaluación",
    "⚙️ Perfil",
])

# ============================================================
# HOY
# ============================================================
with tabs[0]:
    st.subheader(f"{DAY_NAMES[selected_day.weekday()]} · {selected_day.strftime('%d/%m/%Y')}")
    session = PLAN_BY_DATE.get(selected_day.isoformat())

    if not session:
        st.markdown("## 😴 Descanso / recuperación")
        st.write("No hay una sesión programada para esta fecha.")
        future = [
            p for p in PLAN
            if date.fromisoformat(str(p["session_date"])) > selected_day
        ]
        if future:
            nxt = future[0]
            st.info(
                f"Próxima: {date.fromisoformat(str(nxt['session_date'])).strftime('%d/%m')} · "
                f"{nxt['workout_name']} · {float(nxt['planned_km']):g} km"
            )
    else:
        st.markdown(f"## {session['workout_name']}")
        st.caption(
            f"{session['workout_type']} · Semana {session['week_no']} · "
            f"{session['intensity']}"
        )

        a, b, c = st.columns(3)
        a.metric("Distancia", f"{float(session['planned_km']):g} km")
        b.metric("Objetivo", session["target"])
        b.caption("Ritmo / esfuerzo")
        c.metric("Semana", session["week_no"])

        st.markdown("### 📋 Cómo hacerlo")
        st.write(session["description"])

        log = LOG_BY_DATE.get(selected_day.isoformat())
        if log:
            status = str(log.get("status") or "").upper()
            if status in ("COMPLETADO", "MODIFICADO"):
                st.success(
                    f"{status} ✅ · {float(log.get('actual_km') or 0):g} km · "
                    f"{fmt_pace(log.get('actual_duration_sec'), log.get('actual_km'))} · "
                    f"RPE {log.get('rpe') or '—'}"
                )
            elif status == "OMITIDO":
                st.warning("Sesión marcada como omitida.")

# ============================================================
# SEMANA
# ============================================================
with tabs[1]:
    monday = selected_day - timedelta(days=selected_day.weekday())
    sunday = monday + timedelta(days=6)
    st.subheader(f"{monday.strftime('%d/%m')} – {sunday.strftime('%d/%m/%Y')}")

    for i in range(7):
        d = monday + timedelta(days=i)
        s = PLAN_BY_DATE.get(d.isoformat())

        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 2.8, 1.2])
            c1.markdown(f"**{DAY_NAMES[d.weekday()]}**")
            c1.caption(d.strftime("%d/%m"))

            if s:
                c2.markdown(f"**{s['workout_name']}**")
                c2.caption(f"{s['workout_type']} · {s['target']}")
                c3.markdown(f"**{float(s['planned_km']):g} km**")

                log = LOG_BY_DATE.get(d.isoformat())
                if log:
                    c3.caption(str(log.get("status") or "").title())
                else:
                    c3.caption("Pendiente")
            else:
                c2.markdown("**😴 Descanso**")
                c2.caption("Recuperación")

# ============================================================
# PROGRESO
# ============================================================
with tabs[2]:
    st.subheader("PLAN vs REAL")

    weekly = {}
    for p in PLAN:
        week = int(p["week_no"])
        weekly.setdefault(week, {"plan": 0.0, "real": 0.0, "rpes": []})
        # PLAN vs REAL usa la carga base; los rodajes opcionales no inflan el plan.
        if not session_is_optional(p):
            weekly[week]["plan"] += float(p["planned_km"] or 0)

    for l in CURRENT_LOGS:
        if str(l.get("status") or "").upper() not in ("COMPLETADO", "MODIFICADO"):
            continue
        p = PLAN_BY_DATE.get(str(l["session_date"]))
        if not p:
            continue
        week = int(p["week_no"])
        weekly.setdefault(week, {"plan": 0.0, "real": 0.0, "rpes": []})
        weekly[week]["real"] += float(l.get("actual_km") or 0)
        if l.get("rpe") is not None:
            weekly[week]["rpes"].append(float(l["rpe"]))

    values = []
    for week in sorted(weekly):
        values.append({"Semana": str(week), "Serie": "Plan base", "KM": round(weekly[week]["plan"], 1)})
        values.append({"Semana": str(week), "Serie": "Real", "KM": round(weekly[week]["real"], 1)})

    st.vega_lite_chart(
        {
            "data": {"values": values},
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "x": {"field": "Semana", "type": "ordinal"},
                "xOffset": {"field": "Serie"},
                "y": {"field": "KM", "type": "quantitative", "title": "KM"},
                "color": {"field": "Serie", "type": "nominal"},
                "tooltip": [
                    {"field": "Semana", "type": "ordinal"},
                    {"field": "Serie", "type": "nominal"},
                    {"field": "KM", "type": "quantitative"},
                ],
            },
        },
        use_container_width=True,
    )

    rpe_values = [
        {
            "Semana": str(week),
            "RPE": round(sum(data["rpes"]) / len(data["rpes"]), 1),
        }
        for week, data in weekly.items()
        if data["rpes"]
    ]

    st.markdown("### RPE semanal")
    if rpe_values:
        st.vega_lite_chart(
            {
                "data": {"values": rpe_values},
                "mark": {"type": "line", "point": True, "tooltip": True},
                "encoding": {
                    "x": {"field": "Semana", "type": "ordinal"},
                    "y": {
                        "field": "RPE",
                        "type": "quantitative",
                        "scale": {"domain": [1, 10]},
                    },
                },
            },
            use_container_width=True,
        )
    else:
        st.info("Todavía no hay suficientes RPE registrados.")

# ============================================================
# PLAN COMPLETO
# ============================================================
with tabs[3]:
    st.subheader("Mi plan")
    table = []
    for p in PLAN:
        log = LOG_BY_DATE.get(str(p["session_date"]))
        table.append({
            "Fecha": date.fromisoformat(str(p["session_date"])).strftime("%d/%m/%Y"),
            "Semana": p["week_no"],
            "Tipo": p["workout_type"],
            "Entrenamiento": p["workout_name"],
            "KM": float(p["planned_km"]),
            "Objetivo": p["target"],
            "Opcional": "SÍ" if session_is_optional(p) else "NO",
            "Estado": str(log.get("status") or "PENDIENTE") if log else "PENDIENTE",
        })
    st.dataframe(table, use_container_width=True, hide_index=True)

# ============================================================
# REGISTRO
# ============================================================
with tabs[4]:
    st.subheader("Registrar entrenamiento")
    session = PLAN_BY_DATE.get(selected_day.isoformat())

    if not session:
        st.info("Selecciona una fecha que tenga entrenamiento programado.")
    else:
        existing = LOG_BY_DATE.get(selected_day.isoformat(), {})
        with st.form("log_form"):
            r1, r2, r3 = st.columns(3)
            km = r1.number_input(
                "KM reales",
                0.0, 100.0,
                float(existing.get("actual_km") if existing.get("actual_km") is not None else session["planned_km"]),
                .1,
            )
            duration_text = r2.text_input(
                "Duración HH:MM:SS",
                value=fmt_time(existing.get("actual_duration_sec"))
                if existing.get("actual_duration_sec") else "",
            )
            rpe = r3.slider("RPE", 1, 10, int(existing.get("rpe") or 5))

            h1, h2 = st.columns(2)
            avg_hr = h1.number_input(
                "FC media (opcional)",
                0, 230,
                int(existing.get("avg_hr") or 0),
            )
            max_hr = h2.number_input(
                "FC máxima (opcional)",
                0, 240,
                int(existing.get("max_hr") or 0),
            )

            status_options = ["COMPLETADO", "MODIFICADO", "OMITIDO"]
            current_status = str(existing.get("status") or "COMPLETADO").upper()
            status = st.selectbox(
                "Estado",
                status_options,
                index=status_options.index(current_status)
                if current_status in status_options else 0,
            )
            notes = st.text_area(
                "Observaciones",
                value=str(existing.get("notes") or ""),
            )

            submit = st.form_submit_button("💾 Guardar", use_container_width=True)

        if submit:
            seconds = parse_hms(duration_text) if duration_text else 0
            if duration_text and seconds is None:
                st.error("Duración inválida. Usa HH:MM:SS.")
            else:
                if status == "OMITIDO":
                    km_to_save = 0.0
                    seconds = 0
                else:
                    km_to_save = float(km)

                save_log({
                    "session_date": selected_day.isoformat(),
                    "plan_session_id": session["id"],
                    "actual_km": km_to_save,
                    "actual_duration_sec": int(seconds or 0),
                    "rpe": int(rpe),
                    "avg_hr": int(avg_hr) if avg_hr else None,
                    "max_hr": int(max_hr) if max_hr else None,
                    "status": status,
                    "notes": notes.strip(),
                })
                st.success("Guardado permanentemente ✅")
                st.rerun()

        if existing:
            st.divider()
            st.caption(
                "Si este registro fue una prueba o quedó mal guardado, puedes eliminarlo "
                "sin modificar la sesión planificada."
            )
            if st.button(
                "🗑️ Eliminar registro de esta fecha",
                key=f"delete_log_{selected_day.isoformat()}",
                use_container_width=True,
            ):
                delete_log(selected_day.isoformat())
                st.success("Registro eliminado.")
                st.rerun()

# ============================================================
# EVALUACIÓN RCP
# ============================================================
with tabs[5]:
    st.subheader("Evaluación del corredor")
    if not ASSESSMENT_READY:
        st.error(
            "Falta instalar el módulo V6.2 en Supabase. Ejecuta el archivo "
            "supabase_v6_2_assessment.sql y recarga la app."
        )
    elif LATEST_ASSESSMENT:
        show_assessment_result(LATEST_ASSESSMENT)
        st.caption(
            "Tu plan actual NO se modifica al reevaluarte. El resultado queda guardado como historial "
            "y se utilizará por el motor adaptativo en una versión posterior."
        )
        with st.expander("🔄 Hacer una nueva evaluación"):
            assessment_form(existing_assessment=LATEST_ASSESSMENT)

        history = get_assessments(limit=10)
        if len(history) > 1:
            st.divider()
            st.markdown("### Historial")
            rows = []
            for a in history:
                created = str(a.get("created_at") or "")
                try:
                    created_label = datetime.fromisoformat(created.replace("Z", "+00:00")).strftime("%d/%m/%Y %H:%M")
                except Exception:
                    created_label = created[:16]
                rows.append({
                    "Fecha": created_label,
                    "Nivel": str(a.get("runner_level") or "").title(),
                    "Score": int(a.get("runner_score") or 0),
                    "Objetivo": a.get("goal"),
                    "Preparación": a.get("goal_readiness"),
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no has realizado tu evaluación RCP.")
        assessment_form(onboarding=True)

# ============================================================
# PERFIL
# ============================================================
with tabs[6]:
    st.subheader("Mi perfil")
    st.warning(
        "Si actualizas y regeneras el plan, los registros actuales se eliminarán "
        "para evitar mezclar dos planificaciones distintas."
    )
    profile_form(
        profile,
        assessed_level=LATEST_ASSESSMENT.get("runner_level") if LATEST_ASSESSMENT else None,
    )

    st.divider()
    st.markdown("### Mantenimiento de registros")
    if ORPHAN_LOGS:
        st.warning(
            f"Hay {len(ORPHAN_LOGS)} registro(s) que no pertenecen al plan vigente. "
            "Ya no se incluyen en los KPI ni en los gráficos."
        )
        orphan_rows = [
            {
                "Fecha": date.fromisoformat(str(x["session_date"])).strftime("%d/%m/%Y"),
                "Estado": str(x.get("status") or ""),
                "KM": float(x.get("actual_km") or 0),
                "RPE": x.get("rpe"),
            }
            for x in ORPHAN_LOGS
        ]
        st.dataframe(orphan_rows, use_container_width=True, hide_index=True)
        if st.button(
            "🧹 Eliminar registros fuera del plan",
            key="delete_orphan_logs",
            use_container_width=True,
        ):
            for old_log in ORPHAN_LOGS:
                delete_log(old_log["session_date"])
            st.success("Registros fuera del plan eliminados.")
            st.rerun()
    else:
        st.success("No hay registros huérfanos o de planes anteriores.")

    st.divider()
    st.markdown("### Cuenta")
    st.write(f"Correo: **{USER_EMAIL}**")
    st.caption(
        "Cada cuenta accede únicamente a sus propias filas gracias a las políticas RLS."
    )

st.divider()
st.caption(
    "RunningCoachPro genera orientación general de entrenamiento. "
    "No sustituye evaluación médica ni coaching individual. Ante dolor agudo, "
    "mareos, lesión o síntomas anormales, suspende el ejercicio y busca orientación profesional."
)
