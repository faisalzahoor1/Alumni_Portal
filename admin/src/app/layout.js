import "./globals.css";
import "./theme.css";
import QueryProvider from "@/providers/QueryProvider";
import AuthProvider from "@/providers/AuthProvider";
import MotionFX from "@/components/fx/MotionFX";
import Intro, { introScript } from "@/components/fx/Intro";

export const metadata = {
  title: "Admin Portal · Alumni Portal",
  description: "Approve registrations, publish university posts and moderate the community.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: introScript }} />
      </head>
      <body className="admin-app">
        <Intro label="Admin Portal" />
        <MotionFX />
        <QueryProvider>
          <AuthProvider>{children}</AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
