import Header from "@/components/header/header";
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbSeparator,
  BreadcrumbLink,
} from "@/components/ui/breadcrumb";
import { Slash } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router-dom";
import cameraService from "@/services/cam";
import { Menubar, MenubarMenu, MenubarTrigger } from "@/components/ui/menubar";
import useWebSocket from "react-use-websocket";
import { getLogsWsEndpoint, getStreamingWsEndpoint } from "@/utils/common";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import dayjs from "dayjs";
import timezone from "dayjs/plugin/timezone";
dayjs.extend(timezone);
dayjs.tz.setDefault("Asia/Ho_Chi_Minh");

const CameraIdPage = (props) => {
  const [cameraInfo, setCameraInfo] = useState();
  const [imageFromCamera, setImageFromCamera] = useState("");
  const [attendances, setAttendances] = useState([]);
  const params = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const {} = useWebSocket(getStreamingWsEndpoint(params?.cam_id || ""), {
    onOpen: () => console.log("WebSocket connection opened!"),
    onClose: () => console.log("WebSocket connection closed!"),
    onError: (event) => console.error("WebSocket error:", event),
    onMessage: (event) => {
      setImageFromCamera(event.data);
    },
  });

  const {} = useWebSocket(getLogsWsEndpoint(params?.cam_id || ""), {
    onOpen: () => console.log("WebSocket connection opened!"),
    onClose: () => console.log("WebSocket connection closed!"),
    onError: (event) => console.error("WebSocket error:", event),
    onMessage: (event) => {
      attendances.unshift(JSON.parse(event.data));
    },
  });

  useEffect(() => {
    const getCameraInfo = async () => {
      try {
        const res = await cameraService.getCamera(params?.cam_id);
        setCameraInfo(res?.data);
      } catch (err) {
        navigate("/");
      }
    };
    getCameraInfo();
  }, [params?.id]);

  return (
    <div className="w-full h-full">
      <Header />
      <main className="h-full mt-12">
        <div className="w-full mb-12">
          <div className="w-full px-[100px]">
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbLink href="/">Home</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator>
                  <Slash />
                </BreadcrumbSeparator>
                <BreadcrumbItem>
                  <BreadcrumbLink href="/">Camera</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator>
                  <Slash />
                </BreadcrumbSeparator>
                <BreadcrumbItem>
                  <BreadcrumbLink href={`/camera/${params.cam_id || ""}`}>
                    {params.cam_id}
                  </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator>
                  <Slash />
                </BreadcrumbSeparator>
                <BreadcrumbItem>
                  <BreadcrumbLink href={`/camera/${params.cam_id || ""}`}>
                    General
                  </BreadcrumbLink>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
            <div className="w-full flex justify-between my-4">
              <span className="text-lg font-semibold text-rose-600">
                Camera name:{" "}
                <span className="text-zinc-700 font-medium">
                  {cameraInfo?.name || ""}
                </span>
              </span>
              <span className="text-lg font-semibold text-rose-600">
                Camera location:{" "}
                <span className="text-zinc-700 font-medium">
                  {cameraInfo?.location || ""}
                </span>
              </span>
            </div>
            <Menubar>
              <MenubarMenu>
                <MenubarTrigger className="focus:border-none hover:border-none">
                  <Link
                    className={
                      location.pathname.endsWith("general")
                        ? "text-indigo-600 hover:text-indigo-600"
                        : "text-black hover:text-black"
                    }
                    to={`/camera/${params.cam_id}/general`}
                  >
                    General
                  </Link>
                </MenubarTrigger>
              </MenubarMenu>
              <MenubarMenu>
                <MenubarTrigger className="focus:border-none hover:border-none">
                  <Link
                    className={
                      location.pathname.endsWith("members")
                        ? "text-indigo-600 hover:text-indigo-600"
                        : "text-black hover:text-black"
                    }
                    to={`/camera/${params.cam_id}/members`}
                  >
                    Members
                  </Link>
                </MenubarTrigger>
              </MenubarMenu>
              <MenubarMenu>
                <MenubarTrigger className="focus:border-none hover:border-none">
                  <Link
                    className={
                      location.pathname.endsWith("logs")
                        ? "text-indigo-600 hover:text-indigo-600"
                        : "text-black hover:text-black"
                    }
                    to={`/camera/${params.cam_id}/logs`}
                  >
                    Logs
                  </Link>
                </MenubarTrigger>
              </MenubarMenu>
            </Menubar>
          </div>
        </div>
        <div className="flex px-[100px] flex-col lg:flex-row gap-6 mb-12">
          <img
            src={`data:image/png;base64, ${imageFromCamera}`}
            onError={(e) => (e.currentTarget.src = "/images/error.png")}
            height={480}
            width={640}
            alt="Camera stream"
            className="border rounded-md h-[480px] w-[640px] object-cover"
          />
          <div className="flex flex-col gap-6">
            <div className="text-lg font-semibold text-indigo-500">
              Attendances
            </div>
            <Table className="w-full">
              <TableHeader>
                <TableRow>
                  <TableHead className="min-w-[150px] text-center">
                    Time
                  </TableHead>
                  <TableHead className="min-w-[150px] text-center">
                    Member ID
                  </TableHead>
                  <TableHead className="min-w-[150px] text-center">
                    Name
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {attendances.map((attendance, index) => (
                  <TableRow key={index}>
                    <TableCell className="font-medium">
                      {dayjs(attendance.time).format("YYYY-MM-DD HH:mm:ss")}
                    </TableCell>
                    <TableCell>{attendance.member.id}</TableCell>
                    <TableCell>{attendance.member.name}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      </main>
    </div>
  );
};

export default CameraIdPage;
