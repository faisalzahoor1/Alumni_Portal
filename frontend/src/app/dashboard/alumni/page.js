"use client";

import Link from "next/link";
import { PageHeader } from "@/components/layout/DashboardShell";
import Card, { StatCard } from "@/components/ui/Card";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import PostCard from "@/components/posts/PostCard";
import { useAlumniProfile, useAlumniStats } from "@/hooks/useAlumni";

export default function AlumniDashboardPage() {
  const { data: profile } = useAlumniProfile();
  const { data: stats, isLoading, error } = useAlumniStats();
  const firstName = profile?.name?.split(" ")[0];

  return (
    <>
      <PageHeader
        title={firstName ? `Welcome back, ${firstName}` : "Welcome back"}
        subtitle="Here's what's happening in your network."
        actions={
          <Link className="btn btn-primary" href="/dashboard/alumni/posts">
            ＋ New post
          </Link>
        }
      />

      <Alert>{error?.message}</Alert>

      {isLoading ? (
        <SkeletonList count={2} />
      ) : (
        stats && (
          <div className="stack">
            <div className="grid-stats stagger">
              <StatCard label="My posts" value={stats.total_my_posts} />
              <StatCard label="Achievements" value={stats.total_achievements} />
              <StatCard label="Jobs posted" value={stats.total_jobs_posted} />
              <StatCard label="Unread notifications" value={stats.unread_notifications} />
              <StatCard label="Community posts" value={stats.community_feed_posts_count} />
            </div>

            {!stats.profile_completed && (
              <Card
                title="Complete your profile"
                actions={
                  <Link className="btn btn-secondary btn-sm" href="/dashboard/alumni/profile">
                    Edit profile
                  </Link>
                }
              >
                <div className="stack-sm">
                  <div className="progress">
                    <div className="progress-bar" style={{ width: `${stats.profile_completion_percentage}%` }} />
                  </div>
                  <span className="muted small">
                    {stats.profile_completion_percentage}% complete. A full profile helps students and recruiters find you.
                  </span>
                </div>
              </Card>
            )}

            <Card
              title="Your recent posts"
              actions={
                <Link className="small" href="/dashboard/alumni/posts">
                  View all
                </Link>
              }
            >
              {stats.recent_posts?.length ? (
                <div className="stack stagger">
                  {stats.recent_posts.map((post) => (
                    <PostCard key={post.id} post={post} />
                  ))}
                </div>
              ) : (
                <div className="empty">You haven&apos;t posted anything yet.</div>
              )}
            </Card>
          </div>
        )
      )}
    </>
  );
}
