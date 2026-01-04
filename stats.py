import csv
from datetime import date, datetime, timedelta
from collections import defaultdict

def load_diary(file_path="diary.csv"):
    entries = []
    try:
        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row["date"] or not row["kcal"]:
                    continue
                entries.append({
                    "date": datetime.fromisoformat(row["date"]).date(),
                    "meal": row["meal"],
                    "product": row["product"],
                    "grams": float(row["grams"]),
                    "kcal": float(row["kcal"])
                })
    except FileNotFoundError:
        print("❌ Файл diary.csv не знайдено")
    return entries

def stats_today(entries):
    today = date.today()
    total = 0
    per_meal = defaultdict(float)
    for e in entries:
        if e["date"] == today:
            total += e["kcal"]
            per_meal[e["meal"]] += e["kcal"]

    print(f"\n📊 Статистика за сьогодні ({today}):")
    for meal, kcal in per_meal.items():
        print(f"• {meal}: {round(kcal,1)} ккал")
    print(f"🔥 Всього за день: {round(total,1)} ккал")

def stats_week(entries):
    start = date.today() - timedelta(days=6)
    per_day = defaultdict(float)
    for e in entries:
        if e["date"] >= start:
            per_day[e["date"]] += e["kcal"]

    print("\n📈 Статистика за 7 днів:")
    for d in sorted(per_day):
        print(f"{d}: {round(per_day[d],1)} ккал")

    if per_day:
        avg = sum(per_day.values()) / len(per_day)
        print(f"\n📉 Середнє за день: {round(avg,1)} ккал")

# --- Головний виклик ---
if __name__ == "__main__":
    diary_entries = load_diary()
    if diary_entries:
        stats_today(diary_entries)
        stats_week(diary_entries)
