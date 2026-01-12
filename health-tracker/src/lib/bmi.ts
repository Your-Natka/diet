export function calculateBMI(weight: number, height: number) {
  const h = height / 100;
  const bmi = weight / (h * h);

  let status = "Норма";

  if (bmi < 18.5) status = "Недостатня вага";
  else if (bmi >= 25 && bmi < 30) status = "Надмірна вага";
  else if (bmi >= 30) status = "Ожиріння";

  return {
    bmi: bmi.toFixed(1),
    status,
  };
}
