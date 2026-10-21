import { PageHeader } from "@/components/layout/DashboardShell";
import NotificationList from "@/components/notifications/NotificationList";

export default function AlumniNotificationsPage() {
  return (
    <>
      <PageHeader title="Notifications" />
      <NotificationList role="alumni" />
    </>
  );
}
