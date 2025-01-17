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
            'user': os.getenv('DB_USER', 'test'),
            'password': os.getenv('DB_PASSWORD', 'test1234'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'kingfisher')
        }

        connection_string = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
        engine = create_engine(connection_string, isolation_level="AUTOCOMMIT", pool_pre_ping=True)

        # Чтение CSV файла с использованием кодировки 'ISO-8859-1'
        print(f"Чтение файла: {csv_path}")
        df = pd.read_csv(csv_path, encoding='ISO-8859-1', on_bad_lines='skip')

        print("Прочитанные колонки:", df.columns.tolist())
        print("Количество строк:", len(df))

        # Обработка цен с удалением некорректных символов
        if 'price' in df.columns:
            df['price'] = df['price'].astype(str).replace(r'[^\d.]', '', regex=True).astype(float)

        # Проверка отсутствующих колонок
        required_columns = ['name', 'category', 'price', 'description']
        for col in required_columns:
            if col not in df.columns:
                df[col] = None

        # Убеждаемся, что строковые данные корректны
        for col in ['name', 'category', 'description']:
            if col in df.columns:
                df[col] = df[col].fillna('').astype(str)

        print("Попытка подключения к базе данных...")

        # Создаем таблицу, если ее нет
        with engine.connect() as connection:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                category VARCHAR(100),
                price DECIMAL(10,2),
                description TEXT
            );
            """
            connection.execute(create_table_query)

            # Загружаем данные
            df.to_sql('products', connection, if_exists='append', index=False, method='multi', chunksize=1000)
            print("Данные успешно загружены в PostgreSQL")

    except FileNotFoundError:
        print(f"Файл не найден: {csv_path}")
    except pd.errors.EmptyDataError:
        print("CSV файл пуст")
    except UnicodeDecodeError as e:
        print(f"Ошибка декодирования файла: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        import traceback
        print("Детали ошибки:")
        print(traceback.format_exc())
        raise



if __name__ == "__main__":
    csv_path = '../data/products.csv'
    if os.path.exists(csv_path):
        load_data_to_postgres(csv_path)
    else:
        print(f"Ошибка: файл {csv_path} не существует")
