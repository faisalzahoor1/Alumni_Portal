"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { useConfig } from "@/hooks/useConfig";
import { splitList } from "@/lib/utils/formatters";

function toForm(post, postTypes) {
  return {
    title: post?.title || "",
    content: post?.content || "",
    post_type: post?.post_type || postTypes[0]?.value || "",
    job_title: post?.job_title || "",
    company_name: post?.company_name || "",
    job_apply_url: post?.job_apply_url || "",
    external_urls: (post?.external_urls || []).join(", "),
    tags: (post?.tags || []).join(", "),
    is_public: post?.is_public ?? true,
    media_urls: post?.media_urls || [],
  };
}

// Create / edit form for community posts; `hooks` supplies the role's create, update and upload mutations.
export default function PostForm({ post, onDone, hooks }) {
  const { posts: postRules } = useConfig();
  const [form, setForm] = useState(() => toForm(post, postRules.types));
  const [error, setError] = useState("");
  const create = hooks.useCreate();
  const update = hooks.useUpdate();
  const upload = hooks.useUpload();
  const isJob = !!postRules.types.find((t) => t.value === form.post_type)?.job_fields;

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.type === "checkbox" ? e.target.checked : e.target.value }));

  const onFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setError("");
    try {
      const res = await upload.mutateAsync(file);
      setForm((f) => ({ ...f, media_urls: [...f.media_urls, res.file_url] }));
    } catch (err) {
      setError(err.message);
    }
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const data = {
      title: form.title.trim(),
      content: form.content.trim(),
      post_type: form.post_type,
      is_public: form.is_public,
      media_urls: form.media_urls,
      tags: splitList(form.tags),
      external_urls: splitList(form.external_urls),
      job_title: isJob ? form.job_title || null : null,
      company_name: isJob ? form.company_name || null : null,
      job_apply_url: isJob ? form.job_apply_url || null : null,
    };
    try {
      if (post) await update.mutateAsync({ id: post.id, data });
      else await create.mutateAsync(data);
      if (!post) setForm(toForm(null, postRules.types));
      onDone?.();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form className="stack" onSubmit={onSubmit}>
      <Alert>{error}</Alert>
      <div className="grid-2">
        <Input label="Title" name="title" value={form.title} onChange={set("title")} maxLength={postRules.title_max_length} required />
        <Input label="Type" name="post_type" as="select" options={postRules.types} value={form.post_type} onChange={set("post_type")} />
      </div>
      <Input label="What do you want to share?" name="content" as="textarea" rows={5} value={form.content} onChange={set("content")} required />

      {isJob && (
        <div className="grid-2">
          <Input label="Job title" name="job_title" value={form.job_title} onChange={set("job_title")} />
          <Input label="Company" name="company_name" value={form.company_name} onChange={set("company_name")} />
          <Input label="Apply URL" name="job_apply_url" type="url" value={form.job_apply_url} onChange={set("job_apply_url")} />
        </div>
      )}

      <div className="grid-2">
        <Input label="Tags" name="tags" value={form.tags} onChange={set("tags")} hint="Comma separated" />
        <Input label="Links" name="external_urls" value={form.external_urls} onChange={set("external_urls")} hint="Comma separated URLs" />
      </div>

      <div className="stack-sm">
        <div className="row">
          <label className="btn btn-secondary btn-sm">
            {upload.isPending ? "Uploading…" : "＋ Attach media"}
            <input type="file" hidden onChange={onFile} disabled={upload.isPending} />
          </label>
          <label className="checkbox">
            <input type="checkbox" checked={form.is_public} onChange={set("is_public")} />
            Visible in community feed
          </label>
        </div>
        {form.media_urls.length > 0 && (
          <div className="stack-sm small">
            {form.media_urls.map((url) => (
              <div key={url} className="row-between">
                <a href={url} target="_blank" rel="noreferrer" style={{ overflow: "hidden", textOverflow: "ellipsis" }}>
                  {url.split("/").pop()}
                </a>
                <button
                  type="button"
                  className="btn btn-ghost btn-sm"
                  onClick={() => setForm((f) => ({ ...f, media_urls: f.media_urls.filter((u) => u !== url) }))}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="row" style={{ justifyContent: "flex-end" }}>
        {onDone && post && (
          <Button type="button" variant="secondary" onClick={onDone}>
            Cancel
          </Button>
        )}
        <Button type="submit" loading={create.isPending || update.isPending}>
          {post ? "Save changes" : "Publish post"}
        </Button>
      </div>
    </form>
  );
}
