"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { PageHeader, notificationIcon } from "@/components/layout/AdminShell";
import Button from "@/components/ui/Button";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import { useNotificationActions, useNotifications } from "@/hooks/useAdmin";
import { timeAgo } from "@/lib/utils/formatters";

const TARGETS = { registration: "/approvals", report: "/reports" };

export default function NotificationsPage() {
  const router = useRouter();
  const [unreadOnly, setUnreadOnly] = useState(false);
  const { data, isLoading, error } = useNotifications({ limit: 100, unread_only: unreadOnly || undefined });
  const { markRead, markAllRead, remove } = useNotificationActions();

  const open = (n) => {
    if (!n.is_read) markRead.mutate(n.id);
    if (TARGETS[n.type]) router.push(TARGETS[n.type]);
  };

  return (
    <>
      <PageHeader
        title="Notifications"
        subtitle="Registration requests and post reports from across the portal."
        actions={
          <>
            <div className="tabs">
              <button className={`tab ${!unreadOnly ? "tab-active" : ""}`} onClick={() => setUnreadOnly(false)}>
                All
              </button>
              <button className={`tab ${unreadOnly ? "tab-active" : ""}`} onClick={() => setUnreadOnly(true)}>
                Unread
              </button>
            </div>
            <Button variant="secondary" size="sm" loading={markAllRead.isPending} onClick={() => markAllRead.mutate()}>
              Mark all read
            </Button>
          </>
        }
      />
      <Alert>{error?.message}</Alert>
      {isLoading ? (
        <SkeletonList count={4} />
      ) : data?.length ? (
        <div key={String(unreadOnly)} className="stack-sm stagger">
          {data.map((n) => (
            <div key={n.id} className={`card activity notification-card ${n.is_read ? "" : "activity-unread"}`}>
              <span className="notification-type">{notificationIcon(n.type)}</span>
              <button className="notification-open" onClick={() => open(n)}>
                <strong>{n.title}</strong>
                <span className="muted small">{n.message}</span>
                <span className="muted small">{timeAgo(n.created_at)}</span>
              </button>
              <div className="row" style={{ gap: 4 }}>
                {!n.is_read && (
                  <button className="btn btn-ghost btn-sm" onClick={() => markRead.mutate(n.id)} title="Mark as read">
                    ✓
                  </button>
                )}
                <button className="btn btn-ghost btn-sm" onClick={() => remove.mutate(n.id)} title="Delete">
                  ✕
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card empty fade-up">You&apos;re all caught up.</div>
      )}
    </>
  );
}
