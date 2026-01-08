import csv
from datetime import date
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from recipes import recipes

# --- Ліміти калорій на прийом їжі ---
MEAL_LIMITS = {
    "сніданок": 250,
    "перекус": 150,
    "обід": 300,
    "вечеря": 400
}

# --- Завантаження продуктів ---
products = {}
product_names = []
with open("foods_100g_ua.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            products[row["name"]] = {
                "kcal": float(row["kcal"]),
                "protein": float(row["protein"]),
                "fat": float(row["fat"]),
                "carbs": float(row["carbs"]),
                "group": row["group"]
            }
            product_names.append(row["name"])
        except ValueError:
            print(f"❌ Пропущено рядок через некоректні дані: {row}")

# --- Автозаповнення для ручного введення ---
product_completer = WordCompleter(product_names, ignore_case=True, sentence=True)

# --- Вибір прийому їжі ---
meal = input("\nВведи прийом їжі (сніданок / перекус / обід / вечеря): ").strip().lower()

# --- Вибір способу: галерея або ручний ввід ---
mode = input("Вибрати: [1] Галерея готових страв, [2] Ввести продукти вручну: ").strip()

selected_ingredients = []

if mode == "1":
    print("\n📸 Галерея страв:")
    for i, r in enumerate(recipes, 1):
        total_kcal = 0
        for item in r["ingredients"]:
            product = item["product"]
            if product not in products:
                print(f"❌ Немає в базі: {product}")
                continue
            total_kcal += products[product]["kcal"] * item["grams"] / 100
        print(f"{i}. {r['name']} — {round(total_kcal,1)} ккал (Фото: {r['image']})")
    
    try:
        choice = int(input("Введи номер страви: ").strip())
        if 1 <= choice <= len(recipes):
            selected_ingredients = recipes[choice - 1]["ingredients"]
        else:
            print("❌ Невірний вибір, завершуємо.")
            exit()
    except ValueError:
        print("❌ Некоректний ввід, завершуємо.")
        exit()
else:
    # Ручний ввід
    product_input = prompt("Введи продукти через кому:\n", completer=product_completer).split(",")
    grams_input = input("Введи грами відповідно (через кому):\n").split(",")

    try:
        product_input = [p.strip() for p in product_input]
        grams_input = [float(g.strip()) for g in grams_input]
    except ValueError:
        print("❌ Некоректні грами, завершуємо.")
        exit()

    # Знаходимо продукт у базі без урахування регістру
    selected_ingredients = []
    for p, g in zip(product_input, grams_input):
        match = next((name for name in products if name.lower() == p.lower()), None)
        if match is None:
            print(f"❌ Продукт '{p}' не знайдено в базі!")
            continue
        selected_ingredients.append({"product": match, "grams": g})

# --- Запис у diary.csv ---
total_kcal = 0
today = date.today()

with open("diary.csv", "a", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    for item in selected_ingredients:
        product = item["product"]
        grams = item["grams"]
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
if total_kcal > MEAL_LIMITS.get(meal, 0):
    print("⚠️ Перевищено ліміт!")
else:
    print("✅ У межах ліміту")
