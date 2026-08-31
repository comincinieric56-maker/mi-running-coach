# RunningCoachPro V6 Multiusuario

La misma URL puede ser usada por muchas personas, pero cada una tiene:

- cuenta propia,
- perfil propio,
- objetivo propio,
- plan propio,
- registros propios,
- gráficos propios.

## Seguridad

La V6 usa Supabase Auth + Row Level Security (RLS).
Las tablas están filtradas por `auth.uid() = user_id`, por lo que cada usuario
solo puede consultar/modificar sus propias filas.

## Instalación / actualización

1. En Supabase -> SQL Editor ejecuta `supabase_v6_multiuser.sql`.
2. En Supabase -> Settings -> API Keys copia la Publishable key.
3. En Streamlit -> Manage app -> Settings -> Secrets añade:

   SUPABASE_URL = "https://....supabase.co"
   SUPABASE_PUBLISHABLE_KEY = "sb_publishable_..."
   APP_URL = "https://runningcoachpro.streamlit.app"

4. Reemplaza `app.py` y `requirements.txt` en GitHub.
5. Haz Commit changes.
6. Streamlit redeployará automáticamente.

## Auth

Supabase suele exigir confirmación por email en proyectos alojados.
Configura en Supabase Authentication la Site URL como:

https://runningcoachpro.streamlit.app

y añade la misma URL a Redirect URLs.

## Tu plan anterior

`migrar_plan_personal_v5.sql` es opcional. Permite copiar el plan original
Sep-Nov 2026 y los registros de V5 a tu nueva cuenta V6.

Primero crea tu cuenta V6. Luego busca tu UUID en:

Supabase -> Authentication -> Users

y reemplaza `PASTE_YOUR_USER_UUID_HERE` dentro del SQL antes de ejecutarlo.

## Importante

La planificación automática es una orientación general. No sustituye
evaluación médica o coaching individual.
