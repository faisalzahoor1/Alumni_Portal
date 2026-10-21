"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { industryApi } from "@/lib/api/industry";

export function useIndustryProfile() {
  return useQuery({ queryKey: ["industry", "profile"], queryFn: industryApi.getProfile });
}

export function useUpdateIndustryProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: industryApi.updateProfile,
    onSuccess: (data) => queryClient.setQueryData(["industry", "profile"], data),
  });
}

export function useUploadIndustryLogo() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: industryApi.uploadLogo,
    // A new logo also shows on posts and comments, so refetch everything but the config
    onSuccess: (data) => {
      queryClient.setQueryData(["industry", "profile"], data);
      queryClient.invalidateQueries({ predicate: (q) => q.queryKey[0] !== "config" });
    },
  });
}

export function useIndustryStats() {
  return useQuery({ queryKey: ["industry", "stats"], queryFn: industryApi.getStats });
}

export function useIndustryJobs() {
  return useQuery({ queryKey: ["industry", "jobs"], queryFn: industryApi.getJobs });
}

function useInvalidateJobs() {
  const queryClient = useQueryClient();
  return () => {
    queryClient.invalidateQueries({ queryKey: ["industry", "jobs"] });
    queryClient.invalidateQueries({ queryKey: ["industry", "stats"] });
  };
}

export function useCreateJob() {
  const invalidate = useInvalidateJobs();
  return useMutation({ mutationFn: industryApi.createJob, onSuccess: invalidate });
}

export function useUpdateJob() {
  const invalidate = useInvalidateJobs();
  return useMutation({ mutationFn: ({ id, data }) => industryApi.updateJob(id, data), onSuccess: invalidate });
}

export function useDeleteJob() {
  const invalidate = useInvalidateJobs();
  return useMutation({ mutationFn: industryApi.deleteJob, onSuccess: invalidate });
}

export function useApplicants(jobId) {
  return useQuery({
    queryKey: ["industry", "applicants", jobId],
    queryFn: () => industryApi.getApplicants(jobId),
    enabled: !!jobId,
  });
}

export function useUpdateApplicationStatus(jobId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ appId, status }) => industryApi.updateApplicationStatus(jobId, appId, status),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["industry", "applicants", jobId] }),
  });
}

export function useIndustryFeed(filters) {
  return useQuery({ queryKey: ["industry", "feed", filters], queryFn: () => industryApi.getFeed(filters) });
}

export function useIndustryPosts(query = { limit: 50 }) {
  return useQuery({ queryKey: ["industry", "posts", query], queryFn: () => industryApi.getMyPosts(query) });
}

function useInvalidateIndustryPosts() {
  const queryClient = useQueryClient();
  return () => {
    queryClient.invalidateQueries({ queryKey: ["industry", "posts"] });
    queryClient.invalidateQueries({ queryKey: ["industry", "feed"] });
  };
}

export function useCreateIndustryPost() {
  const invalidate = useInvalidateIndustryPosts();
  return useMutation({ mutationFn: industryApi.createPost, onSuccess: invalidate });
}

export function useUpdateIndustryPost() {
  const invalidate = useInvalidateIndustryPosts();
  return useMutation({ mutationFn: ({ id, data }) => industryApi.updatePost(id, data), onSuccess: invalidate });
}

export function useDeleteIndustryPost() {
  const invalidate = useInvalidateIndustryPosts();
  return useMutation({ mutationFn: industryApi.deletePost, onSuccess: invalidate });
}

export function useUploadIndustryPostMedia() {
  return useMutation({ mutationFn: industryApi.uploadMedia });
}
