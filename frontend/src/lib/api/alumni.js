import { api } from "./client";

export const alumniApi = {
  getProfile: () => api.get("/alumni/profile/"),
  updateProfile: (data) => api.put("/alumni/profile/", data),
  uploadAvatar: (file) => {
    const form = new FormData();
    form.append("file", file);
    return api.upload("/alumni/profile/avatar", form);
  },

  getStats: () => api.get("/alumni/dashboard/stats"),

  getMyPosts: (query) => api.get("/alumni/posts/", { query }),
  getPost: (id) => api.get(`/alumni/posts/${id}`),
  createPost: (data) => api.post("/alumni/posts/", data),
  updatePost: (id, data) => api.put(`/alumni/posts/${id}`, data),
  deletePost: (id) => api.delete(`/alumni/posts/${id}`),
  uploadMedia: (file) => {
    const form = new FormData();
    form.append("file", file);
    return api.upload("/alumni/posts/upload-media", form);
  },

  getFeed: (query) => api.get("/alumni/feed/", { query }),
  getFeedPost: (id) => api.get(`/alumni/feed/${id}`),
};
