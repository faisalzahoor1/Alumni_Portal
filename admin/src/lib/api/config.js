import { api } from "./client";

export const configApi = {
  get: () => api.get("/config/", { auth: false }),
};
