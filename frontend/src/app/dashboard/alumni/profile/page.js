import { PageHeader } from "@/components/layout/DashboardShell";
import AlumniProfile from "@/components/alumni/AlumniProfile";

export default function AlumniProfilePage() {
  return (
    <>
      <PageHeader title="Profile" subtitle="How students, alumni and recruiters see you." />
      <AlumniProfile />
    </>
  );
}
