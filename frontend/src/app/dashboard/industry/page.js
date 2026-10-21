"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/DashboardShell";
import Button from "@/components/ui/Button";
import { StatCard } from "@/components/ui/Card";
import Modal from "@/components/ui/Modal";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import IndustryPostForm from "@/components/industry/IndustryPostForm";
import IndustryPostCard, { ApplicantList } from "@/components/industry/IndustryPostCard";
import { useDeleteJob, useIndustryJobs, useIndustryProfile, useIndustryStats } from "@/hooks/useIndustry";

export default function IndustryDashboardPage() {
  const { data: profile } = useIndustryProfile();
  const { data: stats } = useIndustryStats();
  const { data, isLoading, error } = useIndustryJobs();
  const remove = useDeleteJob();
  const [editing, setEditing] = useState(null); // null = closed, {} = new job, job = edit
  const [viewing, setViewing] = useState(null);
  const jobs = Array.isArray(data) ? data : [];
  const openJobs = jobs.filter((job) => job.status === "open").length;

  const onDelete = (job) => {
    if (window.confirm(`Delete "${job.title}"? Its applications will no longer be visible.`)) remove.mutate(job.id);
  };

  return (
    <>
      <PageHeader
        title={profile?.company_name ? `${profile.company_name} dashboard` : "Dashboard"}
        subtitle="Manage your job postings and review applicants."
        actions={<Button onClick={() => setEditing({})}>＋ Post a job</Button>}
      />

      <div className="stack">
        <div className="grid-stats stagger">
          <StatCard label="Jobs posted" value={stats?.total_jobs} />
          <StatCard label="Open positions" value={isLoading ? null : openJobs} />
          <StatCard label="Total applicants" value={stats?.total_applicants} />
        </div>

        <Alert>{error?.message || remove.error?.message}</Alert>

        {isLoading ? (
          <SkeletonList />
        ) : jobs.length === 0 ? (
          <div className="card empty fade-up">
            <p>You haven&apos;t posted any jobs yet.</p>
            <Button onClick={() => setEditing({})}>Post your first job</Button>
          </div>
        ) : (
          <div className="stack stagger">
            {jobs.map((job) => (
              <IndustryPostCard key={job.id} job={job} onEdit={setEditing} onDelete={onDelete} onApplicants={setViewing} />
            ))}
          </div>
        )}
      </div>

      <Modal open={!!editing} title={editing?.id ? "Edit job" : "Post a job"} size="lg" onClose={() => setEditing(null)}>
        {editing && <IndustryPostForm key={editing.id || "new"} job={editing.id ? editing : null} onDone={() => setEditing(null)} />}
      </Modal>

      <Modal open={!!viewing} title={viewing ? `Applicants · ${viewing.title}` : ""} size="lg" onClose={() => setViewing(null)}>
        {viewing && <ApplicantList jobId={viewing.id} />}
      </Modal>
    </>
  );
}
