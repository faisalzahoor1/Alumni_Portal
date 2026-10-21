import { api } from "./client";

export const engagementApi = {
  react: (postId, reaction) => api.put(`/posts/${postId}/reaction`, { reaction }),
  getComments: (postId) => api.get(`/posts/${postId}/comments`),
  addComment: (postId, content, parent_id) => api.post(`/posts/${postId}/comments`, { content, parent_id }),
  report: (postId, reason, details) => api.post(`/posts/${postId}/report`, { reason, details }),
  deleteComment: (postId, commentId) => api.delete(`/posts/${postId}/comments/${commentId}`),
};
