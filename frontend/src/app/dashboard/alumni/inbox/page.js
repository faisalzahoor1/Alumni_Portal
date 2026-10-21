import { Suspense } from "react";
import { PageHeader } from "@/components/layout/DashboardShell";
import Inbox from "@/components/messages/Inbox";
import SkeletonList from "@/components/ui/Skeleton";

export default function AlumniInboxPage() {
  return (
    <>
      <PageHeader title="Inbox" subtitle="Messages from students." />
      <Suspense fallback={<SkeletonList count={3} />}>
        <Inbox emptyHint="No messages yet. Students can reach out to you from your posts." />
      </Suspense>
    </>
  );
}
