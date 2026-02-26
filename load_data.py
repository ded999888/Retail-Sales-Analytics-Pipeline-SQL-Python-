# load_data.py

# 1. Импортируем нужные библиотеки
import pandas as pd          # для работы с данными
import sqlite3               # для создания и работы с базой данных SQLite
import os                    # для работы с файловой системой (проверим, есть ли файл)

# 2. Проверяем, существует ли файл с данными
if not os.path.exists('Walmart_Sales.csv'):
    print("Ошибка: файл Walmart_Sales.csv не найден в текущей папке!")
    exit()  # останавливаем выполнение скрипта

# 3. Загружаем CSV-файл в переменную df (dataframe)
#    Обратите внимание: в файле разделитель - запятая, это стандарт для CSV.
print("Загружаем файл...")
df = pd.read_csv('Walmart_Sales.csv')

# 4. Смотрим, что загрузилось (первые 5 строк)
print("Первые 5 строк исходных данных:")
print(df.head())

# 5. Преобразуем колонку Date из текста в настоящую дату
#    В файле дата записана в формате ДД-ММ-ГГГГ, например "05-02-2010".
#    pandas умеет превращать такие строки в тип "дата" для удобного анализа.
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# 6. Создадим дополнительные колонки: год, месяц, день и номер недели в году.
#    Это очень пригодится для анализа сезонности.
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
# .dt.isocalendar().week возвращает номер недели по стандарту ISO (неделя начинается с понедельника)
df['WeekOfYear'] = df['Date'].dt.isocalendar().week

# 7. Создаём (или подключаемся) к файлу базы данных SQLite.
#    Если файла walmart.db ещё нет, он создастся автоматически.
conn = sqlite3.connect('walmart.db')

# 8. Записываем наш DataFrame в таблицу с именем 'sales'.
#    Параметр if_exists='replace' означает: если таблица уже есть, удалить её и создать заново.
#    index=False — не сохранять индекс DataFrame как отдельную колонку.
df.to_sql('sales', conn, if_exists='replace', index=False)

# 9. Проверяем, что данные успешно загрузились, выполнив простой SQL-запрос.
print("Проверка: первые 5 строк из таблицы sales:")
query = "SELECT * FROM sales LIMIT 5;"
result = pd.read_sql(query, conn)
print(result)

# 10. Закрываем соединение с базой.
conn.close()

print("Готово! Данные загружены в файл walmart.db")