
import streamlit as st
from datetime import date, datetime, timedelta, timezone
import math
import re
import html
from supabase import create_client

st.set_page_config(
    page_title="RunningCoachPro",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# V6.4.1 · Diseño UI/UX responsive · Mobile polish
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --rcp-ink: #0f172a;
        --rcp-muted: #64748b;
        --rcp-blue: #2563eb;
        --rcp-blue-soft: rgba(37, 99, 235, .09);
        --rcp-green: #16a34a;
        --rcp-orange: #ea580c;
        --rcp-violet: #7c3aed;
        --rcp-border: rgba(100, 116, 139, .20);
        --rcp-surface: rgba(248, 250, 252, .78);
    }

    .block-container {
        max-width: 1220px;
        padding-top: 1rem;
        padding-bottom: 4.5rem;
    }

    /* Header / hero */
    .rcp-hero {
        border: 1px solid var(--rcp-border);
        border-radius: 22px;
        padding: 1.15rem 1.25rem;
        margin: .15rem 0 1rem 0;
        background:
            radial-gradient(circle at 95% 10%, rgba(37,99,235,.14), transparent 32%),
            linear-gradient(135deg, rgba(248,250,252,.96), rgba(241,245,249,.78));
    }
    .rcp-eyebrow {
        color: var(--rcp-blue);
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .09em;
        text-transform: uppercase;
        margin-bottom: .18rem;
    }
    .rcp-hero h2 {
        margin: 0;
        color: var(--rcp-ink);
        font-size: 1.72rem;
        line-height: 1.12;
    }
    .rcp-hero p {
        margin: .38rem 0 0 0;
        color: var(--rcp-muted);
    }
    .rcp-pills {
        display: flex;
        flex-wrap: wrap;
        gap: .45rem;
        margin-top: .8rem;
    }
    .rcp-pill {
        display: inline-flex;
        align-items: center;
        gap: .3rem;
        padding: .34rem .62rem;
        border-radius: 999px;
        border: 1px solid var(--rcp-border);
        background: rgba(255,255,255,.72);
        color: var(--rcp-ink);
        font-size: .82rem;
        font-weight: 700;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        border: 1px solid var(--rcp-border);
        border-radius: 17px;
        padding: .82rem .9rem;
        background: var(--rcp-surface);
    }
    [data-testid="stMetricLabel"] {
        color: var(--rcp-muted);
        font-weight: 700;
    }
    [data-testid="stMetricValue"] {
        color: var(--rcp-ink);
        font-weight: 800;
    }

    /* Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--rcp-border) !important;
        border-radius: 18px !important;
    }

    /* Buttons = navigation cards / CTAs */
    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] > button {
        min-height: 48px;
        border-radius: 14px;
        font-weight: 750;
        border-width: 1px;
        transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
    }
    .stButton > button:hover,
    .stDownloadButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 18px rgba(15,23,42,.08);
    }
    button[kind="primary"] {
        min-height: 58px !important;
        font-size: 1.02rem !important;
    }

    /* Inputs */
    div[data-baseweb="input"] input,
    textarea {
        min-height: 44px;
        font-size: 16px !important;
    }

    /* Progress */
    .stProgress > div > div > div > div {
        border-radius: 999px;
    }

    /* Dataframes / charts */
    [data-testid="stDataFrame"],
    [data-testid="stVegaLiteChart"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid var(--rcp-border);
    }

    /* Remove unused tab-strip look if any library widget creates tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: .3rem;
        overflow-x: auto;
        white-space: nowrap;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: .72rem;
            padding-right: .72rem;
            padding-top: .55rem;
            padding-bottom: 5rem;
        }
        .rcp-hero {
            border-radius: 18px;
            padding: .95rem 1rem;
        }
        .rcp-hero h2 {
            font-size: 1.42rem;
        }
        h1 { font-size: 1.82rem !important; line-height: 1.12 !important; }
        h2 { font-size: 1.38rem !important; }
        h3 { font-size: 1.12rem !important; }

        /* En móvil, cualquier fila de columnas se reorganiza realmente a 2 columnas.
           El selector hijo directo vence el apilado 100% que Streamlit aplica por defecto. */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: .48rem !important;
            align-items: stretch !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            flex: 0 0 calc(50% - .24rem) !important;
            width: calc(50% - .24rem) !important;
            max-width: calc(50% - .24rem) !important;
            min-width: 0 !important;
        }
        [data-testid="stMetric"] {
            min-height: 94px;
            padding: .58rem .66rem;
        }
        [data-testid="stMetricLabel"] {
            font-size: .82rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.32rem !important;
            line-height: 1.12 !important;
        }
        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stFormSubmitButton"] > button {
            width: 100% !important;
            min-height: 46px !important;
            padding: .48rem .62rem !important;
            font-size: .94rem !important;
            line-height: 1.15 !important;
        }
        button[kind="primary"] {
            min-height: 48px !important;
            font-size: .96rem !important;
        }
        [data-testid="stVegaLiteChart"] {
            width: 100% !important;
        }
    }

    @media (max-width: 360px) {
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            flex-basis: calc(50% - .2rem) !important;
            width: calc(50% - .2rem) !important;
            max-width: calc(50% - .2rem) !important;
            min-width: 0 !important;
        }
        [data-testid="stHorizontalBlock"] {
            gap: .4rem !important;
        }
        [data-testid="stMetric"] {
            min-height: 88px;
            padding: .5rem .58rem;
        }
        .rcp-pill {
            font-size: .76rem;
        }
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
APP_VERSION = "6.4.1"

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

ASSESSMENT_VERSION = "RCP-1.1"
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

PERFORMANCE_DISTANCE_KM = {
    "1K": 1.0,
    "1 milla": 1.60934,
    "3K": 3.0,
    "5K": 5.0,
    "10K": 10.0,
    "15K": 15.0,
    "21K": 21.1,
    "42K": 42.2,
}
PERFORMANCE_CONTEXTS = ["Carrera oficial", "Carrera no oficial", "Test", "Entrenamiento"]
PERFORMANCE_TERRAINS = ["Plano/asfalto", "Ruta con desnivel", "Trail", "Cinta", "Otro"]

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


def update_profile_fields(payload):
    """Actualiza únicamente campos legacy existentes sin intentar insertar un perfil nuevo."""
    values = dict(payload)
    values["updated_at"] = datetime.now(timezone.utc).isoformat()
    client.table("rc_profiles").update(values).eq("user_id", USER_ID).execute()


def planning_storage_ready():
    """Comprueba que la migración V6.3.2 de objetivos/planes está instalada."""
    try:
        client.table("rc_goals").select("id").eq("user_id", USER_ID).limit(1).execute()
        client.table("rc_plans").select("id").eq("user_id", USER_ID).limit(1).execute()
        client.table("rc_plan_sessions").select("id,plan_id").eq("user_id", USER_ID).limit(1).execute()
        client.table("rc_workout_logs").select("id,plan_id").eq("user_id", USER_ID).limit(1).execute()
        return True
    except Exception:
        return False


def get_goals(limit=50):
    return (
        client.table("rc_goals")
        .select("*")
        .eq("user_id", USER_ID)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
        or []
    )


def get_active_goal():
    rows = (
        client.table("rc_goals")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("status", "ACTIVE")
        .limit(1)
        .execute()
        .data
        or []
    )
    return rows[0] if rows else None


def get_plans(limit=50):
    return (
        client.table("rc_plans")
        .select("*")
        .eq("user_id", USER_ID)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
        or []
    )


def get_active_plan_record():
    rows = (
        client.table("rc_plans")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("status", "ACTIVE")
        .limit(1)
        .execute()
        .data
        or []
    )
    return rows[0] if rows else None


def get_plan(plan_id=None):
    plan_record = get_active_plan_record() if plan_id is None else {"id": plan_id}
    if not plan_record:
        return []
    return (
        client.table("rc_plan_sessions")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("plan_id", int(plan_record["id"]))
        .order("session_date")
        .execute()
        .data
        or []
    )


def get_logs(plan_id=None):
    plan_record = get_active_plan_record() if plan_id is None else {"id": plan_id}
    if not plan_record:
        return []
    return (
        client.table("rc_workout_logs")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("plan_id", int(plan_record["id"]))
        .order("session_date")
        .execute()
        .data
        or []
    )


def get_unassigned_logs():
    """Legacy/orphans sin plan_id. No alimentan métricas del plan activo."""
    try:
        return (
            client.table("rc_workout_logs")
            .select("*")
            .eq("user_id", USER_ID)
            .is_("plan_id", "null")
            .order("session_date")
            .execute()
            .data
            or []
        )
    except Exception:
        return []


def save_log(payload):
    payload = dict(payload)
    active_plan = get_active_plan_record()
    plan_id = payload.get("plan_id") or (active_plan or {}).get("id")
    if not plan_id:
        raise RuntimeError("No existe un plan activo para asociar este registro.")

    payload["user_id"] = USER_ID
    payload["plan_id"] = int(plan_id)
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    client.table("rc_workout_logs").upsert(
        payload, on_conflict="user_id,plan_id,session_date"
    ).execute()


def delete_log(session_date, plan_id=None):
    active_plan = get_active_plan_record()
    pid = plan_id or (active_plan or {}).get("id")
    if not pid:
        return
    (
        client.table("rc_workout_logs")
        .delete()
        .eq("user_id", USER_ID)
        .eq("plan_id", int(pid))
        .eq("session_date", str(session_date))
        .execute()
    )


def delete_log_by_id(log_id):
    if log_id is None:
        return
    client.table("rc_workout_logs").delete().eq("user_id", USER_ID).eq("id", int(log_id)).execute()


def insert_plan_sessions(plan_id, rows):
    if not rows:
        return
    prepared = []
    for raw in rows:
        row = dict(raw)
        row["user_id"] = USER_ID
        row["plan_id"] = int(plan_id)
        prepared.append(row)
    client.table("rc_plan_sessions").insert(prepared).execute()


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
    now_iso = datetime.now(timezone.utc).isoformat()
    row["user_id"] = USER_ID
    row["assessment_version"] = ASSESSMENT_VERSION
    row["status"] = "COMPLETED"
    row["completed_at"] = now_iso
    row["updated_at"] = now_iso
    return client.table("rc_assessments").insert(row).execute()


def assessment_storage_ready():
    """V6.3.1 exige la tabla de evaluaciones y las columnas de estado."""
    try:
        (
            client.table("rc_assessments")
            .select("id,status,completed_at,updated_at")
            .eq("user_id", USER_ID)
            .limit(1)
            .execute()
        )
        return True
    except Exception:
        return False


def assessment_is_complete(assessment):
    """
    Gate central de onboarding.

    No basta con que exista una fila: debe representar una evaluación terminada
    y contener los campos mínimos necesarios para describir al corredor.
    """
    if not assessment or not isinstance(assessment, dict):
        return False

    status = str(assessment.get("status") or "COMPLETED").upper()
    if status != "COMPLETED":
        return False

    if assessment.get("runner_score") is None:
        return False
    if str(assessment.get("runner_level") or "").upper() not in RCP_LEVELS:
        return False
    if not str(assessment.get("safety_status") or "").strip():
        return False

    answers = assessment.get("answers")
    if not isinstance(answers, dict) or not answers:
        return False

    required_keys = [
        "running_status",
        "experience",
        "active_weeks_8",
        "current_days",
        "weekly_km",
        "long_run_km",
        "continuous_min",
        "quality_types",
        "intense_sessions_per_week",
        "strength_frequency",
        "injury_last12m",
        "current_pain",
        "pain_changes_gait",
        "available_days",
        "preferred_long_day",
        "weekday_time",
        "weekend_time",
    ]
    if any(key not in answers for key in required_keys):
        return False

    available_days = answers.get("available_days") or []
    if not isinstance(available_days, list) or len(available_days) < 1:
        return False

    return True


def require_completed_assessment(show_message=True):
    """Devuelve la evaluación vigente o None si el usuario aún no supera el gate."""
    assessment = get_latest_assessment()
    if assessment_is_complete(assessment):
        return assessment

    if show_message:
        st.error(
            "RunningCoachPro requiere una Evaluación RCP completa antes de crear o modificar un plan."
        )
    return None


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


def runner_level_display(level, score):
    """Etiqueta de presentación. El nivel primario sigue siendo el dato canónico."""
    level = str(level or "—").upper()
    score = int(score or 0)
    if level == "PRINCIPIANTE" and score >= 45:
        return "PRINCIPIANTE ALTO"
    if level == "INTERMEDIO" and score >= 80:
        return "INTERMEDIO ALTO"
    return level


def level_limiter_message(answers, level, score):
    """Explica por qué un score alto puede quedar limitado por reglas de experiencia."""
    level = str(level or "").upper()
    score = int(score or 0)
    experience = str(answers.get("experience") or "Nunca")
    active_weeks = int(answers.get("active_weeks_8") or 0)
    current_days = int(answers.get("current_days") or 0)
    weekly_km = float(answers.get("weekly_km") or 0)
    long_km = float(answers.get("long_run_km") or 0)
    quality_count = len(set(answers.get("quality_types") or []))

    if level == "INTERMEDIO" and score >= 75:
        missing = []
        if experience not in ("1–2 años", ">2 años"):
            missing.append(f"experiencia acumulada ({experience})")
        if current_days < 5:
            missing.append(f"frecuencia habitual ({current_days} días/sem)")
        if weekly_km < 40:
            missing.append(f"volumen estable ({weekly_km:g} km/sem)")
        if long_km < 14:
            missing.append(f"tirada larga ({long_km:g} km)")
        if quality_count < 2:
            missing.append("experiencia con al menos dos tipos de calidad")
        if missing:
            return "La clasificación AVANZADO queda limitada por " + ", ".join(missing) + "."

    if level == "PRINCIPIANTE" and score >= 50:
        if experience in ("1–3 meses",) or active_weeks < 6 or current_days <= 2:
            return (
                "La puntuación refleja una capacidad actual favorable, pero el historial reciente "
                "todavía es corto para clasificarte como INTERMEDIO."
            )

    if level == "INICIACIÓN" and score >= 30:
        return (
            "La puntuación no anula las reglas de base mínima: primero se prioriza consistencia "
            "y tolerancia a carrera continua."
        )
    return None


def base_goal_readiness(answers, safety_status):
    """Evalúa si la BASE ACTUAL permite iniciar el tipo de plan, sin mezclar calendario."""
    goal = str(answers.get("goal") or "Condición física")
    active_weeks = int(answers.get("active_weeks_8") or 0)
    weekly_km = float(answers.get("weekly_km") or 0)
    long_km = float(answers.get("long_run_km") or 0)
    continuous_min = int(answers.get("continuous_min") or 0)

    if safety_status != "SIN ALERTAS DECLARADAS":
        return "EVALUAR SEGURIDAD", [
            "El cribado de seguridad debe resolverse antes de progresar el entrenamiento."
        ]

    if goal in ("Empezar a correr", "Correr 30 min continuos", "Condición física", "Volver a correr tras una pausa"):
        return "ADECUADA CON ADAPTACIÓN", [
            "El objetivo puede abordarse con una fase inicial ajustada a tu capacidad actual."
        ]

    if goal == "Mantener rendimiento":
        if active_weeks >= 4 and weekly_km > 0:
            return "ADECUADA", ["Existe actividad reciente suficiente para plantear mantenimiento individualizado."]
        return "BASE PREVIA", ["Conviene reconstruir consistencia antes de un bloque de mantenimiento estructurado."]

    requirements = {
        "5K": (4, 8, 3, 20),
        "10K": (4, 12, 5, 30),
        "21K": (6, 18, 8, 45),
        "42K": (8, 28, 14, 60),
    }
    req = requirements.get(goal)
    if not req:
        return "REVISIÓN MANUAL", ["No hay reglas RCP definidas para este objetivo."]

    req_weeks, req_km, req_long, req_cont = req
    missing = []
    if active_weeks < req_weeks:
        missing.append(f"consistencia reciente ({active_weeks}/8 semanas)")
    if weekly_km < req_km:
        missing.append(f"volumen actual ({weekly_km:g} km/sem; referencia RCP ≥{req_km})")
    if long_km < req_long:
        missing.append(f"tirada larga actual ({long_km:g} km; referencia RCP ≥{req_long})")
    if continuous_min < req_cont:
        missing.append(f"carrera continua ({continuous_min} min; referencia RCP ≥{req_cont})")

    if not missing:
        return "ADECUADA", ["La base declarada cumple los umbrales internos RCP para iniciar este tipo de plan."]
    if len(missing) <= 2:
        return "BASE PREVIA", missing
    return "INSUFICIENTE", missing


def calendar_goal_readiness(answers, safety_status):
    """Evalúa el tiempo disponible hasta la fecha objetivo, de forma separada de la base."""
    if safety_status != "SIN ALERTAS DECLARADAS":
        return "EVALUAR SEGURIDAD", ["Primero debe resolverse el cribado de seguridad."]

    goal = str(answers.get("goal") or "Condición física")
    has_race = bool(answers.get("has_goal_race"))
    race_date_text = answers.get("goal_race_date")
    goal_style = str(answers.get("goal_style") or "Terminar")

    if goal not in GOAL_KM or GOAL_KM.get(goal) is None:
        return "NO APLICA", ["Este objetivo no requiere una fecha de carrera para poder comenzar."]
    if not has_race or not race_date_text:
        return "SIN FECHA", ["No se declaró una fecha objetivo; el plan podrá trabajar por bloques abiertos."]

    try:
        race_day = date.fromisoformat(str(race_date_text))
    except Exception:
        return "FECHA INVÁLIDA", ["No fue posible interpretar la fecha objetivo."]

    days_left = (race_day - date.today()).days
    weeks_left = max(0.0, days_left / 7)
    if days_left <= 0:
        return "INSUFICIENTE", ["La fecha objetivo ya ocurrió o corresponde al día actual."]

    # Umbrales internos de calendario. Son guardrails del motor RCP, no normas universales.
    base_min_weeks = {"5K": 4, "10K": 6, "21K": 8, "42K": 12}.get(goal, 4)
    performance_extra = 2 if goal_style in ("Mejorar mi marca", "Buscar una marca concreta") else 0
    recommended = base_min_weeks + performance_extra

    if weeks_left >= recommended:
        return "SUFICIENTE", [f"Quedan {weeks_left:.1f} semanas; referencia interna RCP ≥{recommended} para este objetivo."]
    if weeks_left >= max(3, recommended - 2):
        return "AJUSTADA", [
            f"Quedan {weeks_left:.1f} semanas. El calendario es corto para la referencia interna RCP de {recommended} semanas; "
            "el motor deberá limitar la progresión y priorizar continuidad."
        ]
    return "INSUFICIENTE", [
        f"Quedan {weeks_left:.1f} semanas; la referencia interna RCP para este objetivo es aproximadamente {recommended} semanas."
    ]


def performance_distance_km(label, custom_km=None):
    if str(label) == "Otra":
        try:
            value = float(custom_km or 0)
            return value if value > 0 else None
        except Exception:
            return None
    return PERFORMANCE_DISTANCE_KM.get(str(label))


def estimate_equivalent_time(source_seconds, source_km, target_km, exponent=1.06):
    """Equivalencia orientativa con modelo de potencia; no sustituye un test fisiológico."""
    if not source_seconds or not source_km or not target_km:
        return None
    if float(source_km) <= 0 or float(target_km) <= 0:
        return None
    return int(round(float(source_seconds) * (float(target_km) / float(source_km)) ** exponent))


def performance_summary(answers):
    """Resume rendimiento reciente y equivalencias para alimentar el futuro motor V7."""
    has_mark = bool(answers.get("race_or_test_recent"))
    if not has_mark:
        return {
            "status": "SIN MARCA RECIENTE",
            "usable": False,
            "message": "Los ritmos iniciales deberán apoyarse en RPE/talk test hasta disponer de una marca fiable.",
        }

    distance_label = str(answers.get("recent_mark_distance") or "")
    source_km = performance_distance_km(distance_label, answers.get("recent_mark_custom_km"))
    source_seconds = parse_hms(answers.get("recent_mark_time"))
    mark_date_text = answers.get("recent_mark_date")

    if not source_km or not source_seconds:
        return {
            "status": "MARCA INCOMPLETA",
            "usable": False,
            "message": "Se declaró una carrera/test reciente, pero faltan distancia o tiempo válidos.",
        }

    age_days = None
    if mark_date_text:
        try:
            age_days = max(0, (date.today() - date.fromisoformat(str(mark_date_text))).days)
        except Exception:
            age_days = None

    usable = age_days is None or age_days <= 120
    status = "DISPONIBLE" if usable else "MARCA ANTIGUA"
    goal = str(answers.get("goal") or "")
    goal_km = GOAL_KM.get(goal)
    estimated_goal_seconds = (
        estimate_equivalent_time(source_seconds, source_km, goal_km)
        if usable and goal_km else None
    )
    target_seconds = parse_hms(answers.get("goal_target_time"))

    gap_pct = None
    target_demand = None
    if estimated_goal_seconds and target_seconds:
        gap_pct = round((estimated_goal_seconds - target_seconds) / estimated_goal_seconds * 100, 1)
        if gap_pct <= 0:
            target_demand = "COMPATIBLE CON LA MARCA ACTUAL"
        elif gap_pct <= 2:
            target_demand = "PROGRESIÓN PEQUEÑA"
        elif gap_pct <= 5:
            target_demand = "OBJETIVO EXIGENTE"
        else:
            target_demand = "OBJETIVO MUY EXIGENTE"

    equivalents = {}
    if usable:
        for label, km in [("5K", 5.0), ("10K", 10.0), ("21K", 21.1), ("42K", 42.2)]:
            eq = estimate_equivalent_time(source_seconds, source_km, km)
            if eq:
                equivalents[label] = eq

    return {
        "status": status,
        "usable": bool(usable),
        "source_distance_label": distance_label,
        "source_distance_km": round(float(source_km), 3),
        "source_time_sec": int(source_seconds),
        "source_time": fmt_time(source_seconds),
        "source_pace": fmt_pace(source_seconds, source_km),
        "date": mark_date_text,
        "age_days": age_days,
        "context": answers.get("recent_mark_context"),
        "terrain": answers.get("recent_mark_terrain"),
        "rpe": answers.get("recent_mark_rpe"),
        "equivalents_sec": equivalents,
        "estimated_goal_sec": estimated_goal_seconds,
        "estimated_goal_time": fmt_time(estimated_goal_seconds) if estimated_goal_seconds else None,
        "target_time_sec": target_seconds,
        "target_time": fmt_time(target_seconds) if target_seconds else None,
        "required_improvement_pct": gap_pct,
        "target_demand": target_demand,
        "message": (
            "Marca reciente utilizable como referencia orientativa."
            if usable else
            "La marca tiene más de 120 días; se conserva como antecedente, pero no se usará automáticamente para prescribir ritmos."
        ),
    }


def goal_readiness(answers, safety_status):
    """Resultado global compatible con la columna legacy goal_readiness."""
    base_status, base_reasons = base_goal_readiness(answers, safety_status)
    calendar_status, calendar_reasons = calendar_goal_readiness(answers, safety_status)

    if safety_status != "SIN ALERTAS DECLARADAS":
        return "EVALUAR SEGURIDAD PRIMERO", base_reasons
    if base_status in ("INSUFICIENTE", "EVALUAR SEGURIDAD"):
        return "BASE INSUFICIENTE", base_reasons
    if calendar_status == "INSUFICIENTE":
        return "TIEMPO LIMITADO", calendar_reasons
    if base_status == "BASE PREVIA":
        return "NECESITA FASE DE BASE", base_reasons
    return "PREPARACIÓN ADECUADA", base_reasons


def build_runner_profile(answers, safety_status, safety_message, score, level, components):
    """Snapshot técnico estable que será la entrada del Plan Engine V7."""
    base_status, base_reasons = base_goal_readiness(answers, safety_status)
    calendar_status, calendar_reasons = calendar_goal_readiness(answers, safety_status)
    perf = performance_summary(answers)
    limiter = level_limiter_message(answers, level, score)

    progression_mode = "ESTÁNDAR"
    experience = str(answers.get("experience") or "Nunca")
    current_pain = int(answers.get("current_pain") or 0)
    if experience in ("Nunca", "<1 mes", "1–3 meses", "3–6 meses") or bool(answers.get("injury_last12m")):
        progression_mode = "CONSERVADORA"
    if current_pain >= 4 or bool(answers.get("pain_changes_gait")) or safety_status != "SIN ALERTAS DECLARADAS":
        progression_mode = "RESTRINGIDA"

    goal_date = answers.get("goal_race_date") if answers.get("has_goal_race") else None
    weeks_to_goal = None
    if goal_date:
        try:
            weeks_to_goal = round(max(0, (date.fromisoformat(str(goal_date)) - date.today()).days) / 7, 1)
        except Exception:
            pass

    return {
        "schema_version": "RCP-RUNNER-PROFILE-1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "classification": {
            "level": str(level).upper(),
            "level_display": runner_level_display(level, score),
            "score": int(score),
            "limiter": limiter,
            "components": components,
        },
        "safety": {
            "status": safety_status,
            "message": safety_message,
        },
        "experience": {
            "running_status": answers.get("running_status"),
            "experience": answers.get("experience"),
            "active_weeks_8": int(answers.get("active_weeks_8") or 0),
            "quality_types": answers.get("quality_types") or [],
            "intense_sessions_per_week": int(answers.get("intense_sessions_per_week") or 0),
            "strength_frequency": answers.get("strength_frequency"),
        },
        "training_base": {
            "current_days": int(answers.get("current_days") or 0),
            "weekly_km": float(answers.get("weekly_km") or 0),
            "weekly_km_detail": answers.get("weekly_km_detail") or [],
            "long_run_km": float(answers.get("long_run_km") or 0),
            "continuous_min": int(answers.get("continuous_min") or 0),
        },
        "tolerance": {
            "injury_last12m": bool(answers.get("injury_last12m")),
            "current_pain": int(answers.get("current_pain") or 0),
            "pain_changes_gait": bool(answers.get("pain_changes_gait")),
            "injury_areas": answers.get("injury_areas") or [],
            "progression_mode": progression_mode,
        },
        "availability": {
            "days": answers.get("available_days") or [],
            "preferred_long_day": answers.get("preferred_long_day"),
            "no_intensity_days": answers.get("no_intensity_days") or [],
            "weekday_time": answers.get("weekday_time"),
            "weekend_time": answers.get("weekend_time"),
        },
        "goal": {
            "type": answers.get("goal"),
            "style": answers.get("goal_style"),
            "date": goal_date,
            "weeks_to_goal": weeks_to_goal,
            "target_time": answers.get("goal_target_time") or None,
            "target_time_sec": parse_hms(answers.get("goal_target_time")),
        },
        "readiness": {
            "base": base_status,
            "base_reasons": base_reasons,
            "calendar": calendar_status,
            "calendar_reasons": calendar_reasons,
        },
        "performance": perf,
    }

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
    # Segunda barrera: incluso si la navegación fallara, el motor legacy no
    # puede generar un plan para un usuario sin evaluación RCP completa.
    if require_completed_assessment(show_message=False) is None:
        raise PermissionError(
            "Se requiere una Evaluación RCP completa antes de generar un plan."
        )

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



def goal_analysis_snapshot(goal_type, goal_style, race_date_value, target_time_sec, assessment=None):
    """Evalúa un objetivo oficial usando el último snapshot del corredor."""
    assessment = assessment or require_completed_assessment(show_message=False)
    if not assessment:
        return {
            "base_status": "EVALUAR SEGURIDAD",
            "calendar_status": "EVALUAR SEGURIDAD",
            "base_reasons": ["No existe una Evaluación RCP completa."],
            "calendar_reasons": [],
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }

    answers = dict(assessment.get("answers") or {})
    answers["goal"] = goal_type
    answers["goal_style"] = goal_style
    answers["has_goal_race"] = bool(race_date_value)
    answers["goal_race_date"] = str(race_date_value) if race_date_value else None
    answers["goal_target_time"] = fmt_time(target_time_sec) if target_time_sec else None

    safety = str(assessment.get("safety_status") or "")
    base_status, base_reasons = base_goal_readiness(answers, safety)
    calendar_status, calendar_reasons = calendar_goal_readiness(answers, safety)
    return {
        "assessment_id": assessment.get("id"),
        "assessment_version": assessment.get("assessment_version"),
        "safety_status": safety,
        "base_status": base_status,
        "calendar_status": calendar_status,
        "base_reasons": base_reasons,
        "calendar_reasons": calendar_reasons,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }


def create_goal_record(goal_type, goal_style, race_date_value=None, target_time_sec=None,
                       status="FUTURE", notes=None, assessment=None):
    assessment = assessment or require_completed_assessment(show_message=False)
    snapshot = goal_analysis_snapshot(
        goal_type, goal_style, race_date_value, target_time_sec, assessment
    )
    payload = {
        "user_id": USER_ID,
        "source_assessment_id": (assessment or {}).get("id"),
        "goal_type": goal_type,
        "goal_style": goal_style,
        "race_date": str(race_date_value) if race_date_value else None,
        "target_time_sec": int(target_time_sec) if target_time_sec else None,
        "status": status,
        "readiness_snapshot": snapshot,
        "notes": notes,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    result = client.table("rc_goals").insert(payload).execute().data or []
    return result[0] if result else None


def update_goal_record(goal_id, **changes):
    values = dict(changes)
    values["updated_at"] = datetime.now(timezone.utc).isoformat()
    client.table("rc_goals").update(values).eq("user_id", USER_ID).eq("id", int(goal_id)).execute()


def update_plan_record(plan_id, **changes):
    values = dict(changes)
    values["updated_at"] = datetime.now(timezone.utc).isoformat()
    client.table("rc_plans").update(values).eq("user_id", USER_ID).eq("id", int(plan_id)).execute()


def archive_active_goal_and_plan(except_goal_id=None):
    """Archiva solo el estado; nunca borra sesiones ni logs."""
    active_plan = get_active_plan_record()
    if active_plan:
        update_plan_record(active_plan["id"], status="ARCHIVED")

    active_goal = get_active_goal()
    if active_goal and int(active_goal["id"]) != int(except_goal_id or -1):
        update_goal_record(active_goal["id"], status="ARCHIVED")


def legacy_profile_for_goal(goal_row, profile, assessment):
    """Adaptador temporal entre el objetivo oficial V6.3.2 y el generador V6."""
    answers = dict((assessment or {}).get("answers") or {})
    available_days = answers.get("available_days") or []
    available_count = len(available_days)
    current_days = int(answers.get("current_days") or 0)
    candidate_days = available_count or current_days or int((profile or {}).get("days_per_week") or 3)
    days = max(3, min(6, candidate_days))

    weekly_km = float(answers.get("weekly_km") or (profile or {}).get("weekly_km") or 8.0)
    weekly_km = max(8.0, weekly_km)

    assessed_level = str((assessment or {}).get("runner_level") or "PRINCIPIANTE").upper()
    level_map = {
        "INICIACIÓN": "Principiante",
        "PRINCIPIANTE": "Principiante",
        "INTERMEDIO": "Intermedio",
        "AVANZADO": "Avanzado",
    }

    goal_type = str(goal_row.get("goal_type") or "Condición física")
    legacy_goal = goal_type if goal_type in GOAL_KM else "Condición física"
    race_date_value = goal_row.get("race_date")
    has_race = bool(race_date_value and legacy_goal != "Condición física")

    recent_seconds = None
    recent_distance_km = None
    if answers.get("race_or_test_recent"):
        recent_seconds = parse_hms(answers.get("recent_mark_time"))
        recent_distance_km = performance_distance_km(
            answers.get("recent_mark_distance"), answers.get("recent_mark_custom_km")
        )

    return {
        "display_name": str((profile or {}).get("display_name") or USER_EMAIL.split("@")[0]),
        "goal": legacy_goal,
        "level": level_map.get(assessed_level, "Principiante"),
        "days_per_week": days,
        "weekly_km": weekly_km,
        "has_race": has_race,
        "race_date": str(race_date_value) if has_race else None,
        "target_time_sec": goal_row.get("target_time_sec"),
        "current_distance_km": recent_distance_km,
        "current_time_sec": recent_seconds,
    }


def can_generate_legacy_plan(goal_row, assessment):
    """V6.3.2 conserva el motor legacy, pero evita forzarlo donde no aplica."""
    if not assessment_is_complete(assessment):
        return False, "Falta una Evaluación RCP completa."

    if str(assessment.get("safety_status") or "") != "SIN ALERTAS DECLARADAS":
        return False, "El cribado de seguridad no permite iniciar una prescripción de intensidad automáticamente."

    goal_type = str(goal_row.get("goal_type") or "")
    if goal_type not in GOAL_KM:
        return False, "Este objetivo será soportado por el Plan Engine V7; el generador V6 no tiene una plantilla válida para esta modalidad."

    answers = assessment.get("answers") or {}
    available_count = len(answers.get("available_days") or [])
    if available_count < 3:
        return False, "El generador V6 requiere al menos 3 días disponibles. V7 permitirá planes de iniciación con 2 días."

    snapshot = goal_row.get("readiness_snapshot") or goal_analysis_snapshot(
        goal_type,
        goal_row.get("goal_style") or "Terminar",
        goal_row.get("race_date"),
        goal_row.get("target_time_sec"),
        assessment,
    )
    if str(snapshot.get("base_status") or "") in ("BASE PREVIA", "INSUFICIENTE", "EVALUAR SEGURIDAD"):
        return False, (
            "La base actual requiere una fase previa. El motor legacy no debe convertir esa necesidad "
            "en un plan específico; esta transición se resolverá con el Plan Engine V7."
        )
    if str(snapshot.get("calendar_status") or "") in ("INSUFICIENTE", "FECHA INVÁLIDA", "EVALUAR SEGURIDAD"):
        return False, "El calendario disponible no permite generar de forma responsable este plan con el motor legacy."

    return True, None


def create_plan_record_for_goal(goal_row, base_profile, assessment, status="ACTIVE"):
    """Crea un ciclo y sus sesiones sin borrar ningún plan anterior."""
    can_generate, reason = can_generate_legacy_plan(goal_row, assessment)
    if not can_generate:
        return None, reason

    legacy_profile = legacy_profile_for_goal(goal_row, base_profile, assessment)
    rows = generate_plan(legacy_profile)
    if not rows:
        return None, "El generador no produjo sesiones para este objetivo."

    plan_payload = {
        "user_id": USER_ID,
        "goal_id": int(goal_row["id"]),
        "status": status,
        "engine_version": "LEGACY-V6.3.2",
        "start_date": rows[0]["session_date"],
        "end_date": rows[-1]["session_date"],
        "initial_weekly_km": float(legacy_profile["weekly_km"]),
        "days_per_week": int(legacy_profile["days_per_week"]),
        "metadata": {
            "source": "official_goal",
            "assessment_id": assessment.get("id"),
            "assessment_version": assessment.get("assessment_version"),
            "note": "Plan generado por motor legacy; se preservará al migrar al Plan Engine V7.",
        },
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    result = client.table("rc_plans").insert(plan_payload).execute().data or []
    if not result:
        return None, "No fue posible crear el registro del plan."

    plan_row = result[0]
    insert_plan_sessions(plan_row["id"], rows)

    # Mantener rc_profiles solo como capa de compatibilidad del motor legacy.
    update_profile_fields({
        "goal": legacy_profile["goal"],
        "level": legacy_profile["level"],
        "days_per_week": legacy_profile["days_per_week"],
        "weekly_km": legacy_profile["weekly_km"],
        "has_race": legacy_profile["has_race"],
        "race_date": legacy_profile["race_date"],
        "target_time_sec": legacy_profile["target_time_sec"],
        "current_distance_km": legacy_profile["current_distance_km"],
        "current_time_sec": legacy_profile["current_time_sec"],
    })
    return plan_row, None


def activate_existing_goal(goal_row, profile, assessment):
    """
    Activa un FUTURE conservando el objetivo/plan anterior como historial.

    Si ya existe un plan ACTIVE, V6.3.2 NO lo archiva hasta comprobar que el
    nuevo objetivo puede recibir un plan con el motor disponible. Así evitamos
    dejar al usuario sin entrenamiento por activar una modalidad todavía no
    soportada por el motor legacy.
    """
    snapshot = goal_analysis_snapshot(
        goal_row.get("goal_type"),
        goal_row.get("goal_style") or "Terminar",
        goal_row.get("race_date"),
        goal_row.get("target_time_sec"),
        assessment,
    )
    candidate = dict(goal_row)
    candidate["readiness_snapshot"] = snapshot

    can_generate, generation_reason = can_generate_legacy_plan(candidate, assessment)
    current_active_plan = get_active_plan_record()

    if current_active_plan and not can_generate:
        update_goal_record(goal_row["id"], readiness_snapshot=snapshot)
        return None, generation_reason, False

    archive_active_goal_and_plan(except_goal_id=goal_row["id"])
    update_goal_record(
        goal_row["id"],
        status="ACTIVE",
        readiness_snapshot=snapshot,
        source_assessment_id=assessment.get("id"),
    )
    candidate["status"] = "ACTIVE"

    plan_row = None
    if can_generate:
        plan_row, generation_reason = create_plan_record_for_goal(candidate, profile, assessment, status="ACTIVE")

    return plan_row, generation_reason, True


def complete_active_goal():
    active_plan = get_active_plan_record()
    active_goal = get_active_goal()
    if active_plan:
        update_plan_record(active_plan["id"], status="COMPLETED")
    if active_goal:
        update_goal_record(active_goal["id"], status="COMPLETED")


def _option_index(options, value, fallback=0):
    try:
        return options.index(value)
    except Exception:
        return fallback


def _readiness_compact(status):
    mapping = {
        "ADECUADA": "🟢 ADECUADA",
        "ADECUADA CON ADAPTACIÓN": "🟢 ADAPTADA",
        "BASE PREVIA": "🟡 BASE PREVIA",
        "INSUFICIENTE": "🔴 INSUFICIENTE",
        "EVALUAR SEGURIDAD": "🔴 REVISAR",
        "SUFICIENTE": "🟢 SUFICIENTE",
        "AJUSTADA": "🟡 AJUSTADA",
        "SIN FECHA": "⚪ SIN FECHA",
        "NO APLICA": "⚪ NO APLICA",
        "FECHA INVÁLIDA": "🔴 REVISAR",
    }
    return mapping.get(str(status or "").upper(), str(status or "—"))


def show_assessment_result(assessment):
    if not assessment:
        return

    score = int(assessment.get("runner_score") or 0)
    level = str(assessment.get("runner_level") or "—")
    safety = str(assessment.get("safety_status") or "—")
    goal = str(assessment.get("goal") or "—")
    answers = assessment.get("answers") or {}
    explanation = assessment.get("explanation") or {}
    components = explanation.get("components") or {}

    runner_profile = explanation.get("runner_profile")
    if not runner_profile:
        # Compatibilidad con evaluaciones RCP-1.0 guardadas antes de V6.3.
        runner_profile = build_runner_profile(
            answers,
            safety,
            assessment.get("safety_message") or "",
            score,
            level,
            components,
        )

    classification = runner_profile.get("classification") or {}
    readiness = runner_profile.get("readiness") or {}
    performance = runner_profile.get("performance") or {}
    goal_profile = runner_profile.get("goal") or {}
    training_base = runner_profile.get("training_base") or {}
    tolerance = runner_profile.get("tolerance") or {}

    level_display = classification.get("level_display") or runner_level_display(level, score)
    base_status = readiness.get("base") or "—"
    calendar_status = readiness.get("calendar") or "—"

    st.markdown("### Tu perfil RCP")
    a, b, c, d = st.columns(4)
    a.metric("Nivel RCP", str(level_display).title())
    b.metric("Capacidad de entrenamiento", f"{score}/100")
    c.metric("Objetivo", goal)
    d.metric("Base objetivo", _readiness_compact(base_status))

    limiter = classification.get("limiter")
    if limiter:
        st.info(f"**Principal limitante de clasificación:** {limiter}")

    if safety == "SIN ALERTAS DECLARADAS":
        st.success(f"**Cribado de seguridad:** {safety}. {assessment.get('safety_message') or ''}")
    elif safety == "PAUSA TEMPORAL":
        st.warning(f"**Cribado de seguridad:** {safety}. {assessment.get('safety_message') or ''}")
    else:
        st.error(f"**Cribado de seguridad:** {safety}. {assessment.get('safety_message') or ''}")

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("KM/sem actuales", f"{float(training_base.get('weekly_km') or 0):g}")
    p2.metric("Días/sem", int(training_base.get("current_days") or 0))
    p3.metric("Tirada larga", f"{float(training_base.get('long_run_km') or 0):g} km")
    p4.metric("Carrera continua", f"{int(training_base.get('continuous_min') or 0)} min")

    left, right = st.columns(2)
    with left:
        st.markdown("#### Perfil de entrenamiento")
        st.write(f"• Experiencia: {answers.get('experience') or '—'}")
        st.write(f"• Progresión inicial RCP: **{tolerance.get('progression_mode') or '—'}**")
        available = (runner_profile.get("availability") or {}).get("days") or []
        st.write(f"• Días disponibles: {', '.join(available) if available else '—'}")

        strengths = explanation.get("strengths") or []
        if strengths:
            st.markdown("#### Fortalezas actuales")
            for item in strengths:
                st.write(f"• {item}")

        development = explanation.get("development") or []
        if development:
            st.markdown("#### Áreas a desarrollar")
            for item in development:
                st.write(f"• {item}")

    with right:
        st.markdown("#### Preparación para el objetivo")
        st.write(f"**Base para {goal}:** {_readiness_compact(base_status)}")
        for item in readiness.get("base_reasons") or []:
            st.write(f"• {item}")

        st.write(f"**Calendario:** {_readiness_compact(calendar_status)}")
        if goal_profile.get("date"):
            st.write(
                f"• Fecha objetivo: {goal_profile.get('date')} · "
                f"{goal_profile.get('weeks_to_goal') if goal_profile.get('weeks_to_goal') is not None else '—'} semanas"
            )
        for item in readiness.get("calendar_reasons") or []:
            st.write(f"• {item}")

        st.markdown("#### Rendimiento actual")
        perf_status = str(performance.get("status") or "SIN MARCA RECIENTE")
        st.write(f"**{perf_status}**")
        if performance.get("source_time"):
            st.write(
                f"• Referencia: {performance.get('source_distance_label')} en {performance.get('source_time')} "
                f"({performance.get('source_pace')})"
            )
        if performance.get("estimated_goal_time") and goal in GOAL_KM:
            st.write(f"• Equivalencia orientativa {goal}: **{performance.get('estimated_goal_time')}**")
        if performance.get("target_time"):
            st.write(f"• Marca objetivo declarada: **{performance.get('target_time')}**")
        if performance.get("target_demand"):
            gap = performance.get("required_improvement_pct")
            gap_text = f" · mejora estimada {gap:.1f}%" if isinstance(gap, (int, float)) and gap > 0 else ""
            st.write(f"• Demanda del objetivo: **{performance.get('target_demand')}**{gap_text}")
        if performance.get("message"):
            st.caption(performance.get("message"))

    equivalents = performance.get("equivalents_sec") or {}
    if equivalents and performance.get("usable"):
        with st.expander("Ver equivalencias orientativas de rendimiento"):
            rows = []
            for distance_name in ["5K", "10K", "21K", "42K"]:
                sec = equivalents.get(distance_name)
                if sec:
                    rows.append({
                        "Distancia": distance_name,
                        "Tiempo equivalente": fmt_time(sec),
                        "Ritmo equivalente": fmt_pace(sec, GOAL_KM[distance_name]),
                    })
            st.dataframe(rows, use_container_width=True, hide_index=True)
            st.caption(
                "Equivalencias matemáticas orientativas basadas en una marca reciente. "
                "No son una predicción garantizada ni una medición fisiológica."
            )

    if components:
        with st.expander("Ver composición del Runner Score"):
            score_rows = [{"Dimensión": k, "Puntos": v} for k, v in components.items()]
            st.dataframe(score_rows, use_container_width=True, hide_index=True)
            st.caption(
                "El Runner Score es un índice interno RCP de experiencia y tolerancia de entrenamiento; "
                "no es una escala médica ni una medida de talento o velocidad. El nivel final también aplica reglas de experiencia mínima."
            )

    with st.expander("Ver perfil técnico que usará el futuro Plan Engine V7"):
        st.json(runner_profile)

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

        st.markdown("#### Marca reciente · opcional")
        st.caption(
            "Si marcaste carrera/test reciente, completa estos datos. RunningCoachPro la usará como referencia de rendimiento; "
            "si no tienes una marca fiable, los ritmos futuros podrán iniciarse por RPE/talk test."
        )
        pm1, pm2, pm3 = st.columns(3)
        recent_distance_options = list(PERFORMANCE_DISTANCE_KM.keys()) + ["Otra"]
        recent_mark_distance = pm1.selectbox(
            "Distancia de la marca",
            recent_distance_options,
            index=_option_index(recent_distance_options, existing_answers.get("recent_mark_distance"), 4),
        )
        recent_mark_custom_km = pm2.number_input(
            "KM si elegiste ‘Otra’",
            min_value=0.0,
            max_value=200.0,
            value=float(existing_answers.get("recent_mark_custom_km") or 0.0),
            step=0.1,
        )
        recent_mark_time = pm3.text_input(
            "Tiempo de la marca",
            value=str(existing_answers.get("recent_mark_time") or ""),
            placeholder="Ej. 49:30 o 1:47:12",
            help="Formato MM:SS o HH:MM:SS.",
        )

        default_mark_date = date.today() - timedelta(days=30)
        if existing_answers.get("recent_mark_date"):
            try:
                default_mark_date = date.fromisoformat(str(existing_answers["recent_mark_date"]))
            except Exception:
                pass
        pm4, pm5, pm6 = st.columns(3)
        recent_mark_date = pm4.date_input(
            "Fecha de la marca",
            value=default_mark_date,
            min_value=date.today() - timedelta(days=730),
            max_value=date.today(),
        )
        recent_mark_context = pm5.selectbox(
            "Tipo de registro",
            PERFORMANCE_CONTEXTS,
            index=_option_index(PERFORMANCE_CONTEXTS, existing_answers.get("recent_mark_context"), 0),
        )
        recent_mark_terrain = pm6.selectbox(
            "Terreno",
            PERFORMANCE_TERRAINS,
            index=_option_index(PERFORMANCE_TERRAINS, existing_answers.get("recent_mark_terrain"), 0),
        )
        recent_mark_rpe = st.slider(
            "RPE de esa carrera/test (1–10)",
            1, 10,
            int(existing_answers.get("recent_mark_rpe") or 8),
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

        st.markdown("### 6 · Objetivo a evaluar")
        st.caption("Este objetivo se usa para estimar preparación durante la evaluación. En V6.3.2 el objetivo deportivo oficial se gestiona aparte en 🎯 Objetivo y no se cambia al reevaluarte.")
        g1, g2 = st.columns(2)
        goal = g1.selectbox(
            "¿Qué objetivo quieres evaluar?",
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
        goal_target_time = st.text_input(
            "Marca objetivo (opcional)",
            value=str(existing_answers.get("goal_target_time") or ""),
            placeholder="Ej. 45:00 o 1:45:00",
            help=(
                "Úsala si quieres buscar una marca concreta. Formato MM:SS o HH:MM:SS. "
                "La app comparará esta meta con una marca reciente si existe."
            ),
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

    if race_or_test:
        recent_km = performance_distance_km(recent_mark_distance, recent_mark_custom_km)
        recent_seconds = parse_hms(recent_mark_time)
        if not recent_km:
            st.error("Si declaras una carrera/test reciente, indica una distancia válida.")
            return False
        if not recent_seconds:
            st.error("Si declaras una carrera/test reciente, escribe un tiempo válido (MM:SS o HH:MM:SS).")
            return False

    target_seconds_check = parse_hms(goal_target_time) if str(goal_target_time).strip() else None
    if str(goal_target_time).strip() and not target_seconds_check:
        st.error("La marca objetivo no tiene un formato válido. Usa MM:SS o HH:MM:SS.")
        return False
    if (
        goal_style == "Buscar una marca concreta"
        and goal in GOAL_KM
        and GOAL_KM.get(goal) is not None
        and not target_seconds_check
    ):
        st.error("Para ‘Buscar una marca concreta’ debes indicar la marca objetivo.")
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
        "recent_mark_distance": recent_mark_distance if race_or_test else None,
        "recent_mark_custom_km": float(recent_mark_custom_km) if race_or_test else None,
        "recent_mark_time": str(recent_mark_time).strip() if race_or_test else None,
        "recent_mark_date": recent_mark_date.isoformat() if race_or_test else None,
        "recent_mark_context": recent_mark_context if race_or_test else None,
        "recent_mark_terrain": recent_mark_terrain if race_or_test else None,
        "recent_mark_rpe": int(recent_mark_rpe) if race_or_test else None,
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
        "goal_target_time": str(goal_target_time).strip() or None,
    }

    safety_status, safety_message = evaluate_safety(answers)
    runner_score, components = calculate_runner_score(answers)
    runner_level = classify_runner(answers, runner_score)
    readiness, readiness_reasons = goal_readiness(answers, safety_status)
    explanation = assessment_explanation(answers, components, runner_level)
    runner_profile = build_runner_profile(
        answers,
        safety_status,
        safety_message,
        runner_score,
        runner_level,
        components,
    )
    explanation["runner_profile"] = runner_profile
    explanation["level_display"] = runner_profile["classification"]["level_display"]
    explanation["limiter"] = runner_profile["classification"].get("limiter")

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

    st.success(
        f"Evaluación guardada · Nivel RCP: {runner_profile['classification']['level_display'].title()} · "
        f"{runner_score}/100"
    )
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

    if require_completed_assessment() is None:
        return False

    st.error(
        "V6.3.2 ya no permite regenerar un plan desde Perfil porque eso podía destruir el historial. "
        "Usa la sección 🎯 Objetivo para crear, cambiar o activar objetivos."
    )
    return False


def basic_profile_form(assessment):
    """Crea solo la identidad/compatibilidad legacy. NO crea ni reemplaza planes."""
    answers = dict((assessment or {}).get("answers") or {})
    st.subheader("👤 Completa tu perfil básico")
    st.caption(
        "Tu Evaluación RCP ya está guardada. Solo falta el nombre con el que quieres aparecer en la app."
    )
    with st.form("basic_profile_form"):
        name = st.text_input("Nombre", value=USER_EMAIL.split("@")[0])
        submit = st.form_submit_button("Continuar", use_container_width=True)

    if not submit:
        return False
    if not name.strip():
        st.error("Escribe tu nombre.")
        return False

    assessed_level = str((assessment or {}).get("runner_level") or "PRINCIPIANTE").upper()
    level_map = {
        "INICIACIÓN": "Principiante",
        "PRINCIPIANTE": "Principiante",
        "INTERMEDIO": "Intermedio",
        "AVANZADO": "Avanzado",
    }
    available_count = len(answers.get("available_days") or [])
    current_days = int(answers.get("current_days") or 0)
    days_legacy = max(3, min(6, available_count or current_days or 3))
    weekly_legacy = max(8.0, float(answers.get("weekly_km") or 0.0))
    assessment_goal = str(answers.get("goal") or "Condición física")
    legacy_goal = assessment_goal if assessment_goal in GOAL_KM else "Condición física"
    race_date_value = answers.get("goal_race_date") if answers.get("has_goal_race") else None
    target_seconds = parse_hms(answers.get("goal_target_time"))

    save_profile({
        "display_name": name.strip(),
        "goal": legacy_goal,
        "level": level_map.get(assessed_level, "Principiante"),
        "days_per_week": days_legacy,
        "weekly_km": weekly_legacy,
        "has_race": bool(race_date_value and legacy_goal != "Condición física"),
        "race_date": race_date_value if legacy_goal != "Condición física" else None,
        "target_time_sec": target_seconds,
        "current_distance_km": None,
        "current_time_sec": None,
    })
    st.success("Perfil básico guardado.")
    st.rerun()
    return True


def _goal_label(goal):
    race = f" · {goal.get('race_date')}" if goal.get("race_date") else ""
    target = f" · {fmt_time(goal.get('target_time_sec'))}" if goal.get("target_time_sec") else ""
    return f"{goal.get('goal_type')} · {goal.get('status')}{race}{target}"


def _validate_goal_time(goal_style, target_text):
    target_seconds = parse_hms(target_text) if str(target_text or "").strip() else None
    if str(target_text or "").strip() and target_seconds is None:
        return None, "La marca objetivo no tiene un formato válido. Usa MM:SS o HH:MM:SS."
    if goal_style == "Buscar una marca concreta" and not target_seconds:
        return None, "Para buscar una marca concreta debes indicar el tiempo objetivo."
    return target_seconds, None


def official_goal_setup(profile, assessment):
    """Paso obligatorio posterior a evaluación cuando todavía no existe objetivo ACTIVE."""
    st.title("🎯 Define tu objetivo")
    st.info(
        "Tu evaluación ya está completa. Ahora RunningCoachPro necesita un objetivo oficial antes de mostrar el plan."
    )

    future_goals = [g for g in get_goals() if str(g.get("status")) == "FUTURE"]
    if future_goals:
        st.markdown("### Objetivos futuros guardados")
        options = {int(g["id"]): _goal_label(g) for g in future_goals}
        selected_id = st.selectbox(
            "Puedes activar uno de ellos",
            list(options.keys()),
            format_func=lambda x: options[x],
            key="setup_future_goal_select",
        )
        if st.button("▶️ Activar objetivo seleccionado", use_container_width=True, key="setup_activate_future"):
            goal_row = next(g for g in future_goals if int(g["id"]) == int(selected_id))
            plan_row, reason, activated = activate_existing_goal(goal_row, profile, assessment)
            if plan_row:
                st.success("Objetivo activado y nuevo plan creado sin borrar el historial anterior.")
            elif activated:
                st.warning(f"Objetivo activado. Aún no se creó un plan: {reason}")
            else:
                st.warning(f"No se activó el objetivo; el plan actual permanece intacto. Motivo: {reason}")
            st.rerun()
        st.divider()

    with st.form("official_goal_setup_form"):
        g1, g2 = st.columns(2)
        goal_type = g1.selectbox(
            "Objetivo principal",
            RCP_GOALS,
            index=_option_index(RCP_GOALS, (assessment.get("answers") or {}).get("goal"), 4),
        )
        styles = ["Terminar", "Terminar cómodo", "Mejorar mi marca", "Buscar una marca concreta"]
        goal_style = g2.selectbox("Finalidad", styles)
        has_date = st.checkbox("Tengo una fecha objetivo", value=bool((assessment.get("answers") or {}).get("has_goal_race")))
        default_date = date.today() + timedelta(weeks=12)
        old_date = (assessment.get("answers") or {}).get("goal_race_date")
        if old_date:
            try:
                default_date = max(date.today() + timedelta(days=1), date.fromisoformat(str(old_date)))
            except Exception:
                pass
        race_date_value = st.date_input(
            "Fecha objetivo",
            value=default_date,
            min_value=date.today() + timedelta(days=1),
            max_value=date.today() + timedelta(days=730),
        )
        target_text = st.text_input(
            "Marca objetivo (opcional)",
            value=str((assessment.get("answers") or {}).get("goal_target_time") or ""),
            placeholder="Ej. 45:00 o 1:47:12",
        )
        submit = st.form_submit_button("Guardar objetivo y continuar", use_container_width=True)

    if not submit:
        return False

    target_seconds, error = _validate_goal_time(goal_style, target_text)
    if error:
        st.error(error)
        return False

    goal_row = create_goal_record(
        goal_type=goal_type,
        goal_style=goal_style,
        race_date_value=race_date_value.isoformat() if has_date else None,
        target_time_sec=target_seconds,
        status="ACTIVE",
        notes="Objetivo oficial creado durante onboarding V6.3.2",
        assessment=assessment,
    )
    if not goal_row:
        st.error("No fue posible guardar el objetivo.")
        return False

    plan_row, reason = create_plan_record_for_goal(goal_row, profile, assessment, status="ACTIVE")
    if plan_row:
        st.success("Objetivo guardado y plan creado. Tu historial queda preparado para futuras planificaciones.")
    else:
        st.warning(f"Objetivo guardado. No se creó un plan automático todavía: {reason}")
    st.rerun()
    return True


def goal_management_ui(active_goal, active_plan, profile, assessment):
    st.subheader("🎯 Objetivo actual")
    if not active_goal:
        st.warning("No existe un objetivo activo.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Objetivo", active_goal.get("goal_type") or "—")
    c2.metric("Finalidad", active_goal.get("goal_style") or "—")
    c3.metric("Fecha", active_goal.get("race_date") or "Sin fecha")
    c4.metric("Meta", fmt_time(active_goal.get("target_time_sec")) if active_goal.get("target_time_sec") else "Sin marca")

    snapshot = active_goal.get("readiness_snapshot") or {}
    if snapshot:
        r1, r2 = st.columns(2)
        r1.info(f"Base para el objetivo: {_readiness_compact(snapshot.get('base_status'))}")
        r2.info(f"Calendario: {_readiness_compact(snapshot.get('calendar_status'))}")

    if active_plan:
        st.success(
            f"Plan activo #{active_plan['id']} · {active_plan.get('engine_version')} · "
            f"{active_plan.get('start_date') or '—'} → {active_plan.get('end_date') or '—'}"
        )
    else:
        st.warning(
            "Este objetivo está activo pero todavía no tiene plan. Puede ocurrir si la base/seguridad no permite "
            "prescripción automática o si el objetivo requiere el futuro Plan Engine V7."
        )

    with st.expander("✏️ Cambiar fecha o marca del objetivo actual"):
        styles = ["Terminar", "Terminar cómodo", "Mejorar mi marca", "Buscar una marca concreta"]
        with st.form("edit_active_goal_form"):
            style = st.selectbox(
                "Finalidad",
                styles,
                index=_option_index(styles, active_goal.get("goal_style"), 0),
            )
            has_date = st.checkbox("Tiene fecha", value=bool(active_goal.get("race_date")))
            default_date = date.today() + timedelta(weeks=12)
            if active_goal.get("race_date"):
                try:
                    default_date = max(date.today() + timedelta(days=1), date.fromisoformat(str(active_goal["race_date"])))
                except Exception:
                    pass
            race_date_value = st.date_input(
                "Fecha",
                value=default_date,
                min_value=date.today() + timedelta(days=1),
                max_value=date.today() + timedelta(days=730),
            )
            target_text = st.text_input(
                "Marca objetivo",
                value=fmt_time(active_goal.get("target_time_sec")) if active_goal.get("target_time_sec") else "",
            )
            save_changes = st.form_submit_button("Guardar cambios", use_container_width=True)

        if save_changes:
            target_seconds, error = _validate_goal_time(style, target_text)
            if error:
                st.error(error)
            else:
                race_iso = race_date_value.isoformat() if has_date else None
                new_snapshot = goal_analysis_snapshot(
                    active_goal.get("goal_type"), style, race_iso, target_seconds, assessment
                )
                update_goal_record(
                    active_goal["id"],
                    goal_style=style,
                    race_date=race_iso,
                    target_time_sec=target_seconds,
                    readiness_snapshot=new_snapshot,
                    source_assessment_id=assessment.get("id"),
                )
                legacy_goal = active_goal.get("goal_type") if active_goal.get("goal_type") in GOAL_KM else "Condición física"
                update_profile_fields({
                    "goal": legacy_goal,
                    "has_race": bool(race_iso and legacy_goal != "Condición física"),
                    "race_date": race_iso if legacy_goal != "Condición física" else None,
                    "target_time_sec": target_seconds,
                })
                st.success("Objetivo actualizado. El plan actual NO fue borrado ni recalibrado.")
                st.info("La recalibración automática de sesiones futuras se conectará al Plan Engine V7.")
                st.rerun()

    with st.expander("➕ Crear otro objetivo"):
        with st.form("create_additional_goal_form"):
            n1, n2 = st.columns(2)
            new_type = n1.selectbox("Nuevo objetivo", RCP_GOALS, key="new_goal_type")
            styles = ["Terminar", "Terminar cómodo", "Mejorar mi marca", "Buscar una marca concreta"]
            new_style = n2.selectbox("Finalidad", styles, key="new_goal_style")
            new_has_date = st.checkbox("Tiene fecha", value=True, key="new_goal_has_date")
            new_date = st.date_input(
                "Fecha",
                value=date.today() + timedelta(weeks=16),
                min_value=date.today() + timedelta(days=1),
                max_value=date.today() + timedelta(days=1095),
                key="new_goal_date",
            )
            new_target = st.text_input("Marca objetivo (opcional)", key="new_goal_target")
            mode = st.radio(
                "Qué hacer",
                ["Guardar como FUTURO", "Activar ahora"],
                horizontal=True,
            )
            create_submit = st.form_submit_button("Guardar nuevo objetivo", use_container_width=True)

        if create_submit:
            target_seconds, error = _validate_goal_time(new_style, new_target)
            if error:
                st.error(error)
            else:
                race_iso = new_date.isoformat() if new_has_date else None
                new_goal = create_goal_record(
                    new_type, new_style, race_iso, target_seconds,
                    status="FUTURE",
                    notes="Creado desde Gestión de Objetivos V6.3.2",
                    assessment=assessment,
                )
                if not new_goal:
                    st.error("No fue posible crear el objetivo.")
                elif mode == "Guardar como FUTURO":
                    st.success("Objetivo futuro guardado. El plan actual permanece intacto.")
                    st.rerun()
                else:
                    plan_row, reason, activated = activate_existing_goal(new_goal, profile, assessment)
                    if plan_row:
                        st.success("Nuevo objetivo activado y nuevo plan creado. El plan anterior quedó archivado, no borrado.")
                    elif activated:
                        st.warning(f"Objetivo activado sin plan automático: {reason}")
                    else:
                        st.warning(f"El nuevo objetivo quedó FUTURO y el plan actual sigue activo. Motivo: {reason}")
                    st.rerun()

    goals = get_goals()
    future_goals = [g for g in goals if str(g.get("status")) == "FUTURE"]
    if future_goals:
        st.markdown("### Próximos objetivos")
        options = {int(g["id"]): _goal_label(g) for g in future_goals}
        selected = st.selectbox(
            "Objetivo futuro",
            list(options.keys()),
            format_func=lambda x: options[x],
            key="future_goal_activate_select",
        )
        if st.button("▶️ Convertir en objetivo activo", use_container_width=True, key="activate_future_goal_button"):
            goal_row = next(g for g in future_goals if int(g["id"]) == int(selected))
            plan_row, reason, activated = activate_existing_goal(goal_row, profile, assessment)
            if plan_row:
                st.success("Objetivo activado. El plan anterior quedó archivado y el nuevo plan fue creado.")
            elif activated:
                st.warning(f"Objetivo activado sin plan automático: {reason}")
            else:
                st.warning(f"No se activó; el plan actual permanece intacto. Motivo: {reason}")
            st.rerun()

    with st.expander("🏁 Finalizar objetivo actual"):
        st.caption(
            "Marca el objetivo y su plan como COMPLETADOS. Los entrenamientos y registros permanecen en el historial."
        )
        if st.button("Marcar como COMPLETADO", use_container_width=True, key="complete_active_goal"):
            complete_active_goal()
            st.success("Objetivo completado. Ahora puedes activar o crear el siguiente.")
            st.rerun()

    st.divider()
    st.markdown("### Historial de objetivos")
    goal_rows = []
    for g in get_goals():
        goal_rows.append({
            "ID": g.get("id"),
            "Objetivo": g.get("goal_type"),
            "Finalidad": g.get("goal_style"),
            "Fecha": g.get("race_date") or "—",
            "Meta": fmt_time(g.get("target_time_sec")) if g.get("target_time_sec") else "—",
            "Estado": g.get("status"),
        })
    if goal_rows:
        st.dataframe(goal_rows, use_container_width=True, hide_index=True)

    st.markdown("### Historial de planes")
    plan_rows = []
    goals_by_id = {int(g["id"]): g for g in get_goals()}
    for p in get_plans():
        g = goals_by_id.get(int(p.get("goal_id") or 0), {})
        plan_rows.append({
            "Plan": p.get("id"),
            "Objetivo": g.get("goal_type") or "—",
            "Inicio": p.get("start_date") or "—",
            "Fin": p.get("end_date") or "—",
            "Motor": p.get("engine_version"),
            "Estado": p.get("status"),
        })
    if plan_rows:
        st.dataframe(plan_rows, use_container_width=True, hide_index=True)



profile = get_profile()
ASSESSMENT_READY = assessment_storage_ready()
LATEST_ASSESSMENT = get_latest_assessment() if ASSESSMENT_READY else None
ASSESSMENT_COMPLETE = assessment_is_complete(LATEST_ASSESSMENT) if ASSESSMENT_READY else False

# ============================================================
# V6.3.1 · GATE OBLIGATORIO DE ONBOARDING
# ============================================================
# Se ejecuta inmediatamente después de autenticar al usuario y ANTES de
# cargar Dashboard, plan, registros o configuración legacy.
if not ASSESSMENT_READY:
    st.title("🏃 RunningCoachPro")
    st.error("Falta activar el gate de Evaluación RCP de V6.3.1 en Supabase.")
    st.write(
        "Ejecuta **supabase_v6_3_1_onboarding.sql** en Supabase → SQL Editor y vuelve a cargar la app."
    )
    st.caption(
        "Por seguridad de la lógica de prescripción, V6.3.1 ya no permite saltarse la evaluación usando el generador legacy."
    )
    st.stop()

if not ASSESSMENT_COMPLETE:
    st.title("🏃 Bienvenido a RunningCoachPro")
    st.write(f"Cuenta: **{USER_EMAIL}**")
    st.info(
        "Antes de acceder al plan y al Dashboard debes completar tu Evaluación RCP. "
        "La app utilizará esta información para conocer tu experiencia, carga actual, tolerancia y disponibilidad."
    )
    st.markdown(
        "**Acceso temporalmente bloqueado hasta completar la evaluación:** "
        "Hoy · Semana · Progreso · Plan · Registro · creación/regeneración de plan."
    )
    assessment_form(existing_assessment=LATEST_ASSESSMENT, onboarding=True)
    st.stop()

# Desde aquí todo usuario tiene una evaluación completa y válida.
if not profile:
    st.title("🏃 RunningCoachPro")
    st.success("Evaluación inicial completada ✅")
    basic_profile_form(LATEST_ASSESSMENT)
    st.stop()

# V6.3.2 requiere la capa de objetivos/planes históricos.
PLANNING_READY = planning_storage_ready()
if not PLANNING_READY:
    st.title("🏃 RunningCoachPro")
    st.error("Falta instalar la migración V6.3.2 de Objetivos y Planes.")
    st.write(
        "Ejecuta **supabase_v6_3_2_goals_plans.sql** en Supabase → SQL Editor y vuelve a cargar la app."
    )
    st.caption("La migración conserva tu plan, sesiones y registros actuales.")
    st.stop()

ACTIVE_GOAL = get_active_goal()
if not ACTIVE_GOAL:
    official_goal_setup(profile, LATEST_ASSESSMENT)
    st.stop()

# Los objetivos migrados desde V6.3.1 no tenían snapshot de readiness.
# Se calcula una vez, sin tocar el plan existente.
if not (ACTIVE_GOAL.get("readiness_snapshot") or {}):
    _migrated_snapshot = goal_analysis_snapshot(
        ACTIVE_GOAL.get("goal_type"),
        ACTIVE_GOAL.get("goal_style") or "Terminar",
        ACTIVE_GOAL.get("race_date"),
        ACTIVE_GOAL.get("target_time_sec"),
        LATEST_ASSESSMENT,
    )
    update_goal_record(
        ACTIVE_GOAL["id"],
        readiness_snapshot=_migrated_snapshot,
        source_assessment_id=LATEST_ASSESSMENT.get("id"),
    )
    ACTIVE_GOAL["readiness_snapshot"] = _migrated_snapshot
    ACTIVE_GOAL["source_assessment_id"] = LATEST_ASSESSMENT.get("id")

ACTIVE_PLAN = get_active_plan_record()
PLAN = get_plan(ACTIVE_PLAN["id"]) if ACTIVE_PLAN else []
LOGS = get_logs(ACTIVE_PLAN["id"]) if ACTIVE_PLAN else []
PLAN_BY_DATE = {str(x["session_date"]): x for x in PLAN}

# Solo los registros asociados al plan ACTIVE alimentan KPI y gráficos.
CURRENT_LOGS = [
    x for x in LOGS
    if str(x.get("session_date")) in PLAN_BY_DATE
]
ORPHAN_LOGS = get_unassigned_logs() + [
    x for x in LOGS
    if str(x.get("session_date")) not in PLAN_BY_DATE
]
LOG_BY_DATE = {str(x["session_date"]): x for x in CURRENT_LOGS}

# ============================================================
# V6.4.1 · Navegación compacta por iconos / Sidebar
# ============================================================
PAGE_META = {
    "Hoy": ("🏠", "Pantalla de inicio"),
    "Semana": ("📅", "Ver la semana"),
    "Progreso": ("📈", "Gráficos y tendencias"),
    "Plan": ("🗓️", "Plan completo"),
    "Registro": ("✅", "Registrar entrenamiento"),
    "Objetivo": ("🎯", "Objetivo activo"),
    "Evaluación": ("🧭", "Evaluación RCP"),
    "Perfil": ("⚙️", "Cuenta y perfil"),
}


def set_page(page, target_day=None):
    st.session_state["rcp_page"] = page
    if target_day is not None:
        # Se aplica antes de crear el date_input en el siguiente rerun.
        st.session_state["rcp_pending_day"] = target_day


def render_icon_navigation():
    current = st.session_state.get("rcp_page", "Hoy")
    items = list(PAGE_META.items())

    for start in (0, 4):
        cols = st.columns(4)
        for col, (page, (icon, subtitle)) in zip(cols, items[start:start + 4]):
            with col:
                is_active = current == page
                if st.button(
                    f"{icon}  {page}",
                    key=f"nav_{page}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                    help=subtitle,
                ):
                    set_page(page)
                    st.rerun()


def parse_date_safe(value):
    try:
        return date.fromisoformat(str(value))
    except Exception:
        return None


def workout_kind(session):
    text = (
        f"{session.get('workout_type') or ''} "
        f"{session.get('workout_name') or ''} "
        f"{session.get('intensity') or ''}"
    ).upper()
    if "CARRERA" in text or "COMPET" in text:
        return "Carrera"
    if "LARGA" in text or "TIRADA" in text:
        return "Larga"
    if "SERIE" in text or "INTERVAL" in text:
        return "Series"
    if "TEMPO" in text or "UMBRAL" in text:
        return "Tempo"
    if "RODAJE" in text or "SUAVE" in text or "RECUP" in text:
        return "Rodaje"
    if "FUERZA" in text:
        return "Fuerza"
    return str(session.get("workout_type") or "Otro").title()


def status_label_for_date(day_value):
    log = LOG_BY_DATE.get(day_value.isoformat())
    if log:
        status = str(log.get("status") or "").upper()
        if status == "COMPLETADO":
            return "✅ Completado"
        if status == "MODIFICADO":
            return "🟡 Modificado"
        if status == "OMITIDO":
            return "⏭️ Omitido"
    if day_value < date.today():
        return "⚠️ Pendiente"
    if day_value == date.today():
        return "⏱️ Hoy"
    return "○ Pendiente"


def week_bounds(day_value):
    monday = day_value - timedelta(days=day_value.weekday())
    return monday, monday + timedelta(days=6)


def week_snapshot(day_value):
    monday, sunday = week_bounds(day_value)
    sessions = [
        p for p in PLAN
        if (d := parse_date_safe(p.get("session_date"))) and monday <= d <= sunday
    ]
    base_sessions = [p for p in sessions if not session_is_optional(p)]
    planned_km = sum(float(p.get("planned_km") or 0) for p in base_sessions)

    real_logs = []
    for log in CURRENT_LOGS:
        d = parse_date_safe(log.get("session_date"))
        if not d or not (monday <= d <= sunday):
            continue
        if str(log.get("status") or "").upper() in ("COMPLETADO", "MODIFICADO"):
            real_logs.append(log)

    real_km = sum(float(l.get("actual_km") or 0) for l in real_logs)
    rpes_local = [float(l["rpe"]) for l in real_logs if l.get("rpe") is not None]
    avg_rpe_local = sum(rpes_local) / len(rpes_local) if rpes_local else None

    due = [
        p for p in base_sessions
        if (d := parse_date_safe(p.get("session_date"))) and d <= date.today()
    ]
    done = [
        p for p in due
        if str(LOG_BY_DATE.get(str(p.get("session_date")), {}).get("status") or "").upper()
        in ("COMPLETADO", "MODIFICADO")
    ]
    pct = (len(done) / len(due) * 100) if due else None
    return {
        "monday": monday,
        "sunday": sunday,
        "sessions": sessions,
        "base_sessions": base_sessions,
        "planned_km": planned_km,
        "real_km": real_km,
        "avg_rpe": avg_rpe_local,
        "due": len(due),
        "done": len(done),
        "compliance": pct,
    }


def all_weekly_stats():
    weekly = {}
    for p in PLAN:
        week = int(p.get("week_no") or 0)
        d = parse_date_safe(p.get("session_date"))
        if not d:
            continue
        item = weekly.setdefault(
            week,
            {
                "week": week,
                "start": d - timedelta(days=d.weekday()),
                "plan": 0.0,
                "real": 0.0,
                "rpes": [],
                "load": 0.0,
                "due": 0,
                "done": 0,
            },
        )
        item["start"] = min(item["start"], d - timedelta(days=d.weekday()))
        if not session_is_optional(p):
            item["plan"] += float(p.get("planned_km") or 0)
            if d <= date.today():
                item["due"] += 1
                status = str(LOG_BY_DATE.get(d.isoformat(), {}).get("status") or "").upper()
                if status in ("COMPLETADO", "MODIFICADO"):
                    item["done"] += 1

    for log in CURRENT_LOGS:
        if str(log.get("status") or "").upper() not in ("COMPLETADO", "MODIFICADO"):
            continue
        p = PLAN_BY_DATE.get(str(log.get("session_date")))
        if not p:
            continue
        week = int(p.get("week_no") or 0)
        item = weekly.get(week)
        if not item:
            continue
        item["real"] += float(log.get("actual_km") or 0)
        if log.get("rpe") is not None:
            item["rpes"].append(float(log["rpe"]))
        duration_sec = float(log.get("actual_duration_sec") or 0)
        if duration_sec > 0 and log.get("rpe") is not None:
            # session-RPE: duración en minutos × RPE
            item["load"] += (duration_sec / 60.0) * float(log["rpe"])

    return [weekly[k] for k in sorted(weekly)]


def render_goal_hero():
    goal_name = html.escape(str(ACTIVE_GOAL.get("goal_type") or "Objetivo"))
    race_day = parse_date_safe(ACTIVE_GOAL.get("race_date"))
    target_sec = ACTIVE_GOAL.get("target_time_sec")
    target_label = fmt_time(target_sec) if target_sec else "Sin marca objetivo"
    if race_day:
        days = (race_day - date.today()).days
        race_label = race_day.strftime("%d/%m/%Y")
        countdown = f"{days} días" if days >= 0 else "Finalizado"
    else:
        race_label = "Sin fecha"
        countdown = "Bloque abierto"

    active_week = "—"
    if PLAN:
        past = [
            p for p in PLAN
            if (d := parse_date_safe(p.get("session_date"))) and d <= date.today()
        ]
        future = [
            p for p in PLAN
            if (d := parse_date_safe(p.get("session_date"))) and d >= date.today()
        ]
        ref = past[-1] if past else (future[0] if future else PLAN[-1])
        active_week = str(ref.get("week_no") or "—")

    display_name_safe = html.escape(str(profile.get("display_name") or "Runner"))
    st.markdown(
        f"""
        <div class="rcp-hero">
          <div class="rcp-eyebrow">RUNNINGCOACHPRO · V{APP_VERSION}</div>
          <h2>Hola, {display_name_safe} 👋</h2>
          <p>Tu entrenamiento de hoy, tu objetivo y tu progreso en un solo lugar.</p>
          <div class="rcp-pills">
            <span class="rcp-pill">🎯 {goal_name}</span>
            <span class="rcp-pill">📅 {race_label}</span>
            <span class="rcp-pill">⏳ {countdown}</span>
            <span class="rcp-pill">⏱️ {target_label}</span>
            <span class="rcp-pill">🗓️ Semana {active_week}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Sidebar: contexto y utilidades, no navegación principal.
st.sidebar.title("🏃 RunningCoachPro")
st.sidebar.caption(f"V{APP_VERSION} · Multiusuario")
st.sidebar.markdown(f"**{profile['display_name']}**")
st.sidebar.caption(USER_EMAIL)
st.sidebar.markdown(f"🎯 **{ACTIVE_GOAL.get('goal_type') or '—'}**")
if ACTIVE_GOAL.get("race_date"):
    st.sidebar.caption(f"Fecha objetivo · {ACTIVE_GOAL.get('race_date')}")

if LATEST_ASSESSMENT:
    _side_score = int(LATEST_ASSESSMENT.get("runner_score") or 0)
    _side_level = str(LATEST_ASSESSMENT.get("runner_level") or "—")
    _side_explanation = LATEST_ASSESSMENT.get("explanation") or {}
    _side_profile = _side_explanation.get("runner_profile") or {}
    _side_display = (
        (_side_profile.get("classification") or {}).get("level_display")
        or runner_level_display(_side_level, _side_score)
    )
    st.sidebar.markdown(f"🧭 **{str(_side_display).title()}** · {_side_score}/100")

if "rcp_pending_day" in st.session_state:
    st.session_state["selected_day_picker"] = st.session_state.pop("rcp_pending_day")
elif "selected_day_picker" not in st.session_state:
    st.session_state["selected_day_picker"] = date.today()

selected_day = st.sidebar.date_input(
    "Explorar fecha",
    key="selected_day_picker",
)

if st.sidebar.button("↩️ Volver a Hoy", use_container_width=True):
    set_page("Hoy", date.today())
    st.rerun()

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
# V6.4 · Dashboard global
# ============================================================
if "rcp_page" not in st.session_state:
    st.session_state["rcp_page"] = "Hoy"

if st.session_state["rcp_page"] not in PAGE_META:
    st.session_state["rcp_page"] = "Hoy"

completed = [
    l for l in CURRENT_LOGS
    if str(l.get("status", "")).upper() in ("COMPLETADO", "MODIFICADO")
]
actual_km_total = sum(float(x.get("actual_km") or 0) for x in completed)

dashboard_day = date.today()
due_sessions = [
    p for p in PLAN
    if (d := parse_date_safe(p.get("session_date")))
    and d <= dashboard_day
    and not session_is_optional(p)
]
done_due = [
    p for p in due_sessions
    if str(LOG_BY_DATE.get(str(p["session_date"]), {}).get("status", "")).upper()
    in ("COMPLETADO", "MODIFICADO")
]
compliance = (len(done_due) / len(due_sessions) * 100) if due_sessions else 0

rpes = [float(x["rpe"]) for x in completed if x.get("rpe") is not None]
avg_rpe = sum(rpes) / len(rpes) if rpes else None

render_goal_hero()
render_icon_navigation()
st.divider()

current_page = st.session_state.get("rcp_page", "Hoy")
icon, subtitle = PAGE_META[current_page]


# ============================================================
# 🏠 HOY · Home real
# ============================================================
if current_page == "Hoy":
    if selected_day == date.today():
        st.subheader("🏠 Hoy")
    else:
        st.subheader(f"📍 {DAY_NAMES[selected_day.weekday()]} · {selected_day.strftime('%d/%m/%Y')}")
        st.caption("Estás explorando otra fecha. Usa “Volver a Hoy” para regresar al inicio.")

    today_session = PLAN_BY_DATE.get(selected_day.isoformat())
    today_log = LOG_BY_DATE.get(selected_day.isoformat())

    with st.container(border=True):
        if not today_session:
            st.markdown("### 😴 Recuperación")
            st.write("No hay una sesión programada para esta fecha.")
            future = [
                p for p in PLAN
                if (d := parse_date_safe(p.get("session_date"))) and d > selected_day
            ]
            if future:
                nxt = future[0]
                nxt_day = parse_date_safe(nxt["session_date"])
                st.info(
                    f"Próxima sesión: **{nxt_day.strftime('%d/%m')} · {nxt['workout_name']} · "
                    f"{float(nxt.get('planned_km') or 0):g} km**"
                )
                c1, c2 = st.columns(2)
                if c1.button("📅 Ver semana", use_container_width=True):
                    set_page("Semana", nxt_day)
                    st.rerun()
                if c2.button("🗓️ Ver plan", use_container_width=True):
                    set_page("Plan")
                    st.rerun()
        else:
            status_label = status_label_for_date(selected_day)
            st.caption(f"{workout_kind(today_session).upper()} · {status_label}")
            st.markdown(f"## {today_session['workout_name']}")
            st.markdown(f"**🎯 {today_session.get('target') or 'Por esfuerzo'}**")

            a, b, c, dcol = st.columns(4)
            a.metric("Distancia", f"{float(today_session.get('planned_km') or 0):g} km")
            b.metric("Semana", int(today_session.get("week_no") or 0))
            c.metric("Intensidad", str(today_session.get("intensity") or "—").title())
            dcol.metric("Estado", status_label.replace("✅ ", "").replace("🟡 ", "").replace("⏭️ ", "").replace("⏱️ ", "").replace("⚠️ ", ""))

            with st.expander("📋 Cómo hacerlo", expanded=False):
                st.write(today_session.get("description") or "Sin instrucciones adicionales.")

            if today_log:
                status = str(today_log.get("status") or "").upper()
                if status in ("COMPLETADO", "MODIFICADO"):
                    st.success(
                        f"{status} ✅ · {float(today_log.get('actual_km') or 0):g} km · "
                        f"{fmt_pace(today_log.get('actual_duration_sec'), today_log.get('actual_km'))} · "
                        f"RPE {today_log.get('rpe') or '—'}"
                    )
                elif status == "OMITIDO":
                    st.warning("Sesión marcada como omitida.")

            q1, q2, q3 = st.columns(3)
            _saved_status = str((today_log or {}).get("status") or "").upper()
            _register_label = (
                "✏️ Ver / editar"
                if _saved_status in ("COMPLETADO", "MODIFICADO", "OMITIDO")
                else "✅ Registrar"
            )
            if q1.button(_register_label, use_container_width=True, type="primary"):
                set_page("Registro", selected_day)
                st.rerun()
            if q2.button("📅 Mi semana", use_container_width=True):
                set_page("Semana", selected_day)
                st.rerun()
            if q3.button("📈 Ver progreso", use_container_width=True):
                set_page("Progreso")
                st.rerun()

    # Resumen semanal
    st.markdown("### Esta semana")
    snap = week_snapshot(date.today())
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Plan", f"{snap['planned_km']:.1f} km")
    s2.metric("Real", f"{snap['real_km']:.1f} km")
    s3.metric(
        "Cumplimiento",
        "—" if snap["compliance"] is None else f"{snap['compliance']:.0f}%",
    )
    s4.metric(
        "RPE medio",
        "—" if snap["avg_rpe"] is None else f"{snap['avg_rpe']:.1f}/10",
    )

    if snap["compliance"] is not None:
        st.progress(min(1.0, max(0.0, snap["compliance"] / 100)))
        st.caption(f"{snap['done']} de {snap['due']} sesiones base vencidas completadas.")

    # Vista rápida de 4 semanas
    weekly_all = all_weekly_stats()
    if weekly_all:
        today_monday, _ = week_bounds(date.today())
        eligible = [w for w in weekly_all if w["start"] <= today_monday]
        preview = (eligible[-4:] if eligible else weekly_all[:4])
        quick_values = []
        for w in preview:
            quick_values.extend([
                {"Semana": f"S{w['week']}", "Serie": "Plan", "KM": round(w["plan"], 1)},
                {"Semana": f"S{w['week']}", "Serie": "Real", "KM": round(w["real"], 1)},
            ])
        st.markdown("### 📊 Últimas semanas")
        st.vega_lite_chart(
            {
                "data": {"values": quick_values},
                "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "tooltip": True},
                "encoding": {
                    "x": {"field": "Semana", "type": "ordinal", "title": None},
                    "xOffset": {"field": "Serie"},
                    "y": {"field": "KM", "type": "quantitative", "title": "KM"},
                    "color": {"field": "Serie", "type": "nominal"},
                    "tooltip": [
                        {"field": "Semana", "type": "ordinal"},
                        {"field": "Serie", "type": "nominal"},
                        {"field": "KM", "type": "quantitative"},
                    ],
                },
                "height": 220,
            },
            use_container_width=True,
        )

    st.markdown("### Próximos entrenamientos")
    upcoming = [
        p for p in PLAN
        if (d := parse_date_safe(p.get("session_date"))) and d >= date.today()
    ][:4]
    if not upcoming:
        st.info("No quedan sesiones futuras en el plan activo.")
    else:
        for p in upcoming:
            d = parse_date_safe(p["session_date"])
            with st.container(border=True):
                c1, c2, c3 = st.columns([1.05, 2.6, 1])
                c1.markdown(f"**{DAY_NAMES[d.weekday()]}**")
                c1.caption(d.strftime("%d/%m"))
                c2.markdown(f"**{p['workout_name']}**")
                c2.caption(f"{workout_kind(p)} · {p.get('target') or 'Por esfuerzo'}")
                c3.markdown(f"**{float(p.get('planned_km') or 0):g} km**")
                if c3.button("Abrir", key=f"home_open_{p['id']}", use_container_width=True):
                    set_page("Registro", d)
                    st.rerun()


# ============================================================
# 📅 SEMANA
# ============================================================
elif current_page == "Semana":
    monday, sunday = week_bounds(selected_day)
    title_col, prev_col, next_col = st.columns([3.5, 1, 1])
    title_col.subheader(f"📅 Semana · {monday.strftime('%d/%m')} – {sunday.strftime('%d/%m/%Y')}")
    if prev_col.button("← Anterior", use_container_width=True):
        set_page("Semana", selected_day - timedelta(days=7))
        st.rerun()
    if next_col.button("Siguiente →", use_container_width=True):
        set_page("Semana", selected_day + timedelta(days=7))
        st.rerun()

    snap = week_snapshot(selected_day)
    w1, w2, w3, w4 = st.columns(4)
    w1.metric("Plan base", f"{snap['planned_km']:.1f} km")
    w2.metric("Real", f"{snap['real_km']:.1f} km")
    w3.metric("Sesiones", len(snap["sessions"]))
    w4.metric(
        "Cumplimiento",
        "—" if snap["compliance"] is None else f"{snap['compliance']:.0f}%",
    )

    for i in range(7):
        d = monday + timedelta(days=i)
        s = PLAN_BY_DATE.get(d.isoformat())
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([1, 2.7, 1, 1])
            c1.markdown(f"**{DAY_NAMES[d.weekday()]}**")
            c1.caption(d.strftime("%d/%m"))
            if s:
                c2.markdown(f"**{s['workout_name']}**")
                c2.caption(f"{workout_kind(s)} · {s.get('target') or 'Por esfuerzo'}")
                c3.markdown(f"**{float(s.get('planned_km') or 0):g} km**")
                c3.caption(status_label_for_date(d))
                if c4.button("Abrir", key=f"week_open_{s['id']}", use_container_width=True):
                    set_page("Registro", d)
                    st.rerun()
            else:
                c2.markdown("**😴 Descanso / recuperación**")
                c2.caption("Sin sesión planificada")
                c3.caption("—")


# ============================================================
# 📈 PROGRESO · Dashboard analítico
# ============================================================
elif current_page == "Progreso":
    st.subheader("📈 Progreso")
    st.caption("Explora carga, volumen, cumplimiento, ritmo, frecuencia cardiaca y evolución de las sesiones.")

    weekly_all = all_weekly_stats()
    period = st.selectbox(
        "Periodo",
        ["Hasta hoy", "Últimas 4 semanas", "Últimas 8 semanas", "Plan completo"],
        index=1,
    )

    current_monday, _ = week_bounds(date.today())
    past_current = [w for w in weekly_all if w["start"] <= current_monday]
    if period == "Últimas 4 semanas":
        weekly_view = past_current[-4:] if past_current else weekly_all[:4]
    elif period == "Últimas 8 semanas":
        weekly_view = past_current[-8:] if past_current else weekly_all[:8]
    elif period == "Hasta hoy":
        weekly_view = past_current
    else:
        weekly_view = weekly_all

    view_weeks = {w["week"] for w in weekly_view}
    plan_km_view = sum(w["plan"] for w in weekly_view)
    real_km_view = sum(w["real"] for w in weekly_view)
    due_view = sum(w["due"] for w in weekly_view)
    done_view = sum(w["done"] for w in weekly_view)
    compliance_view = (done_view / due_view * 100) if due_view else None
    load_view = sum(w["load"] for w in weekly_view)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("KM plan", f"{plan_km_view:.1f}")
    p2.metric("KM real", f"{real_km_view:.1f}")
    p3.metric("Cumplimiento", "—" if compliance_view is None else f"{compliance_view:.0f}%")
    p4.metric("Carga sRPE", "—" if load_view <= 0 else f"{load_view:.0f}")

    # 1 · Plan vs real
    st.markdown("### Plan vs real")
    values = []
    for w in weekly_view:
        values.extend([
            {"Semana": f"S{w['week']}", "Serie": "Plan base", "KM": round(w["plan"], 1)},
            {"Semana": f"S{w['week']}", "Serie": "Real", "KM": round(w["real"], 1)},
        ])
    if values:
        st.vega_lite_chart(
            {
                "data": {"values": values},
                "mark": {"type": "bar", "tooltip": True, "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4},
                "encoding": {
                    "x": {"field": "Semana", "type": "ordinal", "title": None},
                    "xOffset": {"field": "Serie"},
                    "y": {"field": "KM", "type": "quantitative", "title": "KM"},
                    "color": {"field": "Serie", "type": "nominal"},
                    "tooltip": [
                        {"field": "Semana", "type": "ordinal"},
                        {"field": "Serie", "type": "nominal"},
                        {"field": "KM", "type": "quantitative"},
                    ],
                },
                "height": 290,
            },
            use_container_width=True,
        )
    else:
        st.info("No hay semanas disponibles para este periodo.")

    # 2 · Cumplimiento + RPE
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("### Cumplimiento semanal")
        compliance_values = [
            {
                "Semana": f"S{w['week']}",
                "Cumplimiento": round(w["done"] / w["due"] * 100, 1),
                "Completadas": w["done"],
                "Vencidas": w["due"],
            }
            for w in weekly_view if w["due"] > 0
        ]
        if compliance_values:
            st.vega_lite_chart(
                {
                    "data": {"values": compliance_values},
                    "mark": {"type": "bar", "tooltip": True, "cornerRadiusTopLeft": 5, "cornerRadiusTopRight": 5},
                    "encoding": {
                        "x": {"field": "Semana", "type": "ordinal", "title": None},
                        "y": {
                            "field": "Cumplimiento",
                            "type": "quantitative",
                            "scale": {"domain": [0, 100]},
                            "title": "%",
                        },
                        "tooltip": [
                            {"field": "Semana"},
                            {"field": "Cumplimiento"},
                            {"field": "Completadas"},
                            {"field": "Vencidas"},
                        ],
                    },
                    "height": 250,
                },
                use_container_width=True,
            )
        else:
            st.info("Todavía no hay sesiones base vencidas.")

    with c_right:
        st.markdown("### RPE semanal")
        rpe_values = [
            {
                "Semana": f"S{w['week']}",
                "RPE": round(sum(w["rpes"]) / len(w["rpes"]), 1),
            }
            for w in weekly_view if w["rpes"]
        ]
        if rpe_values:
            st.vega_lite_chart(
                {
                    "data": {"values": rpe_values},
                    "mark": {"type": "line", "point": True, "tooltip": True},
                    "encoding": {
                        "x": {"field": "Semana", "type": "ordinal", "title": None},
                        "y": {
                            "field": "RPE",
                            "type": "quantitative",
                            "scale": {"domain": [1, 10]},
                            "title": "RPE",
                        },
                        "tooltip": [{"field": "Semana"}, {"field": "RPE"}],
                    },
                    "height": 250,
                },
                use_container_width=True,
            )
        else:
            st.info("Todavía no hay RPE registrados.")

    # 3 · Carga sRPE
    st.markdown("### Carga interna semanal · session-RPE")
    load_values = [
        {"Semana": f"S{w['week']}", "Carga": round(w["load"], 0)}
        for w in weekly_view if w["load"] > 0
    ]
    if load_values:
        st.vega_lite_chart(
            {
                "data": {"values": load_values},
                "mark": {"type": "area", "line": True, "point": True, "tooltip": True, "opacity": 0.28},
                "encoding": {
                    "x": {"field": "Semana", "type": "ordinal", "title": None},
                    "y": {"field": "Carga", "type": "quantitative", "title": "min × RPE"},
                    "tooltip": [{"field": "Semana"}, {"field": "Carga"}],
                },
                "height": 250,
            },
            use_container_width=True,
        )
        st.caption("Carga sRPE = duración real de la sesión en minutos × RPE. Solo usa registros con duración y RPE.")
    else:
        st.info("Registra duración y RPE para calcular carga interna.")

    # 4 · Tirada larga
    st.markdown("### Evolución de tirada larga")
    long_values = []
    for p in PLAN:
        week = int(p.get("week_no") or 0)
        if week not in view_weeks or workout_kind(p) != "Larga":
            continue
        d = parse_date_safe(p.get("session_date"))
        log = LOG_BY_DATE.get(str(p.get("session_date"))) or {}
        long_values.append({
            "Fecha": d.isoformat() if d else str(p.get("session_date")),
            "Serie": "Plan",
            "KM": round(float(p.get("planned_km") or 0), 1),
        })
        if str(log.get("status") or "").upper() in ("COMPLETADO", "MODIFICADO"):
            long_values.append({
                "Fecha": d.isoformat() if d else str(p.get("session_date")),
                "Serie": "Real",
                "KM": round(float(log.get("actual_km") or 0), 1),
            })
    if long_values:
        st.vega_lite_chart(
            {
                "data": {"values": long_values},
                "mark": {"type": "line", "point": True, "tooltip": True},
                "encoding": {
                    "x": {"field": "Fecha", "type": "temporal", "title": None},
                    "y": {"field": "KM", "type": "quantitative", "title": "KM"},
                    "color": {"field": "Serie", "type": "nominal"},
                    "tooltip": [{"field": "Fecha", "type": "temporal"}, {"field": "Serie"}, {"field": "KM"}],
                },
                "height": 260,
            },
            use_container_width=True,
        )
    else:
        st.info("No hay tiradas largas en el periodo seleccionado.")

    # 5 · Ritmo + FC
    pace_values = []
    hr_values = []
    type_km = {}
    for log in completed:
        p = PLAN_BY_DATE.get(str(log.get("session_date")))
        if not p or int(p.get("week_no") or 0) not in view_weeks:
            continue
        d = parse_date_safe(log.get("session_date"))
        km = float(log.get("actual_km") or 0)
        sec = float(log.get("actual_duration_sec") or 0)
        if km > 0 and sec > 0:
            pace_values.append({
                "Fecha": d.isoformat() if d else str(log.get("session_date")),
                "Ritmo": round((sec / km) / 60.0, 3),
                "Sesión": str(p.get("workout_name") or ""),
            })
        if log.get("avg_hr") is not None and float(log.get("avg_hr") or 0) > 0:
            hr_values.append({
                "Fecha": d.isoformat() if d else str(log.get("session_date")),
                "FC": int(log.get("avg_hr")),
                "Sesión": str(p.get("workout_name") or ""),
            })
        kind = workout_kind(p)
        type_km[kind] = type_km.get(kind, 0.0) + km

    trend_left, trend_right = st.columns(2)
    with trend_left:
        st.markdown("### Ritmo real")
        if pace_values:
            st.vega_lite_chart(
                {
                    "data": {"values": pace_values},
                    "mark": {"type": "line", "point": True, "tooltip": True},
                    "encoding": {
                        "x": {"field": "Fecha", "type": "temporal", "title": None},
                        "y": {
                            "field": "Ritmo",
                            "type": "quantitative",
                            "title": "min/km",
                            "scale": {"reverse": True},
                        },
                        "tooltip": [
                            {"field": "Fecha", "type": "temporal"},
                            {"field": "Ritmo", "type": "quantitative", "format": ".2f"},
                            {"field": "Sesión"},
                        ],
                    },
                    "height": 250,
                },
                use_container_width=True,
            )
        else:
            st.info("Registra distancia y duración para ver tu tendencia de ritmo.")

    with trend_right:
        st.markdown("### FC media")
        if hr_values:
            st.vega_lite_chart(
                {
                    "data": {"values": hr_values},
                    "mark": {"type": "line", "point": True, "tooltip": True},
                    "encoding": {
                        "x": {"field": "Fecha", "type": "temporal", "title": None},
                        "y": {"field": "FC", "type": "quantitative", "title": "lpm", "scale": {"zero": False}},
                        "tooltip": [{"field": "Fecha", "type": "temporal"}, {"field": "FC"}, {"field": "Sesión"}],
                    },
                    "height": 250,
                },
                use_container_width=True,
            )
        else:
            st.info("Registra FC media para activar este gráfico.")

    # 6 · Distribución
    st.markdown("### Distribución de kilómetros realizados")
    distribution_values = [
        {"Tipo": kind, "KM": round(km, 1)}
        for kind, km in sorted(type_km.items(), key=lambda x: x[1], reverse=True)
        if km > 0
    ]
    if distribution_values:
        st.vega_lite_chart(
            {
                "data": {"values": distribution_values},
                "mark": {"type": "arc", "innerRadius": 55, "tooltip": True},
                "encoding": {
                    "theta": {"field": "KM", "type": "quantitative"},
                    "color": {"field": "Tipo", "type": "nominal"},
                    "tooltip": [{"field": "Tipo"}, {"field": "KM"}],
                },
                "height": 300,
            },
            use_container_width=True,
        )
    else:
        st.info("Completa entrenamientos para ver la distribución por tipo.")


# ============================================================
# 🗓️ PLAN
# ============================================================
elif current_page == "Plan":
    st.subheader("🗓️ Mi plan")
    st.caption("Filtra el ciclo y abre una sesión para revisar su detalle.")

    types = sorted({workout_kind(p) for p in PLAN})
    f1, f2, f3 = st.columns(3)
    type_filter = f1.selectbox("Tipo", ["Todos"] + types)
    status_filter = f2.selectbox("Estado", ["Todos", "Pendiente", "Completado", "Modificado", "Omitido"])
    weeks = sorted({int(p.get("week_no") or 0) for p in PLAN})
    week_filter = f3.selectbox("Semana", ["Todas"] + [str(w) for w in weeks])

    table = []
    filtered_plan = []
    for p in PLAN:
        d = parse_date_safe(p.get("session_date"))
        log = LOG_BY_DATE.get(str(p.get("session_date")))
        status = str(log.get("status") or "PENDIENTE").title() if log else "Pendiente"
        kind = workout_kind(p)
        if type_filter != "Todos" and kind != type_filter:
            continue
        if status_filter != "Todos" and status.lower() != status_filter.lower():
            continue
        if week_filter != "Todas" and int(p.get("week_no") or 0) != int(week_filter):
            continue
        filtered_plan.append(p)
        table.append({
            "Fecha": d.strftime("%d/%m/%Y") if d else str(p.get("session_date")),
            "Semana": p.get("week_no"),
            "Tipo": kind,
            "Entrenamiento": p.get("workout_name"),
            "KM": float(p.get("planned_km") or 0),
            "Objetivo": p.get("target"),
            "Opcional": "Sí" if session_is_optional(p) else "No",
            "Estado": status,
        })

    st.dataframe(table, use_container_width=True, hide_index=True)

    if filtered_plan:
        labels = {
            f"{parse_date_safe(p['session_date']).strftime('%d/%m')} · {p['workout_name']}": p
            for p in filtered_plan
        }
        chosen = st.selectbox("Abrir detalle de una sesión", list(labels.keys()))
        p = labels[chosen]
        with st.container(border=True):
            st.markdown(f"### {p['workout_name']}")
            st.caption(
                f"{workout_kind(p)} · Semana {p.get('week_no')} · "
                f"{float(p.get('planned_km') or 0):g} km · {p.get('intensity') or '—'}"
            )
            st.markdown(f"**Objetivo:** {p.get('target') or 'Por esfuerzo'}")
            st.write(p.get("description") or "Sin instrucciones adicionales.")
            d = parse_date_safe(p.get("session_date"))
            if st.button("✅ Ir a registrar esta sesión", use_container_width=True, type="primary"):
                set_page("Registro", d)
                st.rerun()


# ============================================================
# ✅ REGISTRO
# ============================================================
elif current_page == "Registro":
    st.subheader("✅ Registrar entrenamiento")
    st.caption(f"Fecha seleccionada: {selected_day.strftime('%d/%m/%Y')}")

    session = PLAN_BY_DATE.get(selected_day.isoformat())
    if not session:
        st.info("Selecciona en la barra lateral una fecha que tenga entrenamiento programado.")
        nearby = [
            p for p in PLAN
            if (d := parse_date_safe(p.get("session_date"))) and d >= date.today()
        ][:5]
        if nearby:
            st.markdown("### Próximas sesiones")
            for p in nearby:
                d = parse_date_safe(p["session_date"])
                if st.button(
                    f"{d.strftime('%d/%m')} · {p['workout_name']} · {float(p.get('planned_km') or 0):g} km",
                    key=f"reg_pick_{p['id']}",
                    use_container_width=True,
                ):
                    set_page("Registro", d)
                    st.rerun()
    else:
        existing = LOG_BY_DATE.get(selected_day.isoformat(), {})
        with st.container(border=True):
            st.caption(f"{workout_kind(session).upper()} · SEMANA {session.get('week_no')}")
            st.markdown(f"## {session['workout_name']}")
            r1, r2, r3 = st.columns(3)
            r1.metric("Plan", f"{float(session.get('planned_km') or 0):g} km")
            r2.metric("Objetivo", str(session.get("target") or "Por esfuerzo"))
            r3.metric("Estado", status_label_for_date(selected_day).split(" ", 1)[-1])
            with st.expander("📋 Instrucciones"):
                st.write(session.get("description") or "Sin instrucciones adicionales.")

        with st.form("log_form"):
            st.markdown("### ¿Cómo salió?")
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
            avg_hr = h1.number_input("FC media (opcional)", 0, 230, int(existing.get("avg_hr") or 0))
            max_hr = h2.number_input("FC máxima (opcional)", 0, 240, int(existing.get("max_hr") or 0))

            status_options = ["COMPLETADO", "MODIFICADO", "OMITIDO"]
            current_status = str(existing.get("status") or "COMPLETADO").upper()
            status = st.selectbox(
                "Estado",
                status_options,
                index=status_options.index(current_status) if current_status in status_options else 0,
            )
            notes = st.text_area("Observaciones", value=str(existing.get("notes") or ""))
            submit = st.form_submit_button("💾 Guardar entrenamiento", use_container_width=True)

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
                st.success("Entrenamiento guardado ✅")
                set_page("Hoy", selected_day)
                st.rerun()

        if existing:
            st.divider()
            st.caption("Puedes eliminar un registro erróneo sin modificar la sesión planificada.")
            if st.button(
                "🗑️ Eliminar registro de esta fecha",
                key=f"delete_log_{selected_day.isoformat()}",
                use_container_width=True,
            ):
                delete_log(selected_day.isoformat())
                st.success("Registro eliminado.")
                st.rerun()


# ============================================================
# 🎯 OBJETIVO
# ============================================================
elif current_page == "Objetivo":
    st.subheader("🎯 Objetivo")
    goal_management_ui(ACTIVE_GOAL, ACTIVE_PLAN, profile, LATEST_ASSESSMENT)


# ============================================================
# 🧭 EVALUACIÓN
# ============================================================
elif current_page == "Evaluación":
    st.subheader("🧭 Evaluación del corredor")
    if not ASSESSMENT_READY:
        st.error(
            "Falta instalar el módulo V6.2 en Supabase. Ejecuta el archivo "
            "supabase_v6_2_assessment.sql y recarga la app."
        )
    elif LATEST_ASSESSMENT:
        show_assessment_result(LATEST_ASSESSMENT)
        st.caption(
            "Reevaluarte NO modifica tu objetivo oficial ni tu plan activo. "
            "El resultado queda guardado como historial y sirve como snapshot actualizado del corredor."
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
                a_answers = a.get("answers") or {}
                a_explanation = a.get("explanation") or {}
                a_level = str(a.get("runner_level") or "")
                a_score = int(a.get("runner_score") or 0)
                a_profile = a_explanation.get("runner_profile") or {}
                a_display = (
                    (a_profile.get("classification") or {}).get("level_display")
                    or runner_level_display(a_level, a_score)
                )
                a_base = (a_profile.get("readiness") or {}).get("base")
                if not a_base:
                    a_base, _ = base_goal_readiness(a_answers, str(a.get("safety_status") or ""))
                rows.append({
                    "Fecha": created_label,
                    "Versión": a.get("assessment_version"),
                    "Nivel": str(a_display).title(),
                    "Score": a_score,
                    "Objetivo evaluado": a.get("goal"),
                    "Base": a_base,
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no has realizado tu evaluación RCP.")
        assessment_form(onboarding=True)


# ============================================================
# ⚙️ PERFIL
# ============================================================
elif current_page == "Perfil":
    st.subheader("⚙️ Mi perfil")
    st.caption(
        "El objetivo deportivo se gestiona en 🎯 Objetivo. "
        "Editar tu identidad no regenera ni elimina el plan."
    )

    with st.form("profile_identity_form"):
        display_name = st.text_input("Nombre", value=str(profile.get("display_name") or ""))
        save_name = st.form_submit_button("Guardar nombre", use_container_width=True)
    if save_name:
        if not display_name.strip():
            st.error("Escribe tu nombre.")
        else:
            update_profile_fields({"display_name": display_name.strip()})
            st.success("Nombre actualizado.")
            st.rerun()

    if LATEST_ASSESSMENT:
        st.markdown("### Perfil RCP vigente")
        a = LATEST_ASSESSMENT.get("answers") or {}
        score = int(LATEST_ASSESSMENT.get("runner_score") or 0)
        level = str(LATEST_ASSESSMENT.get("runner_level") or "—").title()
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Nivel", level)
        k2.metric("Score", f"{score}/100")
        k3.metric("Base", f"{float(a.get('weekly_km') or 0):g} km/sem")
        k4.metric("Larga", f"{float(a.get('long_run_km') or 0):g} km")

    st.divider()
    st.markdown("### Mantenimiento de registros")
    if ORPHAN_LOGS:
        st.warning(
            f"Hay {len(ORPHAN_LOGS)} registro(s) que no pertenecen al plan vigente. "
            "No se incluyen en KPI ni gráficos."
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
                if old_log.get("id") is not None:
                    delete_log_by_id(old_log.get("id"))
            st.success("Registros fuera del plan eliminados.")
            st.rerun()
    else:
        st.success("No hay registros huérfanos o fuera del plan activo.")

    st.divider()
    st.markdown("### Cuenta")
    st.write(f"Correo: **{USER_EMAIL}**")
    st.caption("Cada cuenta accede únicamente a sus propias filas mediante las políticas RLS.")


st.divider()
st.caption(
    "RunningCoachPro genera orientación general de entrenamiento. "
    "No sustituye evaluación médica ni coaching individual. Ante dolor agudo, "
    "mareos, lesión o síntomas anormales, suspende el ejercicio y busca orientación profesional."
)
