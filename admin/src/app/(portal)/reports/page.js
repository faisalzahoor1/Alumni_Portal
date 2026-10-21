"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/AdminShell";
import Avatar from "@/components/ui/Avatar";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import Alert from "@/components/ui/Alert";
import Modal from "@/components/ui/Modal";
import SkeletonList from "@/components/ui/Skeleton";
import PostCard from "@/components/posts/PostCard";
import { useConfig } from "@/hooks/useConfig";
import { useModerate, useReports } from "@/hooks/useAdmin";
import { timeAgo } from "@/lib/utils/formatters";

const TABS = [
  { value: "pending", label: "Open" },
  { value: "dismissed", label: "Allowed" },
  { value: "actioned", label: "Removed" },
];

export default function ReportsPage() {
  const { reports: reportRules } = useConfig();
  const reasonLabel = (value) => reportRules.reasons.find((r) => r.value === value)?.label || value;
  const [status, setStatus] = useState(TABS[0].value);
  const { data, isLoading, error } = useReports(status);
  const moderate = useModerate();
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [flash, setFlash] = useState(null);
  const [expanded, setExpanded] = useState({});

  const act = async (item, action) => {
    setFlash(null);
    setConfirmDelete(null);
    try {
      await moderate.mutateAsync({ postId: item.post_id, action });
      setFlash({ type: "success", text: action === "allow" ? "Post allowed and its reports closed." : "Post deleted and its author notified." });
    } catch (err) {
      setFlash({ type: "error", text: err.message });
    }
  };

  return (
    <>
      <PageHeader
        title="Reported posts"
        subtitle="Review what the community flagged. Allow the post to keep it, or delete it."
        actions={
          <div className="tabs">
            {TABS.map((t) => (
              <button key={t.value} className={`tab ${status === t.value ? "tab-active" : ""}`} onClick={() => setStatus(t.value)}>
                {t.label}
              </button>
            ))}
          </div>
        }
      />

      <div className="stack">
        {flash && <Alert type={flash.type}>{flash.text}</Alert>}
        <Alert>{error?.message}</Alert>

        {isLoading ? (
          <SkeletonList count={2} />
        ) : data?.length ? (
          <div key={status} className="stack stagger">
            {data.map((item) => (
              <section key={item.post_id} className={`card report-card ${status === "pending" ? "report-card-open" : ""}`}>
                <div className="row-between">
                  <div className="row" style={{ gap: 8 }}>
                    <span className="report-count">
                      ⚑ {item.report_count} report{item.report_count === 1 ? "" : "s"}
                    </span>
                    {Object.entries(item.reasons).map(([reason, n]) => (
                      <Badge key={reason} tone="danger">
                        {`${reasonLabel(reason)}${n > 1 ? ` ×${n}` : ""}`}
                      </Badge>
                    ))}
                  </div>
                  <span className="muted small">last {timeAgo(item.last_reported_at)}</span>
                </div>

                {item.post ? (
                  <PostCard post={item.post} engagement={false} className="report-preview" />
                ) : (
                  <div className="empty muted">This post has already been deleted.</div>
                )}

                <button className="link-btn small" onClick={() => setExpanded((e) => ({ ...e, [item.post_id]: !e[item.post_id] }))}>
                  {expanded[item.post_id] ? "Hide" : "Show"} who reported it ({item.reports.length})
                </button>
                {expanded[item.post_id] && (
                  <div className="stack-sm stagger">
                    {item.reports.map((r) => (
                      <div key={r.id} className="reporter">
                        <Avatar name={r.reporter_name} size={28} />
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div className="small">
                            <strong>{r.reporter_name}</strong> <span className="role-tag">{r.reporter_role}</span> · {reasonLabel(r.reason)}
                          </div>
                          {r.details && <div className="muted small pre-wrap">&ldquo;{r.details}&rdquo;</div>}
                        </div>
                        <span className="muted small">{timeAgo(r.created_at)}</span>
                      </div>
                    ))}
                  </div>
                )}

                {status === "pending" && (
                  <div className="row" style={{ justifyContent: "flex-end" }}>
                    <Button variant="secondary" onClick={() => act(item, "allow")} disabled={moderate.isPending}>
                      ✓ Allow post
                    </Button>
                    <Button variant="danger" onClick={() => setConfirmDelete(item)} disabled={moderate.isPending || !item.post}>
                      Delete post
                    </Button>
                  </div>
                )}
              </section>
            ))}
          </div>
        ) : (
          <div className="card empty fade-up">
            <div style={{ fontSize: "2rem" }}>{status === "pending" ? "🛡️" : "📭"}</div>
            {status === "pending" ? "No open reports. The community is behaving!" : "Nothing here yet."}
          </div>
        )}
      </div>

      <Modal open={!!confirmDelete} title="Delete reported post" onClose={() => setConfirmDelete(null)}>
        {confirmDelete && (
          <div className="stack">
            <p style={{ margin: 0 }}>
              Delete <strong>&ldquo;{confirmDelete.post?.title}&rdquo;</strong> by {confirmDelete.post?.author_name}? Its comments and
              reactions go too, and the author is told it was removed.
            </p>
            <div className="row" style={{ justifyContent: "flex-end" }}>
              <Button variant="secondary" onClick={() => setConfirmDelete(null)}>
                Cancel
              </Button>
              <Button variant="danger" loading={moderate.isPending} onClick={() => act(confirmDelete, "delete")}>
                Delete post
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
}
