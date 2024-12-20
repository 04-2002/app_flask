from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio
from barras_anual import generar_barras_anual 
from lineal_anual import generar_lineal_anual 
from barras_temporal import generar_barras_temporal


app = Flask(__name__)

# Cargar los datos globalmente de los años
def cargar_datos_anual():
    try:
        return pd.read_csv('data/datos.csv', encoding='latin1')
    except Exception as e:
        print(f"Error al cargar el archivo datos.csv: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error
df_datos = cargar_datos_anual()


# Cargar los datos globalmente de temporadas
def cargar_temporadas():
    try:
        return pd.read_csv('data/temporadas.csv', encoding="latin")
    except Exception as e:
        print(f"Error al cargar el archivo temporadas.csv: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error
df_temporadas = cargar_temporadas()

# Ruta principal 
@app.route('/')
def index():
    años = df_datos['Anio'].unique().tolist()
    municipios = df_datos['Nommunicipio'].unique().tolist()
    ciclos_productivos = ['Otoño-Invierno', 'Primavera-Verano', 'Perennes', 'Año agrícola (OI-PV)', 'Cíclicos y Perennes']
    modalidades = df_datos['Nommodalidad'].unique().tolist()
    cultivos = df_datos['Nomcultivo'].unique().tolist()

    return render_template('index.html', años=años, municipios=municipios, ciclos_productivos=ciclos_productivos, modalidades=modalidades, cultivos=cultivos)

# Ruta para recibir los filtros del cliente y generar el gráfico de barras
@app.route('/obtener_barras_anual', methods=['GET'])
def obtener_barras_anual():
    # Obtener los filtros del cliente
    año = request.args.get('año')
    municipio = request.args.get('municipio')
    ciclo_productivo = request.args.get('ciclo_productivo')
    modalidad = request.args.get('modalidad')
    cultivo = request.args.get('cultivo')

    # Generar el gráfico de barras sin pasar df, ya que se carga dentro de la función
    graph_html, success, error_message = generar_barras_anual(año, municipio, ciclo_productivo, modalidad, cultivo)

    if success:
        return jsonify({'success': True, 'graph_html': graph_html})
    else:
        return jsonify({'success': False, 'error_message': error_message})

# Ruta para la variacion de cultivos
@app.route('/variacion_anual', methods=['GET'])
def variacion_anual():
    # Cargar los datos correctamente
    df_datos = cargar_datos_anual()  # Asegúrate de que la función cargar_datos cargue el CSV correcto

    # Obtener los años disponibles desde el DataFrame
    años = df_datos['Anio'].unique().tolist()  # Usando 'Anio' en lugar de 'año'

    # Obtener otros datos disponibles
    municipios = df_datos['Nommunicipio'].unique().tolist()  # Usando 'Nommunicipio' en lugar de 'municipio'
    ciclos_productivos = ['Otoño-Invierno', 'Primavera-Verano', 'Perennes', 'Año agrícola (OI-PV)', 'Cíclicos y Perennes']
    modalidades = df_datos['Nommodalidad'].unique().tolist()  # Usando 'Nommodalidad' en lugar de 'temporada'
    cultivos = df_datos['Nomcultivo'].unique().tolist()  # Usando 'Nomcultivo' en lugar de 'nomcultivo'

    # Renderizar la plantilla con los filtros disponibles
    return render_template('variacion_anual.html', 
                           años=años, 
                           municipios=municipios, 
                           ciclos_productivos=ciclos_productivos,
                           modalidades=modalidades,
                           cultivos=cultivos)  # Enviamos los cultivos como filtro

# Ruta para recibir los filtros del cliente y generar el gráfico de líneas
@app.route('/obtener_lineal_anual', methods=['GET'])
def obtener_lineal_anual():
    # Obtener los parámetros de los filtros del cliente
    año_min = request.args.get('año_min')
    año_max = request.args.get('año_max')
    municipio = request.args.get('municipio')
    ciclo_productivo = request.args.get('ciclo_productivo')
    modalidad = request.args.get('modalidad')
    cultivo = request.args.get('cultivo')

    # Validar combinación no permitida
    if municipio == "Todos (Separados)" and cultivo == "Resumen cultivos":
        return jsonify({'success': False, 'error': 'No se puede generar el gráfico con "Resumen Cultivos" cuando se selecciona "Todos (Separados)"'})

    # Validar rangos de años
    try:
        año_min = int(año_min)
        año_max = int(año_max)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Años no válidos.'})

    if año_min > año_max:
        return jsonify({'success': False, 'error': 'El año mínimo no puede ser mayor que el año máximo.'})

    # Filtrar los datos y generar el gráfico
    graph_html = generar_lineal_anual(df_datos, año_min, año_max, municipio, ciclo_productivo, modalidad, cultivo)

    return jsonify({'success': True, 'graph_html': graph_html})


# Ruta para para las temporadas
@app.route('/temporadas_mensual', methods=['GET'])
def temporadas_mensual():
    # Obtener los filtros para que el usuario pueda elegir directamente desde los datos del CSV
    años = df_temporadas['anio'].unique().tolist()
    municipios = df_temporadas['municipio'].unique().tolist()
    temporadas = df_temporadas['temporada'].unique().tolist()
    cultivos = df_temporadas['nomcultivo'].unique().tolist()
    meses = df_temporadas['mes'].unique().tolist()

    # Renderizar la plantilla 'temporadas_mensual.html' con los datos
    return render_template('temporadas_mensual.html', 
                           años=años, 
                           municipios=municipios, 
                           temporadas=temporadas,
                           cultivos=cultivos,
                           meses=meses)

# Ruta para recibir los filtros del cliente y generar el gráfico de líneas
# Ruta para recibir los filtros del cliente y generar el gráfico de barras
@app.route('/obtener_barras_temporal', methods=['GET'])
def obtener_barras_temporal():
    # Obtener los filtros del cliente
    año = request.args.get('año')
    municipio = request.args.get('municipio')
    temporada = request.args.get('temporada')
    mes = request.args.get('mes')
    cultivo = request.args.get('cultivo')

    # Imprimir los parámetros recibidos
    print(f"Año: {año}, Municipio: {municipio}, Temporada: {temporada}, Mes: {mes}, Cultivo: {cultivo}")

    # Llamar a la función para generar el gráfico
    graph_html, error_message = generar_barras_temporal(df_temporadas, año, municipio, temporada, mes, cultivo)

    if error_message:
        return jsonify({'success': False, 'error_message': error_message})
    else:
        return jsonify({'success': True, 'graph_html': graph_html})

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
