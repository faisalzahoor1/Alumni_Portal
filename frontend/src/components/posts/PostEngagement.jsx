"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Avatar from "@/components/ui/Avatar";
import Button from "@/components/ui/Button";
import Alert from "@/components/ui/Alert";
import Spinner from "@/components/ui/Spinner";
import { useAuth } from "@/hooks/useAuth";
import { useConfig } from "@/hooks/useConfig";
import { useAddComment, useComments, useDeleteComment, useReact } from "@/hooks/useEngagement";
import { useStartConversation } from "@/hooks/useMessages";
import { timeAgo } from "@/lib/utils/formatters";
import ReportDialog from "./ReportDialog";

// Presentation only: reactions themselves come from the backend config
const REACTION_ICONS = { like: "👍", dislike: "👎" };

function CommentForm({ postId, parentId, maxLength, placeholder, autoFocus, onDone }) {
  const add = useAddComment(postId);
  const [text, setText] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    try {
      await add.mutateAsync({ content: text.trim(), parentId });
      setText("");
      onDone?.();
    } catch {
      // shown below
    }
  };

  return (
    <form className="comment-form-wrap" onSubmit={onSubmit}>
      <div className="comment-form">
        <input
          className="input"
          placeholder={placeholder}
          value={text}
          maxLength={maxLength}
          autoFocus={autoFocus}
          onChange={(e) => setText(e.target.value)}
        />
        <Button type="submit" size="sm" loading={add.isPending} disabled={!text.trim()}>
          {parentId ? "Reply" : "Post"}
        </Button>
      </div>
      <Alert>{add.error?.message}</Alert>
    </form>
  );
}

function CommentItem({ comment, postId, canReply, maxLength, onReply, replying, onDelete, deleting, children }) {
  return (
    <div className="comment">
      <Avatar name={comment.author_name} src={comment.author_avatar} size={comment.parent_id ? 26 : 30} />
      <div className="comment-main">
        <div className="comment-body">
          <div className="row-between" style={{ flexWrap: "nowrap" }}>
            <strong className="small">
              {comment.author_name} <span className="role-tag">{comment.author_role}</span>
            </strong>
            <span className="muted small">{timeAgo(comment.created_at)}</span>
          </div>
          <div className="small pre-wrap">{comment.content}</div>
        </div>
        <div className="comment-actions">
          {canReply && (
            <button className="link-btn small" onClick={onReply}>
              Reply
            </button>
          )}
          {comment.is_mine && (
            <button className="link-btn link-danger small" onClick={onDelete} disabled={deleting}>
              Delete
            </button>
          )}
        </div>
        {replying && (
          <CommentForm
            postId={postId}
            parentId={comment.id}
            maxLength={maxLength}
            placeholder={`Reply to ${comment.author_name}…`}
            autoFocus
            onDone={onReply}
          />
        )}
        {children}
      </div>
    </div>
  );
}

function Comments({ postId, canComment, maxLength }) {
  const { data: comments, isLoading, error } = useComments(postId, true);
  const remove = useDeleteComment(postId);
  const [replyTo, setReplyTo] = useState(null);

  // Flat list from the API -> top-level comments with their replies
  const threads = useMemo(() => {
    const list = comments || [];
    const replies = {};
    list.filter((c) => c.parent_id).forEach((c) => (replies[c.parent_id] ||= []).push(c));
    return list.filter((c) => !c.parent_id).map((c) => ({ ...c, replies: replies[c.id] || [] }));
  }, [comments]);

  const toggleReply = (id) => setReplyTo((current) => (current === id ? null : id));
  const itemProps = (c) => ({
    comment: c,
    postId,
    canReply: canComment,
    maxLength,
    onReply: () => toggleReply(c.id),
    replying: replyTo === c.id,
    onDelete: () => remove.mutate(c.id),
    deleting: remove.isPending,
  });

  return (
    <div className="comments">
      <Alert>{error?.message || remove.error?.message}</Alert>
      {isLoading ? (
        <div className="center-pad" style={{ padding: 12 }}>
          <Spinner size="sm" />
        </div>
      ) : threads.length ? (
        <div className="stack-sm stagger">
          {threads.map((thread) => (
            <CommentItem key={thread.id} {...itemProps(thread)}>
              {thread.replies.length > 0 && (
                <div className="replies stagger">
                  {thread.replies.map((reply) => (
                    <CommentItem key={reply.id} {...itemProps(reply)} />
                  ))}
                </div>
              )}
            </CommentItem>
          ))}
        </div>
      ) : (
        <div className="muted small" style={{ padding: "4px 2px" }}>
          No comments yet.{canComment && " Be the first!"}
        </div>
      )}

      {canComment && <CommentForm postId={postId} maxLength={maxLength} placeholder="Write a comment…" />}
    </div>
  );
}

export default function PostEngagement({ post }) {
  const router = useRouter();
  const { role, sub, isAuthenticated } = useAuth();
  const { engagement, messaging, reports } = useConfig();
  const react = useReact(post);
  const start = useStartConversation();
  const [open, setOpen] = useState(false);
  const [bump, setBump] = useState(null);
  const [reporting, setReporting] = useState(false);

  // The server is authoritative (it also requires a verified account); this only decides what to show
  const canEngage = isAuthenticated && engagement.roles.includes(role);
  const canMessage =
    isAuthenticated && messaging.initiator_roles.includes(role) && messaging.recipient_roles.includes(post.author_role);
  const canReport = isAuthenticated && reports.roles.includes(role) && post.author_id !== sub;

  const onReact = (value) => {
    const next = post.my_reaction === value ? null : value;
    setBump(value);
    react.mutate(next);
  };

  const onMessage = async () => {
    try {
      const conversation = await start.mutateAsync(post.author_id);
      router.push(`/dashboard/${role}/inbox?c=${conversation.id}`);
    } catch {
      // shown via start.error
    }
  };

  return (
    <div className="engagement">
      <div className="engagement-bar">
        {engagement.reactions.map(({ value, label }) => {
          const count = post[`${value}s_count`] || 0;
          const active = post.my_reaction === value;
          return (
            <button
              key={value}
              type="button"
              className={`chip ${active ? `chip-active chip-${value}` : ""} ${bump === value ? "chip-bump" : ""}`}
              onClick={() => canEngage && onReact(value)}
              onAnimationEnd={() => setBump(null)}
              disabled={!canEngage}
              title={canEngage ? label : `${count} ${label.toLowerCase()}${count === 1 ? "" : "s"}`}
              aria-pressed={active}
            >
              <span className="chip-icon">{REACTION_ICONS[value] || label[0]}</span>
              <span>{count}</span>
              <span className="chip-label">{label}</span>
            </button>
          );
        })}
        <button type="button" className={`chip ${open ? "chip-active" : ""}`} onClick={() => setOpen((v) => !v)} aria-expanded={open}>
          <span className="chip-icon">💬</span>
          <span>{post.comments_count || 0}</span>
          <span className="chip-label">Comments</span>
        </button>
        {canMessage && (
          <button type="button" className="chip chip-message" onClick={onMessage} disabled={start.isPending}>
            <span className="chip-icon">✉️</span>
            <span>Message {post.author_name?.split(" ")[0]}</span>
          </button>
        )}
        {canReport && (
          <button type="button" className="chip chip-report" onClick={() => setReporting(true)} title="Report this post">
            <span className="chip-icon">⚑</span>
            <span className="chip-label">Report</span>
          </button>
        )}
      </div>
      {canReport && <ReportDialog post={post} open={reporting} onClose={() => setReporting(false)} />}

      {!isAuthenticated && (
        <div className="signin-hint small fade-in">
          <Link href="/auth/login">Sign in</Link> with a verified account to like, comment and message.
        </div>
      )}
      <Alert>{start.error?.message || react.error?.message}</Alert>
      {open && <Comments postId={post.id} canComment={canEngage} maxLength={engagement.comment_max_length} />}
    </div>
  );
}
