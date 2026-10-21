import { api } from "./client";

export const messagesApi = {
  listConversations: () => api.get("/messages/conversations"),
  startConversation: (recipient_id) => api.post("/messages/conversations", { recipient_id }),
  getMessages: (conversationId) => api.get(`/messages/conversations/${conversationId}/messages`),
  sendMessage: (conversationId, content) => api.post(`/messages/conversations/${conversationId}/messages`, { content }),
  unreadCount: () => api.get("/messages/unread-count"),
};
