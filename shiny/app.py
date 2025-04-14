from pathlib import Path
import pandas as pd

# Primer ejemplo de histograma simple
# import matplotlib.pyplot as plt
# import numpy as np
# from shiny.express import ui, input, render

# Segundo ejemplo de dos gráficos con plotly
import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly
import plotly.express as px

from sqlalchemy import create_engine
# from shiny import App, render, ui
# from plotnine import ggplot, aes, geom_bar, labs
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión a PostgreSQL con SQLAlchemy
DB_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@inmobiliario-postgres:5432/inmobiliario_db'

# Crear la conexión con SQLAlchemy
engine = create_engine(DB_URI)

ui.page_opts(title="Análisis inmobiliario del rango 0 - 120k", fillable=True)

# @reactive.calc
# def dat():
#     infile = Path(__file__).parent / "propiedades.csv"
#     return pd.read_csv(infile)

# Función para obtener datos de la base de dato
@reactive.calc
def fetch_data():
    try:
        query = "SELECT * FROM propiedades;"
        data = pd.read_sql_query(query, engine)
        data["fecha_updated"] = pd.to_datetime(data["fecha_updated"], format="%Y%m%d")\
               .dt.strftime('%Y-%m')
        data = data.sort_values("fecha_updated").reset_index(drop=True)
        return data
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return pd.DataFrame()

# with ui.card(full_screen=True):
#     @render.text
#     def value():
#         df = fetch_data()
         
#         return df.dtypes   

with ui.sidebar():
    ui.input_selectize(
        "poblacion",
        "Selecciona una población",
        ["Mataró", "Granollers", "Cabrera de Mar"]
    )
    ui.input_numeric("bins", "Number of bins", 30)

with ui.card(full_screen=True):
    @render_plotly
    def hist():
        df = fetch_data()
        # Filtrar por la población seleccionada
        df_filtered = df[df["poblacion"] == input.poblacion()]

        # Evitar división por cero
        df_filtered = df_filtered[df_filtered["metros"] > 0]

        # Crear nueva columna con el cálculo
        df_filtered["precio_m2"] = df_filtered["precio"] / df_filtered["metros"]

        # Ordenar por fecha para evitar líneas desordenadas
        df_filtered = df_filtered.sort_values(by="fecha_updated")

        fig = px.line(df_filtered, x=df_filtered.index, y="precio_m2", nbins=input.bins(), title="Evolución del precio por metro cuadrado")

        # Configurar formato del eje X para mostrar fechas en lugar de números grandes
        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = df_filtered.index,
                ticktext = df_filtered["fecha_updated"]
            )
        )

        return fig

    # @render_plotly
    # def plot2():
    #     return px.histogram(px.data.habitaciones(), y="habitaciones")

    # @render.data_frame
    # def data():
    #     return dat()

# # UI de la aplicación
# app_ui = ui.page_fluid(
#     ui.tags.head(
#         ui.tags.meta(charset="UTF-8"),
#         ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
#         ui.tags.meta(name="color-scheme", content="light dark"),
#         ui.tags.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
#         ui.tags.title("Análisis de Propiedades Inmobiliarias"),
#     ),
#     ui.layout_sidebar(
#         ui.sidebar(
#             ui.input_slider("n_bins", label="Número de Bins", min=1, max=50, value=10),
#         ),
#         ui.card(
#             ui.h2("Distribución de Precios de Propiedades Leroy 'Horsemouth'"),
#             ui.output_plot("price_plot"),
#         ),
#     ),

# )

# # Lógica del servidor
# def server(input, output, session):
#     @output
#     @render.plot
#     def price_plot():
#         # Obtener los datos de la base de datos
#         data = fetch_data()
#         if data.empty:
#             return ggplot() + labs(title="No se encontraron datos en la base de datos")

#         # Crear el gráfico con plotnine
#         plot = (
#             ggplot(data, aes(x="poblacion", y="precio")) +
#             geom_bar(stat="identity", fill="skyblue") +
#             labs(
#                 title="Precios por Localización",
#                 x="Localización",
#                 y="Precio (€)"
#             )
#         )
#         return plot

# # Crear la aplicación
# app = App(app_ui, server)
