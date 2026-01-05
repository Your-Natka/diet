import csv
from datetime import date, datetime, timedelta
from collections import defaultdict

# ---------- ЗАВАНТАЖЕННЯ БАЗИ ПРОДУКТІВ ----------
def load_foods(path="foods_100g_ua.csv"):
    foods = {}
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            foods[r["name"]] = {
                "kcal": float(r["kcal"]),
                "protein": float(r["protein"]),
                "fat": float(r["fat"]),
                "carbs": float(r["carbs"]),
                "group": r["group"]
            }
    return foods

# ---------- ЗАВАНТАЖЕННЯ ЩОДЕННИКА ----------
def load_diary(path="diary.csv"):
    entries = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                entries.append({
                    "date": datetime.fromisoformat(r["date"]).date(),
                    "meal": r["meal"],
                    "product": r["product"],
                    "grams": float(r["grams"]),
                    "kcal": float(r["kcal"])
                })
            except:
                continue
    return entries

# ---------- СТАТИСТИКА ЗА СЬОГОДНІ ----------
def stats_today(entries, foods):
    today = date.today()
    total = defaultdict(float)
    per_meal = defaultdict(float)

    for e in entries:
        if e["date"] == today:
            food = foods.get(e["product"])
            if not food:
                continue

            factor = e["grams"] / 100
            total["kcal"] += food["kcal"] * factor
            total["protein"] += food["protein"] * factor
            total["fat"] += food["fat"] * factor
            total["carbs"] += food["carbs"] * factor
            per_meal[e["meal"]] += food["kcal"] * factor

    print(f"\n📊 Статистика за сьогодні ({today})")
    for meal, kcal in per_meal.items():
        print(f"• {meal}: {round(kcal,1)} ккал")

    print(f"\n🔥 Всього: {round(total['kcal'],1)} ккал")
    print(f"🥩 Білки: {round(total['protein'],1)} г")
    print(f"🧈 Жири: {round(total['fat'],1)} г")
    print(f"🍞 Вуглеводи: {round(total['carbs'],1)} г")

# ---------- СТАТИСТИКА ЗА 7 ДНІВ ----------
def stats_week(entries):
    start = date.today() - timedelta(days=6)
    per_day = defaultdict(float)

    for e in entries:
        if e["date"] >= start:
            per_day[e["date"]] += e["kcal"]

    print("\n📈 Останні 7 днів:")
    for d in sorted(per_day):
        print(f"{d}: {round(per_day[d],1)} ккал")

    if per_day:
        avg = sum(per_day.values()) / len(per_day)
        print(f"\n📉 Середнє за день: {round(avg,1)} ккал")

# ---------- ГОЛОВНИЙ ЗАПУСК ----------
if __name__ == "__main__":
    foods = load_foods()
    diary = load_diary()

    if diary:
        stats_today(diary, foods)
        stats_week(diary)
