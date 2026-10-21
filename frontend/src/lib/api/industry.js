import { api } from "./client";

export const industryApi = {
  getProfile: () => api.get("/industry/profile/"),
  updateProfile: (data) => api.put("/industry/profile/", data),
  uploadLogo: (file) => {
    const form = new FormData();
    form.append("file", file);
    return api.upload("/industry/profile/logo", form);
  },

  getStats: () => api.get("/industry/dashboard/stats"),

  getJobs: () => api.get("/industry/jobs/"),
  createJob: (data) => api.post("/industry/jobs/", data),
  updateJob: (id, data) => api.put(`/industry/jobs/${id}`, data),
  deleteJob: (id) => api.delete(`/industry/jobs/${id}`),
  getApplicants: (jobId) => api.get(`/industry/jobs/${jobId}/applicants`),
  updateApplicationStatus: (jobId, appId, status) =>
    api.put(`/industry/jobs/${jobId}/applicants/${appId}/status`, { status }),

  getMyPosts: (query) => api.get("/industry/posts/", { query }),
  createPost: (data) => api.post("/industry/posts/", data),
  updatePost: (id, data) => api.put(`/industry/posts/${id}`, data),
  deletePost: (id) => api.delete(`/industry/posts/${id}`),
  uploadMedia: (file) => {
    const form = new FormData();
    form.append("file", file);
    return api.upload("/industry/posts/upload-media", form);
  },

  getFeed: (query) => api.get("/industry/feed/", { query }),
  getFeedPost: (id) => api.get(`/industry/feed/${id}`),
};
