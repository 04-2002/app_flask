import plotly.express as px
import plotly.io as pio
import pandas as pd
import unicodedata

# Función para cargar los datos desde el archivo CSV
def cargar_datos():
    try:
        df = pd.read_csv('data/datos.csv', encoding='latin1')
        if df.empty:
            raise ValueError("El archivo CSV no contiene datos.")
        return df
    except FileNotFoundError:
        raise ValueError("El archivo CSV no se encontró en la ruta especificada.")
    except pd.errors.EmptyDataError:
        raise ValueError("El archivo CSV está vacío o no tiene datos válidos.")
    except Exception as e:
        raise ValueError(f"Error inesperado al cargar los datos: {str(e)}")

# Función para normalizar las cadenas de texto
def normalize_string(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()

# Función para generar el gráfico de barras
# Función para generar el gráfico de barras
def generar_barras_anual(año, municipio, ciclo_productivo, modalidad, cultivo):
    try:
        df = cargar_datos()

        # Normalizar nombres de columnas relevantes
        for col in ['Nommunicipio', 'Nomcicloproductivo', 'Nommodalidad', 'Nomcultivo']:
            df[f'{col}_normalizado'] = df[col].apply(lambda x: normalize_string(str(x).strip()))

        # Aplicar filtros
        if año:
            df = df[df['Anio'] == int(año)]
        if municipio and municipio != "Todos":
            municipio_normalizado = normalize_string(municipio.strip())
            df = df[df['Nommunicipio_normalizado'] == municipio_normalizado]
        if ciclo_productivo:
            ciclo_productivo_normalizado = normalize_string(ciclo_productivo.strip())

            # Verificar si es "Año agrícola" o "Cíclicos y Perennes"
            if ciclo_productivo == "Año agrícola (OI-PV)":
                df = df[df['Nomcicloproductivo'].isin(['Otoño-Invierno', 'Primavera-Verano'])]
            elif ciclo_productivo == "Cíclicos y Perennes":
                # Mostrar todos los ciclos productivos, no aplicamos filtro
                pass
            else:
                df = df[df['Nomcicloproductivo_normalizado'] == ciclo_productivo_normalizado]
        if modalidad:
            modalidad_normalizada = normalize_string(modalidad.strip())

            # Filtrar correctamente "Riego + Temporal" y otras modalidades
            if modalidad == "Riego + Temporal":
                df = df[df['Nommodalidad_normalizado'] == modalidad_normalizada]
            else:
                df = df[df['Nommodalidad_normalizado'] == modalidad_normalizada]
        if cultivo and cultivo != "Resumen cultivos":
            cultivo_normalizado = normalize_string(cultivo.strip())
            df = df[df['Nomcultivo_normalizado'] == cultivo_normalizado]

        # Verificar si hay datos
        if df.empty:
            return None, False, "No hay datos para los filtros seleccionados."

        # Agrupar y procesar datos para la cantidad total por cultivo
        df_grouped = df.groupby(['Nomcultivo', 'Nommunicipio']).agg({
            'Sembrada': 'sum'
        }).reset_index()

        # Crear título dinámico
        info = ""
        filtros = []

        if año:
            filtros.append(f"Año: {año}")
        if ciclo_productivo:
            if ciclo_productivo == "Año agrícola (OI-PV)":
                filtros.append("Año agrícola (OI + PV)")
            elif ciclo_productivo == "Cíclicos y Perennes":
                filtros.append("Cíclicos y Perennes")
            else:
                filtros.append(f"Ciclo: {ciclo_productivo}")
                
        if modalidad:
                 filtros.append(f"Modalidad: {modalidad}")
# Verificar si no se ha seleccionado ni Riego ni Temporal
        if not modalidad:
            filtros.append("Modalidad: Riego + Temporal")


        # Título completo
        if filtros:
            info += "  " + " | ".join(filtros)
        titulo = "Cultivos de la Zona Ríos del Estado de Tabasco"
        # Crear gráfico de barras
        fig = px.bar(
            df_grouped,
            x='Nomcultivo',  # Usar la columna 'Nomcultivo' para las barras
            y='Sembrada',
            #titulo_g 
            title=f"<b>{titulo}</b><br><span style='font-size:12px'>{info}</span></br>",
            labels={'Sembrada': 'Hectáreas Sembradas', 'Nommunicipio': 'Municipio', 'Nomcultivo': 'Cultivo'},  # Cambiar etiqueta a "Cultivo"
            color='Nommunicipio',  # Mantenemos el label de los municipios
            color_discrete_sequence=px.colors.qualitative.D3,
            template='ggplot2',
            width=950,
            height=500,
            text=None,  # No mostrar cantidades dentro de las barras
        )

        # Ajustar el tamaño del título
        fig.update_layout(
            title_font=dict(size=14)  # Ajusta el tamaño del título (puedes cambiar el valor)
        )
        # Guardar el gráfico como HTML
        graph_html = pio.to_html(fig, full_html=False)
        return graph_html, True, None

    except ValueError as ve:
        return None, False, str(ve)
    except Exception as e:
        return None, False, f"Error inesperado: {str(e)}"
