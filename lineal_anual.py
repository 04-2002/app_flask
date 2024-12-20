import pandas as pd
import plotly.express as px
import plotly.io as pio


def generar_lineal_anual(df, año_min=None, año_max=None, municipio=None, ciclo_productivo=None, modalidad=None, cultivo=None):
    # Filtrar el DataFrame según los parámetros proporcionados
    filtered_df = df.copy()
    filtros = []

    # Generar filtros dinámicos
    if ciclo_productivo:
        if ciclo_productivo == "Año agrícola (OI-PV)":
            filtros.append("Ciclo: Año agrícola (OI + PV)")
        elif ciclo_productivo == "Cíclicos y Perennes":
            filtros.append("Cíclicos y Perennes")
        else:
            filtros.append(f"Ciclo: {ciclo_productivo}")

    if modalidad:
        filtros.append(f"Modalidad: {modalidad}")
    if cultivo and cultivo != "Resumen cultivos":
        filtros.append(f"Cultivo: {cultivo}")
    if municipio:
        filtros.append(f"Municipio: {municipio if municipio != 'Todos (Separados)' else 'Todos'}")

    # Crear título dinámico
    info = " | ".join(filtros)
    titulo = "Cultivos de la Zona Ríos del Estado de Tabasco"

    # Aplicar filtros al DataFrame
    if año_min and año_max:
        filtered_df = filtered_df[(filtered_df['Anio'] >= año_min) & (filtered_df['Anio'] <= año_max)]
    elif año_min:
        filtered_df = filtered_df[filtered_df['Anio'] == año_min]

    if ciclo_productivo and ciclo_productivo not in ['Año agrícola (OI-PV)', 'Cíclicos y Perennes']:
        filtered_df = filtered_df[filtered_df['Nomcicloproductivo'] == ciclo_productivo]

    if modalidad and modalidad != 'Riego + Temporal':
        filtered_df = filtered_df[filtered_df['Nommodalidad'] == modalidad]

    if cultivo and cultivo != "Resumen cultivos":
        filtered_df = filtered_df[filtered_df['Nomcultivo'] == cultivo]

    if municipio == 'Todos (Separados)':
        grouped_df = filtered_df.groupby(['Anio', 'Nommunicipio', 'Nomcultivo'], as_index=False)['Sembrada'].sum()

    
        if grouped_df.empty:
            return "No hay datos para mostrar con los filtros aplicados"

        fig = px.line(
            grouped_df,
            x='Anio',
            y='Sembrada',
            color='Nommunicipio',
            title=f"<b>{titulo}</b><br><span style='font-size:12px'>{info}</span></br>",
            labels={'Anio': 'Año', 'Sembrada': 'Hectáreas Sembradas', 'Nommunicipio': 'Municipio', 'Nomcultivo': 'Cultivo'},
            line_shape='linear',
            markers=True,
        )
    elif municipio:
        filtered_df = filtered_df[filtered_df['Nommunicipio'] == municipio]
        grouped_df = filtered_df.groupby(['Anio', 'Nomcultivo'], as_index=False)['Sembrada'].sum()

        if grouped_df.empty:
            return "No hay datos para mostrar con los filtros aplicados"

        fig = px.line(
            grouped_df,
            x='Anio',
            y='Sembrada',
            color='Nomcultivo',
            title=f"<b>{titulo}</b><br><span style='font-size:12px'>{info}</span></br>",
            labels={'Anio': 'Año', 'Sembrada': 'Hectáreas Sembradas', 'Nommunicipio': 'Municipio', 'Nomcultivo': 'Cultivo'},
            line_shape='linear',
            markers=True,
        )
    else:
        grouped_df = filtered_df.groupby(['Anio', 'Nomcultivo'], as_index=False)['Sembrada'].sum()

        if grouped_df.empty:
            return "No hay datos para mostrar con los filtros aplicados"

        fig = px.line(
            grouped_df,
            x='Anio',
            y='Sembrada',
            color='Nomcultivo',
            title=f"<b>{titulo}</b><br><span style='font-size:12px'>{info}</span></br>",
            labels={'Anio': 'Año', 'Sembrada': 'Hectáreas Sembradas', 'Nommunicipio': 'Municipio', 'Nomcultivo': 'Cultivo'},
            line_shape='linear',
            template='ggplot2',
            markers=True,
        )

    # Ajustar el diseño del gráfico
    fig.update_layout(
        title_font=dict(size=14),
        title_x=0.5,  # Centra el título horizontalmente
        width=900,
        height=500,
    )

    # Convertir el gráfico a HTML
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html
