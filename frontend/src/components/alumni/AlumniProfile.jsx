"use client";

import { useEffect, useState } from "react";
import AvatarUpload from "@/components/ui/AvatarUpload";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { PageLoader } from "@/components/ui/Spinner";
import { splitList } from "@/lib/utils/formatters";
import { validateUrl } from "@/lib/utils/validation";
import { useAlumniProfile, useUpdateAlumniProfile, useUploadAlumniAvatar } from "@/hooks/useAlumni";

const TEXT_FIELDS = [
  ["name", "Full name"],
  ["phone", "Phone"],
  ["degree", "Degree"],
  ["department", "Department"],
  ["current_position", "Current position"],
  ["current_company", "Current company"],
  ["location", "Location"],
];

const URL_FIELDS = [
  ["linkedin_url", "LinkedIn"],
  ["github_url", "GitHub"],
  ["portfolio_url", "Portfolio"],
];

function toForm(profile) {
  const form = {};
  [...TEXT_FIELDS, ...URL_FIELDS].forEach(([key]) => (form[key] = profile?.[key] || ""));
  form.bio = profile?.bio || "";
  form.graduation_year = profile?.graduation_year || "";
  form.skills = (profile?.skills || []).join(", ");
  form.achievements = (profile?.achievements || []).join("\n");
  return form;
}

export default function AlumniProfile() {
  const { data: profile, isLoading, error: loadError } = useAlumniProfile();
  const update = useUpdateAlumniProfile();
  const uploadAvatar = useUploadAlumniAvatar();
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
    setErrors(fieldErrors);
    if (Object.keys(fieldErrors).length) return;

    const data = {};
    [...TEXT_FIELDS, ...URL_FIELDS, ["bio"]].forEach(([key]) => (data[key] = form[key].trim() || null));
    data.graduation_year = form.graduation_year ? Number(form.graduation_year) : null;
    data.skills = splitList(form.skills);
    data.achievements = form.achievements.split("\n").map((s) => s.trim()).filter(Boolean);
    try {
      await update.mutateAsync(data);
      setStatus({ success: "Profile saved." });
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
          <AvatarUpload name={profile?.name} src={profile?.avatar_url} upload={uploadAvatar} />
          <div style={{ paddingTop: 12 }}>
            <h2 style={{ margin: 0 }}>{profile?.name || "Your name"}</h2>
            <span className="muted small">{profile?.email}</span>
          </div>
        </div>
      </Card>

      <Card title="About">
        <div className="stack">
          <div className="grid-2">
            {TEXT_FIELDS.map(([key, label]) => (
              <Input key={key} label={label} name={key} value={form[key]} onChange={set(key)} />
            ))}
            <Input
              label="Graduation year"
              name="graduation_year"
              type="number"
              min="1950"
              max="2100"
              value={form.graduation_year}
              onChange={set("graduation_year")}
            />
          </div>
          <Input label="Bio" name="bio" as="textarea" value={form.bio} onChange={set("bio")} />
        </div>
      </Card>

      <Card title="Skills & achievements">
        <div className="stack">
          <Input label="Skills" name="skills" value={form.skills} onChange={set("skills")} hint="Comma separated, e.g. Python, React, Leadership" />
          <Input label="Achievements" name="achievements" as="textarea" value={form.achievements} onChange={set("achievements")} hint="One per line" />
        </div>
      </Card>

      <Card title="Links">
        <div className="grid-2">
          {URL_FIELDS.map(([key, label]) => (
            <Input key={key} label={label} name={key} type="url" value={form[key]} onChange={set(key)} error={errors[key]} />
          ))}
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
