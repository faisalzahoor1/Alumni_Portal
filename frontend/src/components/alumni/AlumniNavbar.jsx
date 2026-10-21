"use client";

import DashboardShell from "@/components/layout/DashboardShell";
import { useAlumniProfile } from "@/hooks/useAlumni";
import { useUnreadMessages } from "@/hooks/useMessages";
import { ALUMNI_LINKS } from "./AlumniSidebar";

export default function AlumniNavbar({ children }) {
  const { data: profile } = useAlumniProfile();
  const { data: unread } = useUnreadMessages();
  const links = ALUMNI_LINKS.map((link) =>
    link.href.endsWith("/inbox") ? { ...link, badge: unread?.unread_count } : link
  );
  return (
    <DashboardShell
      role="alumni"
      roleLabel="Alumni"
      links={links}
      userName={profile?.name || profile?.email || "Alumni"}
      avatarUrl={profile?.avatar_url}
      profileHref="/dashboard/alumni/profile"
    >
      {children}
    </DashboardShell>
  );
}
