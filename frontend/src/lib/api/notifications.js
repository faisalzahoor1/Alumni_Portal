import { api } from "./client";

// Alumni and industry expose identical notification endpoints under their own prefix.
export function notificationsApi(role) {
  const base = `/${role}/notifications`;
  return {
    list: (query) => api.get(`${base}/`, { query }),
    unreadCount: () => api.get(`${base}/unread-count`),
    markRead: (id) => api.put(`${base}/${id}/read`),
    markAllRead: () => api.put(`${base}/read-all`),
    remove: (id) => api.delete(`${base}/${id}`),
  };
}
