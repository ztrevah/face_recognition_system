export const getStreamingWsEndpoint = (cam_id) => {
  const WS_URL = import.meta.env.VITE_PUBLIC_WS_URL;
  return `${WS_URL}/streaming/${cam_id}/`;
};

export const getLogsWsEndpoint = (cam_id) => {
  const WS_URL = import.meta.env.VITE_PUBLIC_WS_URL;
  return `${WS_URL}/logs/${cam_id}/`;
};
