"use client";

import DashboardShell from "@/components/layout/DashboardShell";
import { useStudentProfile } from "@/hooks/useStudent";
import { useUnreadMessages } from "@/hooks/useMessages";
import { STUDENT_LINKS } from "./StudentSidebar";

export default function StudentNavbar({ children }) {
  const { data: profile } = useStudentProfile();
  const { data: unread } = useUnreadMessages();
  const links = STUDENT_LINKS.map((link) =>
    link.href.endsWith("/inbox") ? { ...link, badge: unread?.unread_count } : link
  );
  return (
    <DashboardShell
      role="student"
      roleLabel="Student"
      links={links}
      userName={profile?.name || profile?.registration_no || "Student"}
      avatarUrl={profile?.avatar_url}
      profileHref="/dashboard/student/profile"
    >
      {children}
    </DashboardShell>
  );
}
