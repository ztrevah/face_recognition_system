import axios from "axios";

const request = axios.create({
  withCredentials: true,
  timeout: 30000, // Set timeout to 5 seconds
  headers: {
    "Content-Type": "application/json", // Set content type to JSON
  },
});

// Add a response interceptor
request.interceptors.response.use(
  (response) => {
    // Handle successful responses
    return response;
  },
  (error) => {
    console.log(error);
    // if (error.response) {
    //   console.error('Error status', error.response.status)
    //   console.error('Error data', error.response.data)
    // } else if (error.request) {
    //   console.error('No response received', error.request)
    // } else {
    //   console.error('Request error', error.message)
    // }
    return Promise.reject(error);
  },
);

export default request;
