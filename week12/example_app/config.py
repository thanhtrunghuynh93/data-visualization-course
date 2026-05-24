from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "us_macro_quarterly.csv"

VARIABLE_LABELS = {
    "realgdp": "Real GDP",
    "realcons": "Real Consumption",
    "realinv": "Real Investment",
    "realgovt": "Government Spending",
    "realdpi": "Real Disposable Income",
    "cpi": "Consumer Price Index",
    "m1": "Money Supply (M1)",
    "tbilrate": "Treasury Bill Rate",
    "unemp": "Unemployment Rate",
    "pop": "Population",
    "infl": "Inflation Rate",
    "realint": "Real Interest Rate",
    "gdp_growth_pct": "GDP Growth (%)",
    "consumption_share_pct": "Consumption Share of GDP (%)",
    "investment_share_pct": "Investment Share of GDP (%)",
    "real_rate_gap": "Real Rate Gap",
}

CORRELATION_VARS = [
    "realgdp",
    "realcons",
    "realinv",
    "cpi",
    "tbilrate",
    "unemp",
    "infl",
    "realint",
    "gdp_growth_pct",
]
