-- RunningCoachPro V3
-- Ejecuta este script UNA VEZ en Supabase > SQL Editor.

create table if not exists public.runningcoach_logs (
    runner text not null,
    session_date date not null,
    week_plan integer,
    workout_type text,
    workout_name text,
    planned_km numeric(7,2),
    actual_km numeric(7,2),
    actual_duration_sec integer,
    rpe integer check (rpe between 1 and 10),
    avg_hr integer,
    max_hr integer,
    status text not null default 'COMPLETADO'
        check (status in ('COMPLETADO', 'MODIFICADO', 'OMITIDO')),
    notes text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    primary key (runner, session_date)
);

create index if not exists runningcoach_logs_week_idx
    on public.runningcoach_logs (runner, week_plan);

-- La app usa una clave SECRETA desde el servidor Streamlit.
-- No damos acceso a anon ni authenticated.
alter table public.runningcoach_logs enable row level security;

revoke all on table public.runningcoach_logs from anon, authenticated;
grant select, insert, update, delete on table public.runningcoach_logs to service_role;
