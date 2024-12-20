import { useRouter } from "next/navigation";
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

const HeaderNavigationItem = (props) => {
  const { name, link } = props

  const router = useRouter();
  return (
      <div className="text-zinc-600 text-xl hover:text-black mr-6" onClick={() => router.push(link)}>
          {name}
      </div>
  )
}
const Header = () => {
  const router = useRouter();
  return (
    <header className="sticky top-0 w-full h-[100px] px-10 py-5 shadow flex items-center justify-between bg-white">
      <div className="flex items-center flex-1 text-indigo-600 font-semibold text-3xl cursor-pointer" onClick={() => router.push("/")}>
        <Image
          src="/esp32cam.png"
          alt="Logo"
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
              Chien Nguyen
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem>
                <Library />
                Profile
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Settings />
                Settings
              </DropdownMenuItem>
              <DropdownMenuItem>
                <MessageSquareWarning />
                Feedbacks
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <LogOut />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
};

export default Header;
