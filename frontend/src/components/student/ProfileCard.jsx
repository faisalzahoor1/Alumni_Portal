import Avatar from "@/components/ui/Avatar";
import AvatarUpload from "@/components/ui/AvatarUpload";
import Card from "@/components/ui/Card";
import { formatBytes, formatDate } from "@/lib/utils/formatters";

// Pass `upload` (an avatar upload mutation) to make the picture editable.
export default function ProfileCard({ student, actions, upload }) {
  if (!student) return null;
  const links = [
    ["LinkedIn", student.linkedin_url],
    ["Instagram", student.instagram_url],
  ].filter(([, url]) => url);

  return (
    <Card actions={actions}>
      <div className="stack">
        <div className="row" style={{ alignItems: "flex-start" }}>
          {upload ? (
            <AvatarUpload name={student.name} src={student.avatar_url} upload={upload} />
          ) : (
            <Avatar name={student.name} src={student.avatar_url} size={64} />
          )}
          <div style={{ paddingTop: upload ? 12 : 0 }}>
            <h2 style={{ margin: 0 }}>{student.name}</h2>
            <div className="muted small">{student.registration_no}</div>
            <div className="muted small">{student.email}</div>
          </div>
        </div>

        {links.length > 0 && (
          <div className="row small">
            {links.map(([label, url]) => (
              <a key={label} href={url} target="_blank" rel="noreferrer">
                🔗 {label}
              </a>
            ))}
          </div>
        )}

        {student.cv ? (
          <div className="small">
            📎{" "}
            <a href={student.cv.file_url} target="_blank" rel="noreferrer">
              {student.cv.file_name}
            </a>{" "}
            <span className="muted">
              · {formatBytes(student.cv.file_size)} · uploaded {formatDate(student.cv.uploaded_at)}
            </span>
          </div>
        ) : (
          <div className="muted small">No CV uploaded yet.</div>
        )}
      </div>
    </Card>
  );
}
