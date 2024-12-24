import { ScrollArea } from "../ui/scroll-area";
import { Separator } from "../ui/separator";

const Sidebar = () => {
  return (
    <div className="fixed top-[100px] left-0 w-[200px] p-5 flex flex-col">
      <ScrollArea className="rounded border">
        <h4 className="p-3">Overview</h4>
        <Separator />
        <h4 className="p-3">Members</h4>
        <Separator />
        <h4 className="p-3">Logs</h4>
        <Separator />
        <h4 className="p-3">Settings</h4>
      </ScrollArea>
    </div>
  );
};

export default Sidebar;
