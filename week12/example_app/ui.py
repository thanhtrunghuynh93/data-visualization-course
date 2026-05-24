from shiny import ui

from .config import VARIABLE_LABELS

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Dashboard Controls"),
        ui.input_slider("year_range", "Year range", min=1959, max=2009, value=(1959, 2009), step=1, sep=""),
        ui.input_select("target", "Main variable", choices=VARIABLE_LABELS, selected="realgdp"),
        ui.input_select("compare", "Compare with", choices=VARIABLE_LABELS, selected="unemp"),
        ui.input_select("scatter_x", "Scatter X", choices=VARIABLE_LABELS, selected="unemp"),
        ui.input_select("scatter_y", "Scatter Y", choices=VARIABLE_LABELS, selected="infl"),
        ui.input_slider("rolling_window", "Rolling window (quarters)", min=2, max=16, value=4, step=1),
        ui.input_slider("forecast_horizon", "Forecast horizon (quarters)", min=2, max=12, value=8, step=1),
        ui.hr(),
        ui.markdown("Explore the past first. Then forecast carefully."),
    ),
    ui.h1("US Macroeconomic Time-Series Dashboard"),
    ui.markdown(
        """
        This solution dashboard demonstrates a compact but richer workflow: overview → historical trend → comparison → relationships → seasonality → forecast.
        """
    ),
    ui.navset_tab(
        ui.nav_panel("1. Overview", ui.output_table("summary_table"), ui.output_table("preview_table")),
        ui.nav_panel("2. Trend", ui.output_plot("main_ts_plot"), ui.output_text_verbatim("trend_commentary")),
        ui.nav_panel("3. Compare", ui.output_plot("comparison_plot"), ui.output_text_verbatim("comparison_commentary")),
        ui.nav_panel("4. Relationships", ui.output_plot("scatter_plot"), ui.output_plot("correlation_heatmap")),
        ui.nav_panel("5. Seasonality", ui.output_plot("quarter_boxplot"), ui.output_plot("decade_bar")),
        ui.nav_panel("6. Forecast", ui.output_plot("forecast_plot"), ui.output_table("forecast_table")),
    ),
)
