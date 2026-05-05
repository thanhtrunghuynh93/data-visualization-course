import plotly.express as px
from shiny import App, ui
from shinywidgets import output_widget, render_widget

df = px.data.gapminder()

app_ui = ui.page_fluid(
    ui.h2("Life expectancy distribution"),
    ui.input_slider("year", "Year", min=1952, max=2007, value=2007, step=5),
    ui.input_slider("bins", "Bins", min=5, max=60, value=20),
    output_widget("hist"),
)

def server(input, output, session):
    @render_widget
    def hist():
        data = df[df["year"] == input.year()]
        return px.histogram(
            data,
            x="lifeExp",
            color="continent",
            nbins=input.bins(),
            title=f"Life expectancy distribution ({input.year()})",
        )

app = App(app_ui, server)
