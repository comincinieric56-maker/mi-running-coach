# RunningCoachPro V3

V3 construida directamente desde `RunningCoachPro_Sep_Nov_2026.xlsx`.

## Novedades

- Guardado permanente con Supabase.
- PIN de acceso para proteger una app pública de Streamlit.
- Comparación PLAN vs REAL.
- KM semanales planificados vs reales.
- RPE promedio semanal.
- Semáforo de carga (verde / amarillo / rojo).
- Estados: COMPLETADO, MODIFICADO y OMITIDO.
- El rodaje opcional omitido no penaliza el plan y no se recupera otro día.
- Exportación de respaldo CSV.
- Conserva las 58 sesiones y las zonas del Excel.

## Archivos

- `app.py`: reemplaza el app.py actual.
- `requirements.txt`: reemplaza el actual.
- `supabase_setup.sql`: ejecutar una vez en el SQL Editor de Supabase.
- `secrets_example.toml`: ejemplo de los Secrets de Streamlit.
- `.gitignore`: evita subir secretos locales por accidente.

## Seguridad

NO pongas la clave `sb_secret_...` dentro de app.py ni la subas a GitHub.
Guárdala únicamente en los Secrets de Streamlit.

## Si todavía no configuras Supabase

La app arranca igualmente en "modo temporal", para que puedas comprobar que
la interfaz funciona. Cuando añadas Supabase, el guardado será permanente.
