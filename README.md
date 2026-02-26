# Retail Sales Analytics Pipeline (SQL + Python + SQLite)
End-to-end data analytics pipeline for retail sales analysis based on Walmart dataset.

Project Objective.
Build a structured SQL-based analytics system to:
•	Analyze sales performance;
•	Identify seasonality patterns;
•	Evaluate store efficiency;
•	Assess macroeconomic impact;
•	Generate management-ready reports;

Architecture.
Pipeline consists of 4 main stages:
1.	Data Loading (ETL):
o	CSV ingestion;
o	Date transformation;
o	Feature engineering (Year, Month, WeekOfYear);
o	Loading into SQLite database;
2.	SQL Analytics Layer:
o	Aggregations (SUM, AVG);
o	Window functions (LAG, RANK, NTILE);
o	CTE-based multi-step transformations;
o	Ranking & segmentation;
3.	Advanced Metrics:
o	MoM growth rate;
o	3-month moving average;
o	Sales volatility (stddev);
o	ABC analysis;
o	Seasonal index;
o	Simple rolling forecast;
o	Correlation with macro factors;
4.	Reporting Layer:
o	Automated CSV exports;
o	Consolidated Excel dashboard (multi-sheet report);

Key Business Insights Generated.
•	Top-performing stores by revenue;
•	Holiday vs regular sales comparison;
•	Temperature impact on sales;
•	Sales volatility per store;
•	Store ranking by yearly revenue;
•	ABC segmentation of stores;
•	Correlation with unemployment, fuel price and temperature;
•	Month-over-Month growth tracking;
•	Rolling 3-month forecast;

SQL Techniques Used.
•	GROUP BY aggregations;
•	CASE logic;
•	Common Table Expressions (CTE);
•	Window Functions:
o	LAG();
o	RANK();
o	ROW_NUMBER();
o	NTILE();
•	Rolling averages;
•	Cumulative percentage calculation;

Business Applications
•	Retail performance monitoring
•	Store segmentation
•	Sales forecasting
•	Seasonal planning
•	Operational benchmarking
•	Macro-impact sensitivity analysis

Tech Stack.
•	Python (pandas, sqlite3, openpyxl);
•	SQL. 

# Retail Sales Analytics Pipeline (SQL + Python + SQLite)
End-to-end аналитический пайплайн для анализа розничных продаж (датасет Walmart)

Цель проекта.
Разработать структурированную систему аналитики на базе SQL для:
•	анализа динамики продаж;
•	выявления сезонных закономерностей;
•	оценки эффективности магазинов;
•	анализа влияния макроэкономических факторов;
•	формирования управленческой отчётности;

Архитектура решения.
Пайплайн состоит из четырёх основных этапов:
Загрузка и подготовка данных (ETL):
•	импорт данных из CSV;
•	преобразование дат;
•	feature engineering (Year, Month, WeekOfYear);
•	загрузка данных в базу SQLite;
SQL-слой аналитики:
•	агрегирующие функции (SUM, AVG);
•	оконные функции (LAG, RANK, NTILE);
•	многошаговые преобразования через CTE;
•	ранжирование и сегментация;
Расчёт продвинутых метрик.
•	прирост Month-over-Month (MoM);
•	скользящая средняя за 3 месяца;
•	волатильность продаж (stddev);
•	ABC-анализ;
•	сезонный индекс;
•	скользящее среднее;
•	корреляция с макроэкономическими факторами;

Отчётность:
•	автоматизированный экспорт в CSV;
•	консолидированный Excel-дашборд (многостраничный отчёт);

Полученные бизнес-инсайты:
•	магазины-лидеры по выручке;
•	сравнение праздничных и обычных продаж;
•	влияние температуры на продажи;
•	волатильность продаж по магазинам;
•	ранжирование магазинов по годовой выручке;
•	ABC-сегментация;
•	корреляция с уровнем безработицы, ценами на топливо и температурой;
•	отслеживание MoM-динамики;
•	скользящий трёхмесячный прогноз.

Использованные SQL-функции:
•	агрегирование через GROUP BY;
•	условная логика (CASE);
•	Common Table Expressions (CTE);
•	оконные функции:
o	LAG();
o	RANK();
o	ROW_NUMBER();
o	NTILE();
•	расчёт скользящих средних;
•	вычисление накопительного процента;

Бизнес-применение:
•	мониторинг эффективности розничной сети;
•	сегментация торговых точек;
•	прогнозирование продаж;
•	сезонное планирование
•	операционный бенчмаркинг
•	анализ чувствительности к макрофакторам
________________________________________
🛠 Используемый стек технологий
•	Python (pandas, sqlite3, openpyxl)
•	SQL
