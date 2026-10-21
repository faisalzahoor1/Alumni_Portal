"use client";

import { useEffect, useState } from "react";
import { PageHeader } from "@/components/layout/AdminShell";
import AvatarUpload from "@/components/ui/AvatarUpload";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import { useProfile, useUpdateProfile, useUploadAvatar } from "@/hooks/useAdmin";

export default function ProfilePage() {
  const { data: profile, isLoading, error } = useProfile();
  const update = useUpdateProfile();
  const uploadAvatar = useUploadAvatar();
  const [name, setName] = useState("");
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (profile) setName(profile.name);
  }, [profile]);

  const onSubmit = async (e) => {
    e.preventDefault();
    setSaved(false);
    try {
      await update.mutateAsync({ name: name.trim() });
      setSaved(true);
    } catch {
      // shown below
    }
  };

  return (
    <>
      <PageHeader title="Profile" subtitle="Your picture appears on university posts and on your comments." />
      <Alert>{error?.message}</Alert>
      {isLoading ? (
        <SkeletonList count={1} />
      ) : (
        <div className="stack stagger">
          <Card>
            <div className="row" style={{ alignItems: "flex-start" }}>
              <AvatarUpload name={profile?.name} src={profile?.avatar_url} upload={uploadAvatar} />
              <div style={{ paddingTop: 12 }}>
                <h2 style={{ margin: 0 }}>{profile?.name}</h2>
                <span className="muted small">{profile?.email}</span>
                <div>
                  <span className="role-tag" style={{ marginLeft: 0 }}>
                    admin
                  </span>
                </div>
              </div>
            </div>
          </Card>
          <Card title="Details">
            <form className="stack" onSubmit={onSubmit}>
              <Alert type="success">{saved && "Profile saved."}</Alert>
              <Alert>{update.error?.message}</Alert>
              <Input label="Display name" name="name" value={name} maxLength={100} onChange={(e) => setName(e.target.value)} required />
              <Input label="Email" name="email" value={profile?.email || ""} disabled hint="Sign-in email can't be changed here." />
              <div className="row" style={{ justifyContent: "flex-end" }}>
                <Button type="submit" loading={update.isPending} disabled={!name.trim()}>
                  Save
                </Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </>
  );
}
