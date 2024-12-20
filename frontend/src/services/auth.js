import ENDPOINT from "@/config/endpoint"
import request from "@/utils/requests"

const signin = (data) => {
  return request({
    url: ENDPOINT.SIGNIN,
    method: 'post',
    data
  })
}

const signup = (data) => {
  return request({
    url: ENDPOINT.SIGNUP,
    method: 'post',
    data
  })
}

const logout = () => {
  return request({
    url: ENDPOINT.LOGOUT,
    method: 'post',
  })
}

const verify = () => {
  return request({
    url: ENDPOINT.VERIFY,
    method: 'get',
  })
}

export default {
  signin,
  signup,
  logout,
  verify
}