import "./globals.css";
import "./theme.css";
import QueryProvider from "@/providers/QueryProvider";
import AuthProvider from "@/providers/AuthProvider";
import MotionFX from "@/components/fx/MotionFX";
import Intro, { introScript } from "@/components/fx/Intro";

export const metadata = {
  title: "Alumni Portal",
  description: "Connecting students, alumni and industry partners in one place.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: introScript }} />
      </head>
      <body>
        <Intro label="Alumni Portal" />
        <MotionFX />
        <QueryProvider>
          <AuthProvider>{children}</AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
