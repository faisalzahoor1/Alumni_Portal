"use client";

import { useConfig } from "@/hooks/useConfig";
import { formatBytes } from "@/lib/utils/formatters";
import { validateFile } from "@/lib/utils/validation";

// Picks a CV file; the parent form uploads it on save.
export default function CVUpload({ file, currentCv, onChange, onError }) {
  const { cv: cvRules } = useConfig();

  const onFile = (e) => {
    const picked = e.target.files?.[0];
    e.target.value = "";
    if (!picked) return;
    const error = validateFile(picked, cvRules);
    onError?.(error || "");
    if (!error) onChange(picked);
  };

  return (
    <div className="field">
      <label>CV / Resume</label>
      <div className="row">
        <label className="btn btn-secondary btn-sm">
          {file || currentCv ? "Replace file" : "Choose file"}
          <input type="file" accept={[...cvRules.extensions, ...cvRules.content_types].join(",")} hidden onChange={onFile} />
        </label>
        {file ? (
          <span className="small fade-in">
            {file.name} <span className="muted">· {formatBytes(file.size)}</span>
            <button type="button" className="btn btn-ghost btn-sm" onClick={() => onChange(null)}>
              Remove
            </button>
          </span>
        ) : currentCv ? (
          <a className="small" href={currentCv.file_url} target="_blank" rel="noreferrer">
            {currentCv.file_name}
          </a>
        ) : (
          <span className="muted small">
            {cvRules.extensions.map((ext) => ext.replace(".", "").toUpperCase()).join(", ")}, up to {formatBytes(cvRules.max_size_bytes)}
          </span>
        )}
      </div>
    </div>
  );
}
