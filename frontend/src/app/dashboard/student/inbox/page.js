import { Suspense } from "react";
import { PageHeader } from "@/components/layout/DashboardShell";
import Inbox from "@/components/messages/Inbox";
import SkeletonList from "@/components/ui/Skeleton";

export default function StudentInboxPage() {
  return (
    <>
      <PageHeader title="Inbox" subtitle="Your conversations with alumni." />
      <Suspense fallback={<SkeletonList count={3} />}>
        <Inbox emptyHint="No conversations yet. Tap “Message” on an alumni post in the community feed to start one." />
      </Suspense>
    </>
  );
}
