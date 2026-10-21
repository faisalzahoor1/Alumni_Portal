"use client";

import Link from "next/link";
import { PageHeader, notificationIcon } from "@/components/layout/AdminShell";
import { StatCard } from "@/components/ui/Card";
import Card from "@/components/ui/Card";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import CountUp from "@/components/ui/CountUp";
import { useConfig } from "@/hooks/useConfig";
import { useNotifications, useProfile, useStats } from "@/hooks/useAdmin";
import { timeAgo } from "@/lib/utils/formatters";

function ActionCard({ href, icon, count, title, text, tone }) {
  return (
    <Link href={href} className={`card action-card hover-lift ${count > 0 ? `action-card-${tone}` : ""}`}>
      <span className="action-icon" aria-hidden>
        {icon}
      </span>
      <div style={{ flex: 1 }}>
        <div className="action-count">
          <CountUp value={count ?? 0} />
        </div>
        <strong>{title}</strong>
        <div className="muted small">{text}</div>
      </div>
      <span className="action-arrow" aria-hidden>
        →
      </span>
    </Link>
  );
}

export default function DashboardPage() {
  const { university } = useConfig();
  const { data: profile } = useProfile();
  const { data: stats, error } = useStats();
  const { data: notifications, isLoading } = useNotifications({ limit: 6 });

  return (
    <>
      <PageHeader
        title={`Welcome back${profile?.name ? `, ${profile.name.split(" ")[0]}` : ""}`}
        subtitle={`Here's what needs your attention at ${university.name}.`}
        actions={
          <Link className="btn btn-primary" href="/posts">
            ＋ New {university.short_name} post
          </Link>
        }
      />
      <Alert>{error?.message}</Alert>

      <div className="stack">
        <div className="grid-2 stagger">
          <ActionCard
            href="/approvals"
            icon="🧑‍🎓"
            tone="primary"
            count={stats?.pending_registrations}
            title="Registrations waiting"
            text="Alumni and industry accounts to review"
          />
          <ActionCard
            href="/reports"
            icon="⚑"
            tone="danger"
            count={stats?.reported_posts}
            title="Reported posts"
            text={`${stats?.open_reports ?? 0} open reports to review`}
          />
        </div>

        <div className="grid-stats stagger">
          <StatCard label="Students" value={stats?.students} />
          <StatCard label="Alumni" value={stats?.alumni} />
          <StatCard label="Industry partners" value={stats?.industry} />
          <StatCard label={university.posts_label} value={stats?.university_posts} />
          <StatCard label="Community posts" value={stats?.community_posts} />
        </div>

        <Card
          title="Recent activity"
          actions={
            <Link className="small" href="/notifications">
              View all
            </Link>
          }
        >
          {isLoading ? (
            <SkeletonList count={2} />
          ) : notifications?.length ? (
            <div className="stack-sm stagger">
              {notifications.map((n) => (
                <div key={n.id} className={`activity ${n.is_read ? "" : "activity-unread"}`}>
                  <span className="notification-type">{notificationIcon(n.type)}</span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <strong className="small">{n.title}</strong>
                    <div className="muted small">{n.message}</div>
                  </div>
                  <span className="muted small">{timeAgo(n.created_at)}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty">No activity yet.</div>
          )}
        </Card>
      </div>
    </>
  );
}
