"use client";

import DashboardShell from "@/components/layout/DashboardShell";
import { useIndustryProfile } from "@/hooks/useIndustry";
import { INDUSTRY_LINKS } from "./IndustrySidebar";

export default function IndustryNavbar({ children }) {
  const { data: profile } = useIndustryProfile();
  return (
    <DashboardShell
      role="industry"
      roleLabel="Industry Partner"
      links={INDUSTRY_LINKS}
      userName={profile?.company_name || "Company"}
      avatarUrl={profile?.logo_url}
      profileHref="/dashboard/industry/profile"
    >
      {children}
    </DashboardShell>
  );
}
