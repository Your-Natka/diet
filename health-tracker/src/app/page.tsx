import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center text-center p-6">
      <h1 className="text-4xl font-bold mb-4">Контролюй своє здоров’я</h1>

      <p className="text-gray-600 mb-8 max-w-md">
        Відстежуй вагу, харчування та прогрес схуднення в одному місці
      </p>

      <div className="flex gap-4">
        <Link
          href="/register"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg"
        >
          Почати
        </Link>

        <Link href="/login" className="px-6 py-3 border rounded-lg">
          Увійти
        </Link>
      </div>
    </main>
  );
}
