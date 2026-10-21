"use client";

import { useEffect, useState } from "react";
import AvatarUpload from "@/components/ui/AvatarUpload";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { PageLoader } from "@/components/ui/Spinner";
import { validateUrl } from "@/lib/utils/validation";
import { useIndustryProfile, useUpdateIndustryProfile, useUploadIndustryLogo } from "@/hooks/useIndustry";

const TEXT_FIELDS = [
  ["company_name", "Company name"],
  ["industry_type", "Industry"],
  ["location", "Location"],
  ["employee_count", "Company size", "e.g. 50-200"],
];

const URL_FIELDS = [["website", "Website"]];

function toForm(profile) {
  const form = {};
  [...TEXT_FIELDS, ...URL_FIELDS].forEach(([key]) => (form[key] = profile?.[key] || ""));
  form.description = profile?.description || "";
  return form;
}

export default function IndustryProfile() {
  const { data: profile, isLoading, error: loadError } = useIndustryProfile();
  const update = useUpdateIndustryProfile();
  const uploadLogo = useUploadIndustryLogo();
  const [form, setForm] = useState(toForm());
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState({});

  useEffect(() => {
    if (profile) setForm(toForm(profile));
  }, [profile]);

  if (isLoading) return <PageLoader />;

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const onSubmit = async (e) => {
    e.preventDefault();
    setStatus({});
    const fieldErrors = {};
    URL_FIELDS.forEach(([key]) => {
      const err = validateUrl(form[key]);
      if (err) fieldErrors[key] = err;
    });
    if (!form.company_name.trim()) fieldErrors.company_name = "Company name is required";
    setErrors(fieldErrors);
    if (Object.keys(fieldErrors).length) return;

    const data = {};
    [...TEXT_FIELDS, ...URL_FIELDS, ["description"]].forEach(([key]) => (data[key] = form[key].trim() || null));
    try {
      await update.mutateAsync(data);
      setStatus({ success: "Company profile saved." });
    } catch (err) {
      setStatus({ error: err.message });
    }
  };

  return (
    <form className="stack" onSubmit={onSubmit}>
      <Alert>{loadError?.message || status.error}</Alert>
      <Alert type="success">{status.success}</Alert>

      <Card>
        <div className="row" style={{ alignItems: "flex-start" }}>
          <AvatarUpload name={form.company_name} src={profile?.logo_url} upload={uploadLogo} label="Change logo" />
          <div style={{ paddingTop: 12 }}>
            <h2 style={{ margin: 0 }}>{form.company_name || "Your company"}</h2>
            <span className="muted small">{[form.industry_type, form.location].filter(Boolean).join(" · ")}</span>
          </div>
        </div>
      </Card>

      <Card title="Company details">
        <div className="stack">
          <div className="grid-2">
            {TEXT_FIELDS.map(([key, label, placeholder]) => (
              <Input key={key} label={label} name={key} placeholder={placeholder} value={form[key]} onChange={set(key)} error={errors[key]} />
            ))}
            {URL_FIELDS.map(([key, label]) => (
              <Input key={key} label={label} name={key} type="url" value={form[key]} onChange={set(key)} error={errors[key]} />
            ))}
          </div>
          <Input
            label="About the company"
            name="description"
            as="textarea"
            rows={5}
            value={form.description}
            onChange={set("description")}
          />
        </div>
      </Card>

      <div className="row" style={{ justifyContent: "flex-end" }}>
        <Button type="submit" loading={update.isPending}>
          Save profile
        </Button>
      </div>
    </form>
  );
}
