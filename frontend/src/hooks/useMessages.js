"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { messagesApi } from "@/lib/api/messages";
import { useConfig } from "./useConfig";

function usePollInterval() {
  const config = useConfig();
  return (config?.messaging?.poll_interval_seconds || 0) * 1000 || false;
}

export function useConversations() {
  return useQuery({
    queryKey: ["messages", "conversations"],
    queryFn: messagesApi.listConversations,
    refetchInterval: usePollInterval(),
  });
}

export function useThread(conversationId) {
  const queryClient = useQueryClient();
  return useQuery({
    queryKey: ["messages", "thread", conversationId],
    queryFn: async () => {
      const messages = await messagesApi.getMessages(conversationId);
      // Opening a thread marks it read on the server
      queryClient.invalidateQueries({ queryKey: ["messages", "conversations"] });
      queryClient.invalidateQueries({ queryKey: ["messages", "unread"] });
      return messages;
    },
    enabled: !!conversationId,
    refetchInterval: usePollInterval(),
  });
}

export function useSendMessage(conversationId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (content) => messagesApi.sendMessage(conversationId, content),
    onSuccess: (message) => {
      queryClient.setQueryData(["messages", "thread", conversationId], (list = []) => [...list, message]);
      queryClient.invalidateQueries({ queryKey: ["messages", "conversations"] });
    },
  });
}

export function useStartConversation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: messagesApi.startConversation,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["messages", "conversations"] }),
  });
}

export function useUnreadMessages(enabled = true) {
  return useQuery({
    queryKey: ["messages", "unread"],
    queryFn: messagesApi.unreadCount,
    enabled,
    refetchInterval: usePollInterval(),
  });
}
