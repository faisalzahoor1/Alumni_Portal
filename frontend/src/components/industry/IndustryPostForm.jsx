"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { useConfig } from "@/hooks/useConfig";
import { labelize } from "@/lib/utils/formatters";
import { useCreateJob, useUpdateJob } from "@/hooks/useIndustry";

function toForm(job, jobRules) {
  return {
    title: job?.title || "",
    description: job?.description || "",
    requirements: (job?.requirements || []).join("\n"),
    location: job?.location || "",
    salary_range: job?.salary_range || "",
    job_type: job?.job_type || jobRules.types[0] || "",
    status: job?.status || jobRules.statuses[0] || "",
  };
}

// Create or edit a job posting.
export default function IndustryPostForm({ job, onDone }) {
  const { jobs: jobRules } = useConfig();
  const [form, setForm] = useState(() => toForm(job, jobRules));
  const [error, setError] = useState("");
  const create = useCreateJob();
  const update = useUpdateJob();

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const data = {
      title: form.title.trim(),
      description: form.description.trim(),
      requirements: form.requirements.split("\n").map((s) => s.trim()).filter(Boolean),
      location: form.location.trim(),
      salary_range: form.salary_range.trim() || null,
      job_type: form.job_type,
    };
    try {
      if (job) await update.mutateAsync({ id: job.id, data: { ...data, status: form.status } });
      else await create.mutateAsync(data);
      onDone?.();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form className="stack" onSubmit={onSubmit}>
      <Alert>{error}</Alert>
      <div className="grid-2">
        <Input label="Job title" name="title" value={form.title} onChange={set("title")} required />
        <Input label="Job type" name="job_type" as="select" options={jobRules.types} value={form.job_type} onChange={set("job_type")} />
        <Input label="Location" name="location" value={form.location} onChange={set("location")} required />
        <Input label="Salary range" name="salary_range" placeholder="e.g. PKR 150k–200k" value={form.salary_range} onChange={set("salary_range")} />
        {job && (
          <Input
            label="Status"
            name="status"
            as="select"
            options={jobRules.statuses.map((s) => ({ value: s, label: labelize(s) }))}
            value={form.status}
            onChange={set("status")}
          />
        )}
      </div>
      <Input label="Description" name="description" as="textarea" rows={5} value={form.description} onChange={set("description")} required />
      <Input
        label="Requirements"
        name="requirements"
        as="textarea"
        rows={4}
        value={form.requirements}
        onChange={set("requirements")}
        hint="One per line"
      />
      <div className="row" style={{ justifyContent: "flex-end" }}>
        {onDone && (
          <Button type="button" variant="secondary" onClick={onDone}>
            Cancel
          </Button>
        )}
        <Button type="submit" loading={create.isPending || update.isPending}>
          {job ? "Save changes" : "Post job"}
        </Button>
      </div>
    </form>
  );
}
