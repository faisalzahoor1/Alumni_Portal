"use client";

import { useQuery } from "@tanstack/react-query";
import { feedApi } from "@/lib/api/feed";
import { universityApi } from "@/lib/api/university";

export function usePublicFeed(filters) {
  return useQuery({ queryKey: ["public", "feed", filters], queryFn: () => feedApi.getFeed(filters) });
}

export function useUniversityPosts(filters) {
  return useQuery({ queryKey: ["university", "posts", filters], queryFn: () => universityApi.getPosts(filters) });
}
