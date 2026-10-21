"use client";

import { useEffect, useState } from "react";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import PostCard from "./PostCard";
import { useConfig } from "@/hooks/useConfig";

const LIMIT = 10;

// Renders the community feed; `useFeed` is the role-specific feed query hook.
export default function FeedView({ useFeed, showAuthorFilter = true }) {
  const config = useConfig();
  const [search, setSearch] = useState("");
  const [debounced, setDebounced] = useState("");
  const [authorRole, setAuthorRole] = useState("");
  const [postType, setPostType] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    const t = setTimeout(() => setDebounced(search), 350);
    return () => clearTimeout(t);
  }, [search]);

  useEffect(() => setPage(1), [debounced, authorRole, postType]);

  const { data, isLoading, isFetching, error } = useFeed({
    page,
    limit: LIMIT,
    search: debounced,
    author_role: authorRole,
    post_type: postType,
  });
  const posts = data?.posts || [];

  return (
    <div className="stack">
      <div className="card">
        <div className="feed-filters">
          <Input placeholder="Search posts…" value={search} onChange={(e) => setSearch(e.target.value)} />
          {showAuthorFilter && (
          <Input
            as="select"
            value={authorRole}
            onChange={(e) => setAuthorRole(e.target.value)}
            options={[{ value: "", label: "All authors" }, ...config.feed_author_roles]}
          />
          )}
          <Input
            as="select"
            value={postType}
            onChange={(e) => setPostType(e.target.value)}
            options={[{ value: "", label: "All types" }, ...config.posts.types]}
          />
        </div>
      </div>

      <Alert>{error?.message}</Alert>

      {isLoading ? (
        <SkeletonList />
      ) : posts.length === 0 ? (
        <div className="card empty fade-up">No posts found.</div>
      ) : (
        <div key={`${page}-${debounced}-${authorRole}-${postType}`} className="stack stagger">
          {posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      )}

      {data && (data.page > 1 || data.has_more) && (
        <div className="row-between">
          <Button variant="secondary" disabled={page <= 1 || isFetching} onClick={() => setPage((p) => p - 1)}>
            ← Newer
          </Button>
          <span className="muted small">
            Page {data.page} · {data.total} posts
          </span>
          <Button variant="secondary" disabled={!data.has_more || isFetching} onClick={() => setPage((p) => p + 1)}>
            Older →
          </Button>
        </div>
      )}
    </div>
  );
}
