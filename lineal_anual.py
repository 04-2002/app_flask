import pandas as pd
import plotly.express as px
import plotly.io as pio

def generar_lineal_anual(df, año_min=None, año_max=None, municipio=None, ciclo_productivo=None, modalidad=None, cultivo=None):
    # Filtrar el DataFrame según los parámetros proporcionados
    filtered_df = df.copy()

    if año_min and año_max:
        filtered_df = filtered_df[(filtered_df['Anio'] >= año_min) & (filtered_df['Anio'] <= año_max)]
    elif año_min:
        filtered_df = filtered_df[filtered_df['Anio'] == año_min]

    if municipio:
        filtered_df = filtered_df[filtered_df['Nommunicipio'] == municipio]

    if ciclo_productivo and ciclo_productivo != 'Año agrícola (OI-PV)' and ciclo_productivo != 'Cíclicos y Perennes':
        filtered_df = filtered_df[filtered_df['Nomcicloproductivo'] == ciclo_productivo]

    if modalidad and modalidad != 'Riego + Temporal':
        filtered_df = filtered_df[filtered_df['Nommodalidad'] == modalidad]

    if cultivo:
        filtered_df = filtered_df[filtered_df['Nomcultivo'] == cultivo]

    # Agrupar los datos por año, cultivo y sumar las hectáreas sembradas
    grouped_df = filtered_df.groupby(['Anio', 'Nomcultivo'], as_index=False)['Sembrada'].sum()

    # Comprobar si el DataFrame tiene valores antes de proceder a graficar
    if grouped_df.empty:
        return "No hay datos para mostrar con los filtros aplicados"

    # Crear el gráfico de líneas con las etiquetas de cultivo
    fig = px.line(grouped_df, 
                 x='Anio', 
                 y='Sembrada', 
                 color='Nomcultivo',  # Etiquetas para las líneas (solo el cultivo)
                 title="Variación de Cultivos",
                 labels={'Anio': 'Año', 'Sembrada': 'Hectáreas Sembradas', 'Nomcultivo': 'Cultivo'},
                 line_shape='linear',
                 markers=True,
                 width=900,
                 height=500,
    )


    # Devolver el gráfico en HTML
    graph_html = pio.to_html(fig, full_html=False)

    return graph_html
