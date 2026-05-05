import plotly.express as px
from shiny import App, ui
from shinywidgets import output_widget, render_widget

df = px.data.gapminder()

app_ui = ui.page_fluid(
    ui.h2("Life expectancy over time"),
    ui.input_select(
        "continent",
        "Continent",
        choices=sorted(df["continent"].unique().tolist()),
        selected="Asia",
    ),
    output_widget("line"),
)

def server(input, output, session):
    @render_widget
    def line():
        data = df[df["continent"] == input.continent()]
        return px.line(data, x="year", y="lifeExp", color="country", title=f"Life expectancy in {input.continent()}")

app = App(app_ui, server)
