import axiosClient from './axiosClient';

const phishingApi = {
  welcome() {
    return axiosClient.get(`${import.meta.env.PD_PHISHING_API_BASE}`);
  },
  predict(data) {
    return axiosClient.post(`${import.meta.env.PD_PHISHING_API_BASE}/predict`, data);
  },
};

export default phishingApi;
