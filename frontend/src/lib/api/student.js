import { api } from "./client";

export const studentApi = {
  getMe: () => api.get("/student/me"),
  uploadAvatar: (file) => {
    const form = new FormData();
    form.append("file", file);
    return api.upload("/student/avatar", form);
  },
  updateAdditionalInfo: ({ linkedin_url, instagram_url, cv }) => {
    const form = new FormData();
    if (linkedin_url) form.append("linkedin_url", linkedin_url);
    if (instagram_url) form.append("instagram_url", instagram_url);
    if (cv) form.append("cv", cv);
    return api.upload("/student/additional-info", form, "PATCH");
  },
  getFeed: (query) => api.get("/feed/", { query }),
  getFeedPost: (id) => api.get(`/feed/${id}`),
};
