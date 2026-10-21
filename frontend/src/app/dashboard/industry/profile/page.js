import { PageHeader } from "@/components/layout/DashboardShell";
import IndustryProfile from "@/components/industry/IndustryProfile";

export default function IndustryProfilePage() {
  return (
    <>
      <PageHeader title="Company profile" subtitle="Tell candidates who you are." />
      <IndustryProfile />
    </>
  );
}
