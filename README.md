# Проект по сбору и анализу данных из Kingfisher.kz


## Структура проекта

```
kingfisher-analysis/
├── scraping/
│   └── scraper.py
├── database/
│   ├── docker-compose.yml
│   └── init.sql
├── loader/
│   └── db_loader.py
├── analysis/
│   └── analyzer.py
├── data/
├── results/
├── requirements.txt
└── README.md
```

## Требования

- Python 3.8+
- Docker
- Docker Compose

## Шаги по установке и запуска кода данног проекта

1. Клонирование репозитория:
```bash
git clone https://github.com/alenisaw/kingfisher-analysis.git
cd kingfisher-analysis
```

2. Создание виртуального окружения и установления зависимостей:
```bash
pip install -r requirements.txt
```

3. Запуск PostgreSQL через Docker:
```bash
cd database
docker-compose up -d
```

4. Запуск сбора данных:
```bash
cd ../scraping
python scraper.py
```

5. Загрузка данных в БД:
```bash
cd ../loader
python db_loader.py
```

6. Проведение анализа:
```bash
cd ../analysis
python analyzer.py
```

## Результаты

После выполнения всех шагов мы получим:
- CSV-файл с собранными данными
- Базу данных PostgreSQL с загруженными данными
- Графики с визуализацией в папке results/
- Статистический отчет