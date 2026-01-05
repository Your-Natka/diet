import csv
from datetime import date
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

MEAL_LIMITS = {
    "сніданок": 200,
    "перекус": 100,
    "обід": 400,
    "вечеря": 400
}

# --- Завантаження продуктів ---
products = {}
product_names = []
with open("foods_100g_ua.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        products[row["name"]] = {
            "kcal": float(row["kcal"]),
            "protein": float(row["protein"]),
            "fat": float(row["fat"]),
            "carbs": float(row["carbs"]),
            "group": row["group"]
        }
        product_names.append(row["name"])

# --- Автозаповнення ---
product_completer = WordCompleter(product_names, ignore_case=True, sentence=True)

print("\n🍽 Введи продукти. Підказки працюють незалежно від регістру літер.")

meal = input(
    "\nВведи прийом їжі (сніданок / перекус / обід / вечеря): "
).strip().lower()

product_input = prompt(
    "Введи продукти через кому:\n", completer=product_completer
).split(",")

grams_input = input(
    "Введи грами відповідно (через кому):\n"
).split(",")

product_input = [p.strip() for p in product_input]
grams_input = [float(g.strip()) for g in grams_input]

total_kcal = 0
today = date.today()

with open("diary.csv", "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    # Якщо файл порожній, можна додати заголовки
    # writer.writerow(["date", "meal", "product", "grams", "protein", "fat", "carbs", "group", "kcal"])

    for product, grams in zip(product_input, grams_input):
        if product not in products:
            print(f"❌ Продукт '{product}' не знайдено в базі!")
            continue
        info = products[product]
        kcal = round(info["kcal"] * grams / 100, 1)
        protein = round(info["protein"] * grams / 100, 1)
        fat = round(info["fat"] * grams / 100, 1)
        carbs = round(info["carbs"] * grams / 100, 1)
        total_kcal += kcal

        writer.writerow([
            today,
            meal,
            product,
            grams,
            protein,
            fat,
            carbs,
            info["group"],
            kcal
        ])

print(f"\n🔥 Всього за {meal}: {total_kcal} ккал")
if total_kcal > MEAL_LIMITS[meal]:
    print("⚠️ Перевищено ліміт!")
else:
    print("✅ У межах ліміту")
