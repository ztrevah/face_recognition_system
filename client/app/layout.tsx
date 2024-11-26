import type { Metadata } from "next";
import { Open_Sans } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const font = Open_Sans({subsets: ['latin']});

export const metadata: Metadata = {
  title: "Trackesp",
  description: "IoT tracking system via ESP32 CAM",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn(font.className, "flex flex-col min-h-screen")}
      >
        {children}
      </body>
    </html>
  );
}
