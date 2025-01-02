import ENDPOINT from "@/config/endpoint";
import request from "@/utils/requests";

const getSubscriptions = (params = {}) => {
  return request({
    url: ENDPOINT.SUBSCRIPTION,
    method: "get",
    params,
  });
};

const createSubscription = (data = {}) => {
  return request({
    url: ENDPOINT.SUBSCRIPTION,
    method: "post",
    data,
  });
};

const deleteSubscription = (data = {}) => {
  return request({
    url: ENDPOINT.SUBSCRIPTION,
    method: "delete",
    data,
  });
};

export default {
  getSubscriptions,
  createSubscription,
  deleteSubscription,
};
