"use client";

import PostCard from "@/components/posts/PostCard";
import Dropdown from "@/components/ui/Dropdown";

export default function AlumniPostCard({ post, onEdit, onDelete }) {
  return (
    <PostCard
      post={post}
      actions={
        <Dropdown trigger={<button className="btn btn-ghost btn-sm" aria-label="Post actions">⋯</button>}>
          {(close) => (
            <>
              <button className="dropdown-item" onClick={() => { close(); onEdit(post); }}>
                Edit
              </button>
              <button className="dropdown-item" style={{ color: "var(--danger)" }} onClick={() => { close(); onDelete(post); }}>
                Delete
              </button>
            </>
          )}
        </Dropdown>
      }
    />
  );
}
