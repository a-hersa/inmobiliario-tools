import pandas as pd
from sqlalchemy import create_engine
from shiny import App, render, ui
from plotnine import ggplot, aes, geom_bar, labs
import os
from dotenv import load_dotenv
import matplotlib

matplotlib.use("Agg")  # Forzar backend sin interfaz gráfica

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión a PostgreSQL con SQLAlchemy
DB_URI = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@inmobiliario-postgres:5432/inmobiliario_db'

# Crear la conexión con SQLAlchemy
engine = create_engine(DB_URI)

# Función para obtener datos de la base de datos
def fetch_data():
    try:
        query = "SELECT poblacion, precio FROM propiedades;"
        data = pd.read_sql_query(query, engine)
        return data
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return pd.DataFrame()

# UI de la aplicación
app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.meta(charset="UTF-8"),
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
        ui.tags.meta(name="color-scheme", content="light dark"),
        ui.tags.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
        ui.tags.title("Análisis de Propiedades Inmobiliarias"),
    ),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("n_bins", label="Número de Bins", min=1, max=50, value=10),
        ),
        ui.card(
            ui.h2("Distribución de Precios de Propiedades Leroy 'Horsemouth'"),
            ui.output_plot("price_plot"),
        ),
    ),

)

# Lógica del servidor
def server(input, output, session):
    @output
    @render.plot
    def price_plot():
        # Obtener los datos de la base de datos
        data = fetch_data()
        if data.empty:
            return ggplot() + labs(title="No se encontraron datos en la base de datos")

        # Crear el gráfico con plotnine
        plot = (
            ggplot(data, aes(x="poblacion", y="precio")) +
            geom_bar(stat="identity", fill="skyblue") +
            labs(
                title="Precios por Localización",
                x="Localización",
                y="Precio (€)"
            )
        )
        return plot

# Crear la aplicación
app = App(app_ui, server)
