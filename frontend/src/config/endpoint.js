const BACKEND_URL = import.meta.env.VITE_PUBLIC_API_URL

export default {
    SIGNUP: `${BACKEND_URL}/auth/signup/`,
    SIGNIN: `${BACKEND_URL}/auth/signin/`,
    LOGOUT: `${BACKEND_URL}/auth/logout/`,
    VERIFY: `${BACKEND_URL}/auth/verify/`,
    CAMERA: `${BACKEND_URL}/cameras/`,
    CAMERA_MEMBER: `${BACKEND_URL}/cameras/:cam_id/members/`,
    CAMERA_LOGS: `${BACKEND_URL}/cameras/:cam_id/logs/`,
}