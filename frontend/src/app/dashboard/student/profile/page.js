"use client";

import { PageHeader } from "@/components/layout/DashboardShell";
import Alert from "@/components/ui/Alert";
import SkeletonList from "@/components/ui/Skeleton";
import ProfileCard from "@/components/student/ProfileCard";
import AdditionalInfoForm from "@/components/student/AdditionalInfoForm";
import { useStudentProfile, useUploadStudentAvatar } from "@/hooks/useStudent";

export default function StudentProfilePage() {
  const { data: student, isLoading, error } = useStudentProfile();
  const uploadAvatar = useUploadStudentAvatar();

  return (
    <>
      <PageHeader title="Profile & CV" subtitle="Your name and registration details come from university records." />
      <Alert>{error?.message}</Alert>
      {isLoading ? (
        <SkeletonList count={2} />
      ) : (
        <div className="stack stagger">
          <ProfileCard student={student} upload={uploadAvatar} />
          <AdditionalInfoForm student={student} />
        </div>
      )}
    </>
  );
}
