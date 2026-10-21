"use client";

import { useEffect, useState } from "react";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { validateUrl } from "@/lib/utils/validation";
import { useUpdateStudentInfo } from "@/hooks/useStudent";
import CVUpload from "./CVUpload";

export default function AdditionalInfoForm({ student }) {
  const update = useUpdateStudentInfo();
  const [form, setForm] = useState({ linkedin_url: "", instagram_url: "" });
  const [cv, setCv] = useState(null);
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState({});

  useEffect(() => {
    if (student) setForm({ linkedin_url: student.linkedin_url || "", instagram_url: student.instagram_url || "" });
  }, [student]);

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const onSubmit = async (e) => {
    e.preventDefault();
    setStatus({});
    const fieldErrors = {};
    ["linkedin_url", "instagram_url"].forEach((key) => {
      const err = validateUrl(form[key]);
      if (err) fieldErrors[key] = err;
    });
    setErrors(fieldErrors);
    if (Object.keys(fieldErrors).length) return;

    try {
      await update.mutateAsync({ linkedin_url: form.linkedin_url.trim(), instagram_url: form.instagram_url.trim(), cv });
      setCv(null);
      setStatus({ success: "Profile updated." });
    } catch (err) {
      setStatus({ error: err.message });
    }
  };

  return (
    <Card title="Additional information">
      <form className="stack" onSubmit={onSubmit}>
        <Alert>{status.error}</Alert>
        <Alert type="success">{status.success}</Alert>
        <div className="grid-2">
          <Input
            label="LinkedIn"
            name="linkedin_url"
            type="url"
            placeholder="https://linkedin.com/in/…"
            value={form.linkedin_url}
            onChange={set("linkedin_url")}
            error={errors.linkedin_url}
          />
          <Input
            label="Instagram"
            name="instagram_url"
            type="url"
            placeholder="https://instagram.com/…"
            value={form.instagram_url}
            onChange={set("instagram_url")}
            error={errors.instagram_url}
          />
        </div>
        <CVUpload file={cv} currentCv={student?.cv} onChange={setCv} onError={(msg) => setStatus(msg ? { error: msg } : {})} />
        <div className="row" style={{ justifyContent: "flex-end" }}>
          <Button type="submit" loading={update.isPending}>
            Save
          </Button>
        </div>
      </form>
    </Card>
  );
}
