import pandas as pd

# Зчитуємо таблицю з тарифами
file_path = "/Users/d0n0ts1lly/Desktop/bwauto/calc/rates.xlsx"  # Потрібно вказати правильний шлях до файлу
df = pd.read_excel(file_path, header=None)

# Структура для пошуку вартості
def calculate_delivery(city):
    delivery_df = df.copy()
    delivery_df.replace("-", None, inplace=True)
    
    # Знаходимо місто в таблиці
    city_row = delivery_df[delivery_df[0] == city]
    
    if city_row.empty:
        return f"Місто {city} не знайдено"

    # Отримуємо штати та вартість доставки по суші
    state = city_row.iloc[0, 1]  # Отримуємо штат
    ground_cost = city_row[state].values[0]  # Вартість доставки по суші
    sea_cost = 700  # Вартість морської доставки (за умовами)

    total_cost = float(ground_cost) + sea_cost
    return f"Вартість доставки для {city}: {total_cost} доларів"

# Основний блок для взаємодії з користувачем
def main():
    while True:
        city = input("Введіть місто для розрахунку доставки (або 'exit' для виходу): ").strip()
        
        if city.lower() == 'exit':
            print("Завершення роботи.")
            break
        
        result = calculate_delivery(city)
        print(result)

if __name__ == "__main__":
    main()
