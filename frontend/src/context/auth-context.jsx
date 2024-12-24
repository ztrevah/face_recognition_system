import { createContext, useContext, useEffect, useState } from "react";
import authServices from "@/services/auth";

export const AuthContext = createContext();

export const AuthContextProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(
    JSON.parse(localStorage.getItem("current_user"))
  );

  const signin = async (data) => {
    try {
      const res = await authServices.signin(data);
      setCurrentUser(res.data);
      localStorage.setItem("current_user", JSON.stringify(res.data));
    } catch (err) {
      console.log(err);
      throw new Error(
        err.response.data.error.message || "There has been an error."
      );
    }
  };

  const signup = async (data) => {
    try {
      const res = await authServices.signup(data);
    } catch (err) {
      console.log(err);
      throw new Error(
        err.response.data.error.message || "There has been an error."
      );
    }
  };

  const logout = async () => {
    try {
      const res = await authServices.logout();
      setCurrentUser(null);
      localStorage.removeItem("current_user");
    } catch (err) {
      console.log(err);
    }
  };

  const getCurrentUser = async () => {
    try {
      const res = await authServices.verify();
      setCurrentUser(res.data);
      localStorage.setItem("current_user", JSON.stringify(res.data));
      return res.data;
    } catch (err) {
      console.log(err);
      setCurrentUser(null);
      localStorage.removeItem("current_user");
    }
  };

  useEffect(() => {
    getCurrentUser();
  }, []);

  return (
    <AuthContext.Provider
      value={{ currentUser, signin, signup, getCurrentUser, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    console.log("useCounter must be used within a AuthContextProvider");
  }
  return context;
};
