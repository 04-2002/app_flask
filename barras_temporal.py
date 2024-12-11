import plotly.graph_objects as go
import pandas as pd

def generar_barras_temporal(df_temporadas, anio, municipio, temporada, mes, cultivo):
    # Mapeo de los meses como cadenas a números (1 = enero, 2 = febrero, etc.)
    meses_ordenados = {
        'Enero': 1,
        'Febrero': 2,
        'Marzo': 3,
        'Abril': 4,
        'Mayo': 5,
        'Junio': 6,
        'Julio': 7,
        'Agosto': 8,
        'Septiembre': 9,
        'Octubre': 10,
        'Noviembre': 11,
        'Diciembre': 12
    }

    # Mapeo de meses a temporadas (ejemplo, ajustar según tus datos)
    meses_a_temporadas = {
        'Enero': 'Norte',
        'Febrero': 'Norte',
        'Marzo': 'Seca',
        'Abril': 'Seca',
        'Mayo': 'Seca',
        'Junio': 'Temporal',
        'Julio': 'Temporal',
        'Agosto': 'Temporal',
        'Septiembre': 'Temporal',
        'Octubre': 'Norte',
        'Noviembre': 'Norte',
        'Diciembre': 'Norte'
    }

    # Filtrar los datos según los parámetros proporcionados
    if anio:
        df_temporadas['anio'] = df_temporadas['anio'].astype(int)
        df_temporadas = df_temporadas[df_temporadas['anio'] == int(anio)]

    if municipio:
        df_temporadas = df_temporadas[df_temporadas['municipio'] == municipio]
    if temporada:
        df_temporadas = df_temporadas[df_temporadas['temporada'] == temporada]
    if mes:
        df_temporadas = df_temporadas[df_temporadas['mes'] == str(mes)]
    if cultivo:
        df_temporadas = df_temporadas[df_temporadas['nomcultivo'] == cultivo]

    # Verificar si hay datos filtrados
    if df_temporadas.empty:
        return None, "No se encontraron datos para generar el gráfico."

    # Asegurarse de que la columna de los valores numéricos esté presente
    if 'sembrada' not in df_temporadas.columns:
        return None, "La columna 'sembrada' no se encuentra en los datos."

    # Agrupar por mes y obtener la suma de la columna 'sembrada'
    df_agrupado = df_temporadas.groupby('mes')['sembrada'].sum().reset_index()

    # Añadir la columna de temporada en función del mes
    df_agrupado['temporada'] = df_agrupado['mes'].map(meses_a_temporadas)

    # Ordenar los meses según el mapeo de meses_ordenados
    df_agrupado['mes_num'] = df_agrupado['mes'].map(meses_ordenados)
    df_agrupado = df_agrupado.sort_values(by='mes_num')

    # Eliminar la columna auxiliar 'mes_num'
    df_agrupado = df_agrupado.drop(columns=['mes_num'])

    # Obtener el valor total (último valor del mes de la temporada)
    if not df_agrupado.empty:
        total_ultimo_mes = df_agrupado.iloc[-1]['sembrada']
    else:
        total_ultimo_mes = 0

    # Crear un título dinámico
    title_parts = ['']
    if anio:
        title_parts.append(f"Año: {anio} |")
    if municipio:
        title_parts.append(f"Municipio: {municipio} |")
    if temporada:
        title_parts.append(f"Temporada: {temporada} |")
    if cultivo:
        title_parts.append(f"Cultivo: {cultivo}")
    
    info = "  ".join(title_parts)

    # Título principal
    titulo = "Cultivos de la Zona Ríos del Estado de Tabasco"

    # Crear el gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=df_agrupado['mes'],
        y=df_agrupado['sembrada'],
        text=df_agrupado['sembrada'],
        textposition='auto',
        marker=dict(color='#2F4F4F'),  # Color de las barras
        customdata=df_agrupado['temporada'],  # Asignar temporada como datos personalizados
        hovertemplate=(
            "<b>Mes:</b> %{x}<br>"
            "<b>Hectáreas Sembradas:</b> %{y}<br>"
            "<b>Temporada:</b> %{customdata}<br>"
            "<extra></extra>"  # Eliminar el texto adicional que aparece por defecto
        )
    )])

    # Encontrar el valor máximo de las barras
    max_value = df_agrupado['sembrada'].max()

    # Añadir la anotación con el total al final de la temporada (sin la flecha)
    fig.update_layout(
        title=f"<b>{titulo}</b><br><span style='font-size:12px'>{info}</span><br><span style='font-size:11px; color: rgba(255, 0, 0, 0.5);'>*Seguimiento de cultivos presentes en el año</span><br>",
        xaxis_title='Mes',
        yaxis_title='Hectáreas Sembradas',
        template='ggplot2',
        width=900,
        height=500,
        annotations=[dict(
            x=df_agrupado['mes'].iloc[-1],  # Último mes
            y=max_value + (max_value * 0.1),  # Colocar la anotación un 10% por encima del valor máximo
            text=f"Total de la temporada: {total_ultimo_mes} ha",
            font=dict(
                size=12,
                color='rgba(255, 0, 0, 0.5)'
            ),
            align='center',
            bgcolor='white',
            bordercolor='rgba(255, 0, 0, 0.5)',
            borderwidth=1,
            showarrow=False  # No se muestra la flecha
        )]
    )

    # Generar el gráfico como HTML
    graph_html = fig.to_html(full_html=False)

    return graph_html, None
