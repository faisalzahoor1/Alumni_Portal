"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import NotificationItem from "./NotificationItem";
import { useNotificationActions, useNotifications } from "@/hooks/useNotifications";

export default function NotificationList({ role }) {
  const [unreadOnly, setUnreadOnly] = useState(false);
  const { data, isLoading, error } = useNotifications(role, { limit: 100, unread_only: unreadOnly || undefined });
  const { markRead, markAllRead, remove } = useNotificationActions(role);
  const notifications = Array.isArray(data) ? data : [];

  return (
    <Card
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
    >
      <Alert>{error?.message}</Alert>
      {isLoading ? (
        <SkeletonList count={4} />
      ) : notifications.length === 0 ? (
        <div className="empty">You&apos;re all caught up.</div>
      ) : (
        <div className="stack-sm stagger">
          {notifications.map((n) => (
            <NotificationItem key={n.id} notification={n} onRead={markRead.mutate} onDelete={remove.mutate} />
          ))}
        </div>
      )}
    </Card>
  );
}
