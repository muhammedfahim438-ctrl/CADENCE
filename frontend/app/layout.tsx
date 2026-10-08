import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CADENCE - OPD Waste Taxonomy",
  description: "Hospital OPD waste taxonomy classifier and coverage dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen">{children}</body>
    </html>
  );
}
