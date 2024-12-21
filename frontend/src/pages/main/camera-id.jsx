import Header from "@/components/header/header";
import Sidebar from "@/components/sidebar/sidebar";

const CameraIdPage = (props) => {
    return (
        <div className="w-full h-full">
            <Header />
            <main className="h-full">
                <div className="pl-[200px]">
                    <Sidebar />
                    Camera Id Page
                </div>
            </main>
        </div>
    )
}

export default CameraIdPage;