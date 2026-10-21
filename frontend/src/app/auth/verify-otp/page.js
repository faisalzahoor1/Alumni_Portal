import { Suspense } from "react";
import OTPForm from "@/components/auth/OTPForm";
import { PageLoader } from "@/components/ui/Spinner";

export const metadata = { title: "Verify email · Alumni Portal" };

export default function VerifyOtpPage() {
  // OTPForm reads search params, which requires a Suspense boundary
  return (
    <Suspense fallback={<PageLoader />}>
      <OTPForm />
    </Suspense>
  );
}
