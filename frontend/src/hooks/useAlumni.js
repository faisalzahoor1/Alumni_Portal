"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { alumniApi } from "@/lib/api/alumni";

export function useAlumniProfile() {
  return useQuery({ queryKey: ["alumni", "profile"], queryFn: alumniApi.getProfile });
}

export function useUpdateAlumniProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: alumniApi.updateProfile,
    onSuccess: (data) => {
      queryClient.setQueryData(["alumni", "profile"], data);
      queryClient.invalidateQueries({ queryKey: ["alumni", "stats"] });
    },
  });
}

export function useUploadAlumniAvatar() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: alumniApi.uploadAvatar,
    // A new picture also shows on posts, comments and conversations, so refetch everything but the config
    onSuccess: (data) => {
      queryClient.setQueryData(["alumni", "profile"], data);
      queryClient.invalidateQueries({ predicate: (q) => q.queryKey[0] !== "config" });
    },
  });
}

export function useAlumniStats() {
  return useQuery({ queryKey: ["alumni", "stats"], queryFn: alumniApi.getStats });
}

export function useAlumniPosts(query = { limit: 50 }) {
  return useQuery({ queryKey: ["alumni", "posts", query], queryFn: () => alumniApi.getMyPosts(query) });
}

function useInvalidatePosts() {
  const queryClient = useQueryClient();
  return () => {
    queryClient.invalidateQueries({ queryKey: ["alumni", "posts"] });
    queryClient.invalidateQueries({ queryKey: ["alumni", "stats"] });
    queryClient.invalidateQueries({ queryKey: ["alumni", "feed"] });
  };
}

export function useCreateAlumniPost() {
  const invalidate = useInvalidatePosts();
  return useMutation({ mutationFn: alumniApi.createPost, onSuccess: invalidate });
}

export function useUpdateAlumniPost() {
  const invalidate = useInvalidatePosts();
  return useMutation({ mutationFn: ({ id, data }) => alumniApi.updatePost(id, data), onSuccess: invalidate });
}

export function useDeleteAlumniPost() {
  const invalidate = useInvalidatePosts();
  return useMutation({ mutationFn: alumniApi.deletePost, onSuccess: invalidate });
}

export function useUploadPostMedia() {
  return useMutation({ mutationFn: alumniApi.uploadMedia });
}

export function useAlumniFeed(filters) {
  return useQuery({ queryKey: ["alumni", "feed", filters], queryFn: () => alumniApi.getFeed(filters) });
}
