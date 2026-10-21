import { api } from "./client";

const upload = (path, file) => {
  const form = new FormData();
  form.append("file", file);
  return api.upload(path, form);
};

export const adminApi = {
  getStats: () => api.get("/admin/dashboard/stats"),

  getRegistrations: (status) => api.get("/admin/registrations", { query: { status } }),
  approve: (userId) => api.post(`/admin/registrations/${userId}/approve`),
  reject: (userId) => api.post(`/admin/registrations/${userId}/reject`),

  searchUsers: (query) => api.get("/admin/users", { query }),
  deleteUser: (role, userId) => api.delete(`/admin/users/${role}/${userId}`),

  getPosts: () => api.get("/admin/posts", { query: { limit: 100 } }),
  createPost: (data) => api.post("/admin/posts", data),
  updatePost: (id, data) => api.put(`/admin/posts/${id}`, data),
  deletePost: (id) => api.delete(`/admin/posts/${id}`),
  uploadMedia: (file) => upload("/admin/posts/upload-media", file),

  getReports: (status) => api.get("/admin/reports", { query: { status } }),
  allowPost: (postId) => api.post(`/admin/reports/${postId}/dismiss`),
  deleteReportedPost: (postId) => api.delete(`/admin/reports/${postId}/post`),

  getNotifications: (query) => api.get("/admin/notifications", { query }),
  unreadCount: () => api.get("/admin/notifications/unread-count"),
  markRead: (id) => api.put(`/admin/notifications/${id}/read`),
  markAllRead: () => api.put("/admin/notifications/read-all"),
  deleteNotification: (id) => api.delete(`/admin/notifications/${id}`),

  getProfile: () => api.get("/admin/profile"),
  updateProfile: (data) => api.put("/admin/profile", data),
  uploadAvatar: (file) => upload("/admin/profile/avatar", file),
};
