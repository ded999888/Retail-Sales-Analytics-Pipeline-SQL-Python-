# advanced_metrics.py

import pandas as pd
import sqlite3
import os

# Подключаемся к базе
conn = sqlite3.connect('walmart.db')

# Создаём папку reports, если её нет
os.makedirs('reports', exist_ok=True)

def save_metric(query, filename, description=""):
    """Выполняет SQL и сохраняет результат в CSV, возвращает DataFrame."""
    if description:
        print(f"Выполняю: {description}")
    df = pd.read_sql(query, conn)
    filepath = f'reports/{filename}.csv'
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"  -> Сохранено {len(df)} строк в {filepath}")
    return df

# Словарь для сбора всех новых датафреймов (потом добавим в Excel)
new_dfs = {}

# ------------------------------------------------------------
# 1. Month-over-Month Growth Rate (темп роста месяц к месяцу)
# ------------------------------------------------------------
query_growth = """
WITH monthly AS (
    SELECT
        Store,
        Year,
        Month,
        ROUND(SUM(Weekly_Sales), 2) AS total_sales
    FROM sales
    GROUP BY Store, Year, Month
)
SELECT
    Store,
    Year,
    Month,
    total_sales,
    ROUND(
        (total_sales - LAG(total_sales) OVER (PARTITION BY Store ORDER BY Year, Month))
        / LAG(total_sales) OVER (PARTITION BY Store ORDER BY Year, Month) * 100,
        2
    ) AS mom_growth_percent
FROM monthly
ORDER BY Store, Year, Month;
"""
df_growth = save_metric(query_growth, "growth_rate", "Темп роста продаж (MoM %)")
new_dfs['growth_rate'] = df_growth

# ------------------------------------------------------------
# 2. 3-Month Moving Average (скользящее среднее за 3 месяца)
# ------------------------------------------------------------
query_moving_avg = """
WITH monthly AS (
    SELECT
        Store,
        Year,
        Month,
        ROUND(SUM(Weekly_Sales), 2) AS total_sales
    FROM sales
    GROUP BY Store, Year, Month
)
SELECT
    Store,
    Year,
    Month,
    total_sales,
    ROUND(
        AVG(total_sales) OVER (
            PARTITION BY Store
            ORDER BY Year, Month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2
    ) AS moving_avg_3m
FROM monthly
ORDER BY Store, Year, Month;
"""
df_moving = save_metric(query_moving_avg, "moving_avg_3m", "Скользящее среднее за 3 месяца")
new_dfs['moving_avg_3m'] = df_moving

# ------------------------------------------------------------
# 3. Store Ranking (рейтинг магазинов по годовой выручке)
# ------------------------------------------------------------
query_ranking = """
WITH yearly AS (
    SELECT
        Store,
        Year,
        ROUND(SUM(Weekly_Sales), 2) AS yearly_sales
    FROM sales
    GROUP BY Store, Year
)
SELECT
    Store,
    Year,
    yearly_sales,
    RANK() OVER (PARTITION BY Year ORDER BY yearly_sales DESC) AS sales_rank
FROM yearly
ORDER BY Year, sales_rank;
"""
df_ranking = save_metric(query_ranking, "store_ranking", "Рейтинг магазинов по годам")
new_dfs['store_ranking'] = df_ranking

# ------------------------------------------------------------
# 4. Sales Volatility (стандартное отклонение продаж по магазину)
# ------------------------------------------------------------
print("Вычисляю волатильность продаж (stddev) средствами pandas...")
df_sales_all = pd.read_sql("SELECT Store, Weekly_Sales FROM sales", conn)
volatility_df = df_sales_all.groupby('Store').agg(
    sales_volatility=('Weekly_Sales', lambda x: round(x.std(), 2)),
    avg_sales=('Weekly_Sales', lambda x: round(x.mean(), 2)),
    weeks_count=('Weekly_Sales', 'count')
).reset_index().sort_values('sales_volatility', ascending=False)

vol_path = 'reports/sales_volatility.csv'
volatility_df.to_csv(vol_path, index=False, encoding='utf-8')
print(f"  -> Сохранено {len(volatility_df)} строк в {vol_path}")
new_dfs['sales_volatility'] = volatility_df

# Закрываем соединение
conn.close()

# ------------------------------------------------------------
# Добавляем новые листы в существующий Excel-файл summary_report.xlsx
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