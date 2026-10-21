"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { adminApi } from "@/lib/api/admin";

const POLL_MS = 30_000;

// Most admin actions change the dashboard numbers and badges too
function useInvalidate() {
  const queryClient = useQueryClient();
  return (...keys) => {
    keys.forEach((key) => queryClient.invalidateQueries({ queryKey: [key] }));
    queryClient.invalidateQueries({ queryKey: ["stats"] });
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
  };
}

export function useStats() {
  return useQuery({ queryKey: ["stats"], queryFn: adminApi.getStats, refetchInterval: POLL_MS });
}

// ---------- Registrations ----------

export function useRegistrations(status) {
  return useQuery({ queryKey: ["registrations", status], queryFn: () => adminApi.getRegistrations(status) });
}

export function useDecideRegistration() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: ({ id, approve }) => (approve ? adminApi.approve(id) : adminApi.reject(id)),
    onSuccess: () => invalidate("registrations", "users"),
  });
}

// ---------- Users ----------

export function useUsers(query) {
  return useQuery({ queryKey: ["users", query], queryFn: () => adminApi.searchUsers(query), placeholderData: (prev) => prev });
}

export function useDeleteUser() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: ({ role, id }) => adminApi.deleteUser(role, id),
    onSuccess: () => invalidate("users", "posts", "reports", "registrations"),
  });
}

// ---------- University posts ----------

export function useUniversityPosts() {
  return useQuery({ queryKey: ["posts"], queryFn: adminApi.getPosts });
}

export const UNIVERSITY_POST_HOOKS = {
  useCreate() {
    const invalidate = useInvalidate();
    return useMutation({ mutationFn: adminApi.createPost, onSuccess: () => invalidate("posts") });
  },
  useUpdate() {
    const invalidate = useInvalidate();
    return useMutation({ mutationFn: ({ id, data }) => adminApi.updatePost(id, data), onSuccess: () => invalidate("posts") });
  },
  useUpload() {
    return useMutation({ mutationFn: adminApi.uploadMedia });
  },
};

export function useDeleteUniversityPost() {
  const invalidate = useInvalidate();
  return useMutation({ mutationFn: adminApi.deletePost, onSuccess: () => invalidate("posts") });
}

// ---------- Reports ----------

export function useReports(status) {
  return useQuery({ queryKey: ["reports", status], queryFn: () => adminApi.getReports(status), refetchInterval: POLL_MS });
}

export function useModerate() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: ({ postId, action }) => (action === "allow" ? adminApi.allowPost(postId) : adminApi.deleteReportedPost(postId)),
    onSuccess: () => invalidate("reports", "posts"),
  });
}

// ---------- Notifications ----------

export function useNotifications(query = { limit: 100 }) {
  return useQuery({ queryKey: ["notifications", query], queryFn: () => adminApi.getNotifications(query), refetchInterval: POLL_MS });
}

export function useUnreadCount() {
  return useQuery({ queryKey: ["notifications", "unread"], queryFn: adminApi.unreadCount, refetchInterval: POLL_MS });
}

export function useNotificationActions() {
  const queryClient = useQueryClient();
  const onSuccess = () => {
    queryClient.invalidateQueries({ queryKey: ["notifications"] });
    queryClient.invalidateQueries({ queryKey: ["stats"] });
  };
  return {
    markRead: useMutation({ mutationFn: adminApi.markRead, onSuccess }),
    markAllRead: useMutation({ mutationFn: adminApi.markAllRead, onSuccess }),
    remove: useMutation({ mutationFn: adminApi.deleteNotification, onSuccess }),
  };
}

// ---------- Profile ----------

export function useProfile() {
  return useQuery({ queryKey: ["profile"], queryFn: adminApi.getProfile });
}

export function useUpdateProfile() {
  const queryClient = useQueryClient();
  return useMutation({ mutationFn: adminApi.updateProfile, onSuccess: (data) => queryClient.setQueryData(["profile"], data) });
}

export function useUploadAvatar() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: adminApi.uploadAvatar,
    // The new picture also shows on university posts and admin comments
    onSuccess: (data) => {
      queryClient.setQueryData(["profile"], data);
      queryClient.invalidateQueries({ predicate: (q) => q.queryKey[0] !== "config" && q.queryKey[0] !== "profile" });
    },
  });
}
