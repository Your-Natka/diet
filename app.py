import csv
from datetime import date

MEAL_LIMITS = {
    "сніданок": 200,
    "перекус": 100,
    "обід": 400,
    "вечеря": 400
}

# --- Завантаження продуктів ---
products = {}
with open("products.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        products[row["name"]] = float(row["kcal"])

print("\n🍽 Доступні продукти:")
for p in products:
    print("•", p)
    
meal = input(
    "\nВведи прийом їжі (сніданок / перекус / обід / вечеря): "
).strip().lower()

product_input = input(
    "Введи НАЗВИ ПРОДУКТІВ через кому (як у списку вище):\n"
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

    for product, grams in zip(product_input, grams_input):
        kcal_100 = products[product]
        kcal = round(kcal_100 * grams / 100, 1)
        total_kcal += kcal

        writer.writerow([
            today,
            meal,
            product,
            grams,
            kcal
        ])

print(f"\n🔥 Всього за {meal}: {total_kcal} ккал")

if total_kcal > MEAL_LIMITS[meal]:
    print("⚠️ Перевищено ліміт!")
else:
    print("✅ У межах ліміту")
