const TONES = {
  open: "success",
  accepted: "success",
  closed: "danger",
  rejected: "danger",
  pending: "warning",
  draft: "warning",
  reviewed: "primary",
  alumni: "primary",
  industry: "success",
  achievement: "warning",
  job_opportunity: "success",
  announcement: "primary",
  approved: "success",
  dismissed: "success",
  actioned: "danger",
  student: "primary",
};

export default function Badge({ tone, children }) {
  const resolved = tone || TONES[String(children).toLowerCase()] || "";
  return <span className={`badge ${resolved ? `badge-${resolved}` : ""}`}>{String(children).replace(/_/g, " ")}</span>;
}
