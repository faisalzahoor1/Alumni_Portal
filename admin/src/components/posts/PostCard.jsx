"use client";

import Avatar from "@/components/ui/Avatar";
import Badge from "@/components/ui/Badge";
import { timeAgo } from "@/lib/utils/formatters";
import { useConfig } from "@/hooks/useConfig";
import PostEngagement from "./PostEngagement";

const IMAGE_RE = /\.(png|jpe?g|gif|webp|avif|svg)(\?|$)/i;

export default function PostCard({ post, actions, engagement = true, className = "" }) {
  const { university } = useConfig();
  const official = post.author_role === university.author_role;
  const media = post.media_urls || [];
  const images = media.filter((url) => IMAGE_RE.test(url) || url.includes("/image/upload/"));
  const files = media.filter((url) => !images.includes(url));

  return (
    <article className={`card post-card ${official ? "post-official" : ""} ${className}`}>
      <div className="row-between">
        <div className="post-meta">
          <Avatar name={post.author_name} src={post.author_avatar} size={40} />
          <div>
            <strong>{post.author_name}</strong>
            <span className="muted small">
              {official ? "Official" : <span style={{ textTransform: "capitalize" }}>{post.author_role}</span>} · {timeAgo(post.created_at)}
            </span>
          </div>
        </div>
        <div className="row">
          {official && <Badge tone="primary">✓ {university.short_name}</Badge>}
          {post.post_type && <Badge>{post.post_type}</Badge>}
          {post.is_public === false && <Badge tone="warning">Private</Badge>}
          {actions}
        </div>
      </div>

      <div>
        <h3>{post.title}</h3>
        {(post.job_title || post.company_name) && (
          <p className="muted small" style={{ marginBottom: 6 }}>
            {[post.job_title, post.company_name].filter(Boolean).join(" at ")}
          </p>
        )}
        <div className="pre-wrap">{post.content}</div>
      </div>

      {images.length > 0 && (
        <div className="post-media">
          {images.map((url) => (
            <a key={url} href={url} target="_blank" rel="noreferrer">
              <img src={url} alt="" />
            </a>
          ))}
        </div>
      )}

      {(files.length > 0 || post.external_urls?.length > 0 || post.job_apply_url) && (
        <div className="stack-sm small">
          {files.map((url) => (
            <a key={url} href={url} target="_blank" rel="noreferrer">
              📎 {url.split("/").pop()}
            </a>
          ))}
          {post.external_urls?.map((url) => (
            <a key={url} href={url} target="_blank" rel="noreferrer">
              🔗 {url}
            </a>
          ))}
          {post.job_apply_url && (
            <a className="btn btn-primary btn-sm" style={{ alignSelf: "flex-start" }} href={post.job_apply_url} target="_blank" rel="noreferrer">
              Apply now
            </a>
          )}
        </div>
      )}

      {post.tags?.length > 0 && (
        <div className="tags">
          {post.tags.map((tag) => (
            <span key={tag} className="tag">
              #{tag}
            </span>
          ))}
        </div>
      )}

      {engagement && <PostEngagement post={post} />}
    </article>
  );
}
