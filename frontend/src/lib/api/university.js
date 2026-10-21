import { api } from "./client";

export const universityApi = {
  getPosts: (query) => api.get("/university-posts/", { query }),
};
