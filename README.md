# Mi Running Coach

Aplicación sencilla hecha con Python + Streamlit para generar el entrenamiento de running del día.

## Cómo ejecutarla

1. Instala Python 3.10 o superior.
2. Abre una terminal dentro de esta carpeta.
3. Instala las dependencias:

   pip install -r requirements.txt

4. Ejecuta la app:

   streamlit run app.py

Se abrirá automáticamente en tu navegador.

## Qué incluye esta primera versión

- Objetivo: 5K, 10K, 21K, 42K o condición física.
- Nivel: principiante, intermedio o avanzado.
- Días de carrera por semana.
- Kilometraje semanal actual.
- Generación automática de:
  - rodaje suave,
  - fartlek,
  - tempo,
  - intervalos,
  - tirada larga,
  - descanso.
- Botones para indicar si el entrenamiento fue muy fácil o muy difícil.
- Botón para marcar la sesión del día como completada.

## Importante

Esta primera versión guarda los datos solo mientras la sesión de Streamlit está abierta.
El siguiente paso natural es agregar una base de datos para guardar historial y progreso.
