import plotly.express as px
from shiny import App, ui
from shinywidgets import output_widget, render_widget

df = px.data.gapminder()

app_ui = ui.page_fluid(
    ui.h2("GDP vs Life expectancy"),
    ui.input_slider("year", "Year", min=1952, max=2007, value=2007, step=5),
    output_widget("scatter"),
)

def server(input, output, session):
    @render_widget
    def scatter():
        data = df[df["year"] == input.year()]
        return px.scatter(
            data,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            hover_name="country",
            log_x=True,
            size_max=55,
            title=f"GDP per capita vs life expectancy ({input.year()})",
        )

app = App(app_ui, server)
