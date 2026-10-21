"use client";

import { useState } from "react";
import Card from "@/components/ui/Card";
import Modal from "@/components/ui/Modal";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import AlumniPostCard from "@/components/alumni/AlumniPostCard";
import PostForm from "./PostForm";

// Composer plus the author's own posts with edit / delete. `hooks` is the role's post hooks.
export default function MyPostsPanel({ hooks }) {
  const { data, isLoading, error } = hooks.usePosts();
  const remove = hooks.useDelete();
  const [editing, setEditing] = useState(null);
  const posts = Array.isArray(data) ? data : [];

  const onDelete = (post) => {
    if (window.confirm(`Delete "${post.title}"? This can't be undone.`)) remove.mutate(post.id);
  };

  return (
    <div className="stack">
      <Card title="Create a post">
        <PostForm hooks={hooks} />
      </Card>

      <Alert>{error?.message || remove.error?.message}</Alert>

      {isLoading ? (
        <SkeletonList />
      ) : posts.length === 0 ? (
        <div className="card empty fade-up">No posts yet. Share your first update above.</div>
      ) : (
        <div className="stack stagger">
          {posts.map((post) => (
            <AlumniPostCard key={post.id} post={post} onEdit={setEditing} onDelete={onDelete} />
          ))}
        </div>
      )}

      <Modal open={!!editing} title="Edit post" size="lg" onClose={() => setEditing(null)}>
        {editing && <PostForm key={editing.id} post={editing} hooks={hooks} onDone={() => setEditing(null)} />}
      </Modal>
    </div>
  );
}
