"use client";

import { useState } from "react";
import { calculateBMI } from "../../lib/bmi";

export default function DashboardPage() {
  const [weight, setWeight] = useState("");
  const [height, setHeight] = useState("");
  const [targetLoss, setTargetLoss] = useState("");
  const [months, setMonths] = useState("");

  const [bmiResult, setBmiResult] = useState<{
    bmi: string;
    status: string;
  } | null>(null);

  const [planResult, setPlanResult] = useState<string | null>(null);

  const handleCalculate = () => {
    if (!weight || !height || !targetLoss || !months) {
      setPlanResult("Будь ласка, заповни всі поля");
      return;
    }

    const bmi = calculateBMI(Number(weight), Number(height));
    setBmiResult(bmi);

    const weeklyLoss = Number(targetLoss) / (Number(months) * 4);

    setPlanResult(
      `Ціль: скинути ${targetLoss} кг за ${months} місяців
≈ ${weeklyLoss.toFixed(1)} кг на тиждень`
    );
  };

  return (
    <main className="min-h-screen p-6 max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">Персональний план</h1>

      <div className="flex flex-col gap-4">
        <input
          type="number"
          placeholder="Поточна вага (кг)"
          className="border rounded-lg px-4 py-2"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
        />

        <input
          type="number"
          placeholder="Зріст (см)"
          className="border rounded-lg px-4 py-2"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
        />

        <input
          type="number"
          placeholder="Хочу скинути (кг)"
          className="border rounded-lg px-4 py-2"
          value={targetLoss}
          onChange={(e) => setTargetLoss(e.target.value)}
        />

        <input
          type="number"
          placeholder="Термін (місяці)"
          className="border rounded-lg px-4 py-2"
          value={months}
          onChange={(e) => setMonths(e.target.value)}
        />

        <button
          onClick={handleCalculate}
          className="bg-green-600 text-white rounded-lg py-2 font-medium"
        >
          Розрахувати
        </button>

        {bmiResult && (
          <div className="mt-4 p-4 bg-blue-50 rounded-lg text-center">
            <p className="font-medium">ІМТ: {bmiResult.bmi}</p>
            <p>Статус: {bmiResult.status}</p>
          </div>
        )}

        {planResult && (
          <div className="mt-4 p-4 bg-gray-100 rounded-lg text-center whitespace-pre-line">
            {planResult}
          </div>
        )}
      </div>
    </main>
  );
}
