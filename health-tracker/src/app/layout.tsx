import "./globals.css";

export const metadata = {
  title: "Health Tracker",
  description: "Контроль здоров’я та схуднення",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="uk">
      <body>{children}</body>
    </html>
  );
}
