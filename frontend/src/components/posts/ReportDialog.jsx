"use client";

import { useState } from "react";
import Modal from "@/components/ui/Modal";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { useConfig } from "@/hooks/useConfig";
import { useReportPost } from "@/hooks/useEngagement";

export default function ReportDialog({ post, open, onClose }) {
  const { reports } = useConfig();
  const report = useReportPost(post.id);
  const [reason, setReason] = useState(reports.reasons[0]?.value || "");
  const [details, setDetails] = useState("");
  const [done, setDone] = useState(null);

  const close = () => {
    onClose();
    // reset after the close animation
    setTimeout(() => {
      setDone(null);
      setDetails("");
      report.reset();
    }, 200);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await report.mutateAsync({ reason, details: details.trim() || null });
      setDone(res.message);
    } catch {
      // shown below
    }
  };

  return (
    <Modal open={open} title="Report post" onClose={close}>
      {done ? (
        <div className="stack approval-pending">
          <div className="approval-icon" aria-hidden>
            ✓
          </div>
          <p style={{ margin: 0 }}>{done}</p>
          <Button variant="secondary" onClick={close}>
            Close
          </Button>
        </div>
      ) : (
        <form className="stack" onSubmit={onSubmit}>
          <p className="muted small" style={{ margin: 0 }}>
            Reporting <strong>&ldquo;{post.title}&rdquo;</strong> by {post.author_name}. Admins will review it; the author won&apos;t see who reported it.
          </p>
          <div className="report-reasons">
            {reports.reasons.map((r) => (
              <label key={r.value} className={`report-reason ${reason === r.value ? "report-reason-active" : ""}`}>
                <input type="radio" name="reason" value={r.value} checked={reason === r.value} onChange={() => setReason(r.value)} />
                {r.label}
              </label>
            ))}
          </div>
          <Input
            label="Anything else? (optional)"
            name="details"
            as="textarea"
            rows={3}
            maxLength={reports.details_max_length}
            value={details}
            onChange={(e) => setDetails(e.target.value)}
          />
          <Alert>{report.error?.message}</Alert>
          <div className="row" style={{ justifyContent: "flex-end" }}>
            <Button type="button" variant="secondary" onClick={close}>
              Cancel
            </Button>
            <Button type="submit" variant="danger" loading={report.isPending}>
              Submit report
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}
