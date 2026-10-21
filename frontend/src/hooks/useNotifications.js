"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { notificationsApi } from "@/lib/api/notifications";

export function useNotifications(role, query = { limit: 50 }) {
  return useQuery({
    queryKey: [role, "notifications", query],
    queryFn: () => notificationsApi(role).list(query),
  });
}

export function useUnreadCount(role) {
  return useQuery({
    queryKey: [role, "notifications", "unread"],
    queryFn: () => notificationsApi(role).unreadCount(),
    refetchInterval: 60_000,
  });
}

export function useNotificationActions(role) {
  const queryClient = useQueryClient();
  const api = notificationsApi(role);
  const onSuccess = () => queryClient.invalidateQueries({ queryKey: [role, "notifications"] });
  return {
    markRead: useMutation({ mutationFn: api.markRead, onSuccess }),
    markAllRead: useMutation({ mutationFn: api.markAllRead, onSuccess }),
    remove: useMutation({ mutationFn: api.remove, onSuccess }),
  };
}
