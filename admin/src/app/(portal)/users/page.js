"use client";

import { useEffect, useState } from "react";
import { PageHeader } from "@/components/layout/AdminShell";
import Avatar from "@/components/ui/Avatar";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import Modal from "@/components/ui/Modal";
import SkeletonList from "@/components/ui/Skeleton";
import { useDeleteUser, useUsers } from "@/hooks/useAdmin";
import { formatDate, labelize } from "@/lib/utils/formatters";

const ROLES = ["student", "alumni", "industry"];
const DELETES = {
  student: "their profile, CV, comments, reactions, reports and conversations",
  alumni: "their account, profile, posts, comments, reactions, reports and conversations",
  industry: "their account, company profile, posts, jobs and applications, comments, reactions and reports",
};

export default function UsersPage() {
  const [role, setRole] = useState(ROLES[0]);
  const [search, setSearch] = useState("");
  const [debounced, setDebounced] = useState("");
  const [page, setPage] = useState(1);
  const [deleting, setDeleting] = useState(null);
  const [flash, setFlash] = useState(null);
  const remove = useDeleteUser();

  useEffect(() => {
    const t = setTimeout(() => setDebounced(search.trim()), 300);
    return () => clearTimeout(t);
  }, [search]);
  useEffect(() => setPage(1), [debounced, role]);

  const { data, isLoading, isFetching, error } = useUsers({ role, search: debounced, page });

  const onDelete = async () => {
    const user = deleting;
    setFlash(null);
    try {
      const res = await remove.mutateAsync({ role: user.role, id: user.id });
      setFlash({ type: "success", text: res.message });
      setDeleting(null);
    } catch (err) {
      setFlash({ type: "error", text: err.message });
      setDeleting(null);
    }
  };

  return (
    <>
      <PageHeader
        title="Users"
        subtitle="Search students, alumni and industry partners, and remove accounts when needed."
        actions={
          <div className="tabs">
            {ROLES.map((r) => (
              <button key={r} className={`tab ${role === r ? "tab-active" : ""}`} onClick={() => setRole(r)}>
                {labelize(r)}
              </button>
            ))}
          </div>
        }
      />

      <div className="stack">
        <div className="card search-card">
          <span className="search-icon" aria-hidden>
            🔍
          </span>
          <Input
            placeholder={role === "student" ? "Search by name, email or registration number…" : role === "industry" ? "Search by company or email…" : "Search by name or email…"}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search users"
          />
          {isFetching && <span className="spinner spinner-sm" />}
        </div>

        {flash && <Alert type={flash.type}>{flash.text}</Alert>}
        <Alert>{error?.message}</Alert>

        {isLoading ? (
          <SkeletonList count={3} />
        ) : data?.users?.length ? (
          <>
            <div className="muted small">
              {data.total} {data.total === 1 ? role : `${role} accounts`}
              {debounced && ` matching “${debounced}”`}
            </div>
            <div key={`${role}-${debounced}-${page}`} className="stack-sm stagger">
              {data.users.map((u) => (
                <div key={u.id} className="card user-row">
                  <Avatar name={u.name} src={u.avatar_url} size={44} />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div className="row" style={{ gap: 8 }}>
                      <strong>{u.name}</strong>
                      {u.approval_status && u.approval_status !== "approved" && <Badge>{u.approval_status}</Badge>}
                    </div>
                    <div className="muted small">
                      {[u.registration_no, u.email].filter(Boolean).join(" · ")}
                    </div>
                    {u.created_at && <div className="muted small">Joined {formatDate(u.created_at)}</div>}
                  </div>
                  <Button variant="secondary" size="sm" className="danger-hover" onClick={() => setDeleting(u)}>
                    Delete
                  </Button>
                </div>
              ))}
            </div>
            {(data.page > 1 || data.has_more) && (
              <div className="row-between">
                <Button variant="secondary" disabled={page <= 1 || isFetching} onClick={() => setPage((p) => p - 1)}>
                  ← Previous
                </Button>
                <span className="muted small">Page {data.page}</span>
                <Button variant="secondary" disabled={!data.has_more || isFetching} onClick={() => setPage((p) => p + 1)}>
                  Next →
                </Button>
              </div>
            )}
          </>
        ) : (
          <div className="card empty fade-up">{debounced ? `No ${role} matches “${debounced}”.` : `No ${role} accounts yet.`}</div>
        )}
      </div>

      <Modal open={!!deleting} title={`Delete ${deleting?.role} account`} onClose={() => !remove.isPending && setDeleting(null)}>
        {deleting && (
          <div className="stack">
            <div className="row">
              <Avatar name={deleting.name} src={deleting.avatar_url} size={48} />
              <div>
                <strong>{deleting.name}</strong>
                <div className="muted small">{deleting.registration_no || deleting.email}</div>
              </div>
            </div>
            <Alert type="error">This permanently deletes {DELETES[deleting.role]}. It can&apos;t be undone.</Alert>
            <div className="row" style={{ justifyContent: "flex-end" }}>
              <Button variant="secondary" onClick={() => setDeleting(null)} disabled={remove.isPending}>
                Cancel
              </Button>
              <Button variant="danger" loading={remove.isPending} onClick={onDelete}>
                Delete permanently
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
}
