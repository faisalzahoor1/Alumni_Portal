"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Alert from "@/components/ui/Alert";
import { useConfig } from "@/hooks/useConfig";
import { formatDuration } from "@/lib/utils/formatters";

export default function OTPForm() {
  const params = useSearchParams();
  const { verifyEmail } = useAuth();
  const { otp: otpRules } = useConfig();
  const [email, setEmail] = useState(params.get("email") || "");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [pending, setPending] = useState(null);
  const message = params.get("message");

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await verifyEmail(email.trim(), otp);
      if (!res.access_token) {
        setPending(res.message);
        setLoading(false);
      }
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (pending) {
    return (
      <div className="stack approval-pending">
        <div className="approval-icon" aria-hidden>
          ✓
        </div>
        <div>
          <h1>Email verified!</h1>
          <p className="muted">{pending}</p>
        </div>
        <Alert type="info">Keep an eye on your inbox. Once approved, sign in with the email and password you just used.</Alert>
        <Link className="btn btn-secondary btn-block" href="/">
          Back to home
        </Link>
      </div>
    );
  }

  return (
    <form className="stack" onSubmit={onSubmit}>
      <div>
        <h1>Verify your email</h1>
        <p className="muted">Enter the {otpRules.length}-digit code we sent to your inbox. The code expires in {formatDuration(otpRules.expiry_seconds)}.</p>
      </div>

      <Alert type="info">{message}</Alert>
      <Alert>{error}</Alert>

      <Input label="Email" name="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <Input
        label="Verification code"
        name="otp"
        className="otp-input"
        inputMode="numeric"
        autoComplete="one-time-code"
        maxLength={otpRules.length}
        value={otp}
        onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
        required
      />

      <Button type="submit" block loading={loading} disabled={otp.length !== otpRules.length}>
        Verify &amp; continue
      </Button>

      <p className="muted small" style={{ textAlign: "center" }}>
        Didn&apos;t get a code? <Link href="/auth/signup">Sign up again</Link> with the same email to resend.
      </p>
    </form>
  );
}
