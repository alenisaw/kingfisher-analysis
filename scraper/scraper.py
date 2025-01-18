import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://kingfisher.kz"

# Функция для получения HTML-кода страницы
def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Ошибка при получении страницы: {url}")
        return None

# Функция для извлечения категорий
def get_categories(base_url):
    categories = []
    html = get_html(base_url)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        menu_items = soup.select("li.dropmenu > span")
        for item in menu_items:
            category_name = item.get_text(strip=True).replace("\n", " ")
            category_link = item.find_next("ul").find("a")["href"] if item.find_next("ul") else None
            if category_link:
                categories.append({
                    "name": category_name,
                    "url": base_url + category_link
                })
    return categories

# Функция для извлечения продуктов из категории
def get_products(category):
    products = []
    html = get_html(category["url"])
    if html:
        soup = BeautifulSoup(html, "html.parser")
        product_blocks = soup.select("div.goodsBlock")
        for block in product_blocks:
            name = block.select_one("a.title span").get_text(strip=True).replace("\n", " ") if block.select_one("a.title span") else "Не указано"
            price = block.select_one("span.price span.new").get_text(strip=True).replace("\n", " ") if block.select_one("span.price span.new") else "Не указана"
            description = block.select_one("span.descript span").get_text(strip=True).replace("\n", " ") if block.select_one("span.descript span") else "Нет описания"
            products.append({
                "name": name,
                "category": category["name"],
                "price": price,
                "description": description,
            })
    print(products)
    return products

# Сохранение данных в CSV
def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "category", "price", "description"])
        writer.writeheader()
        writer.writerows(data)

# Основной скрипт
if __name__ == "__main__":
    all_products = []
    categories = get_categories(BASE_URL)

    for category in categories:
        print(f"Сбор данных из категории: {category['name']}")
        products = get_products(category)
        all_products.extend(products)

    save_to_csv(all_products, "../data/products.csv")
    print("Данные успешно сохранены в файл products.csv")
