# Python Shiny Lab: US Macroeconomic Time-Series Dashboard

The dataset contains **quarterly US macroeconomic data from 1959Q1 to 2009Q3**. It has **203 observations** and multiple economic variables, including:

| Column | Meaning |
|---|---|
| `date` | Quarter-end date |
| `period` | Quarter label, such as `1959Q1` |
| `realgdp` | Real gross domestic product |
| `realcons` | Real personal consumption expenditure |
| `realinv` | Real private domestic investment |
| `realgovt` | Real government spending and investment |
| `cpi` | Consumer Price Index |
| `m1` | Money supply measure |
| `tbilrate` | Treasury bill rate |
| `unemp` | Unemployment rate |
| `infl` | Inflation rate |
| `realint` | Real interest rate |
| `gdp_growth_pct` | Quarter-to-quarter GDP growth, created for this lab |
| `consumption_share_pct` | Consumption as a share of GDP |
| `investment_share_pct` | Investment as a share of GDP |
| `real_rate_gap` | Real interest rate minus inflation |

This dataset is useful because it contains several connected time-series. You can ask questions such as:

- Does GDP grow smoothly over time?
- What happens to unemployment during weak economic periods?
- Do inflation and interest rates move together?
- Is investment more volatile than consumption?
- Which variables are easier or harder to forecast?

