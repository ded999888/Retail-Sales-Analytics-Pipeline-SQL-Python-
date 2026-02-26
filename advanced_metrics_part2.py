# advanced_metrics_part2.py

import pandas as pd
import sqlite3
import os
import numpy as np

conn = sqlite3.connect('walmart.db')
os.makedirs('reports', exist_ok=True)

def save_metric(query, filename, description=""):
    if description:
        print(f"Выполняю: {description}")
    df = pd.read_sql(query, conn)
    filepath = f'reports/{filename}.csv'
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"  -> Сохранено {len(df)} строк в {filepath}")
    return df

# Словарь для новых датафреймов
new_dfs = {}

# ------------------------------------------------------------
# 1. Прогноз на следующий месяц (простое скользящее среднее за 3 месяца)
# ------------------------------------------------------------
query_forecast = """
WITH monthly AS (
    SELECT
        Store,
        Year,
        Month,
        ROUND(SUM(Weekly_Sales), 2) AS total_sales
    FROM sales
    GROUP BY Store, Year, Month
),
moving_avg AS (
    SELECT
        Store,
        Year,
        Month,
        total_sales,
        ROUND(AVG(total_sales) OVER (
            PARTITION BY Store
            ORDER BY Year, Month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2) AS moving_avg_3m
    FROM monthly
),
last_month AS (
    SELECT
        Store,
        Year,
        Month,
        total_sales,
        moving_avg_3m,
        ROW_NUMBER() OVER (PARTITION BY Store ORDER BY Year DESC, Month DESC) AS rn
    FROM moving_avg
)
SELECT
    Store,
    Year,
    Month,
    total_sales AS actual_sales,
    moving_avg_3m AS forecast_next_month,
    ROUND(moving_avg_3m - total_sales, 2) AS forecast_error,
    ROUND(100.0 * (moving_avg_3m - total_sales) / total_sales, 2) AS forecast_error_percent
FROM last_month
WHERE rn = 1
ORDER BY Store;
"""
df_forecast = save_metric(query_forecast, "forecast_next_month", "Прогноз на следующий месяц (скользящее среднее за 3 месяца)")
new_dfs['forecast_next_month'] = df_forecast

# ------------------------------------------------------------
# 2. Индекс сезонности по месяцам
# ------------------------------------------------------------
query_seasonal = """
WITH monthly_avg AS (
    SELECT
        Month,
        ROUND(AVG(Weekly_Sales), 2) AS avg_sales_month
    FROM sales
    GROUP BY Month
),
overall_avg AS (
    SELECT ROUND(AVG(Weekly_Sales), 2) AS overall_avg_sales FROM sales
)
SELECT
    m.Month,
    m.avg_sales_month,
    o.overall_avg_sales,
    ROUND(m.avg_sales_month / o.overall_avg_sales, 3) AS seasonal_index
FROM monthly_avg m
CROSS JOIN overall_avg o
ORDER BY m.Month;
"""
df_seasonal = save_metric(query_seasonal, "seasonal_index", "Индекс сезонности по месяцам")
new_dfs['seasonal_index'] = df_seasonal

# ------------------------------------------------------------
# 3. ABC-анализ магазинов по общей выручке
# ------------------------------------------------------------
query_abc = """
WITH store_sales AS (
    SELECT
        Store,
        ROUND(SUM(Weekly_Sales), 2) AS total_sales
    FROM sales
    GROUP BY Store
),
cumulative AS (
    SELECT
        Store,
        total_sales,
        SUM(total_sales) OVER (ORDER BY total_sales DESC) AS running_total,
        SUM(total_sales) OVER () AS grand_total
    FROM store_sales
)
SELECT
    Store,
    total_sales,
    ROUND(100.0 * total_sales / grand_total, 2) AS pct_of_total,
    ROUND(100.0 * running_total / grand_total, 2) AS cumulative_pct,
    CASE
        WHEN 100.0 * running_total / grand_total <= 80 THEN 'A'
        WHEN 100.0 * running_total / grand_total <= 95 THEN 'B'
        ELSE 'C'
    END AS abc_category
FROM cumulative
ORDER BY total_sales DESC;
"""
df_abc = save_metric(query_abc, "abc_analysis", "ABC-анализ магазинов")
new_dfs['abc_analysis'] = df_abc

# ------------------------------------------------------------
# 4. Корреляция продаж с макро-факторами (температура, безработица, цена топлива)
# ------------------------------------------------------------
# Выгрузим все данные по магазинам и посчитаем корреляцию в pandas
print("Вычисляю корреляции с макрофакторами...")
df_all = pd.read_sql("SELECT Store, Weekly_Sales, Temperature, Fuel_Price, Unemployment FROM sales", conn)

# Группируем по магазину и считаем корреляции
correlations = []
for store in df_all['Store'].unique():
    store_data = df_all[df_all['Store'] == store]
    corr_temp = store_data['Weekly_Sales'].corr(store_data['Temperature'])
    corr_fuel = store_data['Weekly_Sales'].corr(store_data['Fuel_Price'])
    corr_unemp = store_data['Weekly_Sales'].corr(store_data['Unemployment'])
    correlations.append({
        'Store': store,
        'corr_temperature': round(corr_temp, 3) if not np.isnan(corr_temp) else None,
        'corr_fuel_price': round(corr_fuel, 3) if not np.isnan(corr_fuel) else None,
        'corr_unemployment': round(corr_unemp, 3) if not np.isnan(corr_unemp) else None
    })

df_corr = pd.DataFrame(correlations)
corr_path = 'reports/correlation_macro.csv'
df_corr.to_csv(corr_path, index=False, encoding='utf-8')
print(f"  -> Сохранено {len(df_corr)} строк в {corr_path}")
new_dfs['correlation_macro'] = df_corr

conn.close()

# ------------------------------------------------------------
# Обновляем сводный Excel-файл
# ------------------------------------------------------------
excel_path = 'reports/summary_report.xlsx'

if os.path.exists(excel_path):
    with pd.ExcelFile(excel_path) as xls:
        sheet_names = xls.sheet_names
        existing_dfs = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in sheet_names}
else:
    existing_dfs = {}

all_dfs = {**existing_dfs, **new_dfs}

with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    for sheet_name, df in all_dfs.items():
        safe_name = sheet_name[:31]
        df.to_excel(writer, sheet_name=safe_name, index=False)

print(f"\nСводный Excel-файл обновлён: {excel_path}")
print("Все дополнительные метрики успешно сохранены!")