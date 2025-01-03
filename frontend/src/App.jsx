import "./App.css";
import { useEffect } from "react";
import {
  createBrowserRouter,
  Outlet,
  RouterProvider,
  useNavigate,
} from "react-router-dom";

import { useAuth } from "./context/auth-context";

import HomePage from "./pages/main/home";
import SignInPage from "./pages/auth/signin";
import SignUpPage from "./pages/auth/signup";
import Error404Page from "./pages/error/404";
import CameraIdPage from "./pages/main/camera-id";

const ProtectedRoute = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (!currentUser) {
      navigate("/sign-in", { replace: true });
    }
  }, [navigate, currentUser]);

  return <Outlet />;
};

const RegisterRoute = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  useEffect(() => {
    if (currentUser) {
      navigate("/", { replace: true });
    }
  }, [navigate, currentUser]);

  return <Outlet />;
};

const router = createBrowserRouter([
  {
    element: <RegisterRoute />,
    children: [
      {
        path: "/sign-in",
        element: <SignInPage />,
      },
      {
        path: "/sign-up",
        element: <SignUpPage />,
      },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/camera/:cam_id/general",
        element: <CameraIdPage />,
      },
      {
        path: "/camera/:cam_id/members",
        element: <CameraIdPage />,
      },
      {
        path: "/camera/:cam_id/logs",
        element: <CameraIdPage />,
      },
    ],
  },
  {
    path: "*",
    element: <Error404Page />,
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
