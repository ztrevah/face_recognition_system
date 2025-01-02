const API_URL = import.meta.env.VITE_PUBLIC_API_URL;
const WS_URL = import.meta.env.VITE_PUBLIC_WS_URL;

export default {
  SIGNUP: `${API_URL}/auth/signup/`,
  SIGNIN: `${API_URL}/auth/signin/`,
  LOGOUT: `${API_URL}/auth/logout/`,
  VERIFY: `${API_URL}/auth/verify/`,
  CAMERA: `${API_URL}/cameras/`,
  CAMERA_MEMBER: `${API_URL}/cameras/:cam_id/members/`,
  CAMERA_LOGS: `${API_URL}/cameras/:cam_id/attendances/`,
  CAMERA_STREAMING: `${WS_URL}/streaming/:cam_id/`,
  CAMERA_LOGS_WS: `${WS_URL}/logs/:cam_id/`,
  SUBSCRIPTION: `${API_URL}/subscriptions/`,
};
