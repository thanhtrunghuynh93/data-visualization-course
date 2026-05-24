import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shiny import Inputs, Outputs, Session, render, reactive

from .config import CORRELATION_VARS, VARIABLE_LABELS
from .data import linear_trend_seasonal_forecast, load_data, normalize_to_100


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def data_filtered() -> pd.DataFrame:
        df = load_data()
        start_year, end_year = input.year_range()
        return df[(df["year"] >= start_year) & (df["year"] <= end_year)].copy()

    @output
    @render.table
    def summary_table():
        df = data_filtered()
        target = input.target()
        rows = [
            ("Rows", len(df)),
            ("Time span", f"{df['period'].iloc[0]} to {df['period'].iloc[-1]}"),
            ("Selected variable", VARIABLE_LABELS[target]),
            ("Minimum", round(float(df[target].min()), 2)),
            ("Maximum", round(float(df[target].max()), 2)),
            ("Mean", round(float(df[target].mean()), 2)),
            ("Missing values", int(df[target].isna().sum())),
        ]
        return pd.DataFrame(rows, columns=["Metric", "Value"])

    @output
    @render.table
    def preview_table():
        return data_filtered().head(10)

    @output
    @render.plot
    def main_ts_plot():
        df = data_filtered()
        target = input.target()
        window = input.rolling_window()
        fig, ax = plt.subplots(figsize=(10, 4.8))
        ax.plot(df["date"], df[target], label="Actual")
        ax.plot(df["date"], df[target].rolling(window=window, min_periods=1).mean(), label=f"{window}-quarter rolling mean")
        ax.set_title(f"Historical trend: {VARIABLE_LABELS[target]}")
        ax.set_xlabel("Date")
        ax.set_ylabel(VARIABLE_LABELS[target])
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig

    @output
    @render.text
    def trend_commentary():
        df = data_filtered()
        target = input.target()
        first = df[target].dropna().iloc[0]
        last = df[target].dropna().iloc[-1]
        pct_change = (last / first - 1) * 100 if first != 0 else np.nan
        return (
            f"From {df['period'].iloc[0]} to {df['period'].iloc[-1]}, "
            f"{VARIABLE_LABELS[target]} changed by about {pct_change:.1f}%. "
            "Use this as a starting point, then inspect whether the change is smooth, cyclical, or shock-driven."
        )

    @output
    @render.plot
    def comparison_plot():
        df = data_filtered()
        target = input.target()
        compare = input.compare()
        corr = df[[target, compare]].corr().iloc[0, 1]
        fig, ax = plt.subplots(figsize=(10, 4.8))
        ax.plot(df["date"], normalize_to_100(df[target]), label=VARIABLE_LABELS[target])
        ax.plot(df["date"], normalize_to_100(df[compare]), label=VARIABLE_LABELS[compare])
        ax.set_title(f"Normalized comparison, correlation = {corr:.2f}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Index: first visible quarter = 100")
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig

    @output
    @render.text
    def comparison_commentary():
        df = data_filtered()
        target = input.target()
        compare = input.compare()
        corr = df[[target, compare]].corr().iloc[0, 1]
        direction = "move together" if corr >= 0 else "move in opposite directions"
        return f"The selected variables have a correlation of {corr:.2f}, so they tend to {direction} in this selected period. Remember: correlation is not causation."

    @output
    @render.plot
    def scatter_plot():
        df = data_filtered().dropna(subset=[input.scatter_x(), input.scatter_y()])
        x = input.scatter_x()
        y = input.scatter_y()
        fig, ax = plt.subplots(figsize=(8.5, 5))
        ax.scatter(df[x], df[y], alpha=0.75)
        if len(df) > 2:
            slope, intercept = np.polyfit(df[x], df[y], 1)
            xs = np.linspace(df[x].min(), df[x].max(), 100)
            ax.plot(xs, intercept + slope * xs, linestyle="--", label="Linear fit")
            ax.legend()
        ax.set_title(f"Relationship: {VARIABLE_LABELS[x]} vs {VARIABLE_LABELS[y]}")
        ax.set_xlabel(VARIABLE_LABELS[x])
        ax.set_ylabel(VARIABLE_LABELS[y])
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig

    @output
    @render.plot
    def correlation_heatmap():
        df = data_filtered()[CORRELATION_VARS].copy()
        corr = df.corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        image = ax.imshow(corr, vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels([VARIABLE_LABELS.get(c, c) for c in corr.columns], rotation=45, ha="right")
        ax.set_yticklabels([VARIABLE_LABELS.get(c, c) for c in corr.columns])
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title("Correlation heatmap")
        fig.tight_layout()
        return fig

    @output
    @render.plot
    def quarter_boxplot():
        df = data_filtered().dropna(subset=[input.target()])
        target = input.target()
        groups = [df.loc[df["quarter"] == q, target] for q in [1, 2, 3, 4]]
        fig, ax = plt.subplots(figsize=(8, 4.8))
        ax.boxplot(groups, labels=["Q1", "Q2", "Q3", "Q4"])
        ax.set_title(f"Quarterly distribution: {VARIABLE_LABELS[target]}")
        ax.set_xlabel("Quarter")
        ax.set_ylabel(VARIABLE_LABELS[target])
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig

    @output
    @render.plot
    def decade_bar():
        df = data_filtered()
        counts = df.groupby("decade")["high_inflation"].sum()
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.bar(counts.index, counts.values)
        ax.set_title("Number of high-inflation quarters by decade")
        ax.set_xlabel("Decade")
        ax.set_ylabel("High-inflation quarters")
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        return fig

    @reactive.Calc
    def forecast_df() -> pd.DataFrame:
        df = data_filtered()
        target = input.target()
        return linear_trend_seasonal_forecast(df, target, input.forecast_horizon())

    @output
    @render.plot
    def forecast_plot():
        df = data_filtered()
        target = input.target()
        fdf = forecast_df()
        fig, ax = plt.subplots(figsize=(10, 4.8))
        ax.plot(df["date"], df[target], label="Historical data")
        ax.plot(fdf["date"], fdf["forecast"], linestyle="--", marker="o", label="Linear trend + quarter adjustment")
        ax.set_title(f"Forecast example: {VARIABLE_LABELS[target]}")
        ax.set_xlabel("Date")
        ax.set_ylabel(VARIABLE_LABELS[target])
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig

    @output
    @render.table
    def forecast_table():
        fdf = forecast_df().copy()
        fdf["quarter"] = pd.PeriodIndex(fdf["date"], freq="Q").astype(str)
        fdf["forecast"] = fdf["forecast"].round(2)
        return fdf[["quarter", "forecast"]]
