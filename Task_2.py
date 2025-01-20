import csv
import timeit
from BTrees.OOBTree import OOBTree


# Функція для завантаження даних із CSV файлу
def load_data(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["ID"] = int(row["ID"])
            row["Price"] = float(row["Price"])
            data.append(row)
    return data


# Функція для додавання товару в OOBTree
def add_item_to_tree(tree, item):
    tree[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"]
    }


# Функція для додавання товару в dict
def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"]
    }


# Функція для виконання діапазонного запиту в OOBTree
def range_query_tree(tree, min_price, max_price):
    return list(tree.items(min=min_price, max=max_price))


# Функція для виконання діапазонного запиту в dict
def range_query_dict(dictionary, min_price, max_price):
    return [item for item in dictionary.items() if min_price <= item[1]["Price"] <= max_price]


# Основний код для виконання завдання
if __name__ == "__main__":
    # Завантаження даних із файлу
    file_path = "data/generated_items_data.csv"
    items = load_data(file_path)

    # Ініціалізація структур даних
    tree = OOBTree()
    dictionary = {}

    # Додавання даних у структури
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Параметри для діапазонного запиту
    min_price = 10.0
    max_price = 100.0

    # Вимірювання часу для OOBTree
    tree_time = timeit.timeit(lambda: range_query_tree(tree, min_price, max_price), number=100)

    # Вимірювання часу для dict
    dict_time = timeit.timeit(lambda: range_query_dict(dictionary, min_price, max_price), number=100)

    # Вивід результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")