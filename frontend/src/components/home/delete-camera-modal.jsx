import { useState } from "react";
import { Button } from "../ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogDescription,
  DialogFooter,
  DialogTitle,
} from "../ui/dialog";
import cameraService from "@/services/cam";
import { Input } from "../ui/input";
const DeleteCameraModal = (props) => {
  const { open, setOpen, camera, getCameraList } = props;
  const [isLoading, setIsLoading] = useState(false);
  const [authToken, setAuthToken] = useState("");
  const [error, setError] = useState("");
  const onClose = () => {
    setOpen(false);
    setError("");
  };
  const onDelete = async () => {
    try {
      setIsLoading(true);
      await cameraService.deleteCamera({
        cam_id: camera.id,
        auth_token: authToken,
      });
      onClose();
      getCameraList();
    } catch (err) {
      console.log(err);
      setError(err.response.data.error.message || "Error");
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="overflow-hidden bg-white p-0 text-black">
        <DialogHeader className="px-6 pt-8">
          <DialogTitle className="text-center text-2xl font-bold">
            Delete Camera
          </DialogTitle>
          <DialogDescription className="text-center text-zinc-500">
            Are you sure you want to do this? <br />
            <span className="font-semibold text-indigo-500">
              {camera?.name}
            </span>{" "}
            will be permanently deleted.
          </DialogDescription>
        </DialogHeader>
        <div className="w-full px-6">
          <Input
            type="password"
            value={authToken}
            onChange={(event) => setAuthToken(event.target.value)}
            placeholder="Enter the camera's auth token"
            className="border-0 bg-zinc-300/50 text-black focus-visible:ring-0 focus-visible:ring-offset-0"
          />
        </div>
        {error && (
          <p className="w-full text-center text-red-500 font-semibold">
            {error}
          </p>
        )}

        <DialogFooter className="bg-gray-100 px-6 py-4">
          <div className="flex w-full items-center justify-between">
            <Button disabled={isLoading} onClick={onClose} variant="ghost">
              Cancel
            </Button>
            <Button
              disabled={isLoading}
              variant="destructive"
              onClick={onDelete}
            >
              Confirm
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default DeleteCameraModal;
