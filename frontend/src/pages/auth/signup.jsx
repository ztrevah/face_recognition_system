import SignUpForm from "@/components/auth/signup-form";

const SignUpPage = (props) => {
    return (
        <div className="w-full h-full flex flex-col items-center m-auto">
            <header className="flex items-center text-3xl text-indigo-600 font-semibold mb-6">
                <Camera className="h-8 w-8 mr-2" />
                Traskesp
            </header>
            <main className="w-full">
                <div className="w-full flex flex-col items-center">
                    <div className="text-xl font-medium mb-4">
                        Create your account
                    </div>
                    <div className="text-lg text-zinc-700 font-medium mb-6">
                        Welcome! Please fill in the details to get started.
                    </div>
                    <SignUpForm />
                </div>
            </main>
        </div>
    )
}

export default SignUpPage