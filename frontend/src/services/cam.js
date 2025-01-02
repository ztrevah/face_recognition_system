import ENDPOINT from "@/config/endpoint";
import request from "@/utils/requests";

const getCameras = (params = {}) => {
  return request({
    url: ENDPOINT.CAMERA,
    method: "get",
    params,
  });
};

const getAttendances = (cam_id, params = {}) => {
  return request({
    url: ENDPOINT.CAMERA_LOGS.replace(":cam_id", cam_id),
    method: "get",
    params,
  });
};

const postCamera = (data) => {
  return request({
    url: ENDPOINT.CAMERA,
    method: "post",
    data,
  });
};

const deleteCamera = (data) => {
  return request({
    url: ENDPOINT.CAMERA,
    method: "delete",
    data,
  });
};

export default {
  getCameras,
  getAttendances,
  postCamera,
  deleteCamera,
};
