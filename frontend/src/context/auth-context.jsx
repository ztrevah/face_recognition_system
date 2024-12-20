import { createContext, useContext, useEffect, useState } from "react";
import authServices from "@/services/auth";

export const AuthContext = createContext<any>(undefined)

export const AuthContextProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null)
    
    const signin = async (data) => {
        try {
            const res = await authServices.signin(data)
            setCurrentUser(res.data)
            return res.data
        } catch(err) {
            throw err
        }
    }

    const signup = async(data) => {
        try {
            const res = await authServices.signup(data)
            setCurrentUser(res.data)
            return res.data
        } catch(err) {
            throw err
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
            const res = await authServices.verify()
            setCurrentUser(res.data)
            return res.data
        } catch(err) {
            console.log(err)
        }
    }

    useEffect(() => {
        getCurrentUser()
    }, [])

    return (
        <AuthContext.Provider value={{currentUser, signin, signup, getCurrentUser, logout}}>
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