import { useNavigate } from "react-router-dom";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuGroup, 
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import { ChevronDown, Library, LogOut, MessageSquareWarning, Settings, UserCircle } from "lucide-react";
import { useAuthContext } from "@/context/auth-context";

const HeaderNavigationItem = (props) => {
  const { name, link } = props

  const navigate = useNavigate()
  return (
      <div className="text-zinc-600 text-xl hover:text-black mr-6" onClick={() => navigate(link)}>
          {name}
      </div>
  )
}


const Header = () => {
  const { currentUser, logout } = useAuthContext()
  const navigate = useNavigate()


  return (
    <header className="sticky top-0 w-full h-[100px] px-10 py-5 shadow flex items-center justify-between bg-white">
      <div className="flex items-center flex-1 text-indigo-600 font-semibold text-3xl cursor-pointer" onClick={() => router.push("/")}>
        <img
          src="/images/esp32cam.jpg"
          alt=""
          width={50}
          height={50}
          className="mr-3"
        />
        TRACKESP
      </div>
      <div className="flex items-center justify-between">
        <HeaderNavigationItem name="About" link="/about" />
        <HeaderNavigationItem name="Docs" link="/docs" />
        <HeaderNavigationItem name="How to use" link="/instruction" />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <div className="flex items-center cursor-pointer hover:bg-zinc-200 p-2 rounded-full">
              <UserCircle className="h-8 w-8 mr-2" />
              <ChevronDown className="h-8 w-8" />
            </div>
          </DropdownMenuTrigger>
          <DropdownMenuContent side="bottom" align="end">
            <DropdownMenuLabel className="text-lg">
              {currentUser?.username || 'Unknown'}
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem>
                <div className="flex items-center gap-2 text-md">
                  <Library className="h-4 w-4" />
                  Profile
                </div>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <div className="flex items-center gap-2 text-md">
                  <Settings className="h-4 w-4" />
                  Settings
                </div>
                
              </DropdownMenuItem>
              <DropdownMenuItem>
                <div className="flex items-center gap-2 text-md">
                  <MessageSquareWarning className="h-4 w-4" />
                  Feedbacks
                </div>
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <div
                onClick={async () => {
                  await logout()
                }}
                className="flex items-center gap-2 text-md"
              >
                <LogOut className="h-4 w-4" />
                Log out
              </div>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
};

export default Header;
