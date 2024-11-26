import Header from "@/components/header/header";

export default function MainLayout({
    children
}: { children: React.ReactNode }) {
    return (
        <>
            <Header />
            <main className="h-full">
                {children}
            </main>
        </>
    );
  }