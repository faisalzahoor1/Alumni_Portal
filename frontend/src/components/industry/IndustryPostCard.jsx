"use client";

import Badge from "@/components/ui/Badge";
import Alert from "@/components/ui/Alert";
import Dropdown from "@/components/ui/Dropdown";
import Input from "@/components/ui/Input";
import { PageLoader } from "@/components/ui/Spinner";
import { useConfig } from "@/hooks/useConfig";
import { formatDate, labelize, timeAgo } from "@/lib/utils/formatters";
import { useApplicants, useUpdateApplicationStatus } from "@/hooks/useIndustry";

// A job posting with its edit / delete / applicants actions.
export default function IndustryPostCard({ job, onEdit, onDelete, onApplicants }) {
  return (
    <article className="card post-card">
      <div className="row-between">
        <div>
          <h3 style={{ margin: 0 }}>{job.title}</h3>
          <span className="muted small">
            {[job.job_type, job.location, job.salary_range].filter(Boolean).join(" · ")}
          </span>
        </div>
        <div className="row">
          <Badge>{job.status}</Badge>
          <Dropdown trigger={<button className="btn btn-ghost btn-sm" aria-label="Job actions">⋯</button>}>
            {(close) => (
              <>
                <button className="dropdown-item" onClick={() => { close(); onEdit(job); }}>
                  Edit
                </button>
                <button className="dropdown-item" style={{ color: "var(--danger)" }} onClick={() => { close(); onDelete(job); }}>
                  Delete
                </button>
              </>
            )}
          </Dropdown>
        </div>
      </div>

      <div className="pre-wrap">{job.description}</div>

      {job.requirements?.length > 0 && (
        <div className="tags">
          {job.requirements.map((req) => (
            <span key={req} className="tag">
              {req}
            </span>
          ))}
        </div>
      )}

      <div className="row-between">
        <span className="muted small">Posted {timeAgo(job.created_at)}</span>
        <button className="btn btn-secondary btn-sm" onClick={() => onApplicants(job)}>
          View applicants
        </button>
      </div>
    </article>
  );
}

export function ApplicantList({ jobId }) {
  const { data, isLoading, error } = useApplicants(jobId);
  const updateStatus = useUpdateApplicationStatus(jobId);
  const { jobs: jobRules } = useConfig();
  const applicants = Array.isArray(data) ? data : [];

  if (isLoading) return <PageLoader />;

  return (
    <div className="stack">
      <Alert>{error?.message || updateStatus.error?.message}</Alert>
      {applicants.length === 0 ? (
        <div className="empty">No one has applied yet.</div>
      ) : (
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>Applicant</th>
                <th>Applied</th>
                <th>Resume</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {applicants.map((app) => (
                <tr key={app.id}>
                  <td>
                    <div className="small">{app.applicant_user_id}</div>
                    {app.cover_letter && <div className="muted small pre-wrap">{app.cover_letter}</div>}
                  </td>
                  <td className="small">{formatDate(app.applied_at)}</td>
                  <td className="small">
                    {app.resume_link ? (
                      <a href={app.resume_link} target="_blank" rel="noreferrer">
                        Open
                      </a>
                    ) : (
                      "–"
                    )}
                  </td>
                  <td style={{ minWidth: 130 }}>
                    <Input
                      as="select"
                      aria-label="Application status"
                      value={app.status}
                      disabled={updateStatus.isPending}
                      onChange={(e) => updateStatus.mutate({ appId: app.id, status: e.target.value })}
                      options={jobRules.application_statuses.map((s) => ({ value: s, label: labelize(s) }))}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
