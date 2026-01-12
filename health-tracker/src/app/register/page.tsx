import Link from "next/link";

export default function RegisterPage() {
  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full max-w-md border rounded-xl p-6 shadow-sm">
        <h1 className="text-2xl font-bold mb-4 text-center">Реєстрація</h1>

        <form className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Імʼя"
            className="border rounded-lg px-4 py-2"
          />

          <input
            type="email"
            placeholder="Email"
            className="border rounded-lg px-4 py-2"
          />

          <input
            type="password"
            placeholder="Пароль"
            className="border rounded-lg px-4 py-2"
          />

          <button
            type="submit"
            className="bg-blue-600 text-white rounded-lg py-2 font-medium"
          >
            Зареєструватися
          </button>
        </form>

        <p className="text-sm text-center mt-4">
          Уже є акаунт?{" "}
          <Link href="/login" className="text-blue-600">
            Увійти
          </Link>
        </p>
      </div>
    </main>
  );
}
