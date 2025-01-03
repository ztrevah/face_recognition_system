import Header from "@/components/header/header";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Check, Loader2, PlusCircle, X } from "lucide-react";
import { useEffect, useState } from "react";
import cameraService from "@/services/cam";
import { Button } from "@/components/ui/button";
import AddCameraModal from "@/components/home/add-camera-modal";
import subscribeService from "@/services/subscribe";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import DeleteCameraModal from "@/components/home/delete-camera-modal";

const HomePage = (props) => {
  const [cameraList, setCameraList] = useState([]);
  const [displayedCameraList, setDisplayedCameraList] = useState([]);
  const [queryName, setQueryName] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [deleteCamera, setDeleteCamera] = useState();
  const getCameraList = async () => {
    try {
      setIsLoading(true);
      const res = await cameraService.getCameras();
      const subscriptionList =
        (await subscribeService.getSubscriptions())?.data || [];
      setCameraList(
        res?.data
          ?.map((camera) => ({
            ...camera,
            subscribed: subscriptionList.some(
              (subscription) => subscription.cam_id === camera.id
            ),
          }))
          .sort((a, b) => a - b)
      );
    } catch (err) {
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    getCameraList();
  }, []);

  useEffect(() => {
    setQueryName("");
  }, [cameraList]);

  useEffect(() => {
    setDisplayedCameraList(
      cameraList.filter((camera) => camera.name.includes(queryName || ""))
    );
  }, [queryName, cameraList]);

  const changeSubscriptionStatus = async (camera) => {
    try {
      if (camera.subscribed)
        await subscribeService.deleteSubscription({ cam_id: camera.id });
      else await subscribeService.createSubscription({ cam_id: camera.id });
      getCameraList();
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="w-full h-full">
      <Header />
      <main className="h-full mt-12">
        <div className="w-full lg:w-[800px] mx-auto">
          <div className="flex flex-col">
            <div className="flex justify-between mb-6">
              <span className="text-xl font-semibold">Camera lists</span>
              <Button
                className="flex items-center text-sm hover:border-0"
                onClick={() => setAddModalOpen(true)}
              >
                <PlusCircle className="w-4 h-4 text-green-500" />
                Add
              </Button>
            </div>
            <Input
              placeholder="Filter by name"
              value={queryName}
              onChange={(event) => {
                setQueryName(event.target.value);
              }}
              className="max-w-sm"
            />
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[100px] whitespace-nowrap overflow-hidden text-ellipsis">
                    ID
                  </TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Subscribe</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center">
                      <Loader2 className="mx-auto h-6 w-6 animate-spin" />
                    </TableCell>
                  </TableRow>
                ) : (
                  <>
                    {displayedCameraList.map((camera, index) => (
                      <TableRow key={index}>
                        <TableCell className="w-[100px] font-medium whitespace-nowrap overflow-hidden text-ellipsis">
                          <Link to={`/camera/${camera?.id}/general`}>
                            {camera?.id || ""}
                          </Link>
                        </TableCell>
                        <TableCell>{camera?.name || ""}</TableCell>
                        <TableCell>{camera?.location || ""}</TableCell>
                        <TableCell>
                          {camera?.subscribed ? (
                            <Check className="h-4 w-4 text-green-500" />
                          ) : (
                            <X className="h-4 w-4 text-red-600" />
                          )}
                        </TableCell>
                        <TableCell>
                          <DropdownMenu>
                            <DropdownMenuTrigger>...</DropdownMenuTrigger>
                            <DropdownMenuContent>
                              <DropdownMenuItem>
                                <div
                                  onClick={() =>
                                    changeSubscriptionStatus(camera)
                                  }
                                >
                                  {camera?.subscribed
                                    ? "Unsubscribe"
                                    : "Subscribe"}
                                </div>
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => {
                                  setDeleteModalOpen(true);
                                  setDeleteCamera(camera);
                                }}
                              >
                                Delete
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    ))}
                  </>
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      </main>
      <AddCameraModal
        open={addModalOpen}
        setOpen={setAddModalOpen}
        getCameraList={getCameraList}
      />
      <DeleteCameraModal
        open={deleteModalOpen}
        setOpen={setDeleteModalOpen}
        camera={deleteCamera}
        getCameraList={getCameraList}
      />
    </div>
  );
};

export default HomePage;
