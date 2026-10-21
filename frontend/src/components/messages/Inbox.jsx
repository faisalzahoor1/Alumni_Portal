"use client";

import { useEffect, useRef, useState } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import Avatar from "@/components/ui/Avatar";
import Button from "@/components/ui/Button";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import { PageLoader } from "@/components/ui/Spinner";
import { useConfig } from "@/hooks/useConfig";
import { useConversations, useSendMessage, useThread } from "@/hooks/useMessages";
import { formatDate, timeAgo } from "@/lib/utils/formatters";

function Thread({ conversation, onBack }) {
  const { messaging } = useConfig();
  const { data: messages, isLoading, error } = useThread(conversation.id);
  const send = useSendMessage(conversation.id);
  const [text, setText] = useState("");
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages?.length]);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    try {
      await send.mutateAsync(text.trim());
      setText("");
    } catch {
      // shown via send.error
    }
  };

  let lastDay = null;
  return (
    <section className="thread">
      <header className="thread-header">
        <button className="btn btn-ghost btn-sm inbox-back" onClick={onBack} aria-label="Back to conversations">
          ←
        </button>
        <Avatar name={conversation.other.name} src={conversation.other.avatar_url} size={36} />
        <div>
          <strong>{conversation.other.name}</strong>
          <div className="muted small" style={{ textTransform: "capitalize" }}>
            {conversation.other.role}
          </div>
        </div>
      </header>

      <div className="thread-body">
        <Alert>{error?.message}</Alert>
        {isLoading ? (
          <PageLoader />
        ) : messages?.length ? (
          messages.map((m) => {
            const day = formatDate(m.created_at);
            const showDay = day !== lastDay;
            lastDay = day;
            return (
              <div key={m.id} className="stack-sm">
                {showDay && <div className="thread-day">{day}</div>}
                <div className={`bubble-row ${m.is_mine ? "bubble-row-mine" : ""}`}>
                  <div className={`bubble ${m.is_mine ? "bubble-mine" : ""}`}>
                    <div className="pre-wrap">{m.content}</div>
                    <span className="bubble-time">{timeAgo(m.created_at)}</span>
                  </div>
                </div>
              </div>
            );
          })
        ) : (
          <div className="empty muted">Say hello to {conversation.other.name.split(" ")[0]} 👋</div>
        )}
        <div ref={endRef} />
      </div>

      <form className="thread-composer" onSubmit={onSubmit}>
        <Alert>{send.error?.message}</Alert>
        <div className="row" style={{ flexWrap: "nowrap" }}>
          <textarea
            className="textarea"
            rows={1}
            placeholder="Type a message…"
            value={text}
            maxLength={messaging.message_max_length}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) onSubmit(e);
            }}
          />
          <Button type="submit" loading={send.isPending} disabled={!text.trim()}>
            Send
          </Button>
        </div>
      </form>
    </section>
  );
}

export default function Inbox({ emptyHint }) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const activeId = params.get("c");
  const { data: conversations, isLoading, error } = useConversations();
  const active = conversations?.find((c) => c.id === activeId);

  const open = (id) => router.replace(id ? `${pathname}?c=${id}` : pathname, { scroll: false });

  if (isLoading) return <SkeletonList count={3} />;

  return (
    <div className={`inbox card ${active ? "inbox-has-active" : ""}`}>
      <aside className="inbox-list">
        <Alert>{error?.message}</Alert>
        {conversations?.length ? (
          <div className="stagger">
            {conversations.map((c) => (
              <button key={c.id} className={`convo ${c.id === activeId ? "convo-active" : ""}`} onClick={() => open(c.id)}>
                <Avatar name={c.other.name} src={c.other.avatar_url} size={40} />
                <div className="convo-text">
                  <div className="row-between" style={{ flexWrap: "nowrap" }}>
                    <strong className="convo-name">{c.other.name}</strong>
                    <span className="muted small">{c.last_message_at ? timeAgo(c.last_message_at) : ""}</span>
                  </div>
                  <div className="row-between" style={{ flexWrap: "nowrap" }}>
                    <span className="convo-preview muted small">{c.last_message || "No messages yet"}</span>
                    {c.unread_count > 0 && <span className="unread-pill">{c.unread_count}</span>}
                  </div>
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="empty small">{emptyHint}</div>
        )}
      </aside>

      {active ? (
        <Thread key={active.id} conversation={active} onBack={() => open(null)} />
      ) : (
        <section className="thread thread-placeholder">
          <div className="empty">
            <div style={{ fontSize: "2rem" }}>💬</div>
            Select a conversation
          </div>
        </section>
      )}
    </div>
  );
}
