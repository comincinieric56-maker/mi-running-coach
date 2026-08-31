-- ==========================================================
-- OPCIONAL: migrar el plan personal V5 al usuario V6
-- ==========================================================
-- 1) Primero crea tu cuenta en RunningCoachPro V6.
-- 2) En Supabase -> Authentication -> Users copia TU UUID.
-- 3) Sustituye PASTE_YOUR_USER_UUID_HERE en las 2 líneas siguientes.
-- 4) Ejecuta el script.
--
-- IMPORTANTE: este script es SOLO para el dueño del plan original.

do $$
declare
    v_user uuid := 'PASTE_YOUR_USER_UUID_HERE'::uuid;
begin
    insert into public.rc_profiles (
        user_id, display_name, goal, level, days_per_week, weekly_km,
        has_race, race_date, target_time_sec, current_distance_km,
        current_time_sec, updated_at
    )
    values (
        v_user, 'ERIC', '21K', 'Intermedio', 5, 42,
        true, '2026-11-29'::date, 6432, 21.1, 6593, now()
    )
    on conflict (user_id) do update set
        display_name = excluded.display_name,
        goal = excluded.goal,
        level = excluded.level,
        days_per_week = excluded.days_per_week,
        weekly_km = excluded.weekly_km,
        has_race = excluded.has_race,
        race_date = excluded.race_date,
        target_time_sec = excluded.target_time_sec,
        current_distance_km = excluded.current_distance_km,
        current_time_sec = excluded.current_time_sec,
        updated_at = now();

    delete from public.rc_workout_logs where user_id = v_user;
    delete from public.rc_plan_sessions where user_id = v_user;

    insert into public.rc_plan_sessions (
        user_id, session_date, week_no, workout_type, workout_name,
        planned_km, target, intensity, description, is_optional
    )
    select
        v_user, x.session_date, x.week_no, x.workout_type, x.workout_name,
        x.planned_km, x.target, x.intensity, x.description, x.is_optional
    from (
        values
        ('2026-09-01'::date,1,'SERIES','6 x 600 m',8.0,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 6 x 600 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-09-03'::date,1,'TEMPO','TEMPO 5 KM',8.0,'4:55-5:00 min/km','MEDIA-ALTA','5 km tempo controlado + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-09-04'::date,1,'RODAJE','RODAJE OPCIONAL POSTURNO 6 KM',6.0,'6:12-6:31 min/km','OPCIONAL','6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-09-06'::date,1,'LARGA','TIRADA LARGA 14 KM',14.0,'5:52-6:08 min/km','MEDIA','14 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',false),
('2026-09-08'::date,2,'SERIES','5 x 800 m',8.5,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 5 x 800 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-09-10'::date,2,'TEMPO','TEMPO 6 KM',9.0,'4:55-5:00 min/km','MEDIA-ALTA','6 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-09-11'::date,2,'RODAJE','RODAJE OPCIONAL POSTURNO 6 KM',6.0,'6:12-6:31 min/km','OPCIONAL','6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-09-12'::date,2,'FUERZA','FUERZA B + MOVILIDAD',0.0,'NO APLICA','MEDIA','SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',false),
('2026-09-13'::date,2,'LARGA','TIRADA LARGA 16 KM',16.0,'5:52-6:08 min/km','MEDIA','16 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',false),
('2026-09-15'::date,3,'SERIES','6 x 800 m',9.5,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 6 x 800 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-09-17'::date,3,'TEMPO','2 x 4 KM UMBRAL',11.0,'4:55-5:00 min/km','MEDIA-ALTA','2 x 4 km + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-09-18'::date,3,'RODAJE','RODAJE OPCIONAL POSTURNO 6 KM',6.0,'6:12-6:31 min/km','OPCIONAL','6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-09-20'::date,3,'LARGA','TIRADA LARGA 18 KM',18.0,'5:52-6:08 min/km','MEDIA','18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 3 KM PROGRESIVOS SIN SUPERAR RPE 7.',false),
('2026-09-22'::date,4,'SERIES','10 x 400 m',8.0,'4:29-4:37 min/km','ALTA','CALENTAMIENTO + 10 x 400 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-09-24'::date,4,'TEMPO','TEMPO 5 KM',8.0,'4:55-5:00 min/km','MEDIA-ALTA','5 km tempo controlado + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-09-25'::date,4,'RODAJE','RODAJE OPCIONAL POSTURNO 6 KM',6.0,'6:12-6:31 min/km','OPCIONAL','6 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-09-26'::date,4,'FUERZA','FUERZA B + MOVILIDAD',0.0,'NO APLICA','MEDIA','SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',false),
('2026-09-27'::date,4,'LARGA','TIRADA LARGA 15 KM',15.0,'5:52-6:08 min/km','MEDIA','15 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',false),
('2026-09-29'::date,5,'SERIES','5 x 1000 m',9.5,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 5 x 1000 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-10-01'::date,5,'TEMPO','TEMPO 7 KM',10.0,'4:55-5:00 min/km','MEDIA-ALTA','7 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-10-02'::date,5,'RODAJE','RODAJE OPCIONAL POSTURNO 7 KM',7.0,'6:12-6:31 min/km','OPCIONAL','7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-10-04'::date,5,'LARGA','TIRADA LARGA 18 KM',18.0,'5:52-6:08 min/km','MEDIA','18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',false),
('2026-10-06'::date,6,'SERIES','6 x 1000 m',10.5,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 6 x 1000 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-10-08'::date,6,'TEMPO','2 x 4 KM UMBRAL',11.0,'4:55-5:00 min/km','MEDIA-ALTA','2 x 4 km + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-10-09'::date,6,'RODAJE','RODAJE OPCIONAL POSTURNO 7 KM',7.0,'6:12-6:31 min/km','OPCIONAL','7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-10-10'::date,6,'FUERZA','FUERZA B + MOVILIDAD',0.0,'NO APLICA','MEDIA','SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',false),
('2026-10-11'::date,6,'LARGA','TIRADA LARGA 20 KM',20.0,'5:52-6:08 min/km','MEDIA','20 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 4 KM PROGRESIVOS HASTA RITMO MODERADO.',false),
('2026-10-13'::date,7,'SERIES','4 x 1200 m',9.5,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 4 x 1200 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-10-15'::date,7,'TEMPO','TEMPO 8 KM',11.0,'4:55-5:00 min/km','MEDIA-ALTA','8 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-10-16'::date,7,'RODAJE','RODAJE OPCIONAL POSTURNO 7 KM',7.0,'6:12-6:31 min/km','OPCIONAL','7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-10-18'::date,7,'LARGA','TIRADA LARGA 16 KM',16.0,'5:52-6:08 min/km','MEDIA','16 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',false),
('2026-10-20'::date,8,'SERIES','5 x 1200 m',10.5,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 5 x 1200 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-10-22'::date,8,'TEMPO','3 x 3 KM UMBRAL',12.0,'4:55-5:00 min/km','MEDIA-ALTA','3 x 3 km + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-10-23'::date,8,'RODAJE','RODAJE OPCIONAL POSTURNO 7 KM',7.0,'6:12-6:31 min/km','OPCIONAL','7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-10-24'::date,8,'FUERZA','FUERZA B + MOVILIDAD',0.0,'NO APLICA','MEDIA','SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',false),
('2026-10-25'::date,8,'LARGA','TIRADA LARGA 21 KM',21.0,'5:52-6:08 min/km','MEDIA','21 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 5 KM PROGRESIVOS SIN ENTRAR EN UMBRAL.',false),
('2026-10-27'::date,9,'SERIES','8 x 600 m',9.0,'4:29-4:37 min/km','ALTA','CALENTAMIENTO + 8 x 600 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-10-29'::date,9,'TEMPO','TEMPO 9 KM',12.0,'4:55-5:00 min/km','MEDIA-ALTA','9 km tempo continuo + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-10-30'::date,9,'RODAJE','RODAJE OPCIONAL POSTURNO 7 KM',7.0,'6:12-6:31 min/km','OPCIONAL','7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-11-01'::date,9,'LARGA','TIRADA LARGA 18 KM',18.0,'5:52-6:08 min/km','MEDIA','18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',false),
('2026-11-03'::date,10,'SERIES','6 x 1000 m',10.5,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 6 x 1000 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-11-05'::date,10,'TEMPO','2 x 5 KM UMBRAL',13.0,'4:55-5:00 min/km','MEDIA-ALTA','2 x 5 km + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-11-06'::date,10,'RODAJE','RODAJE OPCIONAL POSTURNO 7 KM',7.0,'6:12-6:31 min/km','OPCIONAL','7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-11-08'::date,10,'LARGA','TIRADA LARGA 22 KM',22.0,'5:52-6:08 min/km','MEDIA','22 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 4 KM A ESFUERZO STEADY CONTROLADO.',false),
('2026-11-10'::date,11,'SERIES','3 x 1600 m',10.0,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 3 x 1600 m a ritmo controlado de 10K + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-11-12'::date,11,'TEMPO','BLOQUE ESPECÍFICO MM',11.0,'5:05 min/km','MEDIA-ALTA','3 km suaves + 6 km ritmo MM objetivo + 2 km suaves + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-11-13'::date,11,'RODAJE','RODAJE OPCIONAL POSTURNO 7 KM',7.0,'6:12-6:31 min/km','OPCIONAL','7 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-11-14'::date,11,'FUERZA','FUERZA B + MOVILIDAD',0.0,'NO APLICA','MEDIA','SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',false),
('2026-11-15'::date,11,'LARGA','TIRADA LARGA 18 KM',18.0,'5:52-6:08 min/km','MEDIA','18 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. ÚLTIMOS 5 KM CERCA DE RITMO MM OBJETIVO (5:05 MIN/KM) SOLO SI LAS SENSACIONES SON BUENAS.',false),
('2026-11-17'::date,12,'SERIES','5 x 800 m',8.0,'4:42-4:49 min/km','ALTA','CALENTAMIENTO + 5 x 800 m + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-11-19'::date,12,'TEMPO','TEMPO 5 KM',8.0,'4:55-5:00 min/km','MEDIA-ALTA','5 km umbral controlado + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-11-20'::date,12,'RODAJE','RODAJE OPCIONAL POSTURNO 5 KM',5.0,'6:12-6:31 min/km','OPCIONAL','5 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-11-22'::date,12,'LARGA','TIRADA LARGA 14 KM',14.0,'5:52-6:08 min/km','MEDIA','14 KM EN RUTA HABITUAL CON APROXIMADAMENTE 157 M D+. TODO EL RECORRIDO EN ZONA AERÓBICA CONTROLADA.',false),
('2026-11-24'::date,13,'SERIES','6 x 400 m',6.5,'4:29-4:37 min/km','ALTA','CALENTAMIENTO + 6 x 400 m ágiles sin máximo esfuerzo + RECUPERACIONES + ENFRIAMIENTO + FUERZA A',false),
('2026-11-26'::date,13,'TEMPO','ACTIVACIÓN MM',6.0,'5:05 min/km','MEDIA-ALTA','2 km suaves + 3 km ritmo MM + 1 km suave + TRABAJO COMPLEMENTARIO DE FUERZA',false),
('2026-11-27'::date,13,'RODAJE','RODAJE OPCIONAL POSTURNO 5 KM',5.0,'6:12-6:31 min/km','OPCIONAL','5 KM MUY SUAVES. SESIÓN OPCIONAL CONDICIONADA AL DESCANSO POSTURNO.',false),
('2026-11-28'::date,13,'FUERZA','FUERZA B + MOVILIDAD',0.0,'NO APLICA','MEDIA','SEGUNDA EXPOSICIÓN SEMANAL DE FUERZA EN LAS SEMANAS CON SÁBADO PROGRAMADO',false),
('2026-11-29'::date,13,'LARGA','MEDIA MARATÓN OBJETIVO 21.1 KM',21.0975,'5:05 min/km','COMPETENCIA','MEDIA MARATÓN OBJETIVO. SALIDA CONTROLADA Y PROGRESIÓN POR ESFUERZO.',false)
    ) as x(
        session_date, week_no, workout_type, workout_name,
        planned_km, target, intensity, description, is_optional
    );

    -- Copiar los registros existentes de la tabla V5 si existen.
    if to_regclass('public.runningcoach_logs') is not null then
        insert into public.rc_workout_logs (
            user_id, session_date, plan_session_id,
            actual_km, actual_duration_sec, rpe, avg_hr, max_hr,
            status, notes, updated_at
        )
        select
            v_user,
            old.session_date,
            p.id,
            old.actual_km,
            old.actual_duration_sec,
            old.rpe,
            old.avg_hr,
            old.max_hr,
            old.status,
            old.notes,
            coalesce(old.updated_at, now())
        from public.runningcoach_logs old
        left join public.rc_plan_sessions p
          on p.user_id = v_user and p.session_date = old.session_date
        where old.runner = 'ERIC'
        on conflict (user_id, session_date) do update set
            plan_session_id = excluded.plan_session_id,
            actual_km = excluded.actual_km,
            actual_duration_sec = excluded.actual_duration_sec,
            rpe = excluded.rpe,
            avg_hr = excluded.avg_hr,
            max_hr = excluded.max_hr,
            status = excluded.status,
            notes = excluded.notes,
            updated_at = excluded.updated_at;
    end if;
end $$;
