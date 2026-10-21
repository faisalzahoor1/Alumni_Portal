"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { engagementApi } from "@/lib/api/engagement";

// Apply `patch` to a post wherever it is cached (feeds, my posts, dashboard recent posts).
function patchCachedPost(queryClient, postId, patch) {
  const update = (post) => (post?.id === postId ? { ...post, ...patch(post) } : post);
  queryClient.setQueriesData({ predicate: () => true }, (data) => {
    if (!data || typeof data !== "object") return data;
    if (Array.isArray(data)) return data.some((p) => p?.id === postId) ? data.map(update) : data;
    if (Array.isArray(data.posts)) return { ...data, posts: data.posts.map(update) };
    if (Array.isArray(data.recent_posts)) return { ...data, recent_posts: data.recent_posts.map(update) };
    return data;
  });
}

export function useReact(post) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (reaction) => engagementApi.react(post.id, reaction),
    // Optimistic: flip the counts immediately, then reconcile with the server's numbers
    onMutate: (reaction) => {
      const previous = { my_reaction: post.my_reaction, likes_count: post.likes_count, dislikes_count: post.dislikes_count };
      patchCachedPost(queryClient, post.id, (p) => {
        const counts = { likes_count: p.likes_count || 0, dislikes_count: p.dislikes_count || 0 };
        if (p.my_reaction) counts[`${p.my_reaction}s_count`] = Math.max(0, (counts[`${p.my_reaction}s_count`] || 0) - 1);
        if (reaction) counts[`${reaction}s_count`] = (counts[`${reaction}s_count`] || 0) + 1;
        return { ...counts, my_reaction: reaction };
      });
      return previous;
    },
    onError: (_err, _reaction, previous) => patchCachedPost(queryClient, post.id, () => previous),
    onSuccess: (summary) =>
      patchCachedPost(queryClient, post.id, () => ({
        likes_count: summary.likes_count,
        dislikes_count: summary.dislikes_count,
        my_reaction: summary.my_reaction,
      })),
  });
}

export function useComments(postId, enabled) {
  return useQuery({
    queryKey: ["comments", postId],
    queryFn: () => engagementApi.getComments(postId),
    enabled,
  });
}

export function useAddComment(postId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ content, parentId }) => engagementApi.addComment(postId, content, parentId),
    onSuccess: (comment) => {
      queryClient.setQueryData(["comments", postId], (list = []) => [...list, comment]);
      patchCachedPost(queryClient, postId, (p) => ({ comments_count: (p.comments_count || 0) + 1 }));
    },
  });
}

export function useDeleteComment(postId) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (commentId) => engagementApi.deleteComment(postId, commentId),
    onSuccess: (_res, commentId) => {
      // The server removes a comment together with its replies
      const list = queryClient.getQueryData(["comments", postId]) || [];
      const kept = list.filter((c) => c.id !== commentId && c.parent_id !== commentId);
      const removed = list.length - kept.length || 1;
      queryClient.setQueryData(["comments", postId], kept);
      patchCachedPost(queryClient, postId, (p) => ({ comments_count: Math.max(0, (p.comments_count || 0) - removed) }));
    },
  });
}

export function useReportPost(postId) {
  return useMutation({ mutationFn: ({ reason, details }) => engagementApi.report(postId, reason, details) });
}
