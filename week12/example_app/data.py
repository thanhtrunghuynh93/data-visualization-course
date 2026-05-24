import numpy as np
import pandas as pd

from .config import DATA_PATH


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["decade"] = (df["year"] // 10 * 10).astype(int).astype(str) + "s"
    df["high_inflation"] = df["infl"] > df["infl"].quantile(0.75)
    df["stress_index"] = df["unemp"].rank(pct=True) + df["infl"].rank(pct=True)
    return df


def normalize_to_100(series: pd.Series) -> pd.Series:
    clean = series.dropna()
    if clean.empty or clean.iloc[0] == 0:
        return series * np.nan
    return series / clean.iloc[0] * 100


def linear_trend_seasonal_forecast(history: pd.DataFrame, target: str, horizon: int) -> pd.DataFrame:
    """A small transparent forecasting baseline: linear trend + quarter residual average."""
    work = history[["date", "quarter", target]].dropna().copy()
    work["t"] = np.arange(len(work))

    if len(work) < 8:
        last_value = work[target].iloc[-1]
        future_dates = pd.date_range(work["date"].iloc[-1] + pd.offsets.QuarterEnd(), periods=horizon, freq="QE")
        return pd.DataFrame({"date": future_dates, "forecast": np.repeat(last_value, horizon)})

    slope, intercept = np.polyfit(work["t"], work[target], 1)
    work["trend_fit"] = intercept + slope * work["t"]
    work["residual"] = work[target] - work["trend_fit"]
    seasonal_adjustment = work.groupby("quarter")["residual"].mean().to_dict()

    future_t = np.arange(len(work), len(work) + horizon)
    future_dates = pd.date_range(work["date"].iloc[-1] + pd.offsets.QuarterEnd(), periods=horizon, freq="QE")
    future_quarters = pd.Series(future_dates).dt.quarter.to_numpy()
    forecasts = []
    for t, q in zip(future_t, future_quarters):
        trend = intercept + slope * t
        forecasts.append(trend + seasonal_adjustment.get(int(q), 0))

    return pd.DataFrame({"date": future_dates, "forecast": forecasts})
