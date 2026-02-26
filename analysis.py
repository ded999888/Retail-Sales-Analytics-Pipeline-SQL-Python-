# analysis.py

import pandas as pd
import sqlite3

# Подключаемся к нашей базе
conn = sqlite3.connect('walmart.db')

# Функция, которая будет выполнять SQL-запрос и печатать результат
def run_query(query, description=""):
    """Выполняет SQL-запрос и выводит результат в виде таблицы."""
    if description:
        print("\n" + "="*50)
        print(description)
        print("="*50)
    df = pd.read_sql(query, conn)
    print(df.to_string(index=False))  # to_string чтобы таблица выглядела аккуратно
    print(f"\nВсего строк: {len(df)}")
    return df
query1 = "SELECT * FROM sales LIMIT 10;"
run_query(query1, "Первые 10 строк таблицы sales")
# 2. Количество уникальных магазинов
query2 = "SELECT COUNT(DISTINCT Store) as num_stores FROM sales;"
run_query(query2, "Сколько всего магазинов?")

# 3. Уникальные годы
query3 = "SELECT DISTINCT Year FROM sales ORDER BY Year;"
run_query(query3, "Какие годы есть в данных?")
# 4. Сколько праздничных и обычных недель?
query4 = """
    SELECT 
        Holiday_Flag,
        COUNT(*) as weeks_count
    FROM sales
    GROUP BY Holiday_Flag;
"""
run_query(query4, "Количество праздничных (1) и обычных (0) недель")
# 5. Топ-5 магазинов по общей сумме продаж
query5 = """
    SELECT 
        Store,
        ROUND(SUM(Weekly_Sales), 2) as total_sales
    FROM sales
    GROUP BY Store
    ORDER BY total_sales DESC
    LIMIT 5;
"""
run_query(query5, "Топ-5 магазинов по общей выручке")
# 6. Средние продажи по месяцам (за все годы)
query6 = """
    SELECT 
        Month,
        ROUND(AVG(Weekly_Sales), 2) as avg_sales
    FROM sales
    GROUP BY Month
    ORDER BY avg_sales DESC;
"""
run_query(query6, "Средние продажи по месяцам")
# 8. Зависимость продаж от температуры (категории)
query8 = """
    SELECT 
        CASE 
            WHEN Temperature < 40 THEN 'Cold (<40F)'
            WHEN Temperature BETWEEN 40 AND 60 THEN 'Mild (40-60F)'
            WHEN Temperature BETWEEN 60 AND 80 THEN 'Warm (60-80F)'
            ELSE 'Hot (>80F)'
        END as temp_category,
        ROUND(AVG(Weekly_Sales), 2) as avg_sales,
        COUNT(*) as weeks
    FROM sales
    GROUP BY temp_category
    ORDER BY avg_sales DESC;
"""
run_query(query8, "Средние продажи в зависимости от температуры")
# 9. Топ-3 магазина по продажам в каждом месяце
query9 = """
    WITH monthly_sales AS (
        SELECT 
            Year,
            Month,
            Store,
            ROUND(SUM(Weekly_Sales), 2) as monthly_total
        FROM sales
        GROUP BY Year, Month, Store
    ),
    ranked_stores AS (
        SELECT 
            Year,
            Month,
            Store,
            monthly_total,
            ROW_NUMBER() OVER (PARTITION BY Year, Month ORDER BY monthly_total DESC) as rank_in_month
        FROM monthly_sales
    )
    SELECT Year, Month, Store, monthly_total
    FROM ranked_stores
    WHERE rank_in_month <= 3
    ORDER BY Year, Month, rank_in_month;
"""
run_query(query9, "Топ-3 магазина по каждому месяцу")
# 10. Средние продажи в магазинах с разным уровнем безработицы (по квартилям)
query10 = """
    WITH store_unemployment AS (
        SELECT 
            Store,
            ROUND(AVG(Unemployment), 2) as avg_unemployment
        FROM sales
        GROUP BY Store
    ),
    store_quartiles AS (
        SELECT 
            Store,
            avg_unemployment,
            NTILE(4) OVER (ORDER BY avg_unemployment) as unemployment_quartile
        FROM store_unemployment
    )
    SELECT 
        sq.unemployment_quartile,
        ROUND(AVG(s.Weekly_Sales), 2) as avg_sales_in_quartile,
        COUNT(DISTINCT sq.Store) as num_stores
    FROM store_quartiles sq
    JOIN sales s ON sq.Store = s.Store
    GROUP BY sq.unemployment_quartile
    ORDER BY sq.unemployment_quartile;
"""
run_query(query10, "Продажи по квартилям безработицы")