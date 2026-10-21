import { api } from "./client";

export const authApi = {
  signup: (data) => api.post("/auth/signup", data, { auth: false }),
  verifyEmail: (data) => api.post("/auth/verify-email", data, { auth: false }),
  studentLogin: (data) => api.post("/auth/login", data, { auth: false }),
  userLogin: (data) => api.post("/auth/user/login", data, { auth: false }),
  refresh: (refresh_token) => api.post("/auth/refresh", { refresh_token }, { auth: false }),
};
