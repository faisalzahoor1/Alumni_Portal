"use client";

import Link from "next/link";
import Dropdown from "@/components/ui/Dropdown";
import NotificationItem from "./NotificationItem";
import { useNotifications, useUnreadCount } from "@/hooks/useNotifications";

export default function NotificationBell({ role }) {
  const { data: countData } = useUnreadCount(role);
  const { data } = useNotifications(role, { limit: 5 });
  const count = countData?.unread_count || 0;
  const recent = Array.isArray(data) ? data.slice(0, 5) : [];

  return (
    <Dropdown
      wide
      trigger={
        <button className={`btn btn-ghost btn-sm bell ${count > 0 ? "bell-active" : ""}`} aria-label="Notifications">
          <span style={{ fontSize: "1.1rem" }}>🔔</span>
          {count > 0 && <span className="bell-count">{count > 99 ? "99+" : count}</span>}
        </button>
      }
    >
      <div className="row-between" style={{ padding: "6px 10px" }}>
        <strong>Notifications</strong>
        <Link href={`/dashboard/${role}/notifications`} className="small">
          View all
        </Link>
      </div>
      {recent.length === 0 ? (
        <div className="empty small">No notifications yet</div>
      ) : (
        recent.map((n) => <NotificationItem key={n.id} notification={n} compact />)
      )}
    </Dropdown>
  );
}
