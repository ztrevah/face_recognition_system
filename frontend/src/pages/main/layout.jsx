import Header from "@/components/header/header";

export default async function MainLayout({ children }) {
    return (
        <>
            <Header />
            <main className="h-full">
                {children}
            </main>
        </>
    );
}