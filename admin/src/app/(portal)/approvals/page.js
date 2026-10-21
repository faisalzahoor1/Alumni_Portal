"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/AdminShell";
import Avatar from "@/components/ui/Avatar";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import Alert from "@/components/ui/Alert";
import Modal from "@/components/ui/Modal";
import SkeletonList from "@/components/ui/Skeleton";
import { useConfig } from "@/hooks/useConfig";
import { useDecideRegistration, useRegistrations } from "@/hooks/useAdmin";
import { formatDate, labelize, timeAgo } from "@/lib/utils/formatters";

export default function ApprovalsPage() {
  const { approval } = useConfig();
  const [status, setStatus] = useState(approval.statuses[0]);
  const { data, isLoading, error } = useRegistrations(status);
  const decide = useDecideRegistration();
  const [confirm, setConfirm] = useState(null); // { registration, approve }
  const [flash, setFlash] = useState(null);
  const [leaving, setLeaving] = useState(null);

  const onDecide = async () => {
    const { registration, approve } = confirm;
    setConfirm(null);
    setFlash(null);
    setLeaving(registration.id);
    try {
      const res = await decide.mutateAsync({ id: registration.id, approve });
      setFlash({
        type: res.email_sent ? "success" : "info",
        text: `${registration.email} was ${approve ? "approved" : "rejected"}.${
          res.email_sent ? " They've been emailed." : " The email couldn't be sent, so let them know directly."
        }`,
      });
    } catch (err) {
      setFlash({ type: "error", text: err.message });
    } finally {
      setLeaving(null);
    }
  };

  return (
    <>
      <PageHeader
        title="Registration approvals"
        subtitle="Alumni and industry accounts that verified their email. They can sign in once approved."
        actions={
          <div className="tabs">
            {approval.statuses.map((s) => (
              <button key={s} className={`tab ${status === s ? "tab-active" : ""}`} onClick={() => setStatus(s)}>
                {labelize(s)}
              </button>
            ))}
          </div>
        }
      />

      <div className="stack">
        {flash && <Alert type={flash.type}>{flash.text}</Alert>}
        <Alert>{error?.message}</Alert>

        {isLoading ? (
          <SkeletonList count={3} />
        ) : data?.length ? (
          <div key={status} className="stack stagger">
            {data.map((r) => (
              <div key={r.id} className={`card registration ${leaving === r.id ? "registration-leaving" : ""}`}>
                <Avatar name={r.name || r.email} size={48} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div className="row" style={{ gap: 8 }}>
                    <strong>{r.name || r.email}</strong>
                    <Badge>{r.role}</Badge>
                    {status !== approval.statuses[0] && <Badge>{r.approval_status}</Badge>}
                  </div>
                  <div className="muted small">{r.email}</div>
                  <div className="muted small" title={formatDate(r.created_at)}>
                    Signed up {timeAgo(r.created_at)}
                  </div>
                </div>
                <div className="row">
                  {r.approval_status !== "rejected" && (
                    <Button variant="secondary" size="sm" onClick={() => setConfirm({ registration: r, approve: false })} disabled={decide.isPending}>
                      Reject
                    </Button>
                  )}
                  {r.approval_status !== "approved" && (
                    <Button size="sm" onClick={() => setConfirm({ registration: r, approve: true })} disabled={decide.isPending}>
                      ✓ Approve
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="card empty fade-up">
            <div style={{ fontSize: "2rem" }}>🎉</div>
            No {status} registrations.
          </div>
        )}
      </div>

      <Modal open={!!confirm} title={confirm?.approve ? "Approve registration" : "Reject registration"} onClose={() => setConfirm(null)}>
        {confirm && (
          <div className="stack">
            <p style={{ margin: 0 }}>
              {confirm.approve ? "Approve" : "Reject"} <strong>{confirm.registration.email}</strong> as {confirm.registration.role}?{" "}
              {confirm.approve
                ? "They'll be emailed that they can now sign in."
                : "They won't be able to sign in, and they'll be emailed about the decision."}
            </p>
            <div className="row" style={{ justifyContent: "flex-end" }}>
              <Button variant="secondary" onClick={() => setConfirm(null)}>
                Cancel
              </Button>
              <Button variant={confirm.approve ? "primary" : "danger"} onClick={onDecide}>
                {confirm.approve ? "Approve" : "Reject"}
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
}
