import plotly.graph_objects as go
import pandas as pd

def generar_barras_temporal(df_temporadas, año, municipio, temporada, mes, cultivo):
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

    # Filtrar los datos según los parámetros proporcionados
    if año:
        df_temporadas = df_temporadas[df_temporadas['año'] == int(año)]
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

    # Ordenar los meses según el mapeo de meses_ordenados
    df_agrupado['mes_num'] = df_agrupado['mes'].map(meses_ordenados)
    df_agrupado = df_agrupado.sort_values(by='mes_num')

    # Eliminar la columna auxiliar 'mes_num'
    df_agrupado = df_agrupado.drop(columns=['mes_num'])

    # Crear un título dinámico
    title_parts = ['Gráfico de Barras por Mes']
    if año:
        title_parts.append(f"Año: {año}")
    if municipio:
        title_parts.append(f"Municipio: {municipio}")
    if temporada:
        title_parts.append(f"Temporada: {temporada}")
    if mes:
        title_parts.append(f"Mes: {mes}")
    if cultivo:
        title_parts.append(f"Cultivo: {cultivo}")
    
    title = " - ".join(title_parts)

    # Crear el gráfico de barras
    fig = go.Figure(data=[go.Bar(
        x=df_agrupado['mes'],
        y=df_agrupado['sembrada'],
        text=df_agrupado['sembrada'],
        textposition='auto',
        marker=dict(color='royalblue')
    )])

    fig.update_layout(
        title=title,
        xaxis_title='Mes',
        yaxis_title='Sembrada',
        template='plotly_white',
        showlegend=False,
        width=900,
        height=500,
    )

    # Generar el gráfico como HTML
    graph_html = fig.to_html(full_html=False)

    return graph_html, None
