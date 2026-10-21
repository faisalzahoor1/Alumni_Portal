import { PageHeader } from "@/components/layout/DashboardShell";
import NotificationList from "@/components/notifications/NotificationList";

export default function IndustryNotificationsPage() {
  return (
    <>
      <PageHeader title="Notifications" />
      <NotificationList role="industry" />
    </>
  );
}
