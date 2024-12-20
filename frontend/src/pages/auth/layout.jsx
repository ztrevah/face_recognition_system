import { useAuthContext } from "@/context/auth-context";
import { Camera } from "lucide-react";
import { redirect } from "next/navigation";
import React from "react";

export default async function AuthLayout ({ children }) {
    const { currentUser } = useAuthContext()
    if(currentUser) {
        return redirect('/')
    }
    return (
        <div className="w-full h-full flex flex-col items-center m-auto">
            <header className="flex items-center text-3xl text-indigo-600 font-semibold mb-6">
                <Camera className="h-8 w-8 mr-2" />
                Traskesp
            </header>
            <main className="w-full">
                {children}
            </main>
        </div>
    )
}