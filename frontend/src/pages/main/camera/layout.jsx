import Sidebar from "@/components/sidebar/sidebar";

const CameraPageLayout = ({ children }) => {
    return (
        <div className="pl-[200px]">
            <Sidebar />
            {children}
        </div>
    )
}

export default CameraPageLayout;