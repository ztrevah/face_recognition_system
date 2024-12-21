import SignInForm from "@/components/auth/signin-form";
import { Toaster } from "@/components/ui/toaster";
import { Camera } from "lucide-react";

const SignInPage = (props) => {
    return (
        <div className="w-full min-h-screen flex flex-col items-center justify-center">
            <header className="flex items-center text-3xl text-indigo-600 font-semibold mb-6">
                <Camera className="h-8 w-8 mr-2" />
                Traskesp
            </header>
            <main className="">
                <div className="flex flex-col items-center">
                    <div className="text-xl font-medium mb-4">
                        Let's get started
                    </div>
                    <div className="text-lg text-zinc-700 font-medium mb-6">
                        Welcome back! Please sign in to continue
                    </div>
                    <SignInForm />
                </div>
            </main>
            <Toaster />
        </div>
    )
}

export default SignInPage