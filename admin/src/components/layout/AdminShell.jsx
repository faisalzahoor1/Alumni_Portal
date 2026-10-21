"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useConfigQuery } from "@/hooks/useConfig";
import { useNotificationActions, useNotifications, useProfile, useStats, useUnreadCount } from "@/hooks/useAdmin";
import Avatar from "@/components/ui/Avatar";
import Dropdown from "@/components/ui/Dropdown";
import ConfigGate from "@/providers/ConfigGate";
import { timeAgo } from "@/lib/utils/formatters";

const NOTIFICATION_TARGETS = { registration: "/approvals", report: "/reports" };
export const notificationIcon = (type) => ({ registration: "🧑‍🎓", report: "⚑" })[type] || "🔔";

function Bell() {
  const router = useRouter();
  const { data: unread } = useUnreadCount();
  const { data: recent } = useNotifications({ limit: 6 });
  const { markRead } = useNotificationActions();
  const count = unread?.unread_count || 0;

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
      {(close) => (
        <>
          <div className="row-between" style={{ padding: "6px 10px" }}>
            <strong>Notifications</strong>
            <Link href="/notifications" className="small" onClick={close}>
              View all
            </Link>
          </div>
          {recent?.length ? (
            recent.map((n) => (
              <button
                key={n.id}
                className={`dropdown-item notification-row ${n.is_read ? "" : "notification-row-unread"}`}
                onClick={() => {
                  close();
                  if (!n.is_read) markRead.mutate(n.id);
                  router.push(NOTIFICATION_TARGETS[n.type] || "/notifications");
                }}
              >
                <span className="notification-type">{notificationIcon(n.type)}</span>
                <span style={{ flex: 1, minWidth: 0 }}>
                  <strong className="small">{n.title}</strong>
                  <span className="muted small notification-preview">{n.message}</span>
                </span>
                <span className="muted small">{timeAgo(n.created_at)}</span>
              </button>
            ))
          ) : (
            <div className="empty small">You&apos;re all caught up.</div>
          )}
        </>
      )}
    </Dropdown>
  );
}

export default function AdminShell({ children }) {
  const pathname = usePathname();
  const { logout } = useAuth();
  const { data: config } = useConfigQuery();
  const { data: stats } = useStats();
  const { data: profile } = useProfile();
  const { data: unread } = useUnreadCount();
  const [menuOpen, setMenuOpen] = useState(false);

  const links = [
    { href: "/dashboard", label: "Dashboard", icon: "▦" },
    { href: "/approvals", label: "Approvals", icon: "✓", badge: stats?.pending_registrations },
    { href: "/reports", label: "Reports", icon: "⚑", badge: stats?.reported_posts, danger: true },
    { href: "/posts", label: config?.university?.posts_label || "University posts", icon: "🏛" },
    { href: "/users", label: "Users", icon: "👥" },
    { href: "/notifications", label: "Notifications", icon: "🔔", badge: unread?.unread_count },
    { href: "/profile", label: "Profile", icon: "◉" },
  ];

  return (
    <div className="dash">
      {menuOpen && <div className="sidebar-scrim" onClick={() => setMenuOpen(false)} />}
      <aside className={`sidebar admin-sidebar ${menuOpen ? "sidebar-open" : ""}`}>
        <div className="sidebar-brand">
          <span className="brand-mark">Admin Portal</span>
          <span>{config?.university?.short_name || "Alumni Portal"}</span>
        </div>
        {links.map((link) => {
          const active = pathname.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`nav-link ${active ? "nav-link-active" : ""}`}
              onClick={() => setMenuOpen(false)}
            >
              <span aria-hidden>{link.icon}</span>
              {link.label}
              {link.badge > 0 && (
                <span className={`nav-badge ${link.danger ? "nav-badge-danger" : ""}`}>{link.badge > 99 ? "99+" : link.badge}</span>
              )}
            </Link>
          );
        })}
        <div className="sidebar-footer">
          <button className="nav-link" style={{ width: "100%", border: 0, background: "transparent", cursor: "pointer", font: "inherit" }} onClick={logout}>
            <span aria-hidden>↩</span>
            Log out
          </button>
        </div>
      </aside>

      <div className="dash-main">
        <header className="topbar">
          <button className="btn btn-ghost btn-sm menu-toggle" onClick={() => setMenuOpen((v) => !v)} aria-label="Menu">
            ☰
          </button>
          <div />
          <div className="row">
            <Bell />
            <Dropdown
              trigger={
                <button className="btn btn-ghost btn-sm" style={{ padding: 4 }}>
                  <Avatar name={profile?.name} src={profile?.avatar_url} size={32} />
                  <span className="small">{profile?.name || "Admin"}</span>
                </button>
              }
            >
              <Link className="dropdown-item" href="/profile">
                My profile
              </Link>
              <button className="dropdown-item" onClick={logout}>
                Log out
              </button>
            </Dropdown>
          </div>
        </header>
        <main key={pathname} className="dash-content page-enter">
          <ConfigGate>{children}</ConfigGate>
        </main>
      </div>
    </div>
  );
}

export function PageHeader({ title, subtitle, actions }) {
  return (
    <div className="page-header row-between">
      <div>
        <h1>{title}</h1>
        {subtitle && <p className="muted" style={{ margin: 0 }}>{subtitle}</p>}
      </div>
      {actions && <div className="row">{actions}</div>}
    </div>
  );
}
