
import streamlit as st
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import math
import re
import html
import itertools
from supabase import create_client

st.set_page_config(
    page_title="RunningCoachPro",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# V7.1 · Plan Engine RCP + Motor Adaptativo + UI/UX responsive
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

    /* V7.1 · Readiness / Coach */
    .rcp-readiness {
        border: 1px solid var(--rcp-border);
        border-radius: 18px;
        padding: .9rem 1rem;
        margin: .25rem 0 .7rem 0;
        background: var(--rcp-surface);
    }
    .rcp-readiness-green { border-left: 5px solid #16a34a; }
    .rcp-readiness-yellow { border-left: 5px solid #ca8a04; }
    .rcp-readiness-orange { border-left: 5px solid #ea580c; }
    .rcp-readiness-red { border-left: 5px solid #dc2626; }
    .rcp-readiness-title {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: .65rem;
        flex-wrap: wrap;
        margin-bottom: .35rem;
    }
    .rcp-readiness-title strong {
        font-size: 1.05rem;
    }
    .rcp-readiness-score {
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--rcp-ink);
    }
    .rcp-readiness-facts {
        display: flex;
        flex-wrap: wrap;
        gap: .38rem;
        margin: .55rem 0 .35rem 0;
    }
    .rcp-ready-chip {
        display: inline-flex;
        align-items: center;
        padding: .28rem .52rem;
        border-radius: 999px;
        border: 1px solid var(--rcp-border);
        background: rgba(248,250,252,.88);
        font-size: .78rem;
        font-weight: 650;
        color: var(--rcp-ink);
    }
    .rcp-session-guidance {
        margin-top: .48rem;
        padding-top: .48rem;
        border-top: 1px solid var(--rcp-border);
        font-size: .9rem;
        color: var(--rcp-muted);
    }
    .rcp-coach-note {
        border: 1px solid var(--rcp-border);
        border-radius: 16px;
        padding: .78rem .9rem;
        background: rgba(248,250,252,.82);
        margin: .25rem 0 .75rem 0;
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

    /* V6.4.2 · Navigation Grid real sobre el bloque de columnas de Streamlit.
       El selector correcto en Streamlit actual es stColumn. */
    .st-key-rcp_nav_grid [data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: .62rem !important;
        align-items: stretch !important;
    }
    .st-key-rcp_nav_grid [data-testid="stColumn"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;
        flex: none !important;
    }
    .st-key-rcp_nav_grid .stButton > button {
        min-height: 76px !important;
        padding: .55rem .42rem !important;
        border-radius: 16px !important;
        font-size: .95rem !important;
        line-height: 1.15 !important;
        white-space: pre-line !important;
    }
    .st-key-rcp_nav_grid .stButton > button p {
        white-space: pre-line !important;
        line-height: 1.25 !important;
        margin: 0 !important;
    }
    .st-key-rcp_nav_grid {
        margin-bottom: .15rem !important;
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

        /* Métricas y bloques generales: dos columnas reales en móvil. */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: .48rem !important;
            align-items: stretch !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 0 0 calc(50% - .24rem) !important;
            width: calc(50% - .24rem) !important;
            max-width: calc(50% - .24rem) !important;
            min-width: 0 !important;
        }

        /* Navigation Grid: 2 × 4 en móvil, sin depender del breakpoint nativo. */
        .st-key-rcp_nav_grid [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            gap: .52rem !important;
        }
        .st-key-rcp_nav_grid [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            max-width: none !important;
            flex: none !important;
        }
        .st-key-rcp_nav_grid .stButton > button {
            min-height: 70px !important;
            padding: .42rem .28rem !important;
            font-size: .92rem !important;
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
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
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
APP_VERSION = "7.2.3"


# ============================================================
# V7.2.2 · FECHA LOCAL DEL USUARIO (NO FECHA DEL SERVIDOR)
# ============================================================
def rcp_timezone():
    """Zona horaria del navegador; fallback seguro a offset y finalmente UTC."""
    try:
        tz_name = getattr(st.context, "timezone", None)
        if tz_name:
            try:
                return ZoneInfo(str(tz_name)), str(tz_name)
            except Exception:
                pass
    except Exception:
        pass
    try:
        offset = getattr(st.context, "timezone_offset", None)
        if offset is not None:
            tz_obj = timezone(-timedelta(minutes=int(offset)))
            signed = -int(offset)
            sign = "+" if signed >= 0 else "-"
            mins = abs(signed)
            return tz_obj, f"UTC{sign}{mins // 60:02d}:{mins % 60:02d}"
    except Exception:
        pass
    return timezone.utc, "UTC"


def rcp_now():
    tz_obj, _ = rcp_timezone()
    return datetime.now(timezone.utc).astimezone(tz_obj)


def rcp_today():
    return rcp_now().date()


def rcp_timezone_name():
    _, name = rcp_timezone()
    return name


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


# ============================================================
# V7.1 · Persistencia del Motor Adaptativo
# ============================================================
def adaptive_storage_ready():
    """Comprueba la migración V7.1 sin modificar datos."""
    try:
        client.table("rc_daily_readiness").select("id,readiness_score,readiness_status").eq("user_id", USER_ID).limit(1).execute()
        client.table("rc_plan_adjustments").select("id,decision,status").eq("user_id", USER_ID).limit(1).execute()
        client.table("rc_plan_sessions").select(
            "id,baseline_planned_km,baseline_workout_type,baseline_workout_name,"
            "baseline_target,baseline_intensity,baseline_description,adaptation_status,adaptation_id"
        ).eq("user_id", USER_ID).limit(1).execute()
        client.table("rc_workout_logs").select(
            "id,post_pain,post_fatigue,perceived_difficulty,missed_reason"
        ).eq("user_id", USER_ID).limit(1).execute()
        return True
    except Exception:
        return False


def get_readiness_rows(plan_id=None, start_date=None, end_date=None, limit=180):
    if not plan_id:
        active = get_active_plan_record()
        plan_id = (active or {}).get("id")
    if not plan_id:
        return []
    q = (
        client.table("rc_daily_readiness")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("plan_id", int(plan_id))
    )
    if start_date is not None:
        q = q.gte("checkin_date", str(start_date))
    if end_date is not None:
        q = q.lte("checkin_date", str(end_date))
    return q.order("checkin_date", desc=True).limit(limit).execute().data or []


def get_readiness_for_date(day_value, plan_id=None):
    rows = get_readiness_rows(plan_id=plan_id, start_date=day_value, end_date=day_value, limit=1)
    return rows[0] if rows else None


def save_readiness(payload, plan_id=None):
    active = get_active_plan_record()
    pid = plan_id or (active or {}).get("id")
    if not pid:
        raise RuntimeError("No existe un plan activo para asociar el check-in.")
    row = dict(payload)
    row["user_id"] = USER_ID
    row["plan_id"] = int(pid)
    row["updated_at"] = datetime.now(timezone.utc).isoformat()
    return client.table("rc_daily_readiness").upsert(
        row, on_conflict="user_id,plan_id,checkin_date"
    ).execute()


def get_adjustments(plan_id=None, limit=50):
    if not plan_id:
        active = get_active_plan_record()
        plan_id = (active or {}).get("id")
    if not plan_id:
        return []
    return (
        client.table("rc_plan_adjustments")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("plan_id", int(plan_id))
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
        or []
    )


def create_adjustment_record(payload):
    row = dict(payload)
    row["user_id"] = USER_ID
    result = client.table("rc_plan_adjustments").insert(row).execute().data or []
    return result[0] if result else None


def update_adjustment_record(adjustment_id, **fields):
    if not adjustment_id:
        return
    client.table("rc_plan_adjustments").update(fields).eq("user_id", USER_ID).eq("id", int(adjustment_id)).execute()


def update_plan_session_fields(session_id, **fields):
    if not session_id:
        return
    client.table("rc_plan_sessions").update(fields).eq("user_id", USER_ID).eq("id", int(session_id)).execute()


# ============================================================
# V7.2 · Persistencia de replanificación
# ============================================================
def replanning_storage_ready():
    """Comprueba la migración V7.2 sin modificar datos."""
    try:
        client.table("rc_plan_replans").select("id,decision,status").eq("user_id", USER_ID).limit(1).execute()
        client.table("rc_plan_sessions").select(
            "id,baseline_session_date,replan_status,replan_id,replanned_at"
        ).eq("user_id", USER_ID).limit(1).execute()
        return True
    except Exception:
        return False


def get_replans(plan_id=None, limit=80):
    if not plan_id:
        active = get_active_plan_record()
        plan_id = (active or {}).get("id")
    if not plan_id:
        return []
    return (
        client.table("rc_plan_replans")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("plan_id", int(plan_id))
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data
        or []
    )


def create_replan_record(payload):
    row = dict(payload)
    row["user_id"] = USER_ID
    result = client.table("rc_plan_replans").insert(row).execute().data or []
    return result[0] if result else None


def update_replan_record(replan_id, **fields):
    if not replan_id:
        return
    client.table("rc_plan_replans").update(fields).eq("user_id", USER_ID).eq("id", int(replan_id)).execute()


def get_plan_session_by_id(session_id):
    if not session_id:
        return None
    rows = (
        client.table("rc_plan_sessions")
        .select("*")
        .eq("user_id", USER_ID)
        .eq("id", int(session_id))
        .limit(1)
        .execute()
        .data
        or []
    )
    return rows[0] if rows else None


def delete_plan_session_by_id(session_id):
    if not session_id:
        return
    client.table("rc_plan_sessions").delete().eq("user_id", USER_ID).eq("id", int(session_id)).execute()


def insert_replan_session(plan_id, row):
    payload = dict(row)
    payload["user_id"] = USER_ID
    payload["plan_id"] = int(plan_id)
    result = client.table("rc_plan_sessions").insert(payload).execute().data or []
    return result[0] if result else None


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

    days_left = (race_day - rcp_today()).days
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
            age_days = max(0, (rcp_today() - date.fromisoformat(str(mark_date_text))).days)
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
            weeks_to_goal = round(max(0, (date.fromisoformat(str(goal_date)) - rcp_today()).days) / 7, 1)
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

    start = next_monday(rcp_today())
    total_weeks = week_count(start, race_date, has_race)

    # Si la carrera está muy cerca, empezar mañana evita crear sesiones en el pasado.
    if has_race and race_date and (race_date - start).days < 35:
        start = rcp_today() + timedelta(days=1)
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


# ============================================================
# V7.0 · PLAN ENGINE RCP
# ============================================================
# Motor heurístico de entrenamiento basado en Evaluación RCP, objetivo,
# disponibilidad, carga reciente y rendimiento. No es una escala clínica
# validada ni sustituye valoración médica/coaching individual.

DAY_INDEX = {name: idx for idx, name in enumerate(DAY_NAMES)}


def _clamp(value, low, high):
    return max(low, min(high, value))


def _day_gap(a, b):
    """Distancia circular mínima entre dos días de la semana (0..6)."""
    d = abs(int(a) - int(b))
    return min(d, 7 - d)


def _available_day_indices(answers):
    raw = answers.get("available_days") or []
    indices = sorted({DAY_INDEX[x] for x in raw if x in DAY_INDEX})
    return indices


def _choose_running_days(answers, level):
    """Selecciona días reales de entrenamiento sin asumir plantillas fijas."""
    available = _available_day_indices(answers)
    if len(available) < 2:
        return [], None

    current_days = int(answers.get("current_days") or 0)
    level = str(level or "INICIACIÓN").upper()
    level_ceiling = {
        "INICIACIÓN": 3,
        "PRINCIPIANTE": 4,
        "INTERMEDIO": 5,
        "AVANZADO": 6,
    }.get(level, 4)
    floor = 2 if level in ("INICIACIÓN", "PRINCIPIANTE") else 3
    desired = current_days if current_days >= floor else floor
    if current_days > 0:
        desired = min(desired + 1, level_ceiling)
    desired = int(_clamp(desired, 2, min(level_ceiling, len(available))))

    preferred_name = answers.get("preferred_long_day")
    long_day = DAY_INDEX.get(preferred_name) if preferred_name in DAY_INDEX else None
    if long_day not in available:
        weekend = [d for d in (6, 5) if d in available]
        long_day = weekend[0] if weekend else available[-1]

    if len(available) <= desired:
        return available, long_day

    # Selección por separación: siempre conserva el día de larga y agrega
    # iterativamente el día que maximiza distancia respecto de los elegidos.
    selected = [long_day]
    pool = [d for d in available if d != long_day]
    while len(selected) < desired and pool:
        best = max(pool, key=lambda d: (min(_day_gap(d, x) for x in selected), -d))
        selected.append(best)
        pool.remove(best)
    return sorted(selected), long_day


def _quality_days(selected_days, long_day, answers, max_quality):
    no_intensity = {DAY_INDEX[x] for x in (answers.get("no_intensity_days") or []) if x in DAY_INDEX}
    candidates = [d for d in selected_days if d != long_day and d not in no_intensity]
    chosen = []
    for _ in range(max_quality):
        if not candidates:
            break
        if not chosen:
            # Prioriza un día con al menos 2 días de separación respecto a la larga.
            day = max(candidates, key=lambda d: (_day_gap(d, long_day), -d))
        else:
            day = max(
                candidates,
                key=lambda d: (min([_day_gap(d, long_day)] + [_day_gap(d, x) for x in chosen]), -d),
            )
        if _day_gap(day, long_day) < 2 and len(selected_days) >= 4:
            candidates.remove(day)
            continue
        chosen.append(day)
        candidates.remove(day)
    return sorted(chosen)


def _pace_range(fast_sec, slow_sec):
    if not fast_sec or not slow_sec:
        return None
    return f"{pace_string(fast_sec).replace(' min/km','')}–{pace_string(slow_sec)}"


def v7_pace_profile(assessment, goal_row):
    """Ritmos orientativos. Si no hay marca reciente fiable, usa solo RPE/talk test."""
    answers = dict((assessment or {}).get("answers") or {})
    perf = performance_summary(answers)
    out = {
        "basis": "RPE / talk test",
        "usable": False,
        "source": perf,
        "recovery": None,
        "easy": None,
        "long": None,
        "steady": None,
        "threshold": None,
        "interval": None,
        "race": None,
    }
    if not perf.get("usable"):
        return out
    if str(perf.get("terrain") or "").lower() == "trail":
        out["basis"] = "RPE / talk test (marca trail no usada para ritmos de ruta)"
        return out

    equivalents = perf.get("equivalents_sec") or {}
    p5 = (float(equivalents.get("5K")) / 5.0) if equivalents.get("5K") else None
    p10 = (float(equivalents.get("10K")) / 10.0) if equivalents.get("10K") else None
    if not p10:
        source_km = float(perf.get("source_distance_km") or 0)
        source_sec = float(perf.get("source_time_sec") or 0)
        p10 = source_sec / source_km if source_km > 0 else None
    if not p10:
        return out
    if not p5:
        p5 = max(1.0, p10 - 18)

    out.update({
        "basis": "marca reciente + RPE",
        "usable": True,
        "recovery": [round(p10 + 75), round(p10 + 110)],
        "easy": [round(p10 + 55), round(p10 + 90)],
        "long": [round(p10 + 50), round(p10 + 85)],
        "steady": [round(p10 + 30), round(p10 + 50)],
        "threshold": [round(p10 + 10), round(p10 + 25)],
        "interval": [round(max(1, p5 - 5)), round(p5 + 10)],
    })

    goal_km = GOAL_KM.get(str(goal_row.get("goal_type") or ""))
    target_seconds = goal_row.get("target_time_sec")
    source_seconds = perf.get("source_time_sec")
    source_km = perf.get("source_distance_km")
    estimated = estimate_equivalent_time(source_seconds, source_km, goal_km) if goal_km else None
    if goal_km:
        race_sec = None
        # Una meta >5% por delante de la equivalencia actual no se usa como ritmo de
        # prescripción; V7 entrena desde la capacidad actual y conserva la meta como objetivo.
        gap = None
        if estimated and target_seconds:
            gap = (float(estimated) - float(target_seconds)) / float(estimated) * 100
        if target_seconds and (gap is None or gap <= 5):
            race_sec = float(target_seconds) / float(goal_km)
        elif estimated:
            race_sec = float(estimated) / float(goal_km)
        elif target_seconds:
            race_sec = float(target_seconds) / float(goal_km)
        if race_sec:
            out["race"] = round(race_sec)
    return out


def _target_with_pace(label, zone, rpe):
    if zone and isinstance(zone, (list, tuple)) and len(zone) == 2:
        return f"{_pace_range(zone[0], zone[1])} · RPE {rpe}"
    if zone and isinstance(zone, (int, float)):
        return f"{pace_string(zone)} · RPE {rpe}"
    return f"RPE {rpe}"


def _v7_phase_schedule(goal, total_weeks, base_status, level, experience):
    """Devuelve una fase por semana: BASE, DESARROLLO, ESPECÍFICA, TAPER, CARRERA."""
    goal = str(goal or "Condición física")
    race_goal = goal in ("5K", "10K", "21K", "42K")
    if total_weeks <= 0:
        return []

    if not race_goal:
        base_weeks = min(3, max(1, total_weeks // 3))
        return ["BASE" if i < base_weeks else "DESARROLLO" for i in range(total_weeks)]

    taper_weeks = {"5K": 1, "10K": 1, "21K": 2, "42K": 3}.get(goal, 1)
    taper_weeks = min(taper_weeks, max(1, total_weeks - 2))

    short_history = experience in ("Nunca", "<1 mes", "1–3 meses", "3–6 meses")
    base_weeks = 0
    if base_status == "BASE PREVIA":
        base_weeks = min(3, max(1, total_weeks - taper_weeks - 3))
    elif short_history or str(level).upper() in ("INICIACIÓN", "PRINCIPIANTE"):
        base_weeks = 1 if total_weeks >= 6 else 0

    remaining = max(1, total_weeks - base_weeks - taper_weeks)
    specific_weeks = max(1, round(remaining * (0.45 if goal in ("21K", "42K") else 0.40)))
    build_weeks = max(0, remaining - specific_weeks)

    phases = ["BASE"] * base_weeks + ["DESARROLLO"] * build_weeks + ["ESPECÍFICA"] * specific_weeks + ["TAPER"] * taper_weeks
    return phases[:total_weeks]


def _v7_initial_volume(answers, level, base_status, goal):
    current = float(answers.get("weekly_km") or 0)
    continuous = int(answers.get("continuous_min") or 0)
    level = str(level or "INICIACIÓN").upper()

    if current <= 0:
        current = 6.0 if continuous < 20 else 10.0
    factor = 1.0
    if str(goal) == "Volver a correr tras una pausa":
        factor = 0.70
    elif base_status == "BASE PREVIA":
        factor = 0.88
    elif level == "INICIACIÓN":
        factor = 0.80
    elif level == "PRINCIPIANTE":
        factor = 0.92
    return max(5.0, current * factor)


def _v7_weekly_volumes(initial_km, total_weeks, phases, progression_mode, goal):
    if total_weeks <= 0:
        return []
    mode = str(progression_mode or "ESTÁNDAR").upper()
    growth = {"RESTRINGIDA": 0.00, "CONSERVADORA": 0.035, "ESTÁNDAR": 0.05}.get(mode, 0.04)
    peak_cap = {"RESTRINGIDA": 1.05, "CONSERVADORA": 1.20, "ESTÁNDAR": 1.28}.get(mode, 1.20)
    if str(goal) == "42K":
        peak_cap += 0.05

    values = []
    prev = float(initial_km)
    peak = prev
    taper_indices = [i for i, p in enumerate(phases) if p == "TAPER"]
    first_taper = taper_indices[0] if taper_indices else total_weeks

    for i, phase in enumerate(phases):
        if phase == "TAPER":
            taper_pos = taper_indices.index(i)
            taper_count = len(taper_indices)
            factors = {1: [0.58], 2: [0.76, 0.56], 3: [0.84, 0.70, 0.52]}.get(taper_count, [0.60] * taper_count)
            target = peak * factors[min(taper_pos, len(factors) - 1)]
        else:
            if i == 0:
                target = prev
            else:
                target = prev * (1.0 + growth)
                # Descarga cada 4 semanas de carga, pero no durante la fase específica final.
                if (i + 1) % 4 == 0 and phase != "ESPECÍFICA":
                    target = prev * 0.88
            target = min(target, initial_km * peak_cap)
            if phase == "ESPECÍFICA" and i >= max(0, first_taper - 2):
                target = min(target, peak)
            peak = max(peak, target)
        target = max(5.0, float(target))
        values.append(round(target, 1))
        prev = target
    return values


def _v7_long_cap(goal):
    return {
        "5K": 12.0,
        "10K": 18.0,
        "21K": 24.0,
        "42K": 32.0,
        "Condición física": 16.0,
        "Mantener rendimiento": 20.0,
        "Volver a correr tras una pausa": 14.0,
        "Empezar a correr": 8.0,
        "Correr 30 min continuos": 8.0,
    }.get(str(goal), 18.0)


def _v7_long_distance(weekly_km, answers, goal, phase, week_idx, total_weeks, days_count):
    current_long = float(answers.get("long_run_km") or 0)
    cap = _v7_long_cap(goal)
    frac = 0.32 if days_count <= 3 else 0.28
    upper_frac = 0.42 if days_count <= 3 else 0.38
    baseline_long = max(4.0, weekly_km * frac)
    if current_long > 0:
        preserve = current_long * (0.82 if week_idx == 0 else 0.88)
        baseline_long = max(baseline_long, preserve)
    long_km = min(cap, baseline_long, weekly_km * upper_frac)

    if phase == "TAPER":
        taper_weeks_left = max(1, total_weeks - week_idx)
        factor = 0.65 if taper_weeks_left >= 2 else 0.48
        long_km = min(long_km, max(4.0, current_long * factor if current_long else weekly_km * 0.24))
    if str(goal) in ("Empezar a correr", "Correr 30 min continuos"):
        long_km = min(long_km, 6.0)
    return round(max(3.0, long_km), 1)


def _v7_quality_count(level, days_count, phase, answers):
    level = str(level or "INICIACIÓN").upper()
    experience = str(answers.get("experience") or "Nunca")
    prior_quality = len(set(answers.get("quality_types") or []))
    if phase == "BASE" or level == "INICIACIÓN" or days_count <= 2:
        return 0
    if phase == "TAPER":
        return 1 if days_count >= 3 else 0
    if level == "PRINCIPIANTE" or experience in ("<1 mes", "1–3 meses", "3–6 meses"):
        return 1 if days_count >= 3 else 0
    if days_count >= 4 and prior_quality >= 2 and phase in ("DESARROLLO", "ESPECÍFICA"):
        return 2
    return 1


def _run_walk_recipe(week_no):
    recipes = [
        (1, 2, 8),
        (2, 2, 7),
        (3, 2, 6),
        (4, 2, 5),
        (5, 1, 5),
        (8, 1, 4),
        (10, 1, 3),
        (15, 1, 2),
    ]
    run_min, walk_min, reps = recipes[min(max(0, week_no - 1), len(recipes) - 1)]
    return run_min, walk_min, reps


def _v7_quality_session(goal, phase, week_no, slot, pace_profile, level):
    goal = str(goal)
    slot = int(slot)
    if phase == "TAPER":
        return {
            "type": "ACTIVACION",
            "name": "Activación corta",
            "target": _target_with_pace("", pace_profile.get("interval"), "6–7/10"),
            "intensity": "CONTROLADA",
            "description": "15 min suave + 4–6 × 60–90 s alegres con recuperación completa + 10 min suave. Debes terminar con sensación de reserva.",
        }

    if goal == "5K":
        if (week_no + slot) % 2 == 0:
            return {
                "type": "SERIES",
                "name": "Intervalos cortos",
                "target": _target_with_pace("", pace_profile.get("interval"), "7–8/10"),
                "intensity": "ALTA CONTROLADA",
                "description": "15 min suave + movilidad + 8 × 400 m controlados, 75–90 s de trote/pausa + 10 min suave. Evita convertirlo en sprint.",
            }
        return {
            "type": "UMBRAL",
            "name": "Umbral fraccionado",
            "target": _target_with_pace("", pace_profile.get("threshold"), "6–7/10"),
            "intensity": "UMBRAL",
            "description": "15 min suave + 3 × 8 min a esfuerzo de umbral con 2 min suaves + 10 min suave.",
        }

    if goal == "10K":
        if slot == 0:
            return {
                "type": "UMBRAL",
                "name": "Umbral sostenido",
                "target": _target_with_pace("", pace_profile.get("threshold"), "6–7/10"),
                "intensity": "UMBRAL",
                "description": "15 min suave + 20–30 min totales de trabajo a umbral (continuo o 2–3 bloques) + 10 min suave.",
            }
        return {
            "type": "SERIES",
            "name": "Intervalos largos",
            "target": _target_with_pace("", pace_profile.get("interval"), "7–8/10"),
            "intensity": "ALTA CONTROLADA",
            "description": "15 min suave + 5–6 × 800 m o 4–5 × 1 km controlados, 90–120 s suaves + 10 min suave.",
        }

    if goal == "21K":
        if slot == 0:
            return {
                "type": "UMBRAL",
                "name": "Umbral controlado",
                "target": _target_with_pace("", pace_profile.get("threshold"), "6–7/10"),
                "intensity": "UMBRAL",
                "description": "15 min suave + 2–3 bloques de 10–12 min a umbral con 2–3 min suaves + 10 min suave.",
            }
        race_pace = pace_profile.get("race")
        return {
            "type": "RITMO_CARRERA",
            "name": "Bloques a ritmo MM",
            "target": _target_with_pace("", race_pace, "5–6/10"),
            "intensity": "ESPECÍFICA",
            "description": "15 min suave + 3–5 bloques de 1–2 km al esfuerzo específico de media maratón, 2–3 min suaves entre bloques + enfriamiento.",
        }

    if goal == "42K":
        if slot == 0:
            return {
                "type": "UMBRAL",
                "name": "Umbral aeróbico",
                "target": _target_with_pace("", pace_profile.get("threshold"), "6–7/10"),
                "intensity": "UMBRAL",
                "description": "15 min suave + 2–3 × 10 min controlados a umbral con 3 min suaves + 10 min suave.",
            }
        return {
            "type": "RITMO_CARRERA",
            "name": "Ritmo maratón controlado",
            "target": _target_with_pace("", pace_profile.get("race"), "5–6/10"),
            "intensity": "ESPECÍFICA",
            "description": "Rodaje con bloques a esfuerzo de maratón. Mantén control respiratorio; no conviertas la sesión en un tempo máximo.",
        }

    # Objetivos generales / mantenimiento.
    return {
        "type": "FARTLEK",
        "name": "Fartlek controlado",
        "target": "RPE 6–7/10 en los tramos rápidos",
        "intensity": "MODERADA",
        "description": "15 min suave + 8–10 × 1 min ágil / 1–2 min suave + 10 min suave. Debes conservar técnica y control.",
    }


def _v7_allocate_distances(weekly_km, days, long_day, quality_days, long_km, phase, goal):
    roles = {}
    for d in days:
        if d == long_day:
            roles[d] = "LONG"
        elif d in quality_days:
            roles[d] = "QUALITY"
        else:
            roles[d] = "EASY"

    distances = {long_day: long_km}
    remaining = max(0.0, weekly_km - long_km)
    quality_share = 0.0
    if quality_days:
        quality_share = min(remaining * 0.48, weekly_km * (0.22 * len(quality_days)))
    per_quality = quality_share / len(quality_days) if quality_days else 0
    for d in quality_days:
        distances[d] = round(max(4.0, per_quality), 1)

    easy_days = [d for d in days if d != long_day and d not in quality_days]
    used = sum(distances.values())
    easy_remaining = max(0.0, weekly_km - used)
    per_easy = easy_remaining / len(easy_days) if easy_days else 0
    for d in easy_days:
        distances[d] = round(max(3.0, per_easy), 1)

    # Ajuste final para aproximar el total semanal sin tocar la larga.
    total = sum(distances.values())
    delta = round(weekly_km - total, 1)
    adjust_candidates = easy_days or quality_days
    if adjust_candidates and abs(delta) >= 0.1:
        d = adjust_candidates[0]
        distances[d] = round(max(2.5, distances[d] + delta), 1)
    return roles, distances


def can_generate_v7_plan(goal_row, assessment):
    if not assessment_is_complete(assessment):
        return False, "Falta una Evaluación RCP completa."
    if str(assessment.get("safety_status") or "") != "SIN ALERTAS DECLARADAS":
        return False, "El cribado de seguridad no permite generar automáticamente un plan de entrenamiento."

    answers = assessment.get("answers") or {}
    available = _available_day_indices(answers)
    if len(available) < 2:
        return False, "Se requieren al menos 2 días disponibles para generar un plan RCP V7."

    goal_type = str(goal_row.get("goal_type") or "")
    if goal_type not in RCP_GOALS:
        return False, "Objetivo no reconocido por el motor RCP V7."

    snapshot = goal_row.get("readiness_snapshot") or goal_analysis_snapshot(
        goal_type,
        goal_row.get("goal_style") or "Terminar",
        goal_row.get("race_date"),
        goal_row.get("target_time_sec"),
        assessment,
    )
    base_status = str(snapshot.get("base_status") or "")
    calendar_status = str(snapshot.get("calendar_status") or "")

    if goal_type in ("5K", "10K", "21K", "42K"):
        if base_status == "INSUFICIENTE":
            return False, "La base actual es insuficiente para un plan específico de esa distancia. Conviene crear primero un objetivo de base/retorno y reevaluar."
        if calendar_status in ("INSUFICIENTE", "FECHA INVÁLIDA", "EVALUAR SEGURIDAD"):
            return False, "El calendario disponible no permite generar de forma responsable este plan específico."
        if not goal_row.get("race_date"):
            return False, "Para un objetivo de carrera específico V7 necesita una fecha objetivo."
    return True, None


def build_v7_plan(goal_row, assessment, start_date_value=None):
    """Genera filas de rc_plan_sessions + metadata de plan. Función pura salvo USER_ID/rcp_today()."""
    can_generate, reason = can_generate_v7_plan(goal_row, assessment)
    if not can_generate:
        return [], {}, reason

    answers = dict((assessment or {}).get("answers") or {})
    level = str((assessment or {}).get("runner_level") or "INICIACIÓN").upper()
    runner_profile = ((assessment or {}).get("explanation") or {}).get("runner_profile") or {}
    tolerance = runner_profile.get("tolerance") or {}
    progression_mode = str(tolerance.get("progression_mode") or "CONSERVADORA")
    goal = str(goal_row.get("goal_type") or "Condición física")
    if progression_mode == "ESTÁNDAR" and (
        level == "INICIACIÓN"
        or goal in ("Empezar a correr", "Correr 30 min continuos", "Volver a correr tras una pausa")
        or str((goal_row.get("readiness_snapshot") or {}).get("base_status") or "") == "BASE PREVIA"
    ):
        progression_mode = "CONSERVADORA"
    race_date = date.fromisoformat(str(goal_row["race_date"])) if goal_row.get("race_date") else None
    start_date_value = start_date_value or (rcp_today() + timedelta(days=1))

    selected_days, long_day = _choose_running_days(answers, level)
    if len(selected_days) < 2:
        return [], {}, "No fue posible construir una distribución semanal con los días disponibles."

    if race_date:
        total_days = (race_date - start_date_value).days + 1
        total_weeks = max(1, math.ceil(total_days / 7))
    else:
        total_weeks = {
            "Empezar a correr": 8,
            "Correr 30 min continuos": 8,
            "Condición física": 10,
            "Mantener rendimiento": 8,
            "Volver a correr tras una pausa": 8,
        }.get(goal, 10)

    snapshot = goal_row.get("readiness_snapshot") or goal_analysis_snapshot(
        goal,
        goal_row.get("goal_style") or "Terminar",
        goal_row.get("race_date"),
        goal_row.get("target_time_sec"),
        assessment,
    )
    base_status = str(snapshot.get("base_status") or "ADECUADA")
    experience = str(answers.get("experience") or "Nunca")
    phases = _v7_phase_schedule(goal, total_weeks, base_status, level, experience)
    initial_km = _v7_initial_volume(answers, level, base_status, goal)
    weekly_volumes = _v7_weekly_volumes(initial_km, total_weeks, phases, progression_mode, goal)
    pace_profile = v7_pace_profile(assessment, goal_row)

    monday0 = start_date_value - timedelta(days=start_date_value.weekday())
    rows = []
    week_meta = []
    continuous_min = int(answers.get("continuous_min") or 0)
    run_walk_mode = level == "INICIACIÓN" or continuous_min < 20 or goal in ("Empezar a correr", "Correr 30 min continuos")

    for w in range(total_weeks):
        week_no = w + 1
        monday = monday0 + timedelta(days=7 * w)
        phase = phases[w] if w < len(phases) else "DESARROLLO"
        weekly_km = weekly_volumes[w]
        q_count = _v7_quality_count(level, len(selected_days), phase, answers)
        quality_days = _quality_days(selected_days, long_day, answers, q_count)
        long_km = _v7_long_distance(weekly_km, answers, goal, phase, w, total_weeks, len(selected_days))
        roles, distances = _v7_allocate_distances(weekly_km, selected_days, long_day, quality_days, long_km, phase, goal)

        week_meta.append({
            "week": week_no,
            "phase": phase,
            "target_km": weekly_km,
            "long_km": long_km,
            "quality_sessions": len(quality_days),
        })

        quality_slot = 0
        for weekday in selected_days:
            d = monday + timedelta(days=weekday)
            if d < start_date_value:
                continue
            if race_date and d > race_date:
                continue
            if race_date and d == race_date and goal in GOAL_KM and GOAL_KM.get(goal):
                continue

            distance_km = float(distances.get(weekday) or 0)
            role = roles.get(weekday, "EASY")

            _rw_this_week = run_walk_mode and (
                phase == "BASE"
                or goal in ("Empezar a correr", "Correr 30 min continuos")
            )
            if _rw_this_week:
                run_min, walk_min, reps = _run_walk_recipe(week_no)
                if role == "LONG":
                    reps += 1
                description = (
                    f"5–8 min caminando + {reps} × ({run_min} min trote muy suave / {walk_min} min caminata) "
                    "+ 5 min caminando. El objetivo es acumular tiempo cómodo, no velocidad. "
                    "Si aparece dolor que cambie la zancada, detén la sesión."
                )
                rows.append({
                    "user_id": USER_ID,
                    "session_date": d.isoformat(),
                    "week_no": week_no,
                    "workout_type": "RUN_WALK_LONG" if role == "LONG" else "RUN_WALK",
                    "workout_name": f"Run–Walk {'largo ' if role == 'LONG' else ''}{run_min}:{walk_min}",
                    "planned_km": round(max(2.5, distance_km), 1),
                    "target": "RPE 2–3/10 · respiración controlada",
                    "intensity": "ADAPTACIÓN",
                    "description": description,
                    "is_optional": False,
                })
                continue

            if role == "LONG":
                long_target = _target_with_pace("", pace_profile.get("long"), "3–4/10")
                desc = "Empieza muy suave y mantén conversación completa. En subidas manda el esfuerzo, no el ritmo."
                if phase == "ESPECÍFICA" and goal in ("21K", "42K") and pace_profile.get("race") and level in ("INTERMEDIO", "AVANZADO"):
                    desc += " En el tercio final, si estás recuperado, añade 15–25 min al esfuerzo específico de carrera; no es obligatorio si la fatiga es alta."
                rows.append({
                    "user_id": USER_ID,
                    "session_date": d.isoformat(),
                    "week_no": week_no,
                    "workout_type": "LARGA",
                    "workout_name": f"Tirada larga {distance_km:g} km",
                    "planned_km": round(distance_km, 1),
                    "target": long_target,
                    "intensity": "BASE" if phase != "ESPECÍFICA" else "ESPECÍFICA CONTROLADA",
                    "description": desc,
                    "is_optional": False,
                })
                continue

            if role == "QUALITY":
                q = _v7_quality_session(goal, phase, week_no, quality_slot, pace_profile, level)
                quality_slot += 1
                rows.append({
                    "user_id": USER_ID,
                    "session_date": d.isoformat(),
                    "week_no": week_no,
                    "workout_type": q["type"],
                    "workout_name": q["name"],
                    "planned_km": round(max(4.0, distance_km), 1),
                    "target": q["target"],
                    "intensity": q["intensity"],
                    "description": q["description"],
                    "is_optional": False,
                })
                continue

            # Rodaje fácil / recuperación.
            is_recovery = len(selected_days) >= 5 and any(_day_gap(weekday, qd) == 1 for qd in quality_days)
            zone = pace_profile.get("recovery" if is_recovery else "easy")
            target = _target_with_pace("", zone, "2–3/10" if is_recovery else "3–4/10")
            desc = "Muy suave; debe dejarte mejor de lo que empezaste." if is_recovery else "Ritmo conversacional. Mantén técnica relajada y reserva clara al terminar."
            # Dos recordatorios de fuerza/semana sin crear una segunda sesión en la misma fecha.
            easy_rank = [x for x in selected_days if roles.get(x) == "EASY"].index(weekday) if weekday in [x for x in selected_days if roles.get(x) == "EASY"] else -1
            if easy_rank in (0, 1) and phase != "TAPER":
                desc += " Fuerza RCP sugerida después o en otro momento del día: 15–25 min (sentadilla/split squat, bisagra, gemelos/sóleo y core), con técnica controlada."
            rows.append({
                "user_id": USER_ID,
                "session_date": d.isoformat(),
                "week_no": week_no,
                "workout_type": "RECUPERACION" if is_recovery else "RODAJE",
                "workout_name": f"{'Recuperación' if is_recovery else 'Rodaje suave'} {distance_km:g} km",
                "planned_km": round(max(2.5, distance_km), 1),
                "target": target,
                "intensity": "RECUPERACIÓN" if is_recovery else "BASE",
                "description": desc,
                "is_optional": False,
            })

    # Carrera objetivo: se agrega siempre aunque no coincida con un día habitual.
    if race_date and goal in GOAL_KM and GOAL_KM.get(goal):
        race_distance = float(GOAL_KM[goal])
        race_pace = pace_profile.get("race")
        rows = [r for r in rows if r["session_date"] != race_date.isoformat()]
        rows.append({
            "user_id": USER_ID,
            "session_date": race_date.isoformat(),
            "week_no": total_weeks,
            "workout_type": "CARRERA",
            "workout_name": f"{goal} objetivo",
            "planned_km": race_distance,
            "target": _target_with_pace("", race_pace, "según estrategia") if race_pace else "Ritmo/Esfuerzo de carrera controlado",
            "intensity": "COMPETENCIA",
            "description": "Calentamiento habitual. Salida controlada, estabiliza el esfuerzo y reserva capacidad para el tramo final. No persigas una meta de ritmo si las condiciones o sensaciones no la sostienen.",
            "is_optional": False,
        })

    rows.sort(key=lambda x: x["session_date"])
    if not rows:
        return [], {}, "El motor V7 no produjo sesiones en el intervalo disponible."

    metadata = {
        "engine": "RCP-V7.2.2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "assessment_id": assessment.get("id"),
        "assessment_version": assessment.get("assessment_version"),
        "runner_level": level,
        "runner_score": int(assessment.get("runner_score") or 0),
        "progression_mode": progression_mode,
        "goal_type": goal,
        "goal_style": goal_row.get("goal_style"),
        "selected_days": [DAY_NAMES[d] for d in selected_days],
        "long_day": DAY_NAMES[long_day] if long_day is not None else None,
        "initial_weekly_km": round(initial_km, 1),
        "peak_weekly_km": round(max(weekly_volumes) if weekly_volumes else initial_km, 1),
        "pace_basis": pace_profile.get("basis"),
        "pace_profile": {k: v for k, v in pace_profile.items() if k != "source"},
        "weeks": week_meta,
        "methodology": {
            "load": "Progresión RCP individualizada por historial, nivel, base y modo de progresión; incluye descargas y límites de pico.",
            "intensity": "RPE/talk test siempre; ritmos solo cuando existe una marca reciente utilizable.",
            "taper": "Reducción progresiva de volumen manteniendo estímulos breves de intensidad antes de carrera.",
            "strength": "Fuerza complementaria sugerida 1–2 veces/semana según fase y tolerancia.",
        },
    }
    return rows, metadata, None


def replace_active_plan_with_v7(goal_row, profile, assessment, start_date_value=None):
    """Crea primero un plan FUTURE V7; solo después archiva el activo y promueve V7 a ACTIVE."""
    rows, metadata, reason = build_v7_plan(goal_row, assessment, start_date_value=start_date_value)
    if reason:
        return None, reason

    plan_payload = {
        "user_id": USER_ID,
        "goal_id": int(goal_row["id"]),
        "status": "FUTURE",
        "engine_version": "RCP-V7.2.2",
        "start_date": rows[0]["session_date"],
        "end_date": rows[-1]["session_date"],
        "initial_weekly_km": float(metadata.get("initial_weekly_km") or 0),
        "days_per_week": len(metadata.get("selected_days") or []),
        "metadata": metadata,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    created = client.table("rc_plans").insert(plan_payload).execute().data or []
    if not created:
        return None, "No fue posible crear el ciclo V7."
    new_plan = created[0]
    try:
        insert_plan_sessions(new_plan["id"], rows)
    except Exception as exc:
        client.table("rc_plans").delete().eq("user_id", USER_ID).eq("id", int(new_plan["id"])).execute()
        return None, f"No fue posible guardar las sesiones V7: {exc}"

    old_plan = get_active_plan_record()
    if old_plan and int(old_plan["id"]) != int(new_plan["id"]):
        update_plan_record(old_plan["id"], status="ARCHIVED")
    update_plan_record(new_plan["id"], status="ACTIVE")
    new_plan["status"] = "ACTIVE"

    # Compatibilidad de perfil sin convertirlo otra vez en fuente de verdad.
    update_profile_fields({
        "goal": goal_row.get("goal_type") if goal_row.get("goal_type") in GOAL_KM else "Condición física",
        "days_per_week": len(metadata.get("selected_days") or []),
        "weekly_km": float(metadata.get("initial_weekly_km") or 0),
        "has_race": bool(goal_row.get("race_date")),
        "race_date": goal_row.get("race_date"),
        "target_time_sec": goal_row.get("target_time_sec"),
    })
    return new_plan, None



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
    """V7.0: crea un ciclo RCP desde la Evaluación; nunca borra planes anteriores."""
    can_generate, reason = can_generate_v7_plan(goal_row, assessment)
    if not can_generate:
        return None, reason

    rows, metadata, reason = build_v7_plan(goal_row, assessment)
    if reason or not rows:
        return None, reason or "El Plan Engine V7 no produjo sesiones."

    plan_payload = {
        "user_id": USER_ID,
        "goal_id": int(goal_row["id"]),
        "status": status,
        "engine_version": "RCP-V7.2.2",
        "start_date": rows[0]["session_date"],
        "end_date": rows[-1]["session_date"],
        "initial_weekly_km": float(metadata.get("initial_weekly_km") or 0),
        "days_per_week": len(metadata.get("selected_days") or []),
        "metadata": metadata,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    result = client.table("rc_plans").insert(plan_payload).execute().data or []
    if not result:
        return None, "No fue posible crear el registro del plan V7."

    plan_row = result[0]
    try:
        insert_plan_sessions(plan_row["id"], rows)
    except Exception as exc:
        client.table("rc_plans").delete().eq("user_id", USER_ID).eq("id", int(plan_row["id"])).execute()
        return None, f"No fue posible guardar las sesiones V7: {exc}"

    if status == "ACTIVE":
        update_profile_fields({
            "goal": goal_row.get("goal_type") if goal_row.get("goal_type") in GOAL_KM else "Condición física",
            "days_per_week": len(metadata.get("selected_days") or []),
            "weekly_km": float(metadata.get("initial_weekly_km") or 0),
            "has_race": bool(goal_row.get("race_date")),
            "race_date": goal_row.get("race_date"),
            "target_time_sec": goal_row.get("target_time_sec"),
        })
    return plan_row, None


def activate_existing_goal(goal_row, profile, assessment):
    """Activa un FUTURE sin destruir el plan vigente si la creación V7 falla."""
    snapshot = goal_analysis_snapshot(
        goal_row.get("goal_type"),
        goal_row.get("goal_style") or "Terminar",
        goal_row.get("race_date"),
        goal_row.get("target_time_sec"),
        assessment,
    )
    candidate = dict(goal_row)
    candidate["readiness_snapshot"] = snapshot

    can_generate, generation_reason = can_generate_v7_plan(candidate, assessment)
    current_active_plan = get_active_plan_record()
    if not can_generate:
        update_goal_record(goal_row["id"], readiness_snapshot=snapshot)
        return None, generation_reason, False

    # Con plan activo: construir el nuevo ciclo como FUTURE primero. Solo cuando
    # sesiones y metadata existen se archiva el ciclo anterior.
    if current_active_plan:
        future_plan, generation_reason = create_plan_record_for_goal(
            candidate, profile, assessment, status="FUTURE"
        )
        if not future_plan:
            return None, generation_reason, False

        archive_active_goal_and_plan(except_goal_id=goal_row["id"])
        update_goal_record(
            goal_row["id"],
            status="ACTIVE",
            readiness_snapshot=snapshot,
            source_assessment_id=assessment.get("id"),
        )
        update_plan_record(future_plan["id"], status="ACTIVE")
        future_plan["status"] = "ACTIVE"

        meta = future_plan.get("metadata") or {}
        update_profile_fields({
            "goal": goal_row.get("goal_type") if goal_row.get("goal_type") in GOAL_KM else "Condición física",
            "days_per_week": int(future_plan.get("days_per_week") or len(meta.get("selected_days") or []) or 2),
            "weekly_km": float(future_plan.get("initial_weekly_km") or meta.get("initial_weekly_km") or 0),
            "has_race": bool(goal_row.get("race_date")),
            "race_date": goal_row.get("race_date"),
            "target_time_sec": goal_row.get("target_time_sec"),
        })
        return future_plan, None, True

    archive_active_goal_and_plan(except_goal_id=goal_row["id"])
    update_goal_record(
        goal_row["id"],
        status="ACTIVE",
        readiness_snapshot=snapshot,
        source_assessment_id=assessment.get("id"),
    )
    candidate["status"] = "ACTIVE"
    plan_row, generation_reason = create_plan_record_for_goal(
        candidate, profile, assessment, status="ACTIVE"
    )
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

    with st.expander("Ver perfil técnico que usa el Plan Engine RCP V7"):
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

        default_mark_date = rcp_today() - timedelta(days=30)
        if existing_answers.get("recent_mark_date"):
            try:
                default_mark_date = date.fromisoformat(str(existing_answers["recent_mark_date"]))
            except Exception:
                pass
        pm4, pm5, pm6 = st.columns(3)
        recent_mark_date = pm4.date_input(
            "Fecha de la marca",
            value=default_mark_date,
            min_value=rcp_today() - timedelta(days=730),
            max_value=rcp_today(),
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
        default_goal_date = rcp_today() + timedelta(weeks=12)
        if existing_answers.get("goal_race_date"):
            try:
                default_goal_date = date.fromisoformat(str(existing_answers["goal_race_date"]))
            except Exception:
                pass
        goal_race_date = st.date_input(
            "Fecha objetivo (se ignora si no marcaste la casilla anterior)",
            value=default_goal_date,
            min_value=rcp_today() + timedelta(days=1),
            max_value=rcp_today() + timedelta(days=730),
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
                else rcp_today() + timedelta(weeks=12)
            )
            race_date = r1.date_input(
                "Fecha de carrera",
                value=default_race,
                min_value=rcp_today() + timedelta(days=14),
                max_value=rcp_today() + timedelta(days=365),
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
        default_date = rcp_today() + timedelta(weeks=12)
        old_date = (assessment.get("answers") or {}).get("goal_race_date")
        if old_date:
            try:
                default_date = max(rcp_today() + timedelta(days=1), date.fromisoformat(str(old_date)))
            except Exception:
                pass
        race_date_value = st.date_input(
            "Fecha objetivo",
            value=default_date,
            min_value=rcp_today() + timedelta(days=1),
            max_value=rcp_today() + timedelta(days=730),
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
        notes="Objetivo oficial creado durante onboarding V7.0",
        assessment=assessment,
    )
    if not goal_row:
        st.error("No fue posible guardar el objetivo.")
        return False

    plan_row, reason = create_plan_record_for_goal(goal_row, profile, assessment, status="ACTIVE")
    if plan_row:
        st.success("Objetivo guardado y plan RCP V7 creado. Tu historial queda preparado para futuras planificaciones.")
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
            "Este objetivo está activo pero todavía no tiene plan. RunningCoachPro V7 puede generarlo cuando la evaluación, seguridad y calendario lo permiten."
        )

    engine_name = str((active_plan or {}).get("engine_version") or "")
    if active_plan and engine_name.startswith("RCP-V7"):
        meta = active_plan.get("metadata") or {}
        st.markdown("### 🧠 Plan Engine RCP V7")
        e1, e2, e3, e4 = st.columns(4)
        e1.metric("Motor", engine_name)
        e2.metric("Días/sem", int(active_plan.get("days_per_week") or 0))
        e3.metric("Inicio", f"{float(meta.get('initial_weekly_km') or active_plan.get('initial_weekly_km') or 0):g} km")
        e4.metric("Pico previsto", f"{float(meta.get('peak_weekly_km') or 0):g} km")
        selected = meta.get("selected_days") or []
        if selected:
            st.caption(
                f"Días elegidos por V7: {', '.join(selected)} · Tirada larga: {meta.get('long_day') or '—'} · "
                f"Progresión: {meta.get('progression_mode') or '—'} · Ritmos: {meta.get('pace_basis') or 'RPE'}"
            )
    elif active_plan:
        with st.expander("🧠 Actualizar mi plan al motor RCP V7", expanded=True):
            st.write(
                "V7.1 utiliza tu Evaluación RCP, días realmente disponibles, base actual, experiencia, tirada larga, "
                "objetivo, calendario y rendimiento reciente. El plan actual no se borra: queda ARCHIVADO como historial."
            )
            preview_rows, preview_meta, preview_reason = build_v7_plan(
                active_goal, assessment, start_date_value=rcp_today() + timedelta(days=1)
            )
            if preview_reason:
                st.warning(f"Todavía no puedo generar el plan V7: {preview_reason}")
            else:
                v1, v2, v3, v4 = st.columns(4)
                v1.metric("Sesiones", len(preview_rows))
                v2.metric("Días/sem", len(preview_meta.get("selected_days") or []))
                v3.metric("Inicio", f"{float(preview_meta.get('initial_weekly_km') or 0):g} km/sem")
                v4.metric("Pico", f"{float(preview_meta.get('peak_weekly_km') or 0):g} km/sem")
                st.caption(
                    f"Distribución: {', '.join(preview_meta.get('selected_days') or [])} · "
                    f"Larga: {preview_meta.get('long_day') or '—'} · "
                    f"Progresión: {preview_meta.get('progression_mode') or '—'} · "
                    f"Base de ritmos: {preview_meta.get('pace_basis') or 'RPE'}"
                )
                phase_rows = preview_meta.get("weeks") or []
                if phase_rows:
                    st.dataframe(
                        [
                            {
                                "Semana": x.get("week"),
                                "Fase": x.get("phase"),
                                "KM objetivo": x.get("target_km"),
                                "Larga": x.get("long_km"),
                                "Calidad": x.get("quality_sessions"),
                            }
                            for x in phase_rows
                        ],
                        use_container_width=True,
                        hide_index=True,
                    )
                confirm_v7 = st.checkbox(
                    "Entiendo que mi plan actual quedará archivado y el nuevo plan V7 empezará desde la próxima fecha disponible.",
                    key="confirm_upgrade_v7",
                )
                if st.button(
                    "🚀 Crear mi plan RCP V7",
                    use_container_width=True,
                    disabled=not confirm_v7,
                    key="upgrade_plan_v7_button",
                ):
                    new_plan, err = replace_active_plan_with_v7(
                        active_goal, profile, assessment, start_date_value=rcp_today() + timedelta(days=1)
                    )
                    if new_plan:
                        st.success("Plan V7 creado. Tu plan anterior y sus registros permanecen en el historial.")
                        st.rerun()
                    else:
                        st.error(err or "No fue posible crear el plan V7.")

    with st.expander("✏️ Cambiar fecha o marca del objetivo actual"):
        styles = ["Terminar", "Terminar cómodo", "Mejorar mi marca", "Buscar una marca concreta"]
        with st.form("edit_active_goal_form"):
            style = st.selectbox(
                "Finalidad",
                styles,
                index=_option_index(styles, active_goal.get("goal_style"), 0),
            )
            has_date = st.checkbox("Tiene fecha", value=bool(active_goal.get("race_date")))
            default_date = rcp_today() + timedelta(weeks=12)
            if active_goal.get("race_date"):
                try:
                    default_date = max(rcp_today() + timedelta(days=1), date.fromisoformat(str(active_goal["race_date"])))
                except Exception:
                    pass
            race_date_value = st.date_input(
                "Fecha",
                value=default_date,
                min_value=rcp_today() + timedelta(days=1),
                max_value=rcp_today() + timedelta(days=730),
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
                st.info("La recalibración automática semana a semana llegará en V7.1. Cambiar la meta no borra ni reescribe el plan activo.")
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
                value=rcp_today() + timedelta(weeks=16),
                min_value=rcp_today() + timedelta(days=1),
                max_value=rcp_today() + timedelta(days=1095),
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

# V7.1 · Datos adaptativos del plan activo.
ADAPTIVE_READY = adaptive_storage_ready()
READINESS_ROWS = get_readiness_rows(ACTIVE_PLAN["id"]) if ADAPTIVE_READY and ACTIVE_PLAN else []
READINESS_BY_DATE = {str(x.get("checkin_date")): x for x in READINESS_ROWS}
ADJUSTMENTS = get_adjustments(ACTIVE_PLAN["id"]) if ADAPTIVE_READY and ACTIVE_PLAN else []
REPLAN_READY = replanning_storage_ready() if ADAPTIVE_READY else False
REPLANS = get_replans(ACTIVE_PLAN["id"]) if REPLAN_READY and ACTIVE_PLAN else []

# ============================================================
# V6.4.2 · Navigation Grid por iconos / Sidebar
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
    """Launcher responsive: 4×2 escritorio y 2×4 móvil mediante CSS Grid real."""
    current = st.session_state.get("rcp_page", "Hoy")
    items = list(PAGE_META.items())

    with st.container(key="rcp_nav_grid"):
        cols = st.columns(len(items))
        for col, (page, (icon, subtitle)) in zip(cols, items):
            with col:
                is_active = current == page
                if st.button(
                    f"{icon}\n{page}",
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


# ============================================================
# V7.1 · Motor Adaptativo RCP
# ============================================================
def readiness_score_from_inputs(sleep_quality, fatigue, soreness, stress, motivation, pain, illness, pain_changes_gait):
    """Índice heurístico RCP 0–100. No es una escala médica validada."""
    sleep_quality = int(sleep_quality)
    fatigue = int(fatigue)
    soreness = int(soreness)
    stress = int(stress)
    motivation = int(motivation)
    pain = int(pain)

    score = 100
    score -= {1: 30, 2: 20, 3: 8, 4: 2, 5: 0}.get(sleep_quality, 8)
    score -= {1: 0, 2: 4, 3: 10, 4: 20, 5: 30}.get(fatigue, 10)
    score -= 0 if soreness == 0 else (4 if soreness <= 3 else 10 if soreness <= 6 else 20)
    score -= {1: 0, 2: 2, 3: 5, 4: 9, 5: 15}.get(stress, 5)
    score -= {1: 10, 2: 6, 3: 3, 4: 1, 5: 0}.get(motivation, 3)
    score -= 0 if pain == 0 else (8 if pain <= 3 else 25 if pain <= 6 else 40)
    if illness:
        score -= 35
    if pain_changes_gait:
        score -= 40
    score = int(max(0, min(100, score)))

    if illness or pain_changes_gait or pain >= 7:
        status = "RED"
        message = "No se recomienda ejecutar intensidad con este check-in. Prioriza recuperación y valoración si los síntomas o el dolor lo requieren."
    elif score < 55 or pain >= 5 or fatigue >= 5:
        status = "ORANGE"
        message = "La disponibilidad para entrenar está reducida. Conviene disminuir carga e intensidad."
    elif score < 75 or sleep_quality <= 2 or fatigue >= 4 or soreness >= 6:
        status = "YELLOW"
        message = "Hay señales de recuperación incompleta. Mantén una sesión conservadora y reevalúa sensaciones."
    else:
        status = "GREEN"
        message = "Disponibilidad compatible con seguir el plan previsto, manteniendo control del esfuerzo."
    return score, status, message


def readiness_status_label(status):
    return {
        "GREEN": "🟢 Normal",
        "YELLOW": "🟡 Cautela",
        "ORANGE": "🟠 Reducir",
        "RED": "🔴 No intensidad",
    }.get(str(status or "").upper(), "—")


def readiness_session_guidance(readiness_row, session):
    """Conecta el check-in con la sesión del día sin emitir diagnóstico."""
    status = str((readiness_row or {}).get("readiness_status") or "").upper()
    kind = workout_kind(session) if session else "Descanso"
    if not session:
        if status == "RED":
            return "Hoy no hay sesión programada. Prioriza recuperación y reevalúa síntomas/dolor antes de volver a intensidad."
        return "Hoy no hay sesión programada. Usa el día para recuperar y mantener hábitos de sueño, hidratación y movilidad suave si te sienta bien."
    if status == "GREEN":
        return f"Sesión de hoy: {kind}. El check-in es compatible con mantener la prescripción prevista y controlar el esfuerzo."
    if status == "YELLOW":
        if kind in ("Series", "Tempo", "Carrera"):
            return f"Sesión de hoy: {kind}. Hazla de forma conservadora, evita perseguir ritmos si el esfuerzo se eleva y reevalúa durante el calentamiento."
        return f"Sesión de hoy: {kind}. Mantén intensidad cómoda y evita añadir volumen extra."
    if status == "ORANGE":
        return f"Sesión de hoy: {kind}. El estado actual favorece reducir carga; el Coach RCP puede proponer un ajuste temporal de los próximos días."
    if status == "RED":
        return f"Sesión de hoy: {kind}. No se recomienda ejecutar intensidad con este check-in. Si hay enfermedad aguda o dolor que altera la zancada, prioriza recuperación y valoración profesional cuando corresponda."
    return f"Sesión de hoy: {kind}. Completa el check-in para obtener una recomendación contextual."


def readiness_summary_html(readiness_row, session):
    status = str((readiness_row or {}).get("readiness_status") or "GREEN").upper()
    score = int((readiness_row or {}).get("readiness_score") or 0)
    css_status = status.lower() if status.lower() in ("green", "yellow", "orange", "red") else "green"
    sleep = int((readiness_row or {}).get("sleep_quality") or 0)
    fatigue = int((readiness_row or {}).get("fatigue") or 0)
    soreness = int((readiness_row or {}).get("soreness") or 0)
    pain = int((readiness_row or {}).get("pain") or 0)
    message = html.escape(str((readiness_row or {}).get("readiness_message") or ""))
    guidance = html.escape(readiness_session_guidance(readiness_row, session))
    return (
        f'<div class="rcp-readiness rcp-readiness-{css_status}">'
        f'<div class="rcp-readiness-title"><strong>{readiness_status_label(status)}</strong>'
        f'<span class="rcp-readiness-score">{score}/100</span></div>'
        f'<div>{message}</div>'
        f'<div class="rcp-readiness-facts">'
        f'<span class="rcp-ready-chip">🌙 Sueño {sleep}/5</span>'
        f'<span class="rcp-ready-chip">⚡ Fatiga {fatigue}/5</span>'
        f'<span class="rcp-ready-chip">🦵 Agujetas {soreness}/10</span>'
        f'<span class="rcp-ready-chip">📍 Dolor {pain}/10</span>'
        f'</div><div class="rcp-session-guidance"><b>Impacto en hoy:</b> {guidance}</div></div>'
    )


def expected_rpe_range(session):
    kind = workout_kind(session)
    if kind == "Carrera":
        return (7, 10)
    if kind == "Series":
        return (7, 8)
    if kind == "Tempo":
        return (6, 7)
    if kind == "Larga":
        return (3, 5)
    if kind == "Rodaje":
        text = f"{session.get('workout_name') or ''} {session.get('intensity') or ''}".upper()
        if "RECUP" in text:
            return (2, 3)
        return (3, 4)
    return (3, 5)


def _session_baseline(session):
    return {
        "planned_km": float(session.get("baseline_planned_km") if session.get("baseline_planned_km") is not None else session.get("planned_km") or 0),
        "workout_type": session.get("baseline_workout_type") or session.get("workout_type"),
        "workout_name": session.get("baseline_workout_name") or session.get("workout_name"),
        "target": session.get("baseline_target") or session.get("target"),
        "intensity": session.get("baseline_intensity") or session.get("intensity"),
        "description": session.get("baseline_description") or session.get("description"),
    }


def adaptation_snapshot(trigger_day=None):
    """Resume 14 días recientes y propone una acción conservadora sobre el plan futuro."""
    trigger_day = trigger_day or rcp_today()
    start14 = trigger_day - timedelta(days=13)
    start7 = trigger_day - timedelta(days=6)

    recent_sessions = [
        p for p in PLAN
        if (d := parse_date_safe(p.get("session_date")))
        and start14 <= d <= trigger_day
        and not session_is_optional(p)
    ]
    recent_logs = [
        l for l in CURRENT_LOGS
        if (d := parse_date_safe(l.get("session_date"))) and start14 <= d <= trigger_day
    ]
    log_map = {str(l.get("session_date")): l for l in recent_logs}

    due = [p for p in recent_sessions if parse_date_safe(p.get("session_date")) <= trigger_day]
    completed_local = [
        p for p in due
        if str(log_map.get(str(p.get("session_date")), {}).get("status") or "").upper() in ("COMPLETADO", "MODIFICADO")
    ]
    omitted_local = [
        log_map.get(str(p.get("session_date")))
        for p in due
        if str(log_map.get(str(p.get("session_date")), {}).get("status") or "").upper() == "OMITIDO"
    ]
    omitted_local = [x for x in omitted_local if x]

    planned_due_km = sum(float(p.get("planned_km") or 0) for p in due)
    actual_due_km = sum(
        float(log_map.get(str(p.get("session_date")), {}).get("actual_km") or 0)
        for p in completed_local
    )
    adherence = (len(completed_local) / len(due) * 100) if due else None
    km_ratio = (actual_due_km / planned_due_km) if planned_due_km > 0 else None

    rpe_excess = []
    post_pains = []
    post_fatigues = []
    for p in completed_local:
        log = log_map.get(str(p.get("session_date"))) or {}
        if log.get("rpe") is not None:
            _, upper = expected_rpe_range(p)
            rpe_excess.append(max(0.0, float(log.get("rpe")) - float(upper)))
        if log.get("post_pain") is not None:
            post_pains.append(int(log.get("post_pain")))
        if log.get("post_fatigue") is not None:
            post_fatigues.append(int(log.get("post_fatigue")))

    readiness_recent = [
        r for r in READINESS_ROWS
        if (d := parse_date_safe(r.get("checkin_date"))) and start7 <= d <= trigger_day
    ]
    readiness_scores = [int(r.get("readiness_score") or 0) for r in readiness_recent]
    readiness_avg = (sum(readiness_scores) / len(readiness_scores)) if readiness_scores else None
    readiness_statuses = [str(r.get("readiness_status") or "").upper() for r in readiness_recent]
    today_readiness = READINESS_BY_DATE.get(trigger_day.isoformat())
    today_status = str((today_readiness or {}).get("readiness_status") or "").upper()

    avg_rpe_excess = (sum(rpe_excess) / len(rpe_excess)) if rpe_excess else 0.0
    max_post_pain = max(post_pains) if post_pains else 0
    avg_post_fatigue = (sum(post_fatigues) / len(post_fatigues)) if post_fatigues else None

    missed_recovery = sum(
        1 for x in omitted_local
        if str(x.get("missed_reason") or "").lower() in ("fatiga", "dolor/molestia", "enfermedad")
    )
    missed_schedule = sum(
        1 for x in omitted_local
        if str(x.get("missed_reason") or "").lower() in ("falta de tiempo", "viaje")
    )

    adapted_future = [
        p for p in PLAN
        if (d := parse_date_safe(p.get("session_date")))
        and d >= trigger_day
        and str(p.get("adaptation_status") or "BASELINE").upper() != "BASELINE"
        and str(LOG_BY_DATE.get(str(p.get("session_date")), {}).get("status") or "").upper() not in ("COMPLETADO", "MODIFICADO", "OMITIDO")
    ]

    evidence_count = len(completed_local) + len(readiness_recent)
    reasons = []
    decision = "COLLECTING"
    severity = "none"

    hard_flag = (
        today_status == "RED"
        or "RED" in readiness_statuses
        or max_post_pain >= 7
    )
    if hard_flag:
        decision = "PROTECT"
        severity = "high"
        reasons.append("Existe una señal roja reciente de readiness o dolor post-entrenamiento alto.")
    elif (
        today_status == "ORANGE"
        or (readiness_avg is not None and readiness_avg < 58)
        or max_post_pain >= 5
        or missed_recovery >= 2
        or avg_rpe_excess >= 2.0
    ):
        decision = "REDUCE"
        severity = "major"
        reasons.append("La recuperación reciente sugiere una reducción importante de carga durante los próximos días.")
    elif (
        today_status == "YELLOW"
        or (readiness_avg is not None and readiness_avg < 72)
        or (adherence is not None and adherence < 70 and missed_recovery > 0)
        or avg_rpe_excess >= 1.0
        or (avg_post_fatigue is not None and avg_post_fatigue >= 4)
    ):
        decision = "REDUCE"
        severity = "moderate"
        reasons.append("Hay señales de fatiga o esfuerzo mayor de lo previsto; conviene descargar parcialmente.")
    elif evidence_count >= 2:
        if adapted_future and (
            today_status in ("", "GREEN")
            and (readiness_avg is None or readiness_avg >= 75)
            and max_post_pain <= 2
            and avg_rpe_excess <= 0.5
            and (adherence is None or adherence >= 80)
        ):
            decision = "RESTORE"
            severity = "recovery"
            reasons.append("Los indicadores se han normalizado; puede restaurarse el plan hacia su baseline original.")
        else:
            decision = "MAINTAIN"
            severity = "normal"
            reasons.append("Los datos recientes no justifican cambiar la progresión prevista.")
    else:
        reasons.append("Aún faltan datos suficientes. Completa check-ins y entrenamientos para personalizar la adaptación.")

    if missed_schedule >= 2:
        reasons.append("Se observan omisiones por tiempo/viaje; conviene revisar disponibilidad, no aumentar carga para compensarlas.")

    return {
        "trigger_date": trigger_day.isoformat(),
        "decision": decision,
        "severity": severity,
        "reasons": reasons,
        "metrics": {
            "window_days": 14,
            "due_sessions": len(due),
            "completed_sessions": len(completed_local),
            "omitted_sessions": len(omitted_local),
            "adherence_pct": round(adherence, 1) if adherence is not None else None,
            "planned_due_km": round(planned_due_km, 1),
            "actual_due_km": round(actual_due_km, 1),
            "actual_plan_ratio": round(km_ratio, 3) if km_ratio is not None else None,
            "avg_rpe_excess": round(avg_rpe_excess, 2),
            "max_post_pain": max_post_pain,
            "avg_post_fatigue": round(avg_post_fatigue, 2) if avg_post_fatigue is not None else None,
            "readiness_avg_7d": round(readiness_avg, 1) if readiness_avg is not None else None,
            "today_readiness": today_status or None,
            "recovery_related_omissions": missed_recovery,
            "schedule_related_omissions": missed_schedule,
            "adapted_future_sessions": len(adapted_future),
        },
    }


def _adapt_session_fields(session, decision, severity, quality_index=0):
    base = _session_baseline(session)
    kind = workout_kind({**session, **base})
    if kind == "Carrera":
        return None

    if decision == "RESTORE":
        return {
            **base,
            "adaptation_status": "BASELINE",
            "adapted_at": datetime.now(timezone.utc).isoformat(),
            "adaptation_id": None,
        }

    if decision == "PROTECT":
        factor = 0.65 if kind != "Larga" else 0.70
        new_km = max(2.0, round(base["planned_km"] * factor, 1))
        if kind in ("Series", "Tempo"):
            return {
                "planned_km": new_km,
                "workout_type": "RODAJE",
                "workout_name": "Rodaje de recuperación · adaptación RCP",
                "target": "RPE 2–3 · conversación completa",
                "intensity": "BAJA",
                "description": "ADAPTADO V7.1: se retira la intensidad prevista por señales recientes de recuperación. Mantén esfuerzo muy cómodo. Si persisten síntomas o dolor relevante, no entrenes y busca orientación apropiada.",
                "adaptation_status": "PROTECTED",
                "adapted_at": datetime.now(timezone.utc).isoformat(),
            }
        return {
            "planned_km": new_km,
            "target": "RPE 2–3 · muy cómodo",
            "intensity": "BAJA",
            "description": "ADAPTADO V7.1: volumen reducido temporalmente. Prioriza recuperación y técnica relajada.",
            "adaptation_status": "PROTECTED",
            "adapted_at": datetime.now(timezone.utc).isoformat(),
        }

    if decision == "REDUCE":
        major = severity == "major"
        factor = 0.75 if major else 0.85
        if kind == "Larga":
            factor = 0.75 if major else 0.82
        new_km = max(2.0, round(base["planned_km"] * factor, 1))
        if major and kind in ("Series", "Tempo"):
            return {
                "planned_km": new_km,
                "workout_type": "RODAJE",
                "workout_name": "Rodaje suave · descarga adaptativa",
                "target": "RPE 3 · conversación cómoda",
                "intensity": "BAJA",
                "description": "ADAPTADO V7.1: la sesión de calidad se reemplaza por rodaje suave durante la descarga adaptativa.",
                "adaptation_status": "REDUCED",
                "adapted_at": datetime.now(timezone.utc).isoformat(),
            }
        desc = str(base.get("description") or "")
        return {
            "planned_km": new_km,
            "description": f"ADAPTADO V7.1: volumen reducido temporalmente. {desc}",
            "adaptation_status": "REDUCED",
            "adapted_at": datetime.now(timezone.utc).isoformat(),
        }
    return None


def apply_adaptation(recommendation, trigger_day=None):
    if not ADAPTIVE_READY or not ACTIVE_PLAN:
        return False, "El módulo adaptativo V7.1 no está disponible."
    trigger_day = trigger_day or rcp_today()
    decision = str(recommendation.get("decision") or "")
    severity = str(recommendation.get("severity") or "")
    if decision not in ("PROTECT", "REDUCE", "RESTORE"):
        return False, "La recomendación actual no requiere modificar sesiones."

    scope_start = trigger_day
    scope_end = trigger_day + timedelta(days=6)
    targets = []
    for p in PLAN:
        d = parse_date_safe(p.get("session_date"))
        if not d or not (scope_start <= d <= scope_end):
            continue
        if str(LOG_BY_DATE.get(str(p.get("session_date")), {}).get("status") or "").upper() in ("COMPLETADO", "MODIFICADO", "OMITIDO"):
            continue
        if workout_kind(p) == "Carrera":
            continue
        if decision == "RESTORE" and str(p.get("adaptation_status") or "BASELINE").upper() == "BASELINE":
            continue
        targets.append(p)

    if not targets:
        return False, "No hay sesiones futuras elegibles para modificar en los próximos 7 días."

    record = create_adjustment_record({
        "plan_id": int(ACTIVE_PLAN["id"]),
        "trigger_date": trigger_day.isoformat(),
        "scope_start": scope_start.isoformat(),
        "scope_end": scope_end.isoformat(),
        "decision": decision,
        "severity": severity,
        "reason": " ".join(recommendation.get("reasons") or []),
        "metrics": recommendation.get("metrics") or {},
        "changes": [],
        "status": "PENDING",
    })
    if not record:
        return False, "No fue posible crear la auditoría del ajuste."

    changes = []
    touched = []
    quality_index = 0
    try:
        for p in sorted(targets, key=lambda x: str(x.get("session_date"))):
            before = {
                "planned_km": float(p.get("planned_km") or 0),
                "workout_type": p.get("workout_type"),
                "workout_name": p.get("workout_name"),
                "target": p.get("target"),
                "intensity": p.get("intensity"),
                "description": p.get("description"),
                "adaptation_status": p.get("adaptation_status") or "BASELINE",
                "adaptation_id": p.get("adaptation_id"),
            }
            if workout_kind(p) in ("Series", "Tempo"):
                quality_index += 1
            after = _adapt_session_fields(p, decision, severity, quality_index)
            if not after:
                continue
            if decision != "RESTORE":
                after["adaptation_id"] = int(record["id"])
            update_plan_session_fields(p["id"], **after)
            touched.append((p, before))
            changes.append({
                "session_id": p.get("id"),
                "session_date": str(p.get("session_date")),
                "before": before,
                "after": after,
            })

        update_adjustment_record(record["id"], changes=changes, status="APPLIED")
        return True, f"Adaptación aplicada a {len(changes)} sesión(es) entre {scope_start.strftime('%d/%m')} y {scope_end.strftime('%d/%m')}."
    except Exception as exc:
        for p, before in reversed(touched):
            try:
                update_plan_session_fields(p["id"], **before)
            except Exception:
                pass
        update_adjustment_record(record["id"], changes=changes, status="FAILED")
        return False, f"No fue posible completar el ajuste; se intentó revertir los cambios parciales: {exc}"


def revert_last_adaptation():
    rows = [a for a in ADJUSTMENTS if str(a.get("status") or "").upper() == "APPLIED"]
    if not rows:
        return False, "No hay una adaptación aplicada para revertir."
    adj = rows[0]
    changes = adj.get("changes") or []
    if not isinstance(changes, list) or not changes:
        return False, "La última adaptación no contiene cambios auditables."
    try:
        for item in reversed(changes):
            before = dict(item.get("before") or {})
            sid = item.get("session_id")
            # No alterar una sesión que ya fue registrada después del ajuste.
            session_date = str(item.get("session_date") or "")
            if str(LOG_BY_DATE.get(session_date, {}).get("status") or "").upper() in ("COMPLETADO", "MODIFICADO", "OMITIDO"):
                continue
            update_plan_session_fields(sid, **before)
        update_adjustment_record(
            adj["id"],
            status="REVERTED",
            reverted_at=datetime.now(timezone.utc).isoformat(),
        )
        return True, "Última adaptación revertida en las sesiones aún no realizadas."
    except Exception as exc:
        return False, f"No fue posible revertir la adaptación: {exc}"


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
    if day_value < rcp_today():
        return "⚠️ Pendiente"
    if day_value == rcp_today():
        return "⏱️ Hoy"
    return "○ Pendiente"


# ============================================================
# V7.2 · Motor de replanificación RCP
# ============================================================
def _replan_reason_group(reason):
    text = str(reason or "").strip().lower()
    if text in ("fatiga", "dolor/molestia", "enfermedad"):
        return "RECOVERY"
    if text in ("falta de tiempo", "viaje"):
        return "SCHEDULE"
    return "OTHER"


def _hard_session(session):
    return workout_kind(session) in ("Series", "Tempo", "Larga", "Carrera")


def _quality_session(session):
    return workout_kind(session) in ("Series", "Tempo")


def _available_weekday_indexes():
    selected = ((ACTIVE_PLAN or {}).get("metadata") or {}).get("selected_days") or []
    indexes = [DAY_NAMES.index(x) for x in selected if x in DAY_NAMES]
    if indexes:
        return sorted(set(indexes))
    answers = (LATEST_ASSESSMENT or {}).get("answers") or {}
    days = answers.get("available_days") or []
    indexes = [DAY_NAMES.index(x) for x in days if x in DAY_NAMES]
    return sorted(set(indexes)) if indexes else list(range(7))


def _plan_end_date():
    return parse_date_safe((ACTIVE_PLAN or {}).get("end_date")) or max(
        [d for p in PLAN if (d := parse_date_safe(p.get("session_date")))],
        default=rcp_today(),
    )


def _race_date_from_plan():
    race_sessions = [
        parse_date_safe(p.get("session_date"))
        for p in PLAN
        if workout_kind(p) == "Carrera" and parse_date_safe(p.get("session_date"))
    ]
    if race_sessions:
        return min(race_sessions)
    return parse_date_safe((ACTIVE_GOAL or {}).get("race_date"))


def _session_on_date(day_value):
    return PLAN_BY_DATE.get(day_value.isoformat())


def _logged_on_date(day_value):
    return LOG_BY_DATE.get(day_value.isoformat())


def _adjacent_hard_conflict(day_value, ignore_session_id=None, radius=1):
    for delta in range(-radius, radius + 1):
        if delta == 0:
            continue
        d = day_value + timedelta(days=delta)
        p = _session_on_date(d)
        if not p or int(p.get("id") or 0) == int(ignore_session_id or -1):
            continue
        status = str((_logged_on_date(d) or {}).get("status") or "").upper()
        if status in ("COMPLETADO", "MODIFICADO", "OMITIDO"):
            continue
        if _hard_session(p):
            return True
    return False


def _week_no_for_date(day_value, fallback=None):
    monday = day_value - timedelta(days=day_value.weekday())
    sunday = monday + timedelta(days=6)
    week_sessions = [
        p for p in PLAN
        if (d := parse_date_safe(p.get("session_date"))) and monday <= d <= sunday
    ]
    if week_sessions:
        return int(week_sessions[0].get("week_no") or fallback or 1)
    return int(fallback or 1)


def _handled_replan_trigger(log_row, session_row):
    log_id = int((log_row or {}).get("id") or 0)
    session_id = int((session_row or {}).get("id") or 0)
    for r in REPLANS:
        if str(r.get("status") or "").upper() not in ("APPLIED", "PENDING"):
            continue
        if log_id and int(r.get("trigger_log_id") or 0) == log_id:
            return True
        if session_id and int(r.get("trigger_session_id") or 0) == session_id and str(r.get("trigger_date")) == str((log_row or {}).get("session_date")):
            return True
    return False


def unresolved_missed_event(trigger_day=None, lookback_days=14, future_days=7):
    """
    Devuelve una omisión/restricción pendiente de procesar por V7.2.2.

    Además de omisiones ya ocurridas, acepta ausencias futuras explícitamente
    registradas dentro de los próximos `future_days`. Esto permite replanificar
    una guardia, viaje u otra indisponibilidad conocida sin esperar a que llegue
    la fecha. Las omisiones vencidas tienen prioridad; si solo hay futuras, se
    procesa primero la más próxima.
    """
    trigger_day = trigger_day or rcp_today()
    start = trigger_day - timedelta(days=max(1, int(lookback_days)))
    end = trigger_day + timedelta(days=max(0, int(future_days)))
    past_or_today = []
    future = []
    for log in CURRENT_LOGS:
        if str(log.get("status") or "").upper() != "OMITIDO":
            continue
        d = parse_date_safe(log.get("session_date"))
        if not d or not (start <= d <= end):
            continue
        session = PLAN_BY_DATE.get(str(log.get("session_date")))
        if not session or session_is_optional(session):
            continue
        if _handled_replan_trigger(log, session):
            continue
        item = (d, log, session)
        if d <= trigger_day:
            past_or_today.append(item)
        else:
            future.append(item)

    if past_or_today:
        past_or_today.sort(key=lambda x: x[0], reverse=True)
        d, log, session = past_or_today[0]
    elif future:
        future.sort(key=lambda x: x[0])
        d, log, session = future[0]
    else:
        return None

    return {
        "date": d,
        "log": log,
        "session": session,
        "planned_ahead": d > trigger_day,
    }


def _days_since_last_completed(before_or_on=None):
    ref = before_or_on or rcp_today()
    dates = []
    for log in CURRENT_LOGS:
        if str(log.get("status") or "").upper() not in ("COMPLETADO", "MODIFICADO"):
            continue
        d = parse_date_safe(log.get("session_date"))
        if d and d <= ref:
            dates.append(d)
    if not dates:
        return None
    return max(0, (ref - max(dates)).days)


def _recent_omitted_count(trigger_day, days=7):
    start = trigger_day - timedelta(days=days - 1)
    return sum(
        1 for log in CURRENT_LOGS
        if str(log.get("status") or "").upper() == "OMITIDO"
        and (d := parse_date_safe(log.get("session_date")))
        and start <= d <= trigger_day
        and not session_is_optional(PLAN_BY_DATE.get(str(log.get("session_date")), {}))
    )


def _find_safe_replan_target(missed_session, missed_day, trigger_day, kind):
    available = set(_available_weekday_indexes())
    horizon = 2 if kind == "Larga" else 3
    start = max(trigger_day, missed_day + timedelta(days=1))
    race_day = _race_date_from_plan()
    end = min(_plan_end_date(), missed_day + timedelta(days=horizon))
    if race_day:
        end = min(end, race_day - timedelta(days=1))
    if end < start:
        return None

    options = []
    for offset in range((end - start).days + 1):
        d = start + timedelta(days=offset)
        if d.weekday() not in available:
            continue
        existing = _session_on_date(d)
        log = _logged_on_date(d)
        if log and str(log.get("status") or "").upper() in ("COMPLETADO", "MODIFICADO", "OMITIDO"):
            continue
        if existing and workout_kind(existing) in ("Carrera", "Series", "Tempo", "Larga"):
            continue
        radius = 2 if kind == "Larga" else 1
        if _adjacent_hard_conflict(d, ignore_session_id=(existing or {}).get("id"), radius=radius):
            continue
        # Prioriza sustituir un rodaje/fuerza ya previsto: no añade una sesión extra.
        priority = 0 if existing and workout_kind(existing) in ("Rodaje", "Fuerza") else 1
        options.append((priority, d, existing))
    if not options:
        return None
    options.sort(key=lambda x: (x[0], x[1]))
    _, d, existing = options[0]
    return {"date": d, "existing": existing}


def replan_snapshot(trigger_day=None):
    """Clasifica una sesión omitida y propone una replanificación conservadora y auditable."""
    if not REPLAN_READY or not ACTIVE_PLAN:
        return None
    trigger_day = trigger_day or rcp_today()
    event = unresolved_missed_event(trigger_day)
    if not event:
        return None

    missed_day = event["date"]
    log = event["log"]
    session = event["session"]
    planned_ahead = bool(event.get("planned_ahead"))
    kind = workout_kind(session)
    reason = str(log.get("missed_reason") or "No informado")
    reason_group = _replan_reason_group(reason)
    recent_omitted = _recent_omitted_count(trigger_day, 7)
    gap_days = _days_since_last_completed(trigger_day)
    race_day = _race_date_from_plan()
    days_to_race = (race_day - trigger_day).days if race_day else None
    today_readiness = READINESS_BY_DATE.get(trigger_day.isoformat()) or {}
    today_readiness_status = str(today_readiness.get("readiness_status") or "").upper()

    decision = "SKIP"
    if planned_ahead:
        summary = "Ausencia futura registrada; evaluar el plan antes de que llegue la fecha."
        explanation = "V7.2.2 puede anticipar una indisponibilidad conocida y reorganizar sin añadir carga extra."
    else:
        summary = "No recuperar esta sesión; continuar con el plan."
        explanation = "Recuperar una sesión aislada puede concentrar carga sin aportar una adaptación útil."
    target = None
    scope_days = 0

    if kind == "Carrera":
        decision = "REVIEW_GOAL"
        summary = "No mover automáticamente una carrera objetivo."
        explanation = "Una carrera perdida requiere revisar el objetivo y el siguiente ciclo, no trasladarla como una sesión ordinaria."
    elif gap_days is not None and gap_days >= 14:
        decision = "REASSESS"
        summary = "Reevaluar antes de reconstruir el plan."
        explanation = "Han pasado al menos 14 días desde la última sesión completada; V7.2 evita retomar directamente la carga previa."
    elif today_readiness_status in ("RED", "ORANGE"):
        decision = "PROTECT_WEEK"
        summary = "No recuperar la sesión mientras el readiness actual está comprometido."
        explanation = "V7.2 prioriza el estado actual sobre la sesión perdida; primero reduce carga y elimina intensidad durante unos días."
        scope_days = 5
    elif reason_group == "RECOVERY" and gap_days is not None and gap_days >= 7:
        decision = "RETURN_WEEK"
        summary = "Crear una semana de retorno progresivo."
        explanation = "Tras una interrupción de 7–13 días, se prioriza carrera fácil y menor volumen antes de recuperar calidad."
        scope_days = 7
    elif recent_omitted >= 2:
        decision = "REBUILD_WEEK"
        summary = "Reconstruir los próximos 7 días sin acumular sesiones perdidas."
        explanation = "Hay varias omisiones recientes; V7.2 conserva un solo estímulo principal y reduce la densidad de carga."
        scope_days = 7
    elif reason_group == "RECOVERY" and reason.lower() in ("dolor/molestia", "enfermedad"):
        decision = "PROTECT_WEEK"
        summary = "No recuperar la sesión y proteger los próximos días."
        explanation = "Dolor o enfermedad no deben compensarse acumulando entrenamiento; se retira temporalmente intensidad y se reduce volumen."
        scope_days = 5
    elif reason_group == "RECOVERY":
        decision = "SKIP"
        summary = "Dejar atrás la sesión y continuar sin compensarla."
        explanation = "La omisión fue por recuperación/fatiga; la prioridad es absorber la carga, no recuperarla."
    elif kind in ("Rodaje", "Fuerza") or session_is_optional(session):
        decision = "SKIP"
        summary = "No recuperar esta sesión."
        explanation = "Un rodaje fácil o trabajo complementario aislado puede omitirse sin desplazar la semana."
    elif reason_group == "SCHEDULE" and kind in ("Series", "Tempo"):
        target = _find_safe_replan_target(session, missed_day, trigger_day, kind)
        if target:
            decision = "RESCHEDULE_QUALITY"
            summary = f"Reubicar una versión reducida de la calidad al {target['date'].strftime('%d/%m')}."
            explanation = "Existe un hueco compatible sin colocar otra sesión exigente inmediatamente alrededor."
        else:
            decision = "SKIP"
            summary = "No existe un hueco seguro para recuperar la calidad."
            explanation = "V7.2 prefiere perder una sesión a crear dos estímulos exigentes demasiado próximos."
    elif reason_group == "SCHEDULE" and kind == "Larga":
        if days_to_race is not None and days_to_race <= 7:
            decision = "SKIP"
            summary = "No recuperar la tirada larga durante la última semana precompetitiva."
            explanation = "La proximidad de la carrera tiene prioridad sobre recuperar volumen perdido."
        else:
            target = _find_safe_replan_target(session, missed_day, trigger_day, kind)
            if target:
                decision = "RESCHEDULE_LONG"
                summary = f"Reubicar una tirada larga reducida al {target['date'].strftime('%d/%m')}."
                explanation = "El hueco permite mantener distancia respecto de calidad/carrera y se reduce la tirada para limitar carga residual."
            else:
                decision = "SKIP"
                summary = "No existe un hueco seguro para recuperar la tirada larga."
                explanation = "No se apilará una larga sobre la siguiente sesión exigente."

    return {
        "decision": decision,
        "summary": summary,
        "explanation": explanation,
        "event": event,
        "target": target,
        "scope_days": scope_days,
        "metrics": {
            "missed_kind": kind,
            "missed_reason": reason,
            "reason_group": reason_group,
            "planned_ahead": planned_ahead,
            "recent_omitted_7d": recent_omitted,
            "days_since_last_completed": gap_days,
            "days_to_race": days_to_race,
            "today_readiness_status": today_readiness_status or None,
            "today_readiness_score": today_readiness.get("readiness_score"),
        },
    }


def _replan_change_before(session):
    fields = [
        "session_date", "week_no", "workout_type", "workout_name", "planned_km",
        "target", "intensity", "description", "is_optional", "adaptation_status",
        "adaptation_id", "replan_status", "replan_id", "replanned_at",
    ]
    return {k: session.get(k) for k in fields}


def _update_with_replan(session, fields, replan_id, status_label):
    before = _replan_change_before(session)
    values = dict(fields)
    values.update({
        "replan_id": int(replan_id),
        "replan_status": status_label,
        "replanned_at": datetime.now(timezone.utc).isoformat(),
    })
    update_plan_session_fields(session["id"], **values)
    after = dict(before)
    after.update(values)
    return {"op": "UPDATE", "session_id": int(session["id"]), "before": before, "after": after}


def _return_session_fields(session, factor, mode="RETURN"):
    kind = workout_kind(session)
    km = float(session.get("planned_km") or 0)
    new_km = round(max(2.0, km * factor), 1) if km > 0 else 0.0
    if kind in ("Series", "Tempo"):
        return {
            "workout_type": "RODAJE",
            "workout_name": "Rodaje fácil · retorno",
            "planned_km": new_km,
            "target": "RPE 2–3 · ritmo conversacional",
            "intensity": "BAJA",
            "description": "V7.2: sesión de calidad sustituida temporalmente por carrera fácil durante el retorno. No compensar intensidad perdida.",
        }
    if kind == "Larga":
        return {
            "workout_name": "Tirada larga reducida · retorno",
            "planned_km": new_km,
            "target": "RPE 3–4 · ritmo cómodo",
            "intensity": "BAJA-MEDIA",
            "description": "V7.2: tirada larga reducida por replanificación. Mantener esfuerzo cómodo y detener si reaparecen síntomas o dolor relevante.",
        }
    return {
        "planned_km": new_km,
        "target": "RPE 2–4 · ritmo cómodo",
        "intensity": "BAJA",
        "description": f"V7.2: carga reducida temporalmente ({mode.lower()}). Priorizar continuidad y recuperación.",
    }


def apply_replan(recommendation, trigger_day=None):
    if not REPLAN_READY or not ACTIVE_PLAN or not recommendation:
        return False, "La replanificación V7.2 no está disponible."
    event = recommendation.get("event") or {}
    log = event.get("log") or {}
    missed = event.get("session") or {}
    missed_day = event.get("date") or trigger_day or rcp_today()
    decision = str(recommendation.get("decision") or "SKIP")
    scope_days = int(recommendation.get("scope_days") or 0)
    scope_start = max(rcp_today(), missed_day + timedelta(days=1)) if scope_days else None
    scope_end = (scope_start + timedelta(days=scope_days - 1)) if scope_start and scope_days else None

    record = create_replan_record({
        "plan_id": int(ACTIVE_PLAN["id"]),
        "trigger_session_id": int(missed.get("id")) if missed.get("id") else None,
        "trigger_log_id": int(log.get("id")) if log.get("id") else None,
        "trigger_date": missed_day.isoformat(),
        "trigger_type": "MISSED_SESSION",
        "decision": decision,
        "reason": f"{recommendation.get('summary')} {recommendation.get('explanation')}",
        "scope_start": scope_start.isoformat() if scope_start else None,
        "scope_end": scope_end.isoformat() if scope_end else None,
        "metrics": recommendation.get("metrics") or {},
        "changes": [],
        "status": "PENDING",
    })
    if not record:
        return False, "No fue posible crear la auditoría de replanificación."
    replan_id = int(record["id"])
    changes = []

    try:
        if decision in ("SKIP", "REVIEW_GOAL", "REASSESS"):
            pass

        elif decision in ("RESCHEDULE_QUALITY", "RESCHEDULE_LONG"):
            target = recommendation.get("target") or {}
            target_day = target.get("date")
            existing = target.get("existing")
            if not target_day:
                raise RuntimeError("El hueco propuesto ya no está disponible.")
            source_km = float(missed.get("planned_km") or 0)
            factor = 0.90 if decision == "RESCHEDULE_QUALITY" else 0.82
            if existing:
                existing_km = float(existing.get("planned_km") or 0)
                if decision == "RESCHEDULE_QUALITY":
                    new_km = round(min(source_km * factor, max(3.0, existing_km)), 1)
                    fields = {
                        "workout_type": missed.get("workout_type"),
                        "workout_name": f"{missed.get('workout_name')} · reubicada",
                        "planned_km": new_km,
                        "target": missed.get("target"),
                        "intensity": missed.get("intensity"),
                        "description": "V7.2: calidad reubicada por conflicto de agenda. Versión reducida; no añadir el rodaje sustituido en otro día. " + str(missed.get("description") or ""),
                        "is_optional": False,
                    }
                    status_label = "RESCHEDULED_QUALITY"
                else:
                    new_km = round(min(source_km * factor, max(existing_km * 1.20, source_km * 0.65)), 1)
                    fields = {
                        "workout_type": "LARGA",
                        "workout_name": f"{missed.get('workout_name')} · reubicada reducida",
                        "planned_km": new_km,
                        "target": "RPE 3–4 · ritmo cómodo",
                        "intensity": "MEDIA",
                        "description": "V7.2: tirada larga reubicada y reducida. No intentar completar el kilometraje originalmente perdido. " + str(missed.get("description") or ""),
                        "is_optional": False,
                    }
                    status_label = "RESCHEDULED_LONG"
                changes.append(_update_with_replan(existing, fields, replan_id, status_label))
            else:
                # Hueco libre: crea una única sesión reducida, no copia la carga completa.
                new_km = round(max(3.0, source_km * factor), 1)
                row = {
                    "session_date": target_day.isoformat(),
                    "week_no": _week_no_for_date(target_day, missed.get("week_no")),
                    "workout_type": missed.get("workout_type") if decision == "RESCHEDULE_QUALITY" else "LARGA",
                    "workout_name": f"{missed.get('workout_name')} · reubicada",
                    "planned_km": new_km,
                    "target": missed.get("target") if decision == "RESCHEDULE_QUALITY" else "RPE 3–4 · ritmo cómodo",
                    "intensity": missed.get("intensity") if decision == "RESCHEDULE_QUALITY" else "MEDIA",
                    "description": "V7.2: sesión reubicada en hueco libre y reducida para evitar compensación excesiva. " + str(missed.get("description") or ""),
                    "is_optional": False,
                    "replan_id": replan_id,
                    "replan_status": "INSERTED_REPLAN",
                    "replanned_at": datetime.now(timezone.utc).isoformat(),
                }
                inserted = insert_replan_session(ACTIVE_PLAN["id"], row)
                if not inserted:
                    raise RuntimeError("No fue posible guardar la sesión reubicada.")
                changes.append({"op": "INSERT", "session_id": int(inserted["id"]), "after": inserted})

        elif decision in ("RETURN_WEEK", "PROTECT_WEEK", "REBUILD_WEEK"):
            if not scope_start or not scope_end:
                raise RuntimeError("No fue posible definir el bloque de replanificación.")
            future = [
                p for p in PLAN
                if (d := parse_date_safe(p.get("session_date")))
                and scope_start <= d <= scope_end
                and workout_kind(p) != "Carrera"
                and str((_logged_on_date(d) or {}).get("status") or "").upper() not in ("COMPLETADO", "MODIFICADO", "OMITIDO")
            ]
            quality_seen = 0
            for p in future:
                kind = workout_kind(p)
                if decision == "RETURN_WEEK":
                    fields = _return_session_fields(p, 0.68, "RETURN")
                    label = "RETURN_WEEK"
                elif decision == "PROTECT_WEEK":
                    fields = _return_session_fields(p, 0.78, "PROTECT")
                    label = "PROTECT_WEEK"
                else:
                    # Rebuild: máximo un estímulo de calidad; el resto baja densidad/volumen.
                    if _quality_session(p):
                        quality_seen += 1
                        if quality_seen > 1:
                            fields = _return_session_fields(p, 0.80, "REBUILD")
                        else:
                            fields = {"planned_km": round(max(3.0, float(p.get("planned_km") or 0) * 0.88), 1)}
                    elif kind == "Larga":
                        fields = {"planned_km": round(max(4.0, float(p.get("planned_km") or 0) * 0.85), 1)}
                    else:
                        fields = {"planned_km": round(max(2.0, float(p.get("planned_km") or 0) * 0.90), 1)}
                    fields["description"] = "V7.2: semana reconstruida tras múltiples omisiones. No recuperar sesiones perdidas adicionalmente. " + str(p.get("description") or "")
                    label = "REBUILT_WEEK"
                changes.append(_update_with_replan(p, fields, replan_id, label))

        update_replan_record(replan_id, changes=changes, status="APPLIED")
        if decision == "SKIP":
            return True, "Sesión cerrada sin recuperación. El plan continúa sin acumular carga."
        if decision == "REASSESS":
            return True, "V7.2 registró la interrupción. Se recomienda una nueva Evaluación RCP antes de reconstruir el ciclo."
        if decision == "REVIEW_GOAL":
            return True, "La carrera perdida quedó registrada para revisión del objetivo; no se movió automáticamente."
        return True, f"Replanificación V7.2 aplicada · {len(changes)} sesión(es) ajustada(s)."
    except Exception as exc:
        # Rollback best-effort de cambios ya realizados en esta operación.
        for ch in reversed(changes):
            try:
                if ch.get("op") == "UPDATE":
                    update_plan_session_fields(ch["session_id"], **(ch.get("before") or {}))
                elif ch.get("op") == "INSERT":
                    delete_plan_session_by_id(ch["session_id"])
            except Exception:
                pass
        update_replan_record(replan_id, changes=changes, status="FAILED", reason=f"{record.get('reason') or ''} Error: {exc}")
        return False, f"No fue posible aplicar la replanificación: {exc}"


def revert_last_replan():
    rows = [r for r in REPLANS if str(r.get("status") or "").upper() == "APPLIED"]
    if not rows:
        return False, "No hay replanificaciones aplicadas para revertir."
    record = rows[0]
    changes = record.get("changes") or []
    if not isinstance(changes, list):
        return False, "La auditoría de esta replanificación no es válida."

    # No revierte una replanificación si alguna sesión afectada ya fue ejecutada/registrada.
    for ch in changes:
        sid = int(ch.get("session_id") or 0)
        current = get_plan_session_by_id(sid)
        if not current and ch.get("op") == "INSERT":
            continue
        current_date = parse_date_safe((current or {}).get("session_date") or (ch.get("after") or {}).get("session_date"))
        if current_date:
            log = get_logs(ACTIVE_PLAN["id"])
            log = next((x for x in log if str(x.get("session_date")) == current_date.isoformat()), None)
            if log and str(log.get("status") or "").upper() in ("COMPLETADO", "MODIFICADO", "OMITIDO"):
                return False, "No se puede revertir: una de las sesiones replanificadas ya tiene un registro."

    try:
        for ch in reversed(changes):
            if ch.get("op") == "UPDATE":
                update_plan_session_fields(ch["session_id"], **(ch.get("before") or {}))
            elif ch.get("op") == "INSERT":
                delete_plan_session_by_id(ch["session_id"])
        update_replan_record(
            record["id"],
            status="REVERTED",
            reverted_at=datetime.now(timezone.utc).isoformat(),
        )
        return True, "Última replanificación revertida."
    except Exception as exc:
        return False, f"No fue posible revertir la replanificación: {exc}"


def revert_replan_record(record):
    """Revierte una replanificación concreta si ninguna sesión afectada fue ya registrada."""
    if not record:
        return True, "No había replanificación asociada."
    status = str(record.get("status") or "").upper()
    if status in ("REVERTED", "FAILED"):
        return True, "La replanificación asociada ya estaba cerrada."
    changes = record.get("changes") or []
    if not isinstance(changes, list):
        return False, "La auditoría de la replanificación asociada no es válida."
    current_logs = get_logs(ACTIVE_PLAN["id"]) if ACTIVE_PLAN else []
    by_date = {str(x.get("session_date")): x for x in current_logs}
    for ch in changes:
        sid = int(ch.get("session_id") or 0)
        current = get_plan_session_by_id(sid)
        if not current and ch.get("op") == "INSERT":
            continue
        current_date = parse_date_safe((current or {}).get("session_date") or (ch.get("after") or {}).get("session_date"))
        if current_date:
            log = by_date.get(current_date.isoformat())
            if log and str(log.get("status") or "").upper() in ("COMPLETADO", "MODIFICADO", "OMITIDO"):
                return False, "No puedo cancelar esta ausencia porque una sesión afectada por la replanificación ya tiene un registro."
    try:
        for ch in reversed(changes):
            if ch.get("op") == "UPDATE":
                update_plan_session_fields(ch["session_id"], **(ch.get("before") or {}))
            elif ch.get("op") == "INSERT":
                delete_plan_session_by_id(ch["session_id"])
        update_replan_record(record["id"], status="REVERTED", reverted_at=datetime.now(timezone.utc).isoformat())
        return True, "Replanificación asociada revertida."
    except Exception as exc:
        return False, f"No fue posible revertir la replanificación asociada: {exc}"


def cancel_planned_absence(log_row, session_row):
    """Cancela una ausencia futura y deshace su replanificación si ya fue aplicada."""
    if not log_row or str(log_row.get("status") or "").upper() != "OMITIDO":
        return False, "No existe una ausencia planificada para cancelar."
    session_day = parse_date_safe(log_row.get("session_date"))
    if not session_day or session_day <= rcp_today():
        return False, "Esta acción solo se usa para ausencias futuras planificadas."
    log_id = int(log_row.get("id") or 0)
    session_id = int((session_row or {}).get("id") or 0)
    related = []
    for r in REPLANS:
        if str(r.get("status") or "").upper() not in ("APPLIED", "PENDING"):
            continue
        if log_id and int(r.get("trigger_log_id") or 0) == log_id:
            related.append(r)
        elif session_id and int(r.get("trigger_session_id") or 0) == session_id and str(r.get("trigger_date")) == session_day.isoformat():
            related.append(r)
    for record in related:
        ok, msg = revert_replan_record(record)
        if not ok:
            return False, msg
    try:
        delete_log_by_id(log_id) if log_id else delete_log(session_day.isoformat())
        return True, f"Ausencia planificada del {session_day.strftime('%d/%m')} cancelada; la sesión vuelve a estar pendiente."
    except Exception as exc:
        return False, f"No fue posible cancelar la ausencia planificada: {exc}"


def expected_next_training_date(from_day=None):
    from_day = from_day or rcp_today()
    meta = (ACTIVE_PLAN or {}).get("metadata") or {}
    names = meta.get("selected_days") or []
    weekdays = {DAY_INDEX[n] for n in names if n in DAY_INDEX}
    if not weekdays:
        return None
    for offset in range(1, 8):
        d = from_day + timedelta(days=offset)
        if d.weekday() in weekdays:
            return d
    return None


def timezone_plan_gap():
    """Detecta el patrón del bug UTC: el plan empieza después del próximo día elegible local."""
    if not ACTIVE_PLAN or not str(ACTIVE_PLAN.get("engine_version") or "").startswith("RCP-V7"):
        return None
    expected = expected_next_training_date(rcp_today())
    if not expected:
        return None
    future_dates = sorted(d for p in PLAN if (d := parse_date_safe(p.get("session_date"))) and d > rcp_today())
    first = future_dates[0] if future_dates else None
    if first and expected < first and expected.isoformat() not in PLAN_BY_DATE:
        return {"expected": expected, "first": first}
    return None


def render_timezone_plan_repair(location_key="home"):
    """Muestra y ejecuta la reparación del plan si el ciclo activo saltó el próximo día elegible local."""
    gap = timezone_plan_gap()
    if not gap:
        return False

    st.warning(
        f"⚠️ El plan activo tiene un hueco al inicio: según tu zona horaria ({rcp_timezone_name()}), "
        f"el próximo día elegible es {gap['expected'].strftime('%d/%m/%Y')}, pero la primera sesión guardada "
        f"es {gap['first'].strftime('%d/%m/%Y')}."
    )
    st.caption(
        "Esto ocurre cuando el ciclo fue generado antes de corregir la zona horaria. La reparación crea primero "
        "un nuevo ciclo desde la fecha correcta y archiva el ciclo defectuoso; no borra el historial."
    )

    if st.button(
        f"🛠️ Reparar plan desde {gap['expected'].strftime('%d/%m')}",
        type="primary",
        use_container_width=True,
        key=f"repair_timezone_plan_{location_key}",
    ):
        completed_active = [
            l for l in CURRENT_LOGS
            if str(l.get("status") or "").upper() in ("COMPLETADO", "MODIFICADO")
        ]
        if completed_active:
            st.error(
                "El plan activo ya tiene entrenamientos realizados. No lo regenero automáticamente para no reescribir historia."
            )
            return True

        new_plan, err = replace_active_plan_with_v7(
            ACTIVE_GOAL,
            profile,
            LATEST_ASSESSMENT,
            start_date_value=gap["expected"],
        )
        if new_plan:
            st.session_state["rcp_saved_notice"] = (
                f"Plan reparado ✅. El nuevo ciclo comienza el {gap['expected'].strftime('%d/%m/%Y')} "
                f"según {rcp_timezone_name()}."
            )
            st.rerun()
        else:
            st.error(err or "No fue posible reparar el inicio del plan.")
        return True
    return True


def replan_decision_label(decision):
    return {
        "SKIP": "Continuar sin recuperar",
        "RESCHEDULE_QUALITY": "Reubicar calidad",
        "RESCHEDULE_LONG": "Reubicar larga reducida",
        "PROTECT_WEEK": "Proteger próximos días",
        "RETURN_WEEK": "Semana de retorno",
        "REBUILD_WEEK": "Reconstruir semana",
        "REASSESS": "Reevaluación recomendada",
        "REVIEW_GOAL": "Revisar objetivo",
    }.get(str(decision or ""), str(decision or "—"))


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
        if (d := parse_date_safe(p.get("session_date"))) and d <= rcp_today()
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
            if d <= rcp_today():
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


def active_plan_week_info(week_no):
    meta = (ACTIVE_PLAN or {}).get("metadata") or {}
    for item in meta.get("weeks") or []:
        if int(item.get("week") or 0) == int(week_no or 0):
            return item
    return {}


def render_goal_hero():
    goal_name = html.escape(str(ACTIVE_GOAL.get("goal_type") or "Objetivo"))
    race_day = parse_date_safe(ACTIVE_GOAL.get("race_date"))
    target_sec = ACTIVE_GOAL.get("target_time_sec")
    target_label = fmt_time(target_sec) if target_sec else "Sin marca objetivo"
    if race_day:
        days = (race_day - rcp_today()).days
        race_label = race_day.strftime("%d/%m/%Y")
        countdown = f"{days} días" if days >= 0 else "Finalizado"
    else:
        race_label = "Sin fecha"
        countdown = "Bloque abierto"

    active_week = "—"
    if PLAN:
        past = [
            p for p in PLAN
            if (d := parse_date_safe(p.get("session_date"))) and d <= rcp_today()
        ]
        future = [
            p for p in PLAN
            if (d := parse_date_safe(p.get("session_date"))) and d >= rcp_today()
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
st.sidebar.caption(f"🕒 {rcp_timezone_name()} · hoy {rcp_today().strftime('%d/%m/%Y')}")
st.sidebar.markdown(f"🎯 **{ACTIVE_GOAL.get('goal_type') or '—'}**")
if ACTIVE_GOAL.get("race_date"):
    st.sidebar.caption(f"Fecha objetivo · {ACTIVE_GOAL.get('race_date')}")

if ADAPTIVE_READY:
    st.sidebar.markdown("🧠 **Motor adaptativo:** V7.2.3")
else:
    st.sidebar.warning("V7.1 pendiente de migración SQL")

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
    st.session_state["selected_day_picker"] = rcp_today()

selected_day = st.sidebar.date_input(
    "Explorar fecha",
    key="selected_day_picker",
)

if st.sidebar.button("↩️ Volver a Hoy", use_container_width=True):
    set_page("Hoy", rcp_today())
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

dashboard_day = rcp_today()
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


def session_display_name(session):
    """Mantiene el nombre sincronizado con planned_km tras adaptaciones/replanificaciones."""
    name = str((session or {}).get("workout_name") or "Entrenamiento")
    km = float((session or {}).get("planned_km") or 0)
    if re.search(r"\s+\d+(?:[\.,]\d+)?\s*km\s*$", name, flags=re.IGNORECASE):
        base = re.sub(r"\s+\d+(?:[\.,]\d+)?\s*km\s*$", "", name, flags=re.IGNORECASE).rstrip()
        return f"{base} {km:g} km" if km > 0 else base
    return name


# ============================================================
# 🏠 HOY · Home real
# ============================================================
if current_page == "Hoy":
    if selected_day == rcp_today():
        st.subheader("🏠 Hoy")
    else:
        st.subheader(f"📍 {DAY_NAMES[selected_day.weekday()]} · {selected_day.strftime('%d/%m/%Y')}")
        st.caption("Estás explorando otra fecha. Usa “Volver a Hoy” para regresar al inicio.")

    _saved_notice = st.session_state.pop("rcp_saved_notice", None)
    if _saved_notice:
        st.success(_saved_notice)

    if selected_day == rcp_today():
        render_timezone_plan_repair("home")

    today_session = PLAN_BY_DATE.get(selected_day.isoformat())
    today_log = LOG_BY_DATE.get(selected_day.isoformat())

    # V7.1.1 · Readiness compacto. El formulario permanece cerrado por defecto.
    coach = None
    if ADAPTIVE_READY and selected_day == rcp_today():
        existing_ready = READINESS_BY_DATE.get(selected_day.isoformat(), {})
        st.markdown("### 🧠 Estado de hoy")
        if existing_ready:
            st.markdown(
                readiness_summary_html(existing_ready, today_session),
                unsafe_allow_html=True,
            )
            checkin_label = "✏️ Actualizar check-in"
        else:
            st.markdown(
                '<div class="rcp-readiness"><div class="rcp-readiness-title"><strong>⚪ Sin check-in de hoy</strong>'
                '<span class="rcp-readiness-score">—/100</span></div>'
                '<div>Completa un check-in breve para contextualizar la sesión y alimentar el motor adaptativo.</div>'
                '<div class="rcp-session-guidance"><b>Impacto en hoy:</b> hasta completar el check-in, RunningCoachPro mantiene la prescripción sin inferir tu estado de recuperación.</div></div>',
                unsafe_allow_html=True,
            )
            checkin_label = "📝 Hacer check-in"

        with st.expander(checkin_label, expanded=False):
            st.caption("Tarda menos de un minuto. No diagnostica enfermedad; se usa para modular la carga de entrenamiento.")
            with st.form("daily_readiness_form"):
                c1, c2 = st.columns(2)
                sleep_quality = c1.slider("Sueño", 1, 5, int(existing_ready.get("sleep_quality") or 4), help="1 = muy malo · 5 = excelente")
                fatigue = c2.slider("Fatiga", 1, 5, int(existing_ready.get("fatigue") or 2), help="1 = mínima · 5 = muy alta")
                c3, c4 = st.columns(2)
                soreness = c3.slider("Dolor muscular / agujetas", 0, 10, int(existing_ready.get("soreness") or 0))
                stress = c4.slider("Estrés", 1, 5, int(existing_ready.get("stress") or 2))
                c5, c6 = st.columns(2)
                motivation = c5.slider("Motivación", 1, 5, int(existing_ready.get("motivation") or 4))
                pain = c6.slider("Dolor localizado", 0, 10, int(existing_ready.get("pain") or 0))
                illness = st.checkbox("Tengo fiebre o síntomas agudos de enfermedad", value=bool(existing_ready.get("illness")))
                pain_changes_gait = st.checkbox("El dolor modifica mi forma de caminar o correr", value=bool(existing_ready.get("pain_changes_gait")))
                ready_notes = st.text_area("Nota opcional", value=str(existing_ready.get("notes") or ""))
                save_ready = st.form_submit_button("Guardar check-in", use_container_width=True)
            if save_ready:
                rs, rst, rmsg = readiness_score_from_inputs(
                    sleep_quality, fatigue, soreness, stress, motivation, pain, illness, pain_changes_gait
                )
                save_readiness({
                    "checkin_date": selected_day.isoformat(),
                    "sleep_quality": int(sleep_quality),
                    "fatigue": int(fatigue),
                    "soreness": int(soreness),
                    "stress": int(stress),
                    "motivation": int(motivation),
                    "pain": int(pain),
                    "illness": bool(illness),
                    "pain_changes_gait": bool(pain_changes_gait),
                    "notes": ready_notes.strip(),
                    "readiness_score": int(rs),
                    "readiness_status": rst,
                    "readiness_message": rmsg,
                })
                st.success(f"Check-in guardado · {readiness_status_label(rst)} · {rs}/100")
                st.rerun()

        # Se calcula aquí, pero el Coach se presenta DESPUÉS de la sesión del día.
        coach = adaptation_snapshot(rcp_today())

    elif not ADAPTIVE_READY:
        st.warning("Motor adaptativo V7.1 pendiente: ejecuta supabase_v7_1_adaptive.sql para activar check-in y ajustes dinámicos.")

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
            _week_info = active_plan_week_info(today_session.get("week_no"))
            _phase = _week_info.get("phase")
            st.caption(
                f"{workout_kind(today_session).upper()} · {status_label}"
                + (f" · Fase {_phase}" if _phase else "")
            )
            st.markdown(f"## {today_session['workout_name']}")
            st.markdown(f"**🎯 {today_session.get('target') or 'Por esfuerzo'}**")

            a, b, c, dcol = st.columns(4)
            a.metric("Distancia", f"{float(today_session.get('planned_km') or 0):g} km")
            b.metric("Semana", int(today_session.get("week_no") or 0))
            c.metric("Intensidad", str(today_session.get("intensity") or "—").title())
            dcol.metric("Estado", status_label.replace("✅ ", "").replace("🟡 ", "").replace("⏭️ ", "").replace("⏱️ ", "").replace("⚠️ ", ""))

            if str(today_session.get("adaptation_status") or "BASELINE").upper() != "BASELINE":
                base_km = float(today_session.get("baseline_planned_km") or today_session.get("planned_km") or 0)
                st.warning(
                    f"🧠 Sesión adaptada V7.1 · plan original {base_km:g} km → actual {float(today_session.get('planned_km') or 0):g} km."
                )

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

    # V7.1.1 · Coach después de la sesión: Home prioriza readiness → entrenamiento → adaptación.
    if ADAPTIVE_READY and selected_day == rcp_today() and coach is not None:
        decision = coach.get("decision")
        reasons = coach.get("reasons") or []
        metrics = coach.get("metrics") or {}
        st.markdown("### 🤖 Coach RCP")
        if decision == "PROTECT":
            st.error("Protección de carga recomendada: retirar intensidad y reducir temporalmente el volumen de los próximos 7 días.")
        elif decision == "REDUCE":
            st.warning("Descarga adaptativa recomendada para los próximos 7 días.")
        elif decision == "RESTORE":
            st.success("Los indicadores permiten restaurar las sesiones adaptadas hacia el plan original.")
        elif decision == "MAINTAIN":
            st.success("Mantener el plan previsto. No hay señales suficientes para modificar la próxima semana.")
        else:
            st.info("Recolectando datos para personalizar la adaptación.")
        if reasons:
            st.caption(" ".join(reasons))

        with st.expander("Ver indicadores del Coach", expanded=False):
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Adherencia 14 d", "—" if metrics.get("adherence_pct") is None else f"{metrics['adherence_pct']:.0f}%")
            m2.metric("Readiness 7 d", "—" if metrics.get("readiness_avg_7d") is None else f"{metrics['readiness_avg_7d']:.0f}/100")
            m3.metric("Exceso RPE", f"+{float(metrics.get('avg_rpe_excess') or 0):.1f}")
            m4.metric("Dolor post máx.", f"{int(metrics.get('max_post_pain') or 0)}/10")

        latest_applied = next((a for a in ADJUSTMENTS if str(a.get("status") or "").upper() == "APPLIED"), None)
        already_today = bool(
            latest_applied
            and str(latest_applied.get("trigger_date")) == rcp_today().isoformat()
            and str(latest_applied.get("decision") or "") == str(decision or "")
        )
        if decision in ("PROTECT", "REDUCE", "RESTORE"):
            if already_today:
                st.caption("Esta recomendación ya fue aplicada hoy. Los cambios quedan registrados en la auditoría V7.1.")
            else:
                if st.button("🧠 Aplicar adaptación a los próximos 7 días", type="primary", use_container_width=True):
                    ok, msg = apply_adaptation(coach, rcp_today())
                    (st.success if ok else st.error)(msg)
                    if ok:
                        st.rerun()

    # V7.2 · Replanificación de una sesión omitida explícitamente registrada.
    if REPLAN_READY and selected_day == rcp_today():
        replan = replan_snapshot(rcp_today())
        if replan:
            event = replan.get("event") or {}
            missed = event.get("session") or {}
            missed_day = event.get("date")
            metrics = replan.get("metrics") or {}
            st.markdown("### 🔄 Replanificación V7.2.2")
            with st.container(border=True):
                _planned_ahead = bool((replan.get("event") or {}).get("planned_ahead"))
                _event_label = "Ausencia planificada" if _planned_ahead else "Sesión perdida"
                st.caption(
                    f"{_event_label}: {missed_day.strftime('%d/%m') if missed_day else '—'} · "
                    f"{missed.get('workout_name') or '—'} · Motivo: {metrics.get('missed_reason') or 'No informado'}"
                )
                st.markdown(f"**{replan_decision_label(replan.get('decision'))}**")
                st.write(replan.get("summary") or "")
                st.caption(replan.get("explanation") or "")
                target = replan.get("target") or {}
                if target.get("date"):
                    existing_target = target.get("existing")
                    if existing_target:
                        st.info(
                            f"Hueco propuesto: {target['date'].strftime('%d/%m')} · sustituye "
                            f"{existing_target.get('workout_name') or 'la sesión prevista'}; no añade otra sesión."
                        )
                    else:
                        st.info(f"Hueco propuesto: {target['date'].strftime('%d/%m')} · día disponible sin sesión planificada.")

                decision = str(replan.get("decision") or "")
                if decision == "REASSESS":
                    c1, c2 = st.columns(2)
                    if c1.button("🧭 Ir a Evaluación", use_container_width=True, type="primary"):
                        set_page("Evaluación")
                        st.rerun()
                    if c2.button("✅ Registrar recomendación", use_container_width=True):
                        ok, msg = apply_replan(replan, rcp_today())
                        (st.success if ok else st.error)(msg)
                        if ok:
                            st.rerun()
                elif decision == "REVIEW_GOAL":
                    c1, c2 = st.columns(2)
                    if c1.button("🎯 Revisar objetivo", use_container_width=True, type="primary"):
                        set_page("Objetivo")
                        st.rerun()
                    if c2.button("✅ Registrar sin mover", use_container_width=True):
                        ok, msg = apply_replan(replan, rcp_today())
                        (st.success if ok else st.error)(msg)
                        if ok:
                            st.rerun()
                else:
                    if st.button("🔄 Aplicar propuesta V7.2", use_container_width=True, type="primary"):
                        ok, msg = apply_replan(replan, rcp_today())
                        (st.success if ok else st.error)(msg)
                        if ok:
                            st.rerun()
    elif ADAPTIVE_READY and not REPLAN_READY and selected_day == rcp_today():
        st.caption("🔄 Replanificación V7.2 pendiente de activar en Supabase.")

    # Resumen semanal
    st.markdown("### Esta semana")
    snap = week_snapshot(rcp_today())
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
        today_monday, _ = week_bounds(rcp_today())
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
        if (d := parse_date_safe(p.get("session_date"))) and d >= rcp_today()
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
    _week_sessions = [p for p in PLAN if monday <= (parse_date_safe(p.get("session_date")) or monday - timedelta(days=1)) <= sunday]
    if _week_sessions:
        _wi = active_plan_week_info(_week_sessions[0].get("week_no"))
        if _wi:
            title_col.caption(
                f"Fase {_wi.get('phase') or '—'} · Objetivo {_wi.get('target_km') or '—'} km · "
                f"Larga {_wi.get('long_km') or '—'} km"
            )
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

    current_monday, _ = week_bounds(rcp_today())
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

    # 7 · V7.1 Readiness + historial de adaptaciones
    if ADAPTIVE_READY:
        st.divider()
        st.markdown("## 🧠 Adaptación V7.1")
        readiness_values = []
        for r in sorted(READINESS_ROWS, key=lambda x: str(x.get("checkin_date"))):
            readiness_values.append({
                "Fecha": str(r.get("checkin_date")),
                "Readiness": int(r.get("readiness_score") or 0),
                "Estado": str(r.get("readiness_status") or ""),
            })
        if readiness_values:
            st.markdown("### Readiness diario")
            st.vega_lite_chart(
                {
                    "data": {"values": readiness_values},
                    "mark": {"type": "line", "point": True, "tooltip": True},
                    "encoding": {
                        "x": {"field": "Fecha", "type": "temporal", "title": None},
                        "y": {"field": "Readiness", "type": "quantitative", "scale": {"domain": [0, 100]}, "title": "0–100"},
                        "color": {"field": "Estado", "type": "nominal"},
                        "tooltip": [{"field": "Fecha", "type": "temporal"}, {"field": "Readiness"}, {"field": "Estado"}],
                    },
                    "height": 250,
                },
                use_container_width=True,
            )
        else:
            st.info("Haz check-ins desde 🏠 Hoy para activar la tendencia de readiness.")

        if ADJUSTMENTS:
            st.markdown("### Historial de ajustes")
            adj_rows = []
            for a in ADJUSTMENTS[:15]:
                changes = a.get("changes") or []
                adj_rows.append({
                    "Fecha": a.get("trigger_date"),
                    "Decisión": a.get("decision"),
                    "Severidad": a.get("severity") or "—",
                    "Sesiones": len(changes) if isinstance(changes, list) else 0,
                    "Estado": a.get("status"),
                })
            st.dataframe(adj_rows, use_container_width=True, hide_index=True)
            latest_applied = next((a for a in ADJUSTMENTS if str(a.get("status") or "").upper() == "APPLIED"), None)
            if latest_applied:
                if st.button("↩️ Revertir última adaptación aplicada", use_container_width=True):
                    ok, msg = revert_last_adaptation()
                    (st.success if ok else st.error)(msg)
                    if ok:
                        st.rerun()


    # 8 · V7.2 Replanificación
    if REPLAN_READY:
        st.divider()
        st.markdown("## 🔄 Replanificación V7.2.2")
        if REPLANS:
            rows = []
            for r in REPLANS[:20]:
                changes = r.get("changes") or []
                rows.append({
                    "Fecha detonante": r.get("trigger_date"),
                    "Decisión": replan_decision_label(r.get("decision")),
                    "Cambios": len(changes) if isinstance(changes, list) else 0,
                    "Estado": r.get("status"),
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
            latest = next((r for r in REPLANS if str(r.get("status") or "").upper() == "APPLIED"), None)
            if latest:
                if st.button("↩️ Revertir última replanificación", use_container_width=True):
                    ok, msg = revert_last_replan()
                    (st.success if ok else st.error)(msg)
                    if ok:
                        st.rerun()
        else:
            st.info("Todavía no hay replanificaciones. Se crean cuando una sesión se registra como OMITIDA —incluidas ausencias futuras conocidas— y V7.2.2 propone una acción.")


# ============================================================
# 🗓️ PLAN
# ============================================================
elif current_page == "Plan":
    st.subheader("🗓️ Mi plan")
    _plan_engine = str((ACTIVE_PLAN or {}).get("engine_version") or "—")
    _plan_meta = (ACTIVE_PLAN or {}).get("metadata") or {}
    st.caption(
        f"Motor {_plan_engine} · "
        f"{', '.join(_plan_meta.get('selected_days') or []) if _plan_meta.get('selected_days') else 'distribución legacy'} · "
        f"abre una sesión para revisar su detalle."
    )

    # V7.2.3 · La reparación del hueco inicial también es visible directamente en Mi plan.
    render_timezone_plan_repair("plan")

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
            "Entrenamiento": session_display_name(p),
            "KM": float(p.get("planned_km") or 0),
            "KM base": float(p.get("baseline_planned_km") or p.get("planned_km") or 0) if ADAPTIVE_READY else float(p.get("planned_km") or 0),
            "Adaptación": str(p.get("adaptation_status") or "BASELINE").title() if ADAPTIVE_READY else "—",
            "Replanificación": str(p.get("replan_status") or "BASELINE").replace("_", " ").title() if REPLAN_READY else "—",
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
            if REPLAN_READY and str(p.get("replan_status") or "BASELINE").upper() != "BASELINE":
                st.info(f"🔄 Replanificada V7.2 · {str(p.get('replan_status') or '').replace('_', ' ').title()}")
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
            if (d := parse_date_safe(p.get("session_date"))) and d >= rcp_today()
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
            st.markdown(f"## {session_display_name(session)}")
            r1, r2, r3 = st.columns(3)
            r1.metric("Plan", f"{float(session.get('planned_km') or 0):g} km")
            r2.metric("Objetivo", str(session.get("target") or "Por esfuerzo"))
            r3.metric("Estado", status_label_for_date(selected_day).split(" ", 1)[-1])
            with st.expander("📋 Instrucciones"):
                st.write(session.get("description") or "Sin instrucciones adicionales.")

        if existing and str(existing.get("status") or "").upper() == "OMITIDO" and selected_day > rcp_today():
            st.warning(f"📅 Ausencia planificada para {selected_day.strftime('%d/%m/%Y')}. Puedes cancelarla antes de esa fecha.")
            if st.button("↩️ Cancelar ausencia planificada", type="primary", use_container_width=True, key=f"cancel_planned_absence_{selected_day.isoformat()}"):
                ok, msg = cancel_planned_absence(existing, session)
                (st.success if ok else st.error)(msg)
                if ok:
                    st.session_state["rcp_saved_notice"] = msg
                    st.rerun()

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

            if ADAPTIVE_READY:
                st.markdown("#### Recuperación post-sesión")
                a1, a2 = st.columns(2)
                post_pain = a1.slider("Dolor después de entrenar", 0, 10, int(existing.get("post_pain") or 0))
                post_fatigue = a2.slider("Fatiga después de entrenar", 1, 5, int(existing.get("post_fatigue") or 2))
                difficulty_options = ["Mucho más fácil", "Más fácil", "Como esperaba", "Más difícil", "Mucho más difícil"]
                current_difficulty = str(existing.get("perceived_difficulty") or "Como esperaba")
                perceived_difficulty = st.selectbox(
                    "La sesión se sintió…",
                    difficulty_options,
                    index=difficulty_options.index(current_difficulty) if current_difficulty in difficulty_options else 2,
                )
            else:
                post_pain = None
                post_fatigue = None
                perceived_difficulty = None

            status_options = ["COMPLETADO", "MODIFICADO", "OMITIDO"]
            current_status = str(existing.get("status") or "COMPLETADO").upper()
            status = st.selectbox(
                "Estado",
                status_options,
                index=status_options.index(current_status) if current_status in status_options else 0,
            )
            if ADAPTIVE_READY:
                missed_options = ["—", "Falta de tiempo", "Fatiga", "Dolor/molestia", "Enfermedad", "Viaje", "Otro"]
                current_missed = str(existing.get("missed_reason") or "—")
                missed_reason = st.selectbox(
                    "Si la omitiste, motivo",
                    missed_options,
                    index=missed_options.index(current_missed) if current_missed in missed_options else 0,
                )
            else:
                missed_reason = "—"
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
                    "post_pain": int(post_pain) if ADAPTIVE_READY and status != "OMITIDO" else None,
                    "post_fatigue": int(post_fatigue) if ADAPTIVE_READY and status != "OMITIDO" else None,
                    "perceived_difficulty": perceived_difficulty if ADAPTIVE_READY and status != "OMITIDO" else None,
                    "missed_reason": (missed_reason if ADAPTIVE_READY and status == "OMITIDO" and missed_reason != "—" else None),
                    "notes": notes.strip(),
                })
                if status == "OMITIDO" and REPLAN_READY:
                    if selected_day > rcp_today():
                        st.session_state["rcp_saved_notice"] = (
                            f"Ausencia planificada del {selected_day.strftime('%d/%m')} guardada ✅. "
                            "V7.2.2 ya puede evaluarla desde hoy."
                        )
                    else:
                        st.session_state["rcp_saved_notice"] = (
                            f"Sesión del {selected_day.strftime('%d/%m')} marcada como OMITIDA ✅. "
                            "V7.2.2 evaluará si conviene replanificarla sin acumular carga."
                        )
                    set_page("Hoy", rcp_today())
                else:
                    st.session_state["rcp_saved_notice"] = "Entrenamiento guardado ✅"
                    set_page("Hoy", selected_day)
                st.rerun()

        if existing:
            st.divider()
            st.caption("Puedes eliminar un registro erróneo. Para una ausencia futura usa ‘Cancelar ausencia planificada’. ")
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
    "RunningCoachPro genera orientación general de entrenamiento. El Readiness Score y las decisiones adaptativas V7.1 "
    "son heurísticas internas de apoyo al entrenamiento, no escalas médicas validadas. No sustituye evaluación médica "
    "ni coaching individual. Ante dolor agudo, mareos, lesión o síntomas anormales, suspende el ejercicio y busca orientación profesional."
)
