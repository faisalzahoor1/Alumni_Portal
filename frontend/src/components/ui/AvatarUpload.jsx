"use client";

import { useEffect, useRef, useState } from "react";
import Avatar from "./Avatar";
import Spinner from "./Spinner";
import Alert from "./Alert";
import { useConfig } from "@/hooks/useConfig";
import { formatBytes } from "@/lib/utils/formatters";
import { validateFile } from "@/lib/utils/validation";

// Click-to-change profile picture. `upload` is a mutation whose mutateAsync takes the File.
export default function AvatarUpload({ name, src, size = 88, upload, label = "Change photo" }) {
  const { avatar: rules } = useConfig();
  const inputRef = useRef(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => () => preview && URL.revokeObjectURL(preview), [preview]);

  const onFile = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    const invalid = validateFile(file, rules);
    setError(invalid || "");
    if (invalid) return;

    setDone(false);
    setPreview(URL.createObjectURL(file)); // show it immediately while uploading
    try {
      await upload.mutateAsync(file);
      setDone(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setPreview(null);
    }
  };

  return (
    <div className="avatar-upload-wrap">
      <button
        type="button"
        className={`avatar-upload ${upload.isPending ? "avatar-upload-busy" : ""} ${done ? "avatar-upload-done" : ""}`}
        style={{ width: size, height: size }}
        onClick={() => inputRef.current?.click()}
        disabled={upload.isPending}
        aria-label={label}
        title={label}
        onAnimationEnd={() => setDone(false)}
      >
        <Avatar name={name} src={preview || src} size={size} />
        <span className="avatar-upload-overlay" aria-hidden>
          {upload.isPending ? <Spinner size="sm" /> : "📷"}
        </span>
      </button>
      <input
        ref={inputRef}
        type="file"
        accept={[...rules.content_types, ...rules.extensions].join(",")}
        hidden
        onChange={onFile}
      />
      <span className="muted small avatar-upload-hint">
        {upload.isPending ? "Uploading…" : `${label} · up to ${formatBytes(rules.max_size_bytes)}`}
      </span>
      <Alert>{error}</Alert>
    </div>
  );
}
