import { createBrowserRouter, useNavigate } from 'react-router-dom'
import './App.css'
import { useAuthContext } from './context/auth-context';
import HomePage from './pages/main/home';
import SignInPage from './pages/auth/signin';
import SignUpPage from './pages/auth/signup';
import Error404Page from './pages/error/404';

const Route = (props) => {
  const navigate = useNavigate();
  const { currentUser } = useAuthContext();
  useEffect(() => {
    if(props?.type === "protected" && currentUser) {
      navigate("/sign-in", { replace: true });
    }
    if(props?.type === "register" && currentUser) {
      navigate("/", { replace: true });
    }
  }, [currentUser, props, navigate]);
  
  return <Outlet />
}

const router = createBrowserRouter([
  {
    element: <Route type="protected" />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
    ]
  },
  {
    element: <Route type="register" />,
    children: [
      {
        path: "/sign-in",
        element: <SignInPage />
      },
      {
        path: "/sign-up",
        element: <SignUpPage />
      }
    ],
  },
  {
    path: "*",
    element: <Error404Page />
  }
]);


const App = () => {
  return (
    <RouterProvider router={router} />
  );
}

export default App
