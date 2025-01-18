import pandas as pd
from sqlalchemy import create_engine
import os
import chardet

def detect_encoding(file_path):
    """Определение кодировки файла"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def load_data_to_postgres(csv_path: str):
    """Загрузка данных из CSV в PostgreSQL"""
    try:
        # Параметры подключения
        db_params = {
            'user': os.getenv('DB_USER', 'alenish'),
            'password': os.getenv('DB_PASSWORD', '228228'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5436'),
            'database': os.getenv('DB_NAME', 'alenish')
        }

        connection_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
        engine = create_engine(connection_string, isolation_level="AUTOCOMMIT", pool_pre_ping=True)

        # Определение кодировки файла
        encoding = detect_encoding(csv_path)

        # Чтение CSV файла с использованием определенной кодировки
        print(f"Чтение файла: {csv_path} с кодировкой {encoding}")
        df = pd.read_csv(csv_path, encoding=encoding, on_bad_lines='skip')

        print("Прочитанные колонки:", df.columns.tolist())
        print("Количество строк:", len(df))

        # Обработка цен с удалением некорректных символов
        if 'price' in df.columns:
            df['price'] = df['price'].astype(str).replace(r'[^\d.]', '', regex=True).astype(float)

        # Загрузка данных в PostgreSQL
        table_name = os.path.splitext(os.path.basename(csv_path))[0]
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Данные успешно загружены в таблицу {table_name}")

    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")

# Пример использования
load_data_to_postgres('../data/products.csv')
