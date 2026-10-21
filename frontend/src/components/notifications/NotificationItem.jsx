import Badge from "@/components/ui/Badge";
import { timeAgo } from "@/lib/utils/formatters";

export default function NotificationItem({ notification, onRead, onDelete, compact }) {
  const unread = !notification.is_read;
  return (
    <div className={`notification ${unread ? "notification-unread" : ""}`}>
      <span className={`notification-dot ${unread ? "" : "notification-dot-read"}`} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div className="row-between">
          <strong>{notification.title}</strong>
          <span className="muted small">{timeAgo(notification.created_at)}</span>
        </div>
        <div className="small pre-wrap">{notification.message}</div>
        {!compact && (
          <div className="row" style={{ marginTop: 8 }}>
            <Badge>{notification.type}</Badge>
            {unread && onRead && (
              <button className="btn btn-ghost btn-sm" onClick={() => onRead(notification.id)}>
                Mark as read
              </button>
            )}
            {onDelete && (
              <button className="btn btn-ghost btn-sm" onClick={() => onDelete(notification.id)}>
                Delete
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
