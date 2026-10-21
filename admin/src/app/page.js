import { redirect } from "next/navigation";

// Middleware sends signed-out visitors to /login first
export default function Home() {
  redirect("/dashboard");
}
