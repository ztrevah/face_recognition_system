import { createContext, useContext, useEffect, useState } from "react";
import authServices from "@/services/auth";

export const AuthContext = createContext()

export const AuthContextProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    
    const signin = async (data) => {
        try {
            const res = await authServices.signin(data)
            setCurrentUser(res.data)
            // return res.data
        } catch(err) {
            console.log(err)
            throw new Error(err.response.data.error.message || 'There has been an error.')
        }
    }

    const signup = async(data) => {
        try {
            const res = await authServices.signup(data)
            // setCurrentUser(res.data)
            // return res.data
        } catch(err) {
            console.log(err)
            throw new Error(err.response.data.error.message || 'There has been an error.')
        }
    }

    const logout = async () => {
        try {
            const res = await authServices.logout()
            setCurrentUser(null)
        } catch(err) {
            console.log(err)
        }
    }

    const getCurrentUser = async () => {
        try {
            setIsLoading(true)
            const res = await authServices.verify()
            setCurrentUser(res.data)
            return res.data
        } catch(err) {
            console.log(err)
        } finally {
            setIsLoading(false)
        }
    }

    useEffect(() => {
        getCurrentUser()
    }, [])

    return (
        <AuthContext.Provider value={{currentUser, signin, signup, getCurrentUser, logout, isLoading}}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuthContext = () => {
    const context = useContext(AuthContext)
    if (!context) {
        console.log("useCounter must be used within a AuthContextProvider");
    }
    return context;
}