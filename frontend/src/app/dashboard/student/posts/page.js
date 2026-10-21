"use client";

import { PageHeader } from "@/components/layout/DashboardShell";
import FeedView from "@/components/posts/FeedView";
import { useStudentFeed } from "@/hooks/useStudent";

export default function StudentFeedPage() {
  return (
    <>
      <PageHeader title="Community feed" subtitle="Jobs, achievements and announcements from alumni and industry partners." />
      <FeedView useFeed={useStudentFeed} />
    </>
  );
}
