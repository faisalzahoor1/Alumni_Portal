"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { studentApi } from "@/lib/api/student";

export function useStudentProfile() {
  return useQuery({ queryKey: ["student", "me"], queryFn: studentApi.getMe });
}

export function useUpdateStudentInfo() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: studentApi.updateAdditionalInfo,
    onSuccess: (data) => queryClient.setQueryData(["student", "me"], data),
  });
}

export function useUploadStudentAvatar() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: studentApi.uploadAvatar,
    // A new picture also shows on comments and conversations, so refetch everything but the config
    onSuccess: (data) => {
      queryClient.setQueryData(["student", "me"], data);
      queryClient.invalidateQueries({ predicate: (q) => q.queryKey[0] !== "config" });
    },
  });
}

export function useStudentFeed(filters) {
  return useQuery({ queryKey: ["student", "feed", filters], queryFn: () => studentApi.getFeed(filters) });
}
