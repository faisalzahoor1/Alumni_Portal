"use client";

import { PageHeader } from "@/components/layout/DashboardShell";
import FeedView from "@/components/posts/FeedView";
import { useConfig } from "@/hooks/useConfig";
import { useUniversityPosts } from "@/hooks/useFeed";

export default function UniversityPostsPage() {
  const { university } = useConfig();
  return (
    <>
      <PageHeader title={university.posts_label} subtitle={`Official news and announcements from ${university.name}.`} />
      <FeedView useFeed={useUniversityPosts} showAuthorFilter={false} />
    </>
  );
}
