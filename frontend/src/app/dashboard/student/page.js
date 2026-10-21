"use client";

import Link from "next/link";
import { PageHeader } from "@/components/layout/DashboardShell";
import Card from "@/components/ui/Card";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import ProfileCard from "@/components/student/ProfileCard";
import StudentPostCard from "@/components/student/StudentPostCard";
import { useStudentFeed, useStudentProfile } from "@/hooks/useStudent";

export default function StudentDashboardPage() {
  const { data: student, isLoading, error } = useStudentProfile();
  const { data: feed, isLoading: feedLoading } = useStudentFeed({ page: 1, limit: 3 });
  const firstName = student?.name?.split(" ")[0];

  const checklist = student
    ? [
        ["Add your LinkedIn profile", !!student.linkedin_url],
        ["Add your Instagram profile", !!student.instagram_url],
        ["Upload your CV", !!student.cv],
      ]
    : [];
  const done = checklist.filter(([, ok]) => ok).length;

  return (
    <>
      <PageHeader title={firstName ? `Hi, ${firstName}` : "Dashboard"} subtitle="Your student hub for mentorship and opportunities." />

      <Alert>{error?.message}</Alert>

      {isLoading ? (
        <SkeletonList count={2} />
      ) : (
        <div className="stack">
          <div className="grid-2 stagger">
            <ProfileCard
              student={student}
              actions={
                <Link className="btn btn-secondary btn-sm" href="/dashboard/student/profile">
                  Edit
                </Link>
              }
            />
            <Card title="Profile checklist">
              <div className="stack-sm">
                <div className="progress">
                  <div className="progress-bar" style={{ width: `${(done / checklist.length) * 100 || 0}%` }} />
                </div>
                {checklist.map(([label, ok]) => (
                  <div key={label} className="small" style={{ color: ok ? "var(--success)" : undefined }}>
                    {ok ? "✓" : "○"} {label}
                  </div>
                ))}
              </div>
            </Card>
          </div>

          <Card
            title="Latest from the community"
            actions={
              <Link className="small" href="/dashboard/student/posts">
                View feed
              </Link>
            }
          >
            {feedLoading ? (
              <SkeletonList count={2} />
            ) : feed?.posts?.length ? (
              <div className="stack stagger">
                {feed.posts.map((post) => (
                  <StudentPostCard key={post.id} post={post} />
                ))}
              </div>
            ) : (
              <div className="empty">No community posts yet.</div>
            )}
          </Card>
        </div>
      )}
    </>
  );
}
