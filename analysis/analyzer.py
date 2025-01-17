import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os


def analyze_data():
    # Подключение к базе данных
    db_params = {
        'user': os.getenv('DB_USER', 'kingfisher_user'),
        'password': os.getenv('DB_PASSWORD', 'your_strong_password'),
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'kingfisher')
    }

    connection_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
    engine = create_engine(connection_string)

    # Загрузка данных
    df = pd.read_sql_table('products', engine)

    # Анализ по категориям
    plt.figure(figsize=(12, 6))
    category_counts = df['category'].value_counts()
    category_counts.plot(kind='bar', color='skyblue')
    plt.title('Распределение товаров по категориям', fontsize=16)
    plt.xlabel('Категория', fontsize=12)
    plt.ylabel('Количество товаров', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('category_distribution.png')
    plt.show()

    # Анализ цен по категориям
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='category', y='price', data=df, palette="Set2")
    plt.title('Распределение цен по категориям', fontsize=16)
    plt.xlabel('Категория', fontsize=12)
    plt.ylabel('Цена (₸)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('price_distribution.png')
    plt.show()

    # Статистический анализ
    stats = {
        'total_products': len(df),
        'avg_price': df['price'].mean(),
        'median_price': df['price'].median(),
        'min_price': df['price'].min(),
        'max_price': df['price'].max(),
        'categories_count': len(df['category'].unique())
    }

    # Визуализация статистических данных
    stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])

    plt.figure(figsize=(8, 6))
    sns.barplot(x='Metric', y='Value', data=stats_df, palette="coolwarm")
    plt.title('Основные статистические показатели', fontsize=16)
    plt.xlabel('Показатель', fontsize=12)
    plt.ylabel('Значение', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('stats_distribution.png')
    plt.show()

    # Генерация текстового отчета
    report = f"""
    Статистический отчет:

    1. Общее количество товаров: {stats['total_products']}
    2. Средняя цена товара: {stats['avg_price']:.2f} ₸
    3. Медианная цена товара: {stats['median_price']:.2f} ₸
    4. Минимальная цена товара: {stats['min_price']} ₸
    5. Максимальная цена товара: {stats['max_price']} ₸
    6. Количество уникальных категорий: {stats['categories_count']}
    """

    # Сохранение текстового отчета в файл
    with open('statistical_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)

    return stats


if __name__ == "__main__":
    stats = analyze_data()
    print("Статистика по данным:")
    for key, value in stats.items():
        print(f"{key}: {value}")
