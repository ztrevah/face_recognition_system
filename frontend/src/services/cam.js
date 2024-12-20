import ENDPOINT from "@/config/endpoint";
import request from "@/utils/requests";

const getCameras = (params = {}) => {
    return request({
        url: ENDPOINT.CAMERA,
        method: 'get',
        params
    })
}

export default {
    getCameras
}