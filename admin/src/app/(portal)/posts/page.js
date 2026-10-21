"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/AdminShell";
import Card from "@/components/ui/Card";
import Modal from "@/components/ui/Modal";
import Alert from "@/components/ui/Alert";
import Button from "@/components/ui/Button";
import Dropdown from "@/components/ui/Dropdown";
import SkeletonList from "@/components/ui/Skeleton";
import PostCard from "@/components/posts/PostCard";
import PostForm from "@/components/posts/PostForm";
import { useConfig } from "@/hooks/useConfig";
import { UNIVERSITY_POST_HOOKS, useDeleteUniversityPost, useUniversityPosts } from "@/hooks/useAdmin";

export default function UniversityPostsPage() {
  const { university } = useConfig();
  const { data: posts, isLoading, error } = useUniversityPosts();
  const remove = useDeleteUniversityPost();
  const [editing, setEditing] = useState(null);
  const [deleting, setDeleting] = useState(null);

  return (
    <>
      <PageHeader
        title={university.posts_label}
        subtitle={`Official posts appear under "${university.name}" for every student, alumni and industry partner.`}
      />

      <div className="stack">
        <Card title={`New ${university.short_name} post`}>
          <PostForm hooks={UNIVERSITY_POST_HOOKS} />
        </Card>

        <Alert>{error?.message || remove.error?.message}</Alert>

        {isLoading ? (
          <SkeletonList />
        ) : posts?.length ? (
          <div className="stack stagger">
            {posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                actions={
                  <Dropdown trigger={<button className="btn btn-ghost btn-sm" aria-label="Post actions">⋯</button>}>
                    {(close) => (
                      <>
                        <button className="dropdown-item" onClick={() => { close(); setEditing(post); }}>
                          Edit
                        </button>
                        <button className="dropdown-item" style={{ color: "var(--danger)" }} onClick={() => { close(); setDeleting(post); }}>
                          Delete
                        </button>
                      </>
                    )}
                  </Dropdown>
                }
              />
            ))}
          </div>
        ) : (
          <div className="card empty fade-up">No {university.short_name} posts yet. Publish the first one above.</div>
        )}
      </div>

      <Modal open={!!editing} title="Edit post" size="lg" onClose={() => setEditing(null)}>
        {editing && <PostForm key={editing.id} post={editing} hooks={UNIVERSITY_POST_HOOKS} onDone={() => setEditing(null)} />}
      </Modal>

      <Modal open={!!deleting} title="Delete post" onClose={() => setDeleting(null)}>
        {deleting && (
          <div className="stack">
            <p style={{ margin: 0 }}>
              Delete <strong>&ldquo;{deleting.title}&rdquo;</strong>? Its comments and reactions are removed too. This can&apos;t be undone.
            </p>
            <div className="row" style={{ justifyContent: "flex-end" }}>
              <Button variant="secondary" onClick={() => setDeleting(null)}>
                Cancel
              </Button>
              <Button
                variant="danger"
                loading={remove.isPending}
                onClick={async () => {
                  await remove.mutateAsync(deleting.id).catch(() => {});
                  setDeleting(null);
                }}
              >
                Delete
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
}
